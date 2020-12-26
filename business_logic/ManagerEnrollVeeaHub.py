import json
import sys
from pathlib import Path

project_path = Path(".").resolve()
sys.path.insert(0, str(project_path))
print("#####################################")
print(sys.path)

from clients.enrollment.enrollment_client import EnrollmentClient
from clients.acs.els_client import ElasticSearchACS
from clients.bootstrap.bootstrap_db import BootstrapDB
from clients.enrollment.enrollment_db import EnrollmentDB
from business_logic.VeeaHubModel import VeeaHubModel
from conf import settings
from unittest import TestCase
from robot.api import logger
from business_logic.ResourceTestUtil import ResourceTestUtil


def print(value):
    logger.console(value)


class ManagerEnrollVeeaHub(TestCase):

    def __init__(self):
        super().__init__()
        settings.set_local_env()
        self.enrollmentClient = EnrollmentClient()
        self.bootstrap_db = BootstrapDB()
        self.enrollment_db = EnrollmentDB()
        self.resourceUtils = ResourceTestUtil()
        self.elasticsearch = ElasticSearchACS()

    def unenroll_the_veea_hub(self, veea_hub_serial_number):
        # self.client.start()
        return 1

    def enroll_the_veea_hub_in_new_mesh(self, veea_hub_serial_number, user_name):
        veeahub = self.resourceUtils.get_veeahub_for_testing(veea_hub_serial_number)
        owner_id = None
        owner = self.enrollment_db.get_owner_data(user_name)
        if owner is not None:
            owner_id = owner[0]["owner_id"]

        mesh_name = "Mesh-" + veeahub["serialNumber"][-4:]

        payload = self.__get_request_body(owner_id, None, mesh_name, veeahub)
        return self.enrollmentClient.start(payload, user_name)

    def add_veea_hub_in_mesh(self, veea_hub_serial_number, mesh_id):
        veeahub = self.resourceUtils.get_veeahub_for_testing(veea_hub_serial_number)
        veeahub_already_enrolled = self.elasticsearch.get_veeahub_resource_by_mesh_id(mesh_id)[0]

        enrolled_veeahub = VeeaHubModel(veeahub_already_enrolled)
        owner_id = enrolled_veeahub.get_owner_id()
        mesh_name = enrolled_veeahub.get_mesh_name()

        user = self.enrollment_db.get_owner_by_id(owner_id)
        user_name = user[0]["email"]

        payload = self.__get_request_body(owner_id, mesh_id, mesh_name, veeahub)
        return self.enrollmentClient.start(payload, user_name)

    def get_mesh_id_from_enrollment_response(self, response):
        data = response.json()
        mesh = data["response"]["mesh"]
        return mesh["id"]

    def should_return_status_code_200_after_enroll_veea_hub(self, response):
        self.assertEqual(200, response.status_code)

        data = response.json()
        meta = data["meta"]
        device = data["response"]["device"]
        mesh = data["response"]["mesh"]
        connection = data["response"]["connection"]

        self.assertEqual(200, meta["status"])
        self.assertIsNotNone(device)
        self.assertIsNotNone(mesh)
        self.assertIsNotNone(connection)

        return True

    def response_data_should_match_with_database(self, response):
        response = response.json()
        meta = response["meta"]
        device = response["response"]["device"]
        mesh = response["response"]["mesh"]

        serial_number = device["id"]
        mesh_id = mesh["id"]

        # Check data in bootstrap.veea_hub_configuration_data table
        tar_data = self.bootstrap_db.get_veea_hub_configuration_data(serial_number)
        self.assertIsNotNone(tar_data)
        self.assertTrue(len(tar_data) > 0, "There are not tar.gz( table bootstrap_db.veea_hub_configuration_data)" +
                        " for VeeaHub " + serial_number)
        self.assertEqual(3, len(tar_data), "The VeaHub configuration not march, it should have 3 tar.gz" +
                         " (com-veea-base-ies, mas-certs, template-basic) but it has " +
                         str(len(tar_data)))

        # Check mesh data in bootstrap_db
        mesh_data = self.bootstrap_db.get_mesh_by_id(mesh_id)
        self.assertIsNotNone(mesh_data)
        self.assertEqual(1, len(mesh_data),
                         "Mesh record not found in the table bootstrap_db.mesh for VeeaHub " + serial_number)
        owner_id = mesh_data[0]["owner_uuid"]
        self.assertIsNotNone(owner_id)

        # Check software offered to veeahub in bootstra_db
        offered_software = self.bootstrap_db.get_offered_software_veea_hub(serial_number)
        self.assertIsNotNone(offered_software)
        self.assertTrue(len(offered_software) > 0, "Offered software for veeahub {} not found in "
                                                   "bootstrap_db.offered_software_veea_hub".format(serial_number))

        # Check owner exist in enrollment db
        owner_data = self.enrollment_db.get_owner_by_id(owner_id)
        self.assertIsNotNone(owner_data)
        self.assertEqual(1, len(owner_data), "Owner not found in enrollment_db.user for VeeaHub " + serial_number)

        # Check Veea hub status in enrollment_db
        veea_hub_status = self.enrollment_db.get_enroll_status_by_veea_hub(serial_number)
        self.assertIsNotNone(veea_hub_status)
        self.assertEqual(0, len(veea_hub_status), "VeeaHub status found. When the VeeaHub is enrolled, it should not " +
                         "have status in enrollment_db.enroll_status")

        self.check_asserts_for_enrolled_veeahub_in_elasticsearch(serial_number)

    def check_asserts_for_enrolled_veeahub_in_elasticsearch(self, serial_number):
        enrolled_veeahubs = self.elasticsearch.get_veeahub_resource_by_serial_number(serial_number)
        self.assertIsNotNone(enrolled_veeahubs)
        self.assertEqual(1, len(enrolled_veeahubs), "The Veeahub {} not found in elasticsearch".format(serial_number))
        veeahub = enrolled_veeahubs[0]
        keys = list(veeahub.keys())
        expected_size_keys = 9
        self.assertEqual(expected_size_keys, len(keys), "Resource should have {} field in the root, but it has {}"
                         .format(expected_size_keys, len(keys)))

        expected_size_keys = 15  # MN don't have ssid and password
        enrolled_veeahub = VeeaHubModel(veeahub)
        if enrolled_veeahub.is_men():
            expected_size_keys = 17  # MEN has ssid and password

        objects = list(veeahub["resourceCharacteristic"])
        self.assertEqual(expected_size_keys, len(objects), "resourceCharacteristic should have {} items, "
                                                           "but it has {} items int he array"
                         .format(expected_size_keys, len(objects)))

    def __get_request_body(self, owner_id, mesh_id, mesh_name, veeahub):
        action_type = "create"
        if mesh_id is not None:
            action_type = "addTo"
        body = {
            "owner": owner_id,
            "version": "2.5.0",
            "code": veeahub['code'],
            "name": veeahub['name'],
            "nc_node_country": "US",
            "nc_node_timezone_area": "America",
            "nc_node_timezone_region": "New_York",
            "ssid": "My Veeahub",
            "password": "Password",
            "connection": {
                "type": "ethernet"
            },
            "mesh": {
                "type": action_type,
                "name": mesh_name,
                "id": mesh_id
            }
        }

        return body
