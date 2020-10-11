import json
from http import HTTPStatus
from clients.acs.els_client import ElasticSearchACS


class UserConfigStatus:
    els = {}

    def __init__(self):
        self.els = ElasticSearchACS()

    def check_user_config_response_status_code(self, response):
        if response["meta"] is None:
            return False
        if response["meta"]["status"] is None:
            return False

        return response["meta"]["status"] == HTTPStatus.OK

    def check_user_config_response(self, user_id, response):
        mas_data = self.els.get_mas_user_data(user_id)
        resources = self.els.get_veeahub_resource_by_user_id(user_id)
        veeahub_config = self.els.get_veeahub_config(user_id)

        mesh = self.__get_expected_mesh(resources[0])
        mas = self.__get_expected_mas_data(mas_data)
        beacon = self.__get_expected_beacons(veeahub_config)
        devices = self.__get_expected_devices(response)

        passed1 = json.dumps(mas) == json.dumps(response["response"]["mas"])
        passed2 = json.dumps(beacon) == json.dumps(response["response"]["beacons"])

        return passed1 and passed2

    def __get_pair_value(self, pair_value_list, field_name):
        for pair in pair_value_list:
            if pair["name"] == field_name:
                return pair

    def __get_expected_mas_data(self, mas_data):
        pair_value_list = mas_data["pairListData"][0]["values"]
        pair_value = self.__get_pair_value(pair_value_list, "masUserApiKey")
        mas_user_api_key = pair_value["value"]

        url = self.__get_pair_value(pair_value_list, "masUserUri")["value"]
        list_url = url.split('/')
        mar_url = "{}://{}".format(list_url[0], list_url[2])
        return [{"host": mar_url, "userKey": mas_user_api_key}]

    def __get_expected_beacons(self, veeahub_config_data):
        pair_value_list = veeahub_config_data["pairListData"][0]["values"]
        encrypt_key = self.__get_pair_value(pair_value_list, "ncBeaconEncryptKey")["value"]
        instance_id = self.__get_pair_value(pair_value_list, "ncBeaconInstanceId")["value"]
        domain = self.__get_pair_value(pair_value_list, "ncBeaconSubDomain")["value"]

        return [{"encryptKey": encrypt_key, "instanceID": instance_id, "subdomain": domain}]

    def __get_expected_mesh(self, veeahub_resource):
        characteristic = veeahub_resource["resourceCharacteristic"]
        mesh_name = self.__get_pair_value(characteristic, "meshName")["value"]
        mesh_id = self.__get_pair_value(characteristic, "meshId")["value"]
        area = self.__get_pair_value(characteristic, "cnNodeArea")["value"]
        country = self.__get_pair_value(characteristic, "cnNodeCountry")["value"]
        region = self.__get_pair_value(characteristic, "cnNodeRegion")["value"]

        return {
            "id": mesh_id,
            "name": mesh_name,
            "nc_node_country": country,
            "nc_node_timezone_area": area,
            "nc_node_timezone_region": region
        }

    def __get_expected_devices(self, veeahub_resources, status):
        expected = []
        for data in veeahub_resources:
            expected.append(self.__get_expected_device(data, status))

        return expected


    def __get_expected_device(self, veeahub_resource, status):
        characteristic = veeahub_resource["resourceCharacteristic"]
        veeahub_serial = self.__get_pair_value(characteristic, "veeahubSerialNumber")["value"]
        veeahub_name = self.__get_pair_value(characteristic, "veeahubSerialNumber")["veeahubName"]
        owner_id = self.__get_pair_value(characteristic, "veeahubOwnerId")["value"]
        veeahub_type = self.__get_pair_value(characteristic, "cnNodeType")["value"]

        is_men = False
        if veeahub_type == "MEN":
            is_men = True

        return {"id": veeahub_serial, "name": veeahub_name, "status": status, "progress": None, "error": None,
                "isMEN": is_men}

    def __get_expected_owner_id(self, veeahub_resource):
        characteristic = veeahub_resource["resourceCharacteristic"]
        owner_id = self.__get_pair_value(characteristic, "veeahubOwnerId")["value"]
        return owner_id
