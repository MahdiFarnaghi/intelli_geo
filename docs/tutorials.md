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
1. Click in the new conversation icon  
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

In this section, you will generate scripts to process a single data layer.  

**No.:** 6  

**Prompt:** Create a script to calculate the number of data points for each bat in the layer in the workspace "bats_data."  

**Expected output:** Script to calculate the number of points for each bat.  

**Example output:**

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
  
**Example execution:**
```python
Bat Bat4_3D6001852B980 has 1466 data points.
Bat Bat5_3D6001852B98C has 1397 data points.
Bat Bat1_3D6001852B958 has 1265 data points.
Bat Bat6_3D6001852B98E has 1435 data points.
Bat Bat3_3D6001852B978 has 1568 data points.
Bat Bat2_3D6001852B95D has 219 data points.
Bat Bat8_3D6001852B9A7 has 900 data points.
Bat Bat7_3D6001852B9A3 has 1623 data points.
```

---  

**No.:** 7  

**Prompt:** Create a script that calculates basic statistics for the "height" attribute in the "bats_data" layer, which is already loaded in the workspace. The script should compute the following statistics: total number of points, minimum height, maximum height, average (mean) height, standard deviation of height.  

**Expected output:** Script to calculate basic statistics for the field "height."  

**Example output:**

```python
# Import the required module
from qgis.core import QgsVectorLayer, QgsFeatureRequest

# Get the layer
layer = QgsProject.instance().mapLayersByName('bats_data')[0]

# Check if the layer is valid
if not layer.isValid():
    print("Layer failed to load!")
else:
    # Get the index of the 'height' field
    field_index = layer.fields().indexFromName('height')

    # Initialize variables to store statistics
    total_points = 0
    min_height = float('inf')
    max_height = float('-inf')
    sum_height = 0
    sum_squared_height = 0

    # Iterate over each feature in the layer
    for feature in layer.getFeatures():
        # Get the height value
        height = feature.attributes()[field_index]

        # Update statistics
        total_points += 1
        min_height = min(min_height, height)
        max_height = max(max_height, height)
        sum_height += height
        sum_squared_height += height**2

    # Calculate mean and standard deviation
    mean_height = sum_height / total_points
    std_dev_height = (sum_squared_height / total_points - mean_height**2)**0.5

    # Print the statistics
    print(f"Total number of points: {total_points}")
    print(f"Minimum height: {min_height}")
    print(f"Maximum height: {max_height}")
    print(f"Average (mean) height: {mean_height}")
    print(f"Standard deviation of height: {std_dev_height}")
```

**Example execution:**  

```python
Total number of points: 9873
Minimum height: 4.0
Maximum height: 3150.0
Average (mean) height: 650.0176238225463
Standard deviation of height: 252.26758042089847
```

---  

**No.:** 8  

**Prompt:** Modify the lastest produced script to calculate the statistics for each individual bat, for this purpose use the field "bat_id."  

**Expected output:** Script to calculate basic statistics per individual for the field "height."    

**Example output:**

```python
# Import the required module
from qgis.core import QgsVectorLayer, QgsFeatureRequest
from collections import defaultdict

# Get the layer
layer = QgsProject.instance().mapLayersByName('bats_data')[0]

# Check if the layer is valid
if not layer.isValid():
    print("Layer failed to load!")
else:
    # Get the index of the 'height' and 'bat_id' fields
    height_index = layer.fields().indexFromName('height')
    bat_id_index = layer.fields().indexFromName('bat_id')

    # Initialize a dictionary to store statistics for each bat
    bat_stats = defaultdict(lambda: {'total_points': 0, 'min_height': float('inf'), 'max_height': float('-inf'), 'sum_height': 0, 'sum_squared_height': 0})

    # Iterate over each feature in the layer
    for feature in layer.getFeatures():
        # Get the height and bat_id values
        height = feature.attributes()[height_index]
        bat_id = feature.attributes()[bat_id_index]

        # Update statistics for the current bat
        bat_stats[bat_id]['total_points'] += 1
        bat_stats[bat_id]['min_height'] = min(bat_stats[bat_id]['min_height'], height)
        bat_stats[bat_id]['max_height'] = max(bat_stats[bat_id]['max_height'], height)
        bat_stats[bat_id]['sum_height'] += height
        bat_stats[bat_id]['sum_squared_height'] += height**2

    # Calculate mean and standard deviation for each bat and print the statistics
    for bat_id, stats in bat_stats.items():
        mean_height = stats['sum_height'] / stats['total_points']
        std_dev_height = (stats['sum_squared_height'] / stats['total_points'] - mean_height**2)**0.5

        print(f"Bat ID: {bat_id}")
        print(f"Total number of points: {stats['total_points']}")
        print(f"Minimum height: {stats['min_height']}")
        print(f"Maximum height: {stats['max_height']}")
        print(f"Average (mean) height: {mean_height}")
        print(f"Standard deviation of height: {std_dev_height}")
        print()
```

**Example execution:**  

```python
Bat ID: Bat4_3D6001852B980
Total number of points: 1466
Minimum height: 6.0
Maximum height: 1658.0
Average (mean) height: 721.6589358799454
Standard deviation of height: 275.40828363177724

Bat ID: Bat5_3D6001852B98C
Total number of points: 1397
Minimum height: 166.0
Maximum height: 2704.0
Average (mean) height: 755.6406585540444
Standard deviation of height: 246.34593936186914

Bat ID: Bat1_3D6001852B958
Total number of points: 1265
Minimum height: 26.0
Maximum height: 3150.0
Average (mean) height: 668.7446640316206
Standard deviation of height: 279.81218789617225

Bat ID: Bat6_3D6001852B98E
Total number of points: 1435
Minimum height: 4.0
Maximum height: 1228.0
Average (mean) height: 543.7602787456447
Standard deviation of height: 248.23846792712698

Bat ID: Bat3_3D6001852B978
Total number of points: 1568
Minimum height: 22.0
Maximum height: 2266.0
Average (mean) height: 673.4489795918367
Standard deviation of height: 270.03197552342056

Bat ID: Bat2_3D6001852B95D
Total number of points: 219
Minimum height: 22.0
Maximum height: 1550.0
Average (mean) height: 616.3013698630137
Standard deviation of height: 198.86940839731218

Bat ID: Bat8_3D6001852B9A7
Total number of points: 900
Minimum height: 256.0
Maximum height: 1146.0
Average (mean) height: 604.9911111111111
Standard deviation of height: 106.70613815984397

Bat ID: Bat7_3D6001852B9A3
Total number of points: 1623
Minimum height: 70.0
Maximum height: 968.0
Average (mean) height: 580.6247689463955
Standard deviation of height: 194.04819050116532
```

--- 

**No.:** 9  

**Prompt:** Create a script to generate a line vector layer from the existing "bats_data" layer, which is already loaded in the workspace. The script should create one line per bat, using the "bat_id" field to group individual bats. Ensure that the points for each bat are ordered chronologically based on the "timestamp" field before constructing the lines.  

**Expected output:** A script that groups the records per bat and creates line features from these groups.  

**Example output:**

```python
# Import necessary modules
from qgis.PyQt.QtCore import QVariant
from qgis.core import (QgsFeature, QgsField, QgsGeometry, QgsPoint, 
                       QgsVectorLayer, QgsProject)

# Get the bats_data layer
layer = QgsProject.instance().mapLayersByName('bats_data')[0]

# Create a new memory layer for the lines
line_layer = QgsVectorLayer('LineString', 'bat_paths', 'memory')

# Add the necessary fields to the new layer
pr = line_layer.dataProvider()
pr.addAttributes([QgsField('bat_id', QVariant.String)])
line_layer.updateFields()

# Create a dictionary to store the points for each bat
bat_points = {}

# Iterate over the features in the bats_data layer
for feature in layer.getFeatures():
    # Get the bat_id and timestamp for the current feature
    bat_id = feature['bat_id']
    timestamp = feature['timestamp']
    
    # Get the geometry of the current feature and convert it to a point
    geom = feature.geometry()
    point = QgsPoint(geom.asPoint())
    
    # If the bat_id is not already in the dictionary, add it with the point and timestamp
    if bat_id not in bat_points:
        bat_points[bat_id] = [(timestamp, point)]
    # If the bat_id is already in the dictionary, append the point and timestamp to the list
    else:
        bat_points[bat_id].append((timestamp, point))

# Iterate over the bats in the dictionary
for bat_id, points in bat_points.items():
    # Sort the points by timestamp
    points.sort()
    
    # Create a new feature for the line layer
    feat = QgsFeature()
    
    # Set the bat_id field to the current bat_id
    feat.setAttributes([bat_id])
    
    # Create a line geometry from the sorted points and set it for the feature
    line = QgsGeometry.fromPolyline([point for timestamp, point in points])
    feat.setGeometry(line)
    
    # Add the feature to the line layer
    pr.addFeature(feat)

# Update the extents of the line layer
line_layer.updateExtents()

# Add the line layer to the map
QgsProject.instance().addMapLayer(line_layer)
```

**Example execution:**  

<figure>
    <img src="https://raw.githubusercontent.com/MahdiFarnaghi/intelli_geo/main/docs/img/QGIS_UC_2025/fig_bats_lines.png"
         alt="New conversation" width="600px">
    <figcaption><strong>Figure 2:</strong> Individual bats trajectories.</figcaption>
</figure>

--- 

**No.:** 10   

**Prompt:**   

**Expected output:**   

**Example output:**

**Example execution:**  

--- 

### Processing with two data layers

### References 

**[O’Mara et al., 2021]** O'Mara MT, Amorim F, Scacco M, McCracken GF, Safi K, Mata V, Tomé R, Swartz S, Wikelski M, Beja P, Rebelo H, Dechmann DKN. 2021. Bats use topography and nocturnal updrafts to fly high and fast. Curr Biol. doi:10.1016/j.cub.2020.12.042 