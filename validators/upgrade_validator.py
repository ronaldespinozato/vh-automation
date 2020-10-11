from http import HTTPStatus

class UpgradeValidator:
    def check_upgrade_response_status_code(self, response):
        if response["meta"] is None:
            return False
        if response["meta"]["status"] is None:
            return False

        return response["meta"]["status"] == HTTPStatus.OK

    def check_upgrade_response_data(self, response, user_id):
        if response["response"] is None:
            return False
        return response["response"]["hubAction"][0] == "recovery"
