import os
import pytest
import time
import src.libs.gramerf_wrapper
from src.libs import utils


yaml_file_name = "redis_performance_tests.yaml"
tests_yaml_path = os.path.join(os.getcwd(), 'data', yaml_file_name)


@pytest.fixture(scope="session")
def setup_redis_server():
    print("\n-- Setting up server OS parameters ...")
    echo_cmd_path = utils.exec_shell_cmd('which echo')
    cat_cmd_path = utils.exec_shell_cmd('which cat')

    utils.exec_shell_cmd(f"sudo sh -c '{echo_cmd_path} never > /sys/kernel/mm/transparent_hugepage/enabled'")
    utils.exec_shell_cmd(f"sudo sh -c '{echo_cmd_path} 1 > /proc/sys/vm/overcommit_memory'")
    utils.exec_shell_cmd(f"sudo sh -c '{echo_cmd_path} 3 > /proc/sys/vm/drop_caches'")
    utils.exec_shell_cmd("sudo sysctl -w net.core.somaxconn=65535 > /dev/null")
    utils.exec_shell_cmd("sudo swapoff -a")
    
    time.sleep(1)
    
    print("\nChecking values ...\n")
    utils.exec_shell_cmd(f"{echo_cmd_path} 'Checking Server setup: '", None)
    utils.exec_shell_cmd(f"{echo_cmd_path} -e '\tHuge pages - Never'", None)
    utils.exec_shell_cmd(f"{cat_cmd_path} /sys/kernel/mm/transparent_hugepage/enabled", None)
    utils.exec_shell_cmd(f"{echo_cmd_path} ''", None)
    utils.exec_shell_cmd(f"{echo_cmd_path} -e '\tOvercommit_memory > 1'", None)
    utils.exec_shell_cmd(f"{cat_cmd_path} /proc/sys/vm/overcommit_memory", None)
    utils.exec_shell_cmd(f"{echo_cmd_path} ''", None)
    utils.exec_shell_cmd(f"{echo_cmd_path} -e '\tClearing cache > 3'", None)
    # utils.exec_shell_cmd("cat /proc/sys/vm/drop_caches")
    utils.exec_shell_cmd(f"{echo_cmd_path} ''", None)
    utils.exec_shell_cmd(f"{echo_cmd_path} -e '\tMax number of connections >65K'", None)
    utils.exec_shell_cmd(f"{cat_cmd_path} /proc/sys/net/core/somaxconn", None)

    #utils.exec_shell_cmd("service irqbalance stop")
    
    print("\nIf values are not as expected stop the test!!!\n")
    time.sleep(2)


@pytest.mark.usefixtures("setup_redis_server")
@pytest.mark.usefixtures("gracurapp_setup")
class TestClass:

    # In order to use command line values within pytest, using 'pytest.config' global
    # is deprecated from pytest version 4.0 onwards. Instead, we need to pass the config 
    # instance via an autouse fixture in order to access it.
    @pytest.fixture(autouse=True)
    def inject_config(self, request):
        self.config = request.config

    @pytest.mark.redis_curapp_perf
    @pytest.mark.redis_curapp_perf_48_data_size
    @pytest.mark.redis_curapp_perf_48_data_size_1_1_rw_ratio
    def test_redis_curapp_perf_48_data_size_1_1_rw_ratio(self):

        test_result = src.libs.gramerf_wrapper.run_test(self, tests_yaml_path)
        assert test_result

    @pytest.mark.redis_curapp_perf
    @pytest.mark.redis_curapp_perf_48_data_size
    @pytest.mark.redis_curapp_perf_48_data_size_1_9_rw_ratio
    def test_redis_curapp_perf_48_data_size_1_9_rw_ratio(self):

        test_result = src.libs.gramerf_wrapper.run_test(self, tests_yaml_path)
        assert test_result

    @pytest.mark.redis_curapp_perf
    @pytest.mark.redis_curapp_perf_1024_data_size
    @pytest.mark.redis_curapp_perf_1024_data_size_1_1_rw_ratio
    def test_redis_curapp_perf_1024_data_size_1_1_rw_ratio(self):

        test_result = src.libs.gramerf_wrapper.run_test(self, tests_yaml_path)
        assert test_result

    @pytest.mark.redis_curapp_perf
    @pytest.mark.redis_curapp_perf_1024_data_size
    @pytest.mark.redis_curapp_perf_1024_data_size_1_9_rw_ratio
    def test_redis_curapp_perf_1024_data_size_1_9_rw_ratio(self):

        test_result = src.libs.gramerf_wrapper.run_test(self, tests_yaml_path)
        assert test_result

    @pytest.mark.redis_curapp_perf
    @pytest.mark.redis_curapp_perf_4096_data_size
    @pytest.mark.redis_curapp_perf_4096_data_size_1_1_rw_ratio
    def test_redis_curapp_perf_4096_data_size_1_1_rw_ratio(self):

        test_result = src.libs.gramerf_wrapper.run_test(self, tests_yaml_path)
        assert test_result

    @pytest.mark.redis_curapp_perf
    @pytest.mark.redis_curapp_perf_4096_data_size
    @pytest.mark.redis_curapp_perf_4096_data_size_1_9_rw_ratio
    def test_redis_curapp_perf_4096_data_size_1_9_rw_ratio(self):

        test_result = src.libs.gramerf_wrapper.run_test(self, tests_yaml_path)
        assert test_result
