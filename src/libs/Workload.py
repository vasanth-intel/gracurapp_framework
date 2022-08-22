from src.config_files.constants import *
import src.workloads as workloads


class Workload(object):
    """
    Base class for all workloads. Generic actions are taken here.
    All workload specific actions would be implemented in the respective
    derived workload class.
    """
    def __init__(self,
                 test_config_dict):
        self.name = test_config_dict['workload_name']
        self.command = None

        workload_script = test_config_dict['workload_name'] + "Workload"
        self.workload_class = getattr(globals()["workloads"], workload_script)
        self.workload_obj = self.workload_class(test_config_dict)

    def pre_actions(self, test_config_dict):
        """
        Performs pre-actions for the workload.
        :param test_config_dict: Test config data
        :return:
        """
        self.workload_obj.pre_actions(test_config_dict)

    # setup_workload - implement in a subclass if needed
    def setup_workload(self, test_config_dict):
        return self.workload_obj.setup_workload(test_config_dict)

    # execute_workload - implement in a subclass if needed
    def execute_workload(self, test_config_dict):
        self.workload_obj.execute_workload(test_config_dict)
