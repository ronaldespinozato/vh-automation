import json
from tabulate import tabulate
from clients.acs.els_client import ElasticSearchACS
from clients.acs.resource_client import ResourceClient
from clients.acs.package_client import PackageClient


class ACSSummary:
    __els_client = {}
    __resource_client = {}
    __package_client = {}

    def __init__(self):
        self.__els_client = ElasticSearchACS()
        self.__resource_client = ResourceClient()
        self.__package_client = PackageClient()

    def get_owner_with_its_mesh(self, user_id):
        owner = {}
        # resources = self.__els_client.get_veeahub_resource_by_user_id(user_id)
        resources = self.__resource_client.get_resource_by_username()
        if len(resources) != 0:
            owner = self.__get_owner_data(resources[0])

        mesh_list = []
        aux_mesh_dic = {}
        for resource in resources:
            mesh = self.__get_mesh_data(resource)
            mesh_id = mesh["meshId"]
            if aux_mesh_dic.get(mesh_id) is None:
                aux_mesh_dic[mesh_id] = mesh_id
                veeahubs = self.__get_veeahubs_by_mesh_id(resources, mesh_id)
                mesh["veeahubs"] = veeahubs
                mesh_list.append(mesh)
        owner["meshes"] = mesh_list
        return owner

    def __get_veeahubs_by_mesh_id(self, resources, mesh_id):
        result = []
        for resource in resources:
            mesh = self.__get_mesh_data(resource)
            if mesh["meshId"] == mesh_id:
                veeahub = self.__get_veeahub_data(resource)
                result.append(veeahub)
        return result

    def __get_mesh_data(self, resource):
        mesh = {}
        pair_list = resource["resourceCharacteristic"]
        mesh["meshId"] = self.__get_value(pair_list, "meshId")
        mesh["meshName"] = self.__get_value(pair_list, "meshName")
        mesh["cnNodeArea"] = self.__get_value(pair_list, "cnNodeArea")
        mesh["cnNodeCountry"] = self.__get_value(pair_list, "cnNodeCountry")
        mesh["cnNodeRegion"] = self.__get_value(pair_list, "cnNodeRegion")
        return mesh

    def __get_veeahub_data(self, resource):
        veeahub = {}
        pair_list = resource["resourceCharacteristic"]
        veeahub["veeahubSerialNumber"] = self.__get_value(pair_list, "veeahubSerialNumber")
        veeahub["veeahubName"] = self.__get_value(pair_list, "veeahubName")
        veeahub["veeahubConnectionType"] = self.__get_value(pair_list, "veeahubConnectionType")
        veeahub["packageId"] = self.__get_value(pair_list, "packageId").split(",")
        veeahub["lastError"] = self.__get_veeahub_last_error(resource)
        return veeahub

    def __get_owner_data(self, resource):
        pair_list = resource["resourceCharacteristic"]
        data = {}
        data["veeaUserId"] = self.__get_value(pair_list, "veeaUserId")
        data["veeahubOwnerId"] = self.__get_value(pair_list, "veeahubOwnerId")
        data["ownerCertSerialNumber"] = self.__get_value(pair_list, "ownerCertSerialNumber")
        data["individualUuid"] = self.__get_value(pair_list, "individualUuid")
        return data

    def __get_veeahub_last_error(self, resource):
        errors = self.__get_veeahub_errors(resource)
        if len(errors) == 0:
            return None
        else:
            return errors[-1]

    def __get_veeahub_errors(self, resource):
        errors = []
        for history in resource["operationalHistory"]:
            if not history["succeeded"]:
                errors.append(errors)
        return errors

    def __get_value(self, pair_list, field_name):
        for pair in pair_list:
            if pair["name"] == field_name:
                return pair["value"]
        return None

    def print_summary(self, user_id):
        owner = self.get_owner_with_its_mesh(user_id)

        print(self.__get_owner_info_summary(owner), end='')
        print("--------------------------------------------------")
        summary = []
        for mesh in owner["meshes"]:
            print(self.__get_mesh_info_summary(mesh), end='')
            veeahub_summary = []
            for veeahub in mesh["veeahubs"]:
                veeahub_summary.append(self.__get_veeahub_summary(veeahub))
            print(tabulate(veeahub_summary, headers="keys"))
            print("")

    def __get_owner_info_summary(self, owner):
        title = "OwnerId: {}\nUserId: {}\n".format(owner["veeahubOwnerId"], owner["veeaUserId"])
        return title
    def __get_mesh_info_summary(self, mesh):
        title = "MeshName: {}\nMeshId: {}\n".format(mesh["meshName"], mesh["meshId"])
        return title

    def __get_veeahub_summary(self, veeahub):
        error_msg = "-"
        if veeahub["lastError"] is not None:
            error_msg = veeahub["lastError"]["info"]

        summary = {"SerialNumber": veeahub["veeahubSerialNumber"], "ErrorMessageACS": error_msg}

        packages_id_column = []
        packages_type_column = []
        for package_id in veeahub["packageId"]:
            package = self.__package_client.get_package_by_id(package_id)
            packages_id_column.append(package_id)
            packages_type_column.append("{}({})".format(package["type"], package["version"]))

        summary["AppliedPackages"] = ",".join(packages_id_column)
        summary["PackageInfo"] = ",".join(packages_type_column)

        return summary

