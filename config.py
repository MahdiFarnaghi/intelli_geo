import os, sys


def load_env_file(path=None):
    """Load environment variables from a .env file."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()


load_env_file()

DEBUG_MODE = os.environ.get("INTELLIGEO_DEBUG", "False") == "True"

BACKEND_URL = os.environ.get("BACKEND_URL", "https://owsgip.itc.utwente.nl/intelligeo/")

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

EXTLIBS_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "extlibs")
if not os.path.exists(EXTLIBS_DIRECTORY):
    os.makedirs(EXTLIBS_DIRECTORY, exist_ok=True)
if EXTLIBS_DIRECTORY not in sys.path:
    sys.path.insert(0, EXTLIBS_DIRECTORY)


REQUIREMENTS_PATH = (
    os.path.join(SCRIPT_DIRECTORY, "requirements.txt")
    if not DEBUG_MODE
    else os.path.join(SCRIPT_DIRECTORY, "requirements-dev.txt")
)
