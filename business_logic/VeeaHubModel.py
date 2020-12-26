class VeeaHubModel:
    resource = {}

    def __init__(self, enrolled_resource):
        self.resource = enrolled_resource

    def get_mesh_id(self):
        return self.__get_value_by_name_from_characteristic("meshId")

    def get_owner_id(self):
        return self.__get_value_by_name_from_characteristic("veeahubOwnerId")

    def get_serial_number(self):
        return self.__get_value_by_name_from_characteristic("veeahubSerialNumber")

    def get_mesh_name(self):
        return self.__get_value_by_name_from_characteristic("meshName")

    def get_applied_packages(self):
        return self.__get_value_by_name_from_characteristic("packageId")

    def is_men(self):
        node_type = self.__get_value_by_name_from_characteristic("cnNodeType")
        if node_type == 'MEN':
            return True
        return False

    def __get_value_by_name_from_characteristic(self, name):
        resource_characteristic = self.resource["resourceCharacteristic"]
        for characteristic in resource_characteristic:
            if characteristic["name"] == name:
                return characteristic["value"]

        return None
