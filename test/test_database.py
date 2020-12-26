import json
import sys
from pathlib import Path

project_path = Path(".").resolve()
sys.path.insert(0, str(project_path))
print(sys.path)

from conf.settings import set_env
from clients.acs import acs_db

# ================================================
#  python ./test/test_database.py local ronald.espinoza@mojix.com
# ================================================

# local, dev, qa, prod
environment = sys.argv[1]
# ronald.espinoza@mojix.com
impersonated_username = sys.argv[2]
set_env(environment, impersonated_username)

acs_db = acs_db.AcsDB()
data = acs_db.get_realm_to_privafy_carrier_id()

print(data)
