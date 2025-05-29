from . import config
import os
import logging
import traceback
from qgis.core import QgsApplication
from datetime import datetime

# Create log directory in user's home directory, OS-independent
profile_folder = QgsApplication.qgisSettingsDirPath()
log_dir = os.path.join(profile_folder, "logs", "intelli_geo")
os.makedirs(log_dir, exist_ok=True)

# Define paths for error and debug logs
error_log_path = os.path.join(log_dir, "error.log")
debug_log_path = os.path.join(log_dir, "debug.log")

# Configure error logger
error_logger = logging.getLogger("intelli_geo_error")
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(error_log_path, mode='a')
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)
error_logger.error("=== New Logging Session Started ===")

# Configure debug logger
debug_logger = logging.getLogger("intelli_geo_debug")
debug_logger.setLevel(logging.DEBUG)
debug_handler = logging.FileHandler(debug_log_path, mode='a')
debug_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
debug_handler.setFormatter(debug_formatter)
debug_logger.addHandler(debug_handler)
debug_logger.debug("=== New Logging Session Started ===")


def log_debug(message):
    if config.DEBUG_MODE:
        debug_logger.debug(f"\n{message}\n{'-'*60}")
        
def log_error(message, exc=None):
    # Log to standard QGIS error logger
    if exc:
        parts = [f"Message: {message}"]
        parts.append(f"Error Type: {type(exc).__name__}")
        if hasattr(exc, "returncode"):
            parts.append(f"Command failed with exit code: {exc.returncode}")
        parts.append(f"Error Message: {str(exc)}")
        if hasattr(exc, "output"):
            parts.append("=== Output and Error ===")
            if isinstance(exc.output, bytes):
                parts.append(exc.output.decode("utf-8", errors="replace"))
            else:
                parts.append(str(exc.output))
        parts.append("=== Traceback ===")
        parts.append(traceback.format_exc())
        error_logger.error("\n".join(parts) + "\n" + "-" * 60)
    else:
        error_logger.error(f"\n{message}\n{'-'*60}")