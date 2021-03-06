from clients.enrollment.enrollment_client import EnrollmentClient
from clients.enrollment.enrollment_db import EnrollmentDB
from clients.bootstrap.bootstrap_db import BootstrapDB
from clients.acs.els_client import ElasticSearchACS
from clients.redis.redisclient import RedisClient
from unittest import TestCase
from robot.api import logger


class UnEnrollmentManager(TestCase):

    def __init__(self):
        super().__init__()
        self.enrollment_client = EnrollmentClient()
        self.enrollment_db = EnrollmentDB()
        self.bootstrap_db = BootstrapDB()
        self.elasticsearch = ElasticSearchACS()
        self.redis = RedisClient()

    def un_enrollment_veea_hub(self, serial_number, user_name):
        response = self.enrollment_client.un_enroll_veeahub(user_name, serial_number)
        return response

    def should_return_status_code_200_after_un_enrollment(self, response):
        self.assertEqual(200, response.status_code, "The status code of response is not 200")
        data = response.json()
        meta = data["meta"]
        self.assertEqual(200, meta["status"], "Body response does not have status 200")
        self.assertEqual({}, data["response"], "The response body contains additional information")
        self.assertTrue(meta["message"].find("has been successfully unenrolled"))

    def data_in_database_should_be_cleaned(self, serial_number, user_name):
        self.check_assert_in_databases_after_un_enrollment_veea_hub(serial_number, user_name)
        self.check_assert_in_elasticsearch_after_un_enrollment_veea_hub(serial_number, user_name)
        self.check_assert_in_redis_after_un_enrollment_veea_hub(serial_number)

    def check_assert_in_databases_after_un_enrollment_veea_hub(self, serial_number, user_name):
        status = self.enrollment_db.get_enroll_status_by_veea_hub(serial_number)
        owner = self.enrollment_db.get_owner_data(user_name)
        self.assertEqual(None, status,
                         "The VeeaHub status exist in enrollment_db, it should empty for " + serial_number)
        self.assertTrue(owner is not None, "The Owner data should exist in enrollment_db.user for {} "
                                           "because it is the last VeeaHub in the Mesh".format(user_name))

        offered_software = self.bootstrap_db.get_offered_software_veea_hub(serial_number)
        self.assertTrue(len(offered_software) == 0, "Software was not offered to VeeaHub in "
                                                    "bootstrap_db.offered_software_veea_hub" + serial_number)

        tar_gz = self.bootstrap_db.get_veea_hub_configuration_data(serial_number)
        self.assertTrue(len(tar_gz) == 0, "The Veeahub {} should not have configurations in the table"
                                          " bootstrap_db.veea_hub_configuration_data".format(serial_number))
        veea_hub_data = self.bootstrap_db.get_veeahub_by_serial_number(serial_number)
        self.assertEqual(None, veea_hub_data["owner_uuid"], "The VeeaHub {} contains owner uuid in table"
                                                            " bootstrap_db.veea_hub".format(serial_number))
        self.assertEqual(None, veea_hub_data["mesh_uuid"], "The VeeaHub {} contains owner uuid in table"
                                                           " bootstrap_db.veea_hub ".format(serial_number))

        veea_hub_logs = self.bootstrap_db.get_veea_hub_logs_by_serial_number(serial_number)
        # self.assertEqual(0, len(veea_hub_logs), "The Veeahub {} contains logs in bootstrap_db.veea_hub_log,"
        #                                         " it should be empty".format(serial_number))

    def check_assert_in_elasticsearch_after_un_enrollment_veea_hub(self, serial_number, user_name):
        data = self.elasticsearch.get_veeahub_resource_by_serial_number(serial_number)
        self.assertTrue(len(data) == 0, "EnrollmentVeeahub Resource was found in elasticsearch into index resource")

    def check_assert_in_redis_after_un_enrollment_veea_hub(self, serial_number):
        exist = self.redis.exist_key_for_veea_hub(serial_number)
        self.assertFalse(exist, "There is an entry in Redis for VeeaHub {}".format(serial_number))


