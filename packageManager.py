import os
import sys
import platform
import subprocess
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsApplication
from datetime import datetime
from . import log_manager



class PackageManager:
    def __init__(self, dependencies):
        """
        Initialize with a list of required dependencies.
        :param dependencies: List of module names as strings.
        """

        log_manager.log_debug("Initializing PackageManager")

        self.scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.extpluginDir = os.path.join(self.scriptDir, "extlibs")
        self.qgisPython = self._get_qgis_python_path()

        log_manager.log_debug(
            f"QGIS Python executable: {self.qgisPython}\nscriptDir: {self.scriptDir}\nextpluginDir: {self.extpluginDir}"
        )

        if self.extpluginDir not in sys.path:
            sys.path.insert(0, self.extpluginDir)
            log_manager.log_debug(
                f"Added extpluginDir to sys.path: {self.extpluginDir}"
            )

        print(f"extpluginDir: {self.extpluginDir}")
        self.dependencies = dependencies
        self.missingDependencies = []

    def _get_qgis_python_path(self):
        """
        Return the path to the Python interpreter used by QGIS.
        Handles macOS, Windows, and Linux.
        """
        python_path = sys.executable
        system = platform.system()

        if system == "Darwin" and python_path.endswith("QGIS"):
            python_path = os.path.join(os.path.dirname(python_path), "bin", "python3")

        elif system == "Windows":
            # Typically: C:\Program Files\QGIS <version>\bin\qgis-bin.exe
            # We want:   C:\Program Files\QGIS <version>\bin\python.exe
            qgis_bin_dir = os.path.dirname(python_path)
            candidate = os.path.join(qgis_bin_dir, "python.exe")
            if os.path.exists(candidate):
                python_path = candidate

        elif system == "Linux" and "qgis" in python_path.lower():
            possible_path = os.path.join(os.path.dirname(python_path), "bin", "python3")
            if os.path.exists(possible_path):
                python_path = possible_path

        return python_path

    def checkDependencies(self):
        """
        Check for missing dependencies and prompt the user to install them.
        """
        log_manager.log_debug(
            "Checking dependencies with checkDependencies(): {}".format(
                self.dependencies
            )
        )

        self.missingDependencies = [
            dep for dep in self.dependencies if not self._isModuleInstalled(dep)
        ]
        log_manager.log_debug(f"Missing dependencies:{self.missingDependencies}")
        if self.missingDependencies:
            self._promptInstallation()

    def _isModuleInstalled(self, moduleName):
        """
        Check if a Python module is installed.
        :param module_name: Name of the module to check.
        :return: True if installed, False otherwise.
        """
        try:
            __import__(moduleName)
            return True
        except ImportError:
            return False

    def _promptInstallation(self):
        """
        Prompt the user to install missing dependencies.
        """
        reply = QMessageBox.question(
            None,
            "Missing Dependencies",
            f"The following modules are required but not installed:\n\n"
            f'{", ".join(self.missingDependencies)}\n\n'
            "Do you want to install them now?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            self._installDependencies()
        else:
            QMessageBox.warning(
                None,
                "Dependencies Not Installed",
                "The plugin may not function correctly without the required dependencies."
                "Please install them manually.",
            )

    def _installDependencies(self):
        """
        Attempt to install missing dependencies using subprocess and pip.
        Uses platform-aware logic and prioritizes installing to extpluginDir.
        """

        if not self._isPipAvailable():
            log_manager.log_debug("pip is not available, attempting to install it.")
            self._attemptInstallPip()
            if not self._isPipAvailable():
                return

        log_manager.log_debug("Starting _installDependencies() to install missing dependencies.")
        requirementsPath = os.path.join(self.scriptDir, "requirements.txt")

        if not os.path.exists(requirementsPath):
            log_manager.log_debug("requirements.txt not found.")
            QMessageBox.critical(None, "Missing File", "Could not find requirements.txt.")
            return

        install_commands = [
            {
                "description": "Install to extpluginDir using QGIS Python",
                "cmd": [
                    self.qgisPython,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "--target",
                    self.extpluginDir,
                    "-r",
                    requirementsPath,
                ],
            },
            {
                "description": "Fallback: Install to default QGIS Python environment",
                "cmd": [
                    self.qgisPython,
                    "-m",
                    "pip",
                    "install",
                    "--upgrade",
                    "-r",
                    requirementsPath,
                ],
            },
        ]

        for attempt in install_commands:
            try:
                log_manager.log_debug(f"Attempting: {attempt['description']}")
                result = subprocess.run(
                    attempt["cmd"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                log_manager.log_debug(f"{attempt['description']} stdout:\n{result.stdout}")
                log_manager.log_debug(f"{attempt['description']} stderr:\n{result.stderr}")

                missingDependencies = [
                    dep for dep in self.dependencies if not self._isModuleInstalled(dep)
                ]
                if not missingDependencies:
                    QMessageBox.information(
                        None,
                        "Installation Successful",
                        "All required modules have been installed successfully.",
                    )
                    return
                else:
                    log_manager.log_debug(
                        f"Still missing dependencies after {attempt['description']}: {missingDependencies}"
                    )
            except subprocess.CalledProcessError as e:
                stderr = getattr(e, "stderr", None)
                log_manager.log_debug(f"{attempt['description']} failed: {stderr}")
                log_manager.log_error("Dependency installation failed", exc=e)
            except Exception as e:
                log_manager.log_debug(f"Unexpected error during {attempt['description']}: {e}")
                log_manager.log_error("Dependency installation failed", exc=e)

        QMessageBox.critical(
            None,
            "Installation Failed",
            "Failed to install the required modules. Please install them manually using the following command:\n\n"
            f"{self.qgisPython} -m pip install --target {self.extpluginDir} -r {requirementsPath}\n\n"
            "Make sure you have network access and sufficient permissions.",
        )

    def _forceInstallDependencies(self):
        """
        Attempt to force install missing dependencies using pip.
        This uses subprocess and respects extpluginDir targeting.
        """
        requirementsPath = os.path.join(self.scriptDir, "requirements.txt")

        if not os.path.exists(requirementsPath):
            log_manager.log_debug("requirements.txt not found.")
            QMessageBox.critical(
                None, "Missing File", "Could not find requirements.txt."
            )
            return

        if not os.path.exists(self.extpluginDir):
            os.makedirs(self.extpluginDir, exist_ok=True)
            log_manager.log_debug(f"Created extpluginDir: {self.extpluginDir}")

        try:
            log_manager.log_debug("Attempting forced installation using QGIS Python.")
            subprocess.check_call(
                [
                    self.qgisPython,
                    "-m",
                    "pip",
                    "install",
                    "--no-deps",
                    "--force-reinstall",
                    "--use-deprecated=legacy-resolver",
                    "--target",
                    self.extpluginDir,
                    "-r",
                    requirementsPath,
                ]
            )
            log_manager.log_debug("Force install succeeded.")

            if self.extpluginDir not in sys.path:
                sys.path.insert(0, self.extpluginDir)
                log_manager.log_debug(
                    f"Added extpluginDir to sys.path: {self.extpluginDir}"
                )

            missingDependencies = [
                dep for dep in self.dependencies if not self._isModuleInstalled(dep)
            ]
            if not missingDependencies:
                QMessageBox.information(
                    None,
                    "Installation Successful",
                    "All required modules have been installed successfully. Please restart QGIS to apply changes.",
                )
                return

        except subprocess.CalledProcessError as e:
            log_manager.log_debug(f"Force install failed with CalledProcessError: {e}")
            log_manager.log_error("Dependency installation failed", exc=e)
        except Exception as e:
            log_manager.log_debug(f"Force install failed with unexpected error: {e}")
            log_manager.log_error("Dependency installation failed", exc=e)

        QMessageBox.critical(
            None,
            "Force Installation Failed",
            "Failed to force install the required modules. Please install them manually or consult the error log for details.",
        )


    def _isPipAvailable(self):
        """
        Check whether pip is available in the current Python environment.
        :return: True if pip is importable, False otherwise.
        """
        try:
            import pip

            return True
        except ImportError:
            return False

    def _attemptInstallPip(self):
        """
        Attempt to install pip for the QGIS Python interpreter.
        Handles macOS, Windows, and Linux platforms with appropriate guidance.
        """
        import platform
        import shutil

        log_manager.log_debug("Attempting to install pip for QGIS Python.")

        system = platform.system()

        if system == "Darwin":
            QMessageBox.information(
                None,
                "Manual pip Installation Required (macOS)",
                "Automatic pip installation is not supported on macOS due to QGIS's protected Python environment.\n\n"
                "Please run the following commands in Terminal:\n\n"
                "curl https://bootstrap.pypa.io/get-pip.py -o ~/Downloads/get-pip.py\n"
                f"{self.qgisPython} ~/Downloads/get-pip.py\n\n"
                "Then restart QGIS.",
            )
            return

        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_path = os.path.join(self.scriptDir, "get-pip.py")

        try:
            import urllib.request
            urllib.request.urlretrieve(get_pip_url, get_pip_path)
            log_manager.log_debug(f"Downloaded get-pip.py to {get_pip_path}")
        except Exception as e:
            log_manager.log_debug(f"Failed to download get-pip.py: {e}")
            log_manager.log_error("Dependency installation failed", exc=e)
            QMessageBox.critical(
                None,
                "Download Failed",
                "Could not download get-pip.py. Please check your network connection and try again.",
            )
            return

        cmd = [self.qgisPython, get_pip_path]
        try:
            subprocess.check_call(cmd)
            log_manager.log_debug("pip installed successfully.")
            QMessageBox.information(
                None,
                "pip Installed",
                "pip has been successfully installed in the QGIS Python environment.",
            )
        except subprocess.CalledProcessError as e:
            log_manager.log_debug(f"pip installation failed with CalledProcessError: {e}")
            log_manager.log_error("Dependency installation failed", exc=e)

            if system == "Linux":
                suggestion = (
                    "Automated pip installation failed. On Ubuntu/Debian systems, you can install pip manually using:\n\n"
                    "sudo apt install python3-pip\n\n"
                    f"Then run:\n{self.qgisPython} -m pip install --target path/to/extlibs -r requirements.txt"
                )
            else:
                suggestion = f"Automated pip installation failed. Try running:\n\n{self.qgisPython} {get_pip_path}"

            QMessageBox.critical(
                None,
                "Installation Failed",
                suggestion,
            )
        except Exception as e:
            log_manager.log_debug(f"Unexpected error during pip installation: {e}")
            log_manager.log_error("Dependency installation failed", exc=e)
            QMessageBox.critical(
                None,
                "Installation Failed",
                "An unexpected error occurred while attempting to install pip.",
            )
        finally:
            try:
                if os.path.exists(get_pip_path):
                    os.remove(get_pip_path)
                    log_manager.log_debug(f"Cleaned up get-pip.py from {get_pip_path}")
            except Exception as cleanup_error:
                log_manager.log_debug(f"Failed to remove get-pip.py: {cleanup_error}")
