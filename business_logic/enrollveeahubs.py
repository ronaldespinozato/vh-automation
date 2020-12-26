import json
import time
from pathlib import Path
from clients.enrollment.enrollment_client import EnrollmentClient
from validators.user_config_status import UserConfigStatus
from clients.bootstrap.bootstrap_db import BootstrapDB


class ManagerEnrollVeeaHub:

    def enroll_owner_veeahubs(self):
        users = self.__read_users_from_resource()
        for user in users:
            username = user['username']
            for mesh in user['meshes']:
                self.__enroll_mesh_veeahub(mesh, username)
                print("")

        # response = EnrollmentClient().get_mesh_config(user['username'])
        # passed = UserConfigStatus().check_user_config_response_status_code(response)
        # print(passed)

    def un_enroll_veeahubs(self):
        users = self.__read_users_from_resource()
        for user in users:
            for mesh in user['meshes']:
                veea_hubs = self.__read_mesh_veeahubs_from_resource(mesh)
                for veea_hub in veea_hubs:
                    EnrollmentClient().un_enroll_veeahub(user['username'], veea_hub['serialNumber'])

    def __read_users_from_resource(self):
        project_path = Path(".").resolve()
        file = Path("{}/resource/users.json".format(project_path)).resolve()

        with open(file) as f:
            owners = json.load(f)

        return owners

    def __read_veeahub_from_resource(self, serial_number):
        project_path = Path(".").resolve()
        file = Path("{}/resource/veeahubs/{}.json".format(project_path, serial_number)).resolve()

        with open(file) as f:
            veeahub = json.load(f)

        return veeahub

    def __read_mesh_veeahubs_from_resource(self, mesh):
        veea_hubs = []
        for serial_number in mesh["veeahubs"]:
            veeahub = self.__read_veeahub_from_resource(serial_number)
            veea_hubs.append(veeahub)
        return veea_hubs

    def __enroll_mesh_veeahub(self, mesh, username):
        enroll_client = EnrollmentClient()
        owner_id = enroll_client.get_mesh_config(username)['response']['ownerId']
        mesh_id = None
        for veea_hub in self.__read_mesh_veeahubs_from_resource(mesh):
            body = self.__get_request_body(owner_id, mesh_id, mesh['name'], veea_hub)
            response = enroll_client.start(body, username)
            if mesh_id is None:
                mesh_id = response.json()["response"]["mesh"]["id"]
            print("> Enrolled VeeaHub: username => {}, mesh_id => {}, veea_hub => {}".format(username, mesh_id, veea_hub["serialNumber"]))

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
