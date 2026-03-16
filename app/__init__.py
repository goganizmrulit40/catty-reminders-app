"""
This module builds shared parts for other modules.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import os

from fastapi.templating import Jinja2Templates


# --------------------------------------------------------------------------------
# Read Configuration
# --------------------------------------------------------------------------------

with open('config.json') as config_json:
  config = json.load(config_json)
  users = config['users']
  db_path = config['db_path']

# Получаем текущий коммит из git
import subprocess
try:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd="/opt/catty-reminders",
        capture_output=True,
        text=True,
        timeout=2
    )
    if result.returncode == 0:
        DEPLOY_REF = result.stdout.strip()
    else:
        DEPLOY_REF = "NA"
except:
    DEPLOY_REF = "NA"

# --------------------------------------------------------------------------------
# Establish the Secret Key
# --------------------------------------------------------------------------------

secret_key = config['secret_key']


# --------------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------------

templates = Jinja2Templates(directory="templates")
