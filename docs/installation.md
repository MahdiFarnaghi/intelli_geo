
# Installation

There are two ways to install the IntelliGeo plugin: via the QGIS plugin hub or by installing it from the source.

## **Install from plugin hub**

![Screenshot from 2024-10-09 12-51-30](https://github.com/user-attachments/assets/2737f989-e808-440d-997e-2d80c601fdf5)

In QGIS, click on `plugins`->`Manage and install Plugins`, In the search bar, type "IntelliGeo", locate the plugin and click on `Install Experimental Plugin`.

## **Install from source**

Visit the [IntelliGeo GitHub repository](https://github.com/MahdiFarnaghi/intelli_geo) and download the latest [release](https://github.com/MahdiFarnaghi/intelli_geo/releases) of the plugin as a ZIP file.

Install via QGIS Plugin Manager:

- Open QGIS.
- Go to `Plugins` > `Manage and Install Plugins`.
- Click the `Install from ZIP` button.
- Browse to the location where you downloaded the IntelliGeo ZIP file and select it.
- Click `Install Plugin`.
    
Activate the Plugin:

- Go to `Plugins` > `Manage and Install Plugins`.
- Find IntelliGeo in the list and check the box next to it to activate the plugin.

**Dependency**

> [!NOTE]
> In some cases, you may need to install the dependencies manually. We are working on fixing this issue, but some users may still need to take this step.

For Linux or macOS, use `pip` to install the Python dependencies listed in the [requirements.txt](https://github.com/MahdiFarnaghi/intelli_geo/blob/main/requirements.txt) file.

For Windows, ou can use the OSGeo4W shell, which comes with QGIS. First, open the OSGeo4W shell (found in the QGIS installation folder). Then, use the `pip` command to install packages listed in the [requirements.txt](https://github.com/MahdiFarnaghi/intelli_geo/blob/main/requirements.txt) file., just as you would in a regular Python environment, by running `pip install package_name`. This will ensure that the packages are installed in the environment QGIS uses. For a step-by-step guide, you can watch [this video tutorial](https://www.youtube.com/watch?v=9Jdc331qofg) that demonstrates the process in detail.
