from summary.acs_summary import ACSSummary
from summary.es_summary import EnrollmentSummary
from clients.authorization import VeeaAuthorization


class Summary:
    __acs_summary = {}
    __es_summary = {}
    __auth = {}

    def __init__(self):
        self.__acs_summary = ACSSummary()
        self.__es_summary = EnrollmentSummary()
        self.__auth = VeeaAuthorization()

    def print_acs_summary(self):
        user = self.__auth.get_user_inf()
        self.__acs_summary.print_summary(user["veeaUserId"])

    def print_es_summary(self):
        pass
