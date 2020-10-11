import json
from http import HTTPStatus
from pathlib import Path
from clients.acs.els_client import ElasticSearchACS


class EnrollmentValidator:
    els = {}

    def __init__(self):
        self.els = ElasticSearchACS()

    def check_enrollment_response_status_code(self, response):
        if response["meta"] is None:
            return False
        if response["meta"]["status"] is None:
            return False
        return response["meta"]["status"] == HTTPStatus.OK

    def check_downgrade_response_data(self, response, serial_number):
        if response["response"] is None:
            return False

        resource = self.els.get_veeahub_resource_by_serial_number(serial_number)

        passed1 = json.dumps(response["response"]["device"]) == json.dumps(self.__get_expected_veeahub(resource))
        passed2 = json.dumps(response["response"]["mesh"]) == json.dumps(self.__get_expected_mesh(resource))
        passed3 = response["response"]["connection"] == "ethernet"
        return passed1 and passed2 and passed3

    def __get_pair_value(self, pair_value_list, field_name):
        for pair in pair_value_list:
            if pair["name"] == field_name:
                return pair

    def __get_expected_veeahub(self, resource):
        characteristic = resource["resourceCharacteristic"]
        id = self.__get_pair_value(characteristic, "veeahubSerialNumber")["value"]
        name = self.__get_pair_value(characteristic, "veeahubName")["value"]
        code = self.__get_veeahub_code(id)
        return {
            "id": id,
            "name": name,
            "code": code
        }

    def __get_veeahub_code(self, serial_number):
        project_path = Path(".").resolve()
        file = Path("{}/resource/veeahubs/{}".format(project_path, serial_number)).resolve()
        with open(file) as f:
            self.configJson = json.load(f)
        return self.configJson["code"]

    def __get_expected_mesh(self, resource):
        characteristic = resource["resourceCharacteristic"]
        mesh_id = self.__get_pair_value(characteristic, "meshId")["value"]
        mesh_name = self.__get_pair_value(characteristic, "meshName")["value"]
        country = self.__get_pair_value(characteristic, "cnNodeCountry")["value"]
        area = self.__get_pair_value(characteristic, "cnNodeArea")["value"]
        region = self.__get_pair_value(characteristic, "cnNodeRegion")["value"]

        return {
            "id": mesh_id,
            "name": mesh_name,
            "nc_node_country": country,
            "nc_node_timezone_area": area,
            "nc_node_timezone_region": region
        }
