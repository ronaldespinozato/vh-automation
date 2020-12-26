import json
from pathlib import Path


class ResourceTestUtil:
    config = {}

    def __init__(self):
        self.config = {}

    def get_users_for_testing(self):
        list_users_names = []
        user_test_data = self.__read_users_from_resource()
        for user_data in user_test_data:
            list_users_names.append(user_data["username"])
        # distinct users
        return set(list_users_names)

    def get_veeahub_for_testing(self, serial_number):
        return self.__read_veeahub_from_resource(serial_number)

    def __read_users_from_resource(self):
        project_path = Path("").resolve()
        file = Path("{}/resource/users.json".format(project_path)).resolve()

        with open(file) as f:
            owners = json.load(f)

        return owners

    def __read_veeahub_from_resource(self, serial_number):
        project_path = Path("").resolve()
        file = Path("{}/resource/veeahubs/{}.json".format(project_path, serial_number)).resolve()

        with open(file) as f:
            veeahub = json.load(f)

        return veeahub
