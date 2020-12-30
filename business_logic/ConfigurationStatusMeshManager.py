from clients.enrollment.enrollment_client import EnrollmentClient
from clients.acs.els_client import ElasticSearchACS
from clients.bootstrap.bootstrap_db import BootstrapDB
from clients.enrollment.enrollment_db import EnrollmentDB
from string_utils.validation import is_full_string

from conf import settings
from unittest import TestCase
from robot.api import logger


class ConfigurationStatusMeshManager(TestCase):

    def __init__(self):
        super().__init__()
        settings.set_local_env()
        self.enrollment_client = EnrollmentClient()
        self.bootstrap_db = BootstrapDB()
        self.enrollment_db = EnrollmentDB()
        self.elasticsearch = ElasticSearchACS()

    def get_configuration_status_mesh(self, user_name):
        response = self.enrollment_client.get_mesh_config(user_name)
        return response

    def should_return_status_code_200_after_get_configuration_status_mesh(self, response):
        self.assertEqual(200, response.status_code,
                         "The status code of response is not 200 after call get configuration status mesh")
        data = response.json()
        meta = data["meta"]
        self.assertEqual(200, meta["status"], "Body response does not have status 200 "
                                              "after call get configuration status mesh")

    def check_assert_mesh_configuration_status_after_enrollment_veea_hub(self, response):
        self.check_assert_mesh_configuration_status_field_owner(response)
        self.check_assert_mesh_configuration_status_field_mas(response)
        self.check_assert_mesh_configuration_status_field_beacons(response)
        self.check_assert_mesh_configuration_status_field_mesh_data(response)
        self.check_assert_mesh_configuration_status_field_device_after_enrollment_veea_hub(response)

    def check_assert_mesh_configuration_status_after_upgrade_mesh(self, response):
        self.check_assert_mesh_configuration_status_field_owner(response)
        self.check_assert_mesh_configuration_status_field_mas(response)
        self.check_assert_mesh_configuration_status_field_beacons(response)
        self.check_assert_mesh_configuration_status_field_mesh_data(response)
        self.check_assert_mesh_configuration_status_field_device_after_upgrade_mesh(response)

    def check_assert_mesh_configuration_status_after_upgrade_mesh_and_complete_its_configuration(self, response):
        self.check_assert_mesh_configuration_status_field_owner(response)
        self.check_assert_mesh_configuration_status_field_mas(response)
        self.check_assert_mesh_configuration_status_field_beacons(response)
        self.check_assert_mesh_configuration_status_field_mesh_data(response)
        self.check_assert_mesh_configuration_status_field_device_after_upgrade_mesh_and_complete_its_configuration(response)

    def check_assert_mesh_configuration_status_field_mesh_data(self, response):
        data = response.json()
        meshes = data["response"]["meshes"]
        for mesh in meshes:
            self.assertTrue(is_full_string(mesh["id"]), "id is not a string, it should be a string data")
            self.assertTrue(is_full_string(mesh["name"]), "name is not a string, it should be a string data")
            self.assertTrue(is_full_string(mesh["nc_node_country"]), "nc_node_country is not a string")
            self.assertTrue(is_full_string(mesh["nc_node_timezone_area"]), "nc_node_timezone_area is not a string")
            self.assertTrue(is_full_string(mesh["nc_node_timezone_region"]), "nc_node_timezone_region is not a string")

    def check_assert_mesh_configuration_status_field_device_after_upgrade_mesh_and_complete_its_configuration(self, response):
        data = response.json()
        meshes = data["response"]["meshes"]
        for mesh in meshes:
            devices = mesh["devices"]
            self.assertTrue(len(devices) > 0, "The Mesh does not have Devices")
            for veea_hub in devices:
                self.assertTrue(is_full_string(veea_hub["id"]), "id is not a VeeaHub serial number")
                self.assertTrue(is_full_string(veea_hub["name"]), "name is not a string")
                self.assertEqual("ready", veea_hub["status"], "The status is not ready")
                self.assertEqual(None, veea_hub["progress"], "The progress is invalid, it should be null or 100")
                self.assertEqual(None, veea_hub["error"], "The VeeaHub {} has errors".format(veea_hub["id"]))
                self.assertTrue(isinstance(veea_hub["isMEN"], bool), "The field isMen is not a boolean for {}"
                                .format(veea_hub["id"]))

    def check_assert_mesh_configuration_status_field_device_after_upgrade_mesh(self, response):
        data = response.json()
        meshes = data["response"]["meshes"]
        for mesh in meshes:
            devices = mesh["devices"]
            self.assertTrue(len(devices) > 0, "The Mesh does not have Devices")
            for veea_hub in devices:
                self.assertTrue(is_full_string(veea_hub["id"]), "id is not a VeeaHub serial number")
                self.assertTrue(is_full_string(veea_hub["name"]), "name is not a string")
                self.assertEqual("bootstrapping", veea_hub["status"], "The status is not bootstrapping")
                self.assertEqual(25, veea_hub["progress"], "The progress is invalid, it should be 25")
                self.assertEqual(None, veea_hub["error"], "The VeeaHub {} has errors".format(veea_hub["id"]))
                self.assertTrue(isinstance(veea_hub["isMEN"], bool), "The field isMen is not a boolean for {}"
                                .format(veea_hub["id"]))

    def check_assert_mesh_configuration_status_field_device_after_enrollment_veea_hub(self, response):
        data = response.json()
        meshes = data["response"]["meshes"]
        for mesh in meshes:
            devices = mesh["devices"]
            self.assertTrue(len(devices) > 0, "The Mesh does not have Devices")
            for veea_hub in devices:
                self.assertTrue(is_full_string(veea_hub["id"]), "id is not a VeeaHub serial number")
                self.assertTrue(is_full_string(veea_hub["name"]), "name is not a string")
                self.assertEqual("bootstrapping", veea_hub["status"], "The status is not bootstrapping")
                self.assertEqual(57, veea_hub["progress"], "The progress is invalid, it should be 57")
                self.assertEqual(None, veea_hub["error"], "The VeeaHub {} has errors".format(veea_hub["id"]))
                self.assertTrue(isinstance(veea_hub["isMEN"], bool), "The field isMen is not a boolean for {}"
                                .format(veea_hub["id"]))

    def check_assert_mesh_configuration_status_field_beacons(self, response):
        # validate beacons
        data = response.json()
        response_data = data["response"]
        beacons = response_data["beacons"]
        self.assertTrue(len(beacons) > 0, "The beacons array is empty, it should have an object data")
        self.assertTrue(is_full_string(beacons[0]["encryptKey"]),
                        "encryptKey is null or empty, it should have a string value")
        self.assertTrue(is_full_string(beacons[0]["instanceID"]),
                        "instanceID is null or empty, it should have a string value")
        self.assertTrue(is_full_string(beacons[0]["subdomain"]),
                        "subdomain is null or empty, it should have a string value")

    def check_assert_mesh_configuration_status_field_mas(self, response):
        # validate mas data
        data = response.json()
        response_data = data["response"]
        mas = response_data["mas"]
        self.assertTrue(len(mas) > 0, "The array MAS data is empty, it should have a object data")
        self.assertTrue(is_full_string(mas[0]["host"]), "mas host is null or empty, it should have an url")
        self.assertTrue(is_full_string(mas[0]["userKey"]), "mas userKey is null or empty,"
                                                           " it should be have a string value")

    def check_assert_mesh_configuration_status_field_owner(self, response):
        data = response.json()
        response_data = data["response"]
        self.assertTrue(is_full_string(response_data["ownerId"]), "OwnerId is empty or null, it should be a string")
