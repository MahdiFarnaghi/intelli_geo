import os
import sys
import subprocess
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsApplication


class PackageManager:
    def __init__(self, dependencies):
        """
        Initialize with a list of required dependencies.
        :param dependencies: List of module names as strings.
        """
        self.dependencies = dependencies
        self.missingDependencies = []

    def checkDependencies(self):
        """
        Check for missing dependencies and prompt the user to install them.
        """
        self.missingDependencies = [dep for dep in self.dependencies if not self._isModuleInstalled(dep)]
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
            'Missing Dependencies',
            f'The following modules are required but not installed:\n\n'
            f'{", ".join(self.missingDependencies)}\n\n'
            'Do you want to install them now?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            self._installDependencies()
        else:
            QMessageBox.warning(
                None,
                'Dependencies Not Installed',
                'The plugin may not function correctly without the required dependencies. '
                'Please install them manually.'
            )

    def _installDependencies(self):
        """
        Attempt to install missing dependencies using pip.
        """
        try:
            # Determine the path to the QGIS Python interpreter
            qgisPython = sys.executable

            # Install each missing dependency
            scriptDir = os.path.dirname(os.path.abspath(__file__))
            requirementsPath = os.path.join(scriptDir, 'requirements.txt')
            output = subprocess.check_output(
                [qgisPython, "-m", "pip", "install", "-r", requirementsPath],
                stderr=subprocess.STDOUT
            )

            QMessageBox.information(
                None,
                'Installation Successful',
                'All required modules have been installed successfully. Please restart QGIS to apply changes.'
            )
        except subprocess.CalledProcessError as e:
            self._logError(e)
            reply = QMessageBox.question(
                None,
                'Installation Failed',
                'Failed to install the required modules. Would you like to attempt a forced installation? '
                'If you choose "No," you can manually install the dependencies by running `pip install -r'
                'requirements.txt` in the console located in the plugin folder. To locate the plugin folder, navigate'
                'within QGIS to "Settings" > "User Profile" > "Open Active Profile Folder," then open the "IntelliGeo"'
                'folder.'
                ,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self._forceInstallDependencies()
            else:
                # No action needed if the user selects No
                pass

    def _forceInstallDependencies(self):
        """
        Attempt to force install missing dependencies using pip.
        """
        try:
            # Determine the path to the QGIS Python interpreter
            qgisPython = sys.executable

            # Install each missing dependency
            scriptDir = os.path.dirname(os.path.abspath(__file__))
            requirementsPath = os.path.join(scriptDir, 'requirements.txt')
            output = subprocess.check_output(
                [qgisPython, "-m", "pip", "install", "--no-deps", "--force-reinstall",
                 "--use-deprecated=legacy-resolver", "-r", requirementsPath],
                stderr=subprocess.STDOUT
            )

            QMessageBox.information(
                None,
                'Installation Successful',
                'All required modules have been installed successfully. Please restart QGIS to apply changes.'
            )
        except subprocess.CalledProcessError as e:
            self._logError(e)
            QMessageBox.critical(
                None,
                'Installation Failed',
                'Failed to install the required modules. Please install them manually or consult the error log'
                'for details.'
            )

    def _logError(self, error):
        """
        Log installation errors to a file.
        :param error: The exception object containing error details.
        """
        errorLogDir = os.path.expanduser("~/Documents/QGIS_IntelliGeo")
        os.makedirs(errorLogDir, exist_ok=True)
        errorLogPath = os.path.join(errorLogDir, "error_log.txt")
        with open(errorLogPath, "w", encoding="utf-8") as f:
            f.write(f"Command failed with exit code: {error.returncode}\n")
            f.write("=== Output and Error ===\n")
            f.write(error.output.decode("utf-8", errors="replace"))
