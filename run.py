import json
import sys
from business_logic.enrollveeahubs import ManagerEnrollVeeaHub
from summary.acs_summary import ACSSummary
from summary.summary import Summary
from clients.acs.resource_client import ResourceClient
from conf.settings import set_env
from clients.authorization import VeeaAuthorization

# ================================================
# python run.py local ronald.espinoza@mojix.com
# ================================================

# local, dev, qa, prod
environment = sys.argv[1]
# ronald.espinoza@mojix.com
impersonated_username = sys.argv[2]
set_env(environment, impersonated_username)

summary = Summary()
summary.print_acs_summary()
summary.print_es_summary()

# client = EnrollmentClient()
# client.start({}, "ronald.espinoza@mojix.com")
# client.enrollVeeaHub("C05BCB00C0A000001022")

# ManagerEnrollVeeaHub().enroll_owner_veeahubs()
# ManagerEnrollVeeaHub().un_enroll_veeahubs()


# Config().get_acs_base_url()
# print(Config().get_config_bootstrap_db())

# data = BootstrapDB().get_veeahub_by_serial_number("C05BCB00C0A000001024")
# data = BootstrapDB().get_veea_hub_configuration_data("C05BCB00C0A000001024")
# print(data)

# data = ElasticSearchACS().get_veeahub_resource_by_mesh_id("742cf0bd-b1ff-460f-ba1a-4a19c112053e")
# data = ElasticSearchACS().get_veeahub_resource_by_serial_number("C05BCB00C0A000001022")
# data = ElasticSearchACS().get_mas_user_data("1")
# data = ElasticSearchACS().get_veeahub_config("1")
# print(json.dumps(data))

# ACSSummary().print_summary("1")
# data = ResourceClient().get_resource_by_username("ronald.espinoza@mojix.com")
# print(json.dumps(data))
