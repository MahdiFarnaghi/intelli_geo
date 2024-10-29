# Blog Posts

## Workshop at [QGIS User Conference 2024](https://uc2024.qgis.sk/) in Bratislava

In a [workshop](https://talks.osgeo.org/qgis-uc2024/talk/DNHKHQ/) at QGIS User Conference 2024, the **IntelliGeo** plugin was presented to the QGIS user community. We had a full room of interested people actively participating in the workshop. The workshop was started with an introduction to the IntelliGeo plugin and it's relation with AI/LLMs. Then the participants installed IntelliGeo, participated in a hands-on activity where they use the plugin to perform different GIS tasks. Finally, we had a very constructive feedback round where we collected amazing suggestion and collaboration opportunities. 

Bellow is the image of abstract of the workshop and a few selected images. 

    Large Language Models and GIS

    In a project funded by the AiNED program, we are developing a plugin, named IntelliGeo, that integrates general-purpose Large Language Models (LLMs) into QGIS. The idea is to use the modelling power of LLMs to facilitate the generation of Geoprocessing workflows in the Model Designer of QGIS. In this plugin, an LLM plays the role of a modelling assistant that receives the user’s instructions and develops a Geoprocessing workflow based on the provided specification, accounting for the geoprocessing tools in QGIS and the loaded data in the table of contents. The plugin also helps the user to improve the model iteratively through verbal instructions.

    The interactions between users and the LLM through the plugin are recorded. These records will be used afterwards to fine-tune the LLMs and improve their ability to solve GIS problems.

    The first release of the plugin will be available in the coming months. In the workshop, we will introduce the plugin to the QGIS community, receive their requirements and opinions about the future direction of the plugin, and seek collaborators for the project. The program for the workshop will be as follows:
    15:30 – 15:45 | Introduction to the IntelliGeo plugin
    15:45 – 16:00 | Installation of the IntelliGeo plugin
    16:00 – 16:30 | Interactive demonstration
    16:30 – 16:45 | Individual testing
    16:45 – 17:00 | Feedback

    You can download the demo project from the resources.

    IntelliGeo requirements:
    - langchain_cohere >= 0.1.9
    - langchain_openai >= 0.1.6
    - pyperclip >= 1.3.0
    - langchain >= 0.2.2
    - requests >= 2.31.0
    - psutil~=6.0.0


## **IntelliGeo** at ICT Open 2024

IntelliGeo project was presented at NWO ICT.OPEN2024 which was held in Jaarbeurs Utrecht, 10 and April 2024. The title of the presentation by [Mahdi]() and [Gustavo]() was **"Fine-Tuning LLMs for Spatial Analysis and Modeling – An Initial Step"**. 

The abstract of the talk:

    Geospatial Information Science (GIScience) combines Geography, Earth Science, and Computer Science to develop methods for handling geographical data such as satellite/UAV imagery and GPS observations, aiding in complex model building using Geographical Information System (GIS) platforms in sectors like climate change, food security, and health. The intersection of GIScience and recent advances in Large Language Models (LLMs) presents an opportunity to transform spatial analysis and modelling. However, the integration of LLMs into GIScience applications is hindered by the absence of fine-tuning datasets for spatial analysis and modelling tasks, thus a lack of task-specific LLMs in the GIScience domain. In response, we are working on a research project funded by the NWO Ai NED program to integrate general-purpose LLMs into QGIS, a widely used GIS platform. The main idea is to record expert user interactions with an out-of-the-box, general-purpose LLM. Since the LLM is not specialized for GIS tasks, users will need to interact with it iteratively to solve the GIS tasks. We hypothesize that recording such interactions will allow us to build a community-based specialized dataset to fine-tune LLMs for spatial analysis and modelling. This presentation will explain the main objectives of the project, its primary results, and the remaining steps. We will showcase our initial findings about the effective mechanisms to translate users’ analytical descriptions into executable geoprocessing workflows in GIS. Primary results affirm the capacity of the proposed approach to democratize spatial analysis by embedding advanced Artificial Intelligence within GIS platforms.

    Keywords: LLM, GIS, Fine-tuning, Dataset, Spatial

