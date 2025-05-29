import os

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