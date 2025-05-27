import os
from dotenv import load_dotenv

plugin_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(plugin_dir, ".env")
load_dotenv(dotenv_path)

DEBUG_MODE = os.environ.get("INTELLIGEO_DEBUG", "False") == "True"