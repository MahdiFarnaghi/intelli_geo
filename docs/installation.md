
# Installation and API Keys

To be able to use IntelliGeo, you need to first install it in your QGIS software and then obtain an API key to use large language models. Section 1 of this page explains how you can install the library and section 2 walk you through obtaining API keys for large language models from OpenAI, Cohere and Groq and registering them in QGIS.  


## 1. Installation

There are two ways to install the IntelliGeo plugin: via the QGIS plugin hub or by installing it from the source.

### **Install from plugin hub**

![Screenshot from 2024-10-09 12-51-30](https://github.com/user-attachments/assets/2737f989-e808-440d-997e-2d80c601fdf5)

In QGIS, click on `plugins`->`Manage and install Plugins`, In the search bar, type "IntelliGeo", locate the plugin and click on `Install Experimental Plugin`.

### **Install from source**

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

#### Dependency

> [!NOTE]
> In some cases, you may need to install the dependencies manually. We are working on fixing this issue, but some users may still need to take this step.

##### Linux & MacOS

For Linux or macOS, use `pip` to install the Python dependencies listed in the [requirements.txt](https://github.com/MahdiFarnaghi/intelli_geo/blob/main/requirements.txt) file.

Navigate to `IntelliGeo` folder, and run the following command,

```
pip install -r requirements.txt
```

##### Windows

For Windows, ou can use the OSGeo4W shell, which comes with QGIS. First, open the OSGeo4W shell (found in the QGIS installation folder). Then, use the `pip` command to install packages listed in the [requirements.txt](https://github.com/MahdiFarnaghi/intelli_geo/blob/main/requirements.txt) file., just as you would in a regular Python environment, by running `pip install package_name`. This will ensure that the packages are installed in the environment QGIS uses. For a step-by-step guide, you can watch [this video tutorial](https://www.youtube.com/watch?v=9Jdc331qofg) that demonstrates the process in detail.

## 2. Obtaining API Key for IntelliGeo

To use the IntelliGeo plugin, you need access to a large language model (LLM) via an API. Currently, we support both [OpenAI](https://openai.com/) and [Cohere](https://cohere.com/). Based on our experience, OpenAI models perform better but require a paid plan. Cohere, while offering free access to their API, delivers slightly lower performance compared to OpenAI.


### OpenAI Guide

#### Step 1: Sign Up

Register for ChatGPT at [OpenAI Signup](https://platform.openai.com/signup?launch). You can sign up using an email address or an existing Google, Microsoft, or Apple account.

#### Step 2: Open the Dashboard

Once registered, navigate to the OpenAI dashboard at [OpenAI Dashboard](https://platform.openai.com/api-keys) to access your API keys.

#### Step 3: Generate an API Key

To create a new API key, go to the `API Keys` section, click on `+ Create new secret key`, and optionally name it in the pop-up. Once you click 'Create secret key', a unique alphanumeric API key will be generated. Be sure to store this key securely.

![Screenshot from 2024-10-18 16-51-01](https://github.com/user-attachments/assets/eda6d221-3168-4741-b14d-a0f0e6a4a8f3)

This API key works universally for all OpenAI models; you don’t need separate keys for each model.

#### Step 4: Use the API Key in IntelliGeo

Copy your API key and input it when starting a new conversation within IntelliGeo. The key will be saved only in your local database; the IntelliGeo backend does not store or access your API key.

![image](https://github.com/user-attachments/assets/2c5f8f79-f30d-47b3-8cf7-442402bec704)

### Cohere Guide

#### Step 1: Sign Up

Sign up for Cohere at [Cohere Signup](https://dashboard.cohere.com/welcome/register). You can register using your email address or an existing Google or GitHub account.

#### Step 2: Access the Dashboard

Once logged in, go to the API Keys section to manage your API keys.

#### Step 3: Create an API Key

To generate an API key, go to `API Keys`, then click `+ New Trial key`, optionally name it, and click 'Create secret key' to generate your unique API key. Make sure to store the key securely.

![Screenshot from 2024-10-18 17-15-56](https://github.com/user-attachments/assets/90e0970b-9fff-4927-98ca-ff6bfb294ec8)

The Cohere API key works for all models, so you don’t need to create multiple keys.

#### Step 4: Use the API Key in IntelliGeo

Copy your Cohere API key and input it when starting a new conversation in IntelliGeo. As with OpenAI, your key is stored locally and never accessed by IntelliGeo’s backend.

![image](https://github.com/user-attachments/assets/2c5f8f79-f30d-47b3-8cf7-442402bec704)

Once your API key is set up, you can start using the IntelliGeo plugin. Click on the IntelliGeo icon to open the chat interface. From there, you can chat and use the AI-powered geo-workflow features. 

### Groq Guide

#### Step 1: Sign Up

Sign up for Groq at [Groq Signup](https://console.groq.com/login). You can register using your email address or an existing Google or GitHub account.

#### Step 2: Access the Dashboard

Once logged in, go to the API Keys section to manage your API keys.

#### Step 3: Create an API Key

To generate an API key, go to `API Keys`, then click `Create API key`, optionally name it, and click 'Submit' to generate your unique API key. Make sure to store the key securely.

![image](https://github.com/user-attachments/assets/72310dd6-396d-48c7-81c6-6c6188e9bb24)

The Groq API key works for all models, so you don’t need to create multiple keys.

#### Step 4: Use the API Key in IntelliGeo

Copy your Groq API key and input it when starting a new conversation in IntelliGeo. As with OpenAI, your key is stored locally and never accessed by IntelliGeo’s backend.

![image](https://github.com/user-attachments/assets/2c5f8f79-f30d-47b3-8cf7-442402bec704)

Once your API key is set up, you can start using the IntelliGeo plugin. Click on the IntelliGeo icon to open the chat interface. From there, you can chat and use the AI-powered geo-workflow features. 


### DeepSeek Guide

#### Step 1: Sign Up

Sign up for deepseek at [DeepSeek Signup](https://platform.deepseek.com/sign_up). You can register using your email address or an existing Google account.

#### Step 2: Access the Dashboard

Once logged in, go to the API Keys section to manage your API keys.

#### Step 3: Create an API Key

To generate an API key, go to `API Keys`, then click `Create New API key`, optionally name it, and click 'Create API key' to generate your unique API key. Make sure to store the key securely.

![Screenshot from 2025-02-12 11-11-01(1)](https://github.com/user-attachments/assets/f9aacb8a-f6de-4b99-8ed9-69c48583128b)

The Deepseek API key works for all models, so you don't need to create multiple keys.

#### Step 4: Use the API Key in IntelliGeo

Copy your DeepSeek API key and input it when starting a new conversation in IntelliGeo. As with OpenAI, your key is stored locally and never accessed by IntelliGeo's backend.

![image](https://github.com/user-attachments/assets/2c5f8f79-f30d-47b3-8cf7-442402bec704)

Once your API key is set up, you can start using the IntelliGeo plugin. Click on the IntelliGeo icon to open the chat interface. From there, you can chat and use the AI-powered geo-workflow features. 
