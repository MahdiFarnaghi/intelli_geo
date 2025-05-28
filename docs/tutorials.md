# Tutorials

## QGIS User Conference 2025

This tutorial was prepared as part of the workshop "AI-powered model building in QGIS," held at the [QGIS UC25](https://talks.osgeo.org/qgis-uc2025/talk/H3SKPN/).

Requirements for this tutorial:  
- QGIS >= 3.0.0  
- IntelliGeo plugin >= 0.1.0  
- [Sample project]()  

### About the data

The sample project includes data from two data sources: [Movebank](https://www.movebank.org/) and [GADM](https://gadm.org/). The GPS tracking data of European Freetailed bats (Tadarida teniotis) was produced by [O’Mara et al., 2021], and is available under a Creative Commons license in the website [Movebank](https://www.movebank.org/). The data layer with administrative units (level 1) for Portugal and Spain were prepared using data available under a Creative Commons license at [GADM](https://gadm.org/). 

### Plugin installation

### Creating a new conversation

**Figure 1** illustrates the process to create a new conversation:  
1. click in the new conversation icon  
2. Provide a name  
3. Provide a description  
4. Select the LLM to use as back-end  
5. Provide a valid API Key for the LLM  

<figure>
    <img src="https://raw.githubusercontent.com/MahdiFarnaghi/intelli_geo/main/docs/img/QGIS_UC_2025/fig_new_conversation.png"
         alt="New conversation" width="600px">
    <figcaption><strong>Figure 1:</strong> Creating a new conversation.</figcaption>
</figure>



### Requesting general information

In this section, you will interact with **IntelliGeo** to request general information about **QGIS**, the plugin, and the data available at your working space. You are encourage to experiment with the provided prompts:

| No.   | Prompt   | Expected output   | Example output |
| ----- | -------- | ----------------- | -------------- |
| 1     | What is QGIS? | Description of the QGIS software. | QGIS (Quantum GIS) is a free and open-source Geographic Information System (GIS) that allows you to create, edit, visualize, analyze and publish geospatial information. It supports various formats and functionalities, including vector, raster, and database formats. QGIS is widely used for spatial analysis, data management, and map production. It also supports plugins to enhance its functionality and can be customized using the PyQGIS Python API. |  
| 2     | What is a QGIS plugin? | Description of a plugin for QGIS. | A QGIS plugin is a piece of software that adds new functionality or extends the capabilities of the QGIS application. Plugins can be developed by anyone using the Python programming language and the QGIS API (Application Programming Interface). They can be used for a variety of tasks, such as automating common tasks, customizing the user interface, performing complex spatial analyses, connecting to external databases, and much more. QGIS has a built-in Plugin Manager that allows users to install, update, and manage plugins directly within the application. |
| 3     | Where can I get information about QGIS plugins? | Information about QGIS Plugin Repository. | You can find information about QGIS plugins in several places: 1. **QGIS Plugin Repository**: This is the official repository where all approved QGIS plugins are listed. You can access it directly from your QGIS software by going to Plugins > Manage and Install Plugins. Here, you can search for plugins, read their descriptions, and install them. 2. **QGIS Documentation**: The official QGIS documentation provides information about core plugins and how to use them. You can access it at https://docs.qgis.org. 3. **Plugin Documentation**: Most plugins come with their own documentation that provides detailed information about their functionality and usage. This documentation is usually accessible from the plugin's page in the QGIS Plugin Repository. 4. **QGIS Community**: The QGIS community is a great resource for information about plugins. You can ask questions and share experiences on the QGIS mailing list or on GIS Stack Exchange. Remember to always check the compatibility of the plugin with your QGIS version. |
| 4     | Is IntelliGeo a QGIS plugin? | Confirmation that IntelliGeo is a QGIS plugin. | Yes, IntelliGeo is a QGIS plugin designed to assist users with various GIS tasks within the QGIS environment. It provides guidance, troubleshooting advice, and support for creating processing workflows. |
| 5     | What can I do with IntelliGeo? | A list of tasks that IntelliGeo can support. | With IntelliGeo, you can: 1. Get step-by-step instructions for various GIS tasks in QGIS. 2. Receive troubleshooting advice for common issues and errors. 3. Get support in designing and executing project workflows. 4. Learn about the latest updates on QGIS features and plugins. 5. Generate processing workflows for the model designer by creating .model3 files. 6. Get assistance in using PyQGIS for scripting and automating GIS tasks. 7. Retrieve detailed information about your current QGIS project environment, including layer details and attributes. Remember, IntelliGeo is designed to provide concise, straightforward, and actionable information to help you efficiently use QGIS for your spatial analysis and GIS project needs. |


### Processing with a single data layer

No.: 6  

Prompt: Create a script to calculate the number of data points for each bat in the layer in the workspace "bats_data."  

Expected output: Script to calculate the number of points for each bat.  

Example output:

Sure, here is a PyQGIS script that calculates the number of data points for each bat in the "bats_data" layer.  
  
```python
# Import necessary modules
from qgis.core import QgsProject

# Get the project instance
project = QgsProject.instance()

# Get the "bats_data" layer
layer = project.mapLayersByName('bats_data')[0]

# Check if the layer is valid
if not layer.isValid():
    print("Layer failed to load!")
else:
    # Create a dictionary to store the count of data points for each bat
    bat_counts = {}

    # Iterate over each feature (data point) in the layer
    for feature in layer.getFeatures():
        # Get the bat name from the feature's attributes
        bat_name = feature['bat_name']

        # If the bat name is already in the dictionary, increment the count
        if bat_name in bat_counts:
            bat_counts[bat_name] += 1
        # If the bat name is not in the dictionary, add it with a count of 1
        else:
            bat_counts[bat_name] = 1

    # Print the count of data points for each bat
    for bat, count in bat_counts.items():
        print(f"Bat {bat} has {count} data points.")
```  
  
This script first gets the "bats_data" layer from the current QGIS project. It then iterates over each feature (data point) in the layer, getting the bat name from the feature's attributes. The script keeps a count of the number of data points for each bat in a dictionary. Finally, it prints out the count of data points for each bat.  
  
---  


### Processing with two data layers

### References 

**[O’Mara et al., 2021]** O'Mara MT, Amorim F, Scacco M, McCracken GF, Safi K, Mata V, Tomé R, Swartz S, Wikelski M, Beja P, Rebelo H, Dechmann DKN. 2021. Bats use topography and nocturnal updrafts to fly high and fast. Curr Biol. doi:10.1016/j.cub.2020.12.042 