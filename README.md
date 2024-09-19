# IntelliGeo

![Static Badge](https://img.shields.io/badge/QGIS->=3.34-86f060)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/MahdiFarnaghi/intelli_geo)
![Github Created At](https://img.shields.io/github/created-at/MahdiFarnaghi/intelli_geo)
![GitHub License](https://img.shields.io/github/license/MahdiFarnaghi/intelli_geo)
![GitHub last commit](https://img.shields.io/github/last-commit/MahdiFarnaghi/intelli_geo)
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/MahdiFarnaghi/intelli_geo)





IntelliGeo is a [QGIS](https://www.qgis.org/) plugin that facilitates interaction with Large Language Models in QGIS environment.

The plugin is in development phase. Soon, we will release version `0.0.1`. 

## The Repository

Welcome to the IntelliGeo repository. 

This is the central hub where our team ([Mahdi Farnaghi](https://github.com/MahdiFarnaghi), [Gustavo García](https://github.com/chape1331), [Zehao Lu](https://github.com/com3dian)）, in collaboration with the community, develops the IntelliGeo software. Here you'll find the source code and issue tracker for the project. 

The code is released under the [Apache 2.0 license](https://github.com/MahdiFarnaghi/intelli_geo/tree/main?tab=Apache-2.0-1-ov-file).

## IntelliGeo

![Plugin Show](https://github.com/MahdiFarnaghi/intelli_geo/blob/main/.github/IMAGES/Screenshot%20from%202024-09-19%2014-29-26.png)

IntelliGeo is a QGIS plugin that leverages **Large Language Models** (LLMs) to automate geospatial workflows. 

Designed for GIS professionals, it assists users by automatically operating QGIS software through two primary methods: generating **PyQGIS scripts** or creating **graphical models**. This AI-powered tool streamlines complex GIS tasks, enabling users to efficiently design and execute geoprocessing workflows without extensive manual coding or model building. By integrating seamlessly with QGIS, IntelliGeo enhances productivity and simplifies the execution of sophisticated geospatial analyses.

### Key Features

- Seamless integration with QGIS
- LLM-powered geoprocessing workflows
- Collaborative modeling between AI and human experts

### Installation

Download the Plugin:

- Visit the [IntelliGeo GitHub repository](https://github.com/MahdiFarnaghi/intelli_geo) and download the latest [release](https://github.com/MahdiFarnaghi/intelli_geo/releases) of the plugin as a ZIP file.

Install via QGIS Plugin Manager:

- Open QGIS.
- Go to `Plugins` > `Manage and Install Plugins`.
- Click the `Install from ZIP` button.
- Browse to the location where you downloaded the IntelliGeo ZIP file and select it.
- Click `Install Plugin`.
    
Activate the Plugin:

- Go to `Plugins` > `Manage and Install Plugins`.
- Find IntelliGeo in the list and check the box next to it to activate the plugin.

### Dependency

> [!NOTE]
> In some cases, you may need to install the dependencies manually. We are working on fixing this issue, but some users may still need to take this step.

For Linux or macOS, use `pip` to install the Python dependencies listed in the [requirements.txt](https://github.com/MahdiFarnaghi/intelli_geo/blob/main/requirements.txt) file.

For Windows, ...

### How to Use

![user interface](https://github.com/MahdiFarnaghi/intelli_geo/blob/main/.github/IMAGES/Screenshot%20from%202024-09-19%2015-27-26.png)

IntelliGeo offers a chat interface that allows users to input requests and receive either PyQGIS code or a graphical model. This output can be used to execute QGIS operations directly.

### Bug Reports & Feature Requests

If you encounter any issues while using IntelliGeo, please report them on our [GitHub repository](https://github.com/MahdiFarnaghi/intelli_geo). Your feedback helps us enhance the plugin and provide a better experience for all users. To submit a bug report or feature request, visit our [GitHub Issues page](https://github.com/MahdiFarnaghi/intelli_geo/issues).


## Contributing
