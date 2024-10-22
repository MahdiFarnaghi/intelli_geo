# IntelliGeo

![Static Badge](https://img.shields.io/badge/QGIS->=3.34-86f060)
![Static Badge](https://img.shields.io/badge/plugin-IntelliGeo-2D9596)
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

There are two ways to install the IntelliGeo plugin: via the QGIS plugin hub or by installing it from the source.

**Install from plugin hub**:

![Screenshot from 2024-10-09 12-51-30](https://github.com/user-attachments/assets/2737f989-e808-440d-997e-2d80c601fdf5)

In QGIS, click on `plugins`->`Manage and install Plugins`, In the search bar, type "IntelliGeo", locate the plugin and click on `Install Experimental Plugin`.

**Install from source**:

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

For Windows, ou can use the OSGeo4W shell, which comes with QGIS. First, open the OSGeo4W shell (found in the QGIS installation folder). Then, use the `pip` command to install packages listed in the [requirements.txt](https://github.com/MahdiFarnaghi/intelli_geo/blob/main/requirements.txt) file., just as you would in a regular Python environment, by running `pip install package_name`. This will ensure that the packages are installed in the environment QGIS uses. For a step-by-step guide, you can watch [this video tutorial](https://www.youtube.com/watch?v=9Jdc331qofg) that demonstrates the process in detail.

### How to Use

To use the IntelliGeo plugin, you need access to a large language model (LLM) via an API call. Currently, we support [OpenAI](https://openai.com/) and [Cohere](https://cohere.com/). Based on our experience, OpenAI’s models perform better, but they are not free. Cohere offers free access to their API calls, although their performance is not as high as that of OpenAI’s models.

#### OpenAI Manual

##### Step 1: Signing up

Sign up for Chat GPT at https://platform.openai.com/signup?launch
You can register using your email address or an existing Google, Microsoft, or Apple account.

##### Step 2: Open dashborad
After registration, you will go to to OpenAI dashboard https://platform.openai.com/api-keys to get your API key.

##### Step 3: Create API key
Create a new ChatGPT API key by clicking on `API Keys` to access the API Keys page. Then, click `+ Create new secret key` and enter an optional name in the popup. Click 'Create secret key' to generate your unique alphanumeric API key. Be sure to save it somewhere safe.

![Screenshot from 2024-10-18 16-51-01](https://github.com/user-attachments/assets/eda6d221-3168-4741-b14d-a0f0e6a4a8f3)


The ChatGPT API key is universal for all models; you do not need to create separate keys for each one.

##### Step 4: Use the API key in IntelliGeo

Copy the API key and enter it when creating new conversations. The key will be stored only in your local database; IntelliGeo backend does not store or access your key.

![image](https://github.com/user-attachments/assets/2c5f8f79-f30d-47b3-8cf7-442402bec704)

#### Cohere manual

##### Step 1: Signning up
Sign up for Cohere at https://dashboard.cohere.com/welcome/register
You can register using your email address or an existing Google, or github account.

##### Step 2: Open dashborad
After registration, Once logged in, navigate to the API Keys section.

##### Step 3: Create API key
Create a new ChatGPT API key by clicking on `API Keys` to access the API Keys page. Then, click `+ New Trial key` and enter an optional name in the popup. Click 'Create secret key' to generate your unique alphanumeric API key. Be sure to save it somewhere safe.

![image](https://github.com/user-attachments/assets/ecc2ba35-6480-46cd-bf93-57834127302f)


The Cohere API key is universal for all models; you do not need to create separate keys for each one.

##### Step 4: Use the API key in IntelliGeo

Copy the API key and enter it when creating new conversations. The key will be stored only in your local database; IntelliGeo backend does not store or access your key.

![image](https://github.com/user-attachments/assets/2c5f8f79-f30d-47b3-8cf7-442402bec704)

After setting up your API key, you can now use the IntelliGeo plugin. Clicking on the IntelliGeo icon will open the chat interface. To start chatting and experience the powerful AI-driven geo-workflow, you can follow the video tutorial.

https://github.com/user-attachments/assets/0c85f177-c175-41a1-a96c-fff775ccdf1e

IntelliGeo offers a chat interface that allows users to input requests and receive either PyQGIS code or a graphical model. This output can be used to execute QGIS operations directly.


> [!IMPORTANT]
> To use the IntelliGeo plugin, you need to select a desired LLM provider and provide an API key (we won’t take your key!). For OpenAI, log into your account and visit the [provide link](https://platform.openai.com/api-keys). For Cohere, visit the [this link](https://dashboard.cohere.com/api-keys).


### Bug Reports & Feature Requests

If you encounter any issues while using IntelliGeo, please report them on our [GitHub repository](https://github.com/MahdiFarnaghi/intelli_geo). Your feedback helps us enhance the plugin and provide a better experience for all users. To submit a bug report or feature request, visit our [GitHub Issues page](https://github.com/MahdiFarnaghi/intelli_geo/issues).


## Contributing
