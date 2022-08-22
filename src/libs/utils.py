import yaml
import subprocess
import csv
from datetime import date
import collections
import pandas as pd
import socket
import netifaces as ni
import re
from src.config_files.constants import *


def verify_output(cmd_output, search_str): return re.search(search_str, cmd_output, re.IGNORECASE)


# calculate the percent degradation
def percent_degradation(baseline, testapp):
    return '{:0.3f}'.format(100 * (float(baseline) - float(testapp)) / float(baseline))


def exec_shell_cmd(cmd, stdout_val=subprocess.PIPE):
    cmd_stdout = subprocess.run([cmd], shell=True, check=True, stdout=stdout_val, stderr=subprocess.STDOUT, universal_newlines=True)
    if cmd_stdout.returncode != 0:
        raise Exception(f"\n-- Failed to execute the process cmd: {cmd}")

    if stdout_val is not None and cmd_stdout.stdout is not None:
        return cmd_stdout.stdout.strip()

    return cmd_stdout


def read_config_yaml(config_file_path):
    with open(config_file_path, "r") as config_fd:
        try:
            config_dict = yaml.safe_load(config_fd)
        except yaml.YAMLError as exc:
            raise Exception(exc)
    return config_dict


def clear_system_cache():
    """
    Function to clear pagecache, dentries, and inodes. We need to clear system cache to get
    consistent results. This function can be removed after we implement the restart logic.
    :return:
    """
    echo_cmd_path = exec_shell_cmd('which echo')
    clear_cache_cmd = "sudo sh -c \"" + echo_cmd_path + " 3 > /proc/sys/vm/drop_caches\""
    print("\n-- Executing clear cache command..", clear_cache_cmd)
    exec_shell_cmd(clear_cache_cmd)


def set_http_proxies():
    """
    Function to set environment http and https proxies.
    :return:
    """
    os.environ['http_proxy'] = HTTP_PROXY
    os.environ['HTTP_PROXY'] = HTTP_PROXY
    os.environ['https_proxy'] = HTTPS_PROXY
    os.environ['HTTPS_PROXY'] = HTTPS_PROXY
    print("\n-- Setting http_proxy : \n", os.environ['http_proxy'])
    print("\n-- Setting https_proxy : \n", os.environ['https_proxy'])


def set_cpu_freq_scaling_governor():
    """
    Function to set the CPU frequency scaling governor to 'performance' mode.
    :return:
    """
    print("\n-- Setting CPU frequency scaling governor to 'performance' mode..")
    cpu_freq_file = os.path.join(FRAMEWORK_HOME_DIR, 'src/config_files', 'set_cpu_freq_scaling_governor.sh')

    chmod_cmd = 'chmod +x ' + cpu_freq_file
    set_cpu_freq_cmd = 'sudo ' + cpu_freq_file

    exec_shell_cmd(chmod_cmd)

    exec_shell_cmd(set_cpu_freq_cmd)


def set_threads_cnt_env_var():
    """
    Function to determine and set 'THREADS_CNT' env var.
    :return:
    """
    lscpu_output = exec_shell_cmd('lscpu')
    lines = lscpu_output.splitlines()
    core_per_socket, threads_per_core = 0, 0
    for line in lines:
        if 'Core(s) per socket:' in line:
            core_per_socket = int(line.split(':')[-1].strip())
        if 'Thread(s) per core:' in line:
            threads_per_core = int(line.split(':')[-1].strip())
        if core_per_socket and threads_per_core:
            break
    os.environ['THREADS_CNT'] = str(core_per_socket * threads_per_core)
    os.environ['CORES_PER_SOCKET'] = str(core_per_socket)

    print("\n-- Setting the THREADS_CNT env variable to ", os.environ['THREADS_CNT'])
    print("\n-- Setting the CORES_PER_SOCKET env variable to ", os.environ['CORES_PER_SOCKET'])


def determine_host_ip_addr():
    host_IP = socket.gethostbyname(socket.gethostname())
    
    if host_IP.startswith("127."):
        sock_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # The IP address specified in below connect call doesn't have to be reachable..
        sock_obj.connect(('10.255.255.255', 1))
        host_IP = sock_obj.getsockname()[0]
        
    for ifaceName in ni.interfaces():
        if ni.ifaddresses(ifaceName).setdefault(ni.AF_INET) is not None and \
                ni.ifaddresses(ifaceName).setdefault(ni.AF_INET)[0]['addr'].startswith('192.'):
            host_IP = ni.ifaddresses(ifaceName).setdefault(ni.AF_INET)[0]['addr']
            break

    return host_IP


def write_to_csv(tcd, test_dict):
    csv_res_folder = os.path.join(PERF_RESULTS_DIR, tcd['workload_name'])
    if not os.path.exists(csv_res_folder): os.makedirs(csv_res_folder)
    csv_res_file = os.path.join(csv_res_folder, tcd['test_name']+'.csv')
    with open(csv_res_file, 'w') as csvfile:
        csvwriter = csv.DictWriter(csvfile, test_dict.keys())
        csvwriter.writeheader()
        csvwriter.writerow(test_dict)
    

def write_to_report(workload_name, test_results):
    throughput_dict = collections.defaultdict(dict)
    latency_dict = collections.defaultdict(dict)
    generic_dict = collections.defaultdict(dict)

    for k in test_results:
        if 'throughput' in k:
            throughput_dict[k] = test_results[k]
        elif 'latency' in k:
            latency_dict[k] = test_results[k]
        else:
            generic_dict[k] = test_results[k]

    report_name = os.path.join(PERF_RESULTS_DIR, "Gramine_Performance_Data_{}".format(str(date.today())) + ".xlsx")
    if not os.path.exists(PERF_RESULTS_DIR): os.makedirs(PERF_RESULTS_DIR)
    if os.path.exists(report_name):
        writer = pd.ExcelWriter(report_name, engine='openpyxl', mode='a')
    else:
        writer = pd.ExcelWriter(report_name, engine='openpyxl')
    
    cols = ['native', 'gramine-direct', 'gramine-sgx', 'native-avg', 'direct-avg', 'sgx-avg', 'direct-deg', 'sgx-deg']

    if len(throughput_dict) > 0:
        throughput_df = pd.DataFrame.from_dict(throughput_dict, orient='index', columns=cols).dropna(axis=1)
        throughput_df.columns = throughput_df.columns.str.upper()
        throughput_df.to_excel(writer, sheet_name=workload_name)

    if len(latency_dict) > 0:
        latency_df = pd.DataFrame.from_dict(latency_dict, orient='index', columns=cols).dropna(axis=1)
        latency_df.columns = latency_df.columns.str.upper()
        if len(throughput_dict) > 0:
            latency_df.to_excel(writer, sheet_name=workload_name, startcol=throughput_df.shape[1]+2)
        else:
            latency_df.to_excel(writer, sheet_name=workload_name)
    
    if len(generic_dict) > 0:
        generic_df = pd.DataFrame.from_dict(generic_dict, orient='index', columns=cols).dropna(axis=1)
        generic_df.columns = generic_df.columns.str.upper()
        generic_df.to_excel(writer, sheet_name=workload_name)

    writer.save()


def generate_performance_report(trd):
    print("\n###### In generate_performance_report #####\n")

    for workload, tests in trd.items():
        write_to_report(workload, tests)

def check_machine():
    service_cmd = "sudo systemctl --type=service --state=running"
    service_output = exec_shell_cmd(service_cmd)
    if "walinuxagent.service" in service_output:
        print("Running on Azure Linux Agent")
        return "Azure Linux Agent"
    elif "pccs.service" in service_output:
        print("Running on DCAP client")
        return "DCAP client"
    else:
        print("No Provisioning service found, cannot run tests with attestation.")
        return "No Provisioning enabled"

def get_docker_image_name(test_config_dict):
    try:
        return test_config_dict['docker_image'].split("/")[1]
    except Exception as e:
        return ''
