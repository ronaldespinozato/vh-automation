from clients.enrollment.enrollment_client import EnrollmentClient
from clients.acs.els_client import ElasticSearchACS
from clients.bootstrap.bootstrap_db import BootstrapDB
from clients.enrollment.enrollment_db import EnrollmentDB
from string_utils.validation import is_full_string

from conf import settings
from unittest import TestCase
from robot.api import logger


class UpgradeMeshManager(TestCase):

    def __init__(self):
        super().__init__()
        settings.set_local_env()
        self.enrollment_client = EnrollmentClient()
        self.bootstrap_db = BootstrapDB()
        self.enrollment_db = EnrollmentDB()
        self.elasticsearch = ElasticSearchACS()

    def upgrade_mesh_with_premium_package(self, mesh_id, package_id, user_name):
        return self.enrollment_client.upgrade_mesh(mesh_id, package_id, user_name)

    def check_assert_status_code_should_be_200_after_upgrade(self, response):
        self.assertEqual(200, response.status_code,
                         "The status code of response is not 200 after call get configuration status mesh")
        data = response.json()
        meta = data["meta"]
        self.assertEqual(200, meta["status"], "Body response does not have status 200 "
                                              "after upgrade the mesh mesh")

    def check_assert_action_in_mesh_should_be_recovery_after_upgrade(self, response):
        data = response.json()
        actions = data["response"]["hubAction"]
        self.assertTrue(len(actions) > 0, "None actions were found after upgrade mesh")
        self.assertEqual("recovery", actions[0], "The action is not recovery after upgrade mesh")
