import pytest
import re
from src.config_files.constants import *
from src.libs import utils
#from src.libs import gramine_libs
from collections import defaultdict
#import sys
#s_path_program = os.path.dirname(__file__)
#sys.path.append(s_path_program + '../../')
#sys.path.append("curated_apps")
#from curated_apps import conftest
#from curated_apps.conftest import *
#from curated_apps.conftest import *


# Global dictionary to hold the results of all the tests in the following format.
# Tests_results_dictionary (trd)
# {
#   Workload_name1: 
#       { test_name1: {native:[], direct:[], sgx:[], native-avg, direct-avg, sgx-avg, direct_degradation, sgx_degradation} }
#       { test_name2: {native:[], direct:[], sgx:[], native-avg, direct-avg, sgx-avg, direct_degradation, sgx_degradation} }
#   Workload_name2: 
#       { test_name1: {native:[], direct:[], sgx:[], native-avg, direct-avg, sgx-avg, direct_degradation, sgx_degradation} }
#       { test_name2: {native:[], direct:[], sgx:[], native-avg, direct-avg, sgx-avg, direct_degradation, sgx_degradation} }
#  }
trd = defaultdict(dict)


def dcap_setup():
    copy_cmd = "cp /etc/sgx_default_qcnl.conf {}/verifier_image/".format(os.path.join(ORIG_CURATED_PATH, CURATED_PATH))
    utils.run_subprocess(copy_cmd)
    fd = open(VERIFIER_DOCKERFILE)
    fd_contents = fd.read()
    azure_dcap = "(.*)RUN wget https:\/\/packages.microsoft(.*)\n(.*)amd64.deb"
    updated_content = re.sub(azure_dcap, "", fd_contents)
    dcap_library = "RUN apt-get install -y gramine-dcap\nRUN apt install -y libsgx-dcap-default-qpl libsgx-dcap-default-qpl-dev\nCOPY sgx_default_qcnl.conf  /etc/sgx_default_qcnl.conf"
    new_data = re.sub("RUN apt-get install -y gramine-dcap", dcap_library, updated_content)
    fd.close()

    fd = open(VERIFIER_DOCKERFILE, "w+")
    fd.write(new_data)
    fd.close()


def curated_setup():
    print("Cleaning old contrib repo")
    rm_cmd = "rm -rf {}".format(ORIG_CURATED_PATH)
    utils.exec_shell_cmd(rm_cmd)
    print("Cloning and checking out Contrib Git Repo")
    utils.exec_shell_cmd(CONTRIB_GIT_CMD)
    # utils.exec_shell_cmd(GIT_CHECKOUT_CMD)
    if utils.check_machine() == "DCAP client":
        print("Configuring the contrib repo to setup DCAP client")
        dcap_setup()


def copy_repo():
    copy_cmd = "cp -rf {} {}".format(ORIG_CURATED_PATH, REPO_PATH)
    utils.exec_shell_cmd("rm -rf contrib_repo")
    utils.exec_shell_cmd(copy_cmd)


@pytest.fixture(scope="session")
def gracurapp_setup():
    print("\n###### In gracurapp_setup #####\n")

    # Setting http/https proxies.
    utils.set_http_proxies()

    curated_setup()
    copy_repo()

    # Delete old logs if any and create new logs directory.
    if os.path.exists(LOGS_DIR):
        del_logs_cmd = 'rm -rf ' + LOGS_DIR
        os.system(del_logs_cmd)
    if os.path.exists(PERF_RESULTS_DIR):
        del_logs_cmd = 'rm -rf ' + PERF_RESULTS_DIR
        os.system(del_logs_cmd)

    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(PERF_RESULTS_DIR, exist_ok=True)

    # Clearing buff cache.    
    utils.clear_system_cache()

    yield

    # Generate the report using the global results dict.
    #utils.generate_performance_report(trd)


def pytest_addoption(parser):
    print("\n##### In pytest_addoption #####\n")
    parser.addoption("--iterations", action="store", type=int, default=1)
    parser.addoption("--exec_mode", action="store", type=str, default="None")
