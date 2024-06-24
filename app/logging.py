import json
import os

from app.exceptions import IncorrectConfiguration
from app.settings import ROOT_DIR


def logging_config():
    file_path = os.path.join(ROOT_DIR, 'logging' + '.json')
    if not file_path:
        raise IncorrectConfiguration('Improperly Configured')
    try:
        with open(file_path) as fd:
            content = fd.read()
            return json.loads(content)
    except Exception:
        raise IncorrectConfiguration('Improperly Configured')


LOGGING = logging_config()
