# Tutorials

***QGIS User Conference 2025***

---

This tutorial was prepared as part of the workshop "AI-powered model building in QGIS," held at the [QGIS UC25](https://talks.osgeo.org/qgis-uc2025/talk/H3SKPN/).

Requirements for this tutorial:  

- [QGIS >= 3.0.0](https://qgis.org/download/)  
- [IntelliGeo plugin >= 0.1.0](https://plugins.qgis.org/plugins/intelli_geo/)  
- [Sample project]()  

## About the data

The sample project includes data from two data sources: [Movebank](https://www.movebank.org/) and [GADM](https://gadm.org/). The GPS tracking data of European Freetailed bats (Tadarida teniotis) was produced by [O’Mara et al., 2021], and is available under a Creative Commons license on the website [Movebank](https://www.movebank.org/). The data layer with administrative units (level 1) for Portugal and Spain was prepared using data available under a Creative Commons license at [GADM](https://gadm.org/).

## Plugin installation

For detailed installation instructions, please refer to [installation.md](installation.md).

## Creating a new conversation

**Figure 1** illustrates the process to create a new conversation:  

1. Click on the new conversation icon  
2. Provide a name  
3. Provide a description  
4. Select the LLM to use as back-end  
5. Provide a valid API Key for the LLM  

<figure>
    <img src="https://raw.githubusercontent.com/MahdiFarnaghi/intelli_geo/main/docs/img/QGIS_UC_2025/fig_new_conversation.png"
         alt="New conversation" width="600px">
    <figcaption><strong>Figure 1:</strong> Creating a new conversation.</figcaption>
</figure>

## Requesting general information

In this section, you will interact with **IntelliGeo** to request general information about **QGIS**, the plugin, and the data available at your working space. You are encouraged to experiment with the provided prompts.

### **Step:** 1  

**Prompt:** What is QGIS?  

**Expected output:** Description of the QGIS software.  

**Example output:**  
QGIS (Quantum GIS) is a free and open-source Geographic Information System (GIS) that allows you to create, edit, visualize, analyze and publish geospatial information. It supports various formats and functionalities, including vector, raster, and database formats. QGIS is widely used for spatial analysis, data management, and map production. It also supports plugins to enhance its functionality and can be customized using the PyQGIS Python API.  

### **Step:** 2  

**Prompt:** What is a QGIS plugin?  

**Expected output:** Description of a plugin for QGIS.  

**Example output:**  
A QGIS plugin is a piece of software that adds new functionality or extends the capabilities of the QGIS application. Plugins can be developed by anyone using the Python programming language and the QGIS API (Application Programming Interface). They can be used for a variety of tasks, such as automating common tasks, customizing the user interface, performing complex spatial analyses, connecting to external databases, and much more. QGIS has a built-in Plugin Manager that allows users to install, update, and manage plugins directly within the application.

### **Step:** 3  

**Prompt:** Where can I get information about QGIS plugins?  

**Expected output:** Information about QGIS Plugin Repository.  

**Example output:**  
You can find information about QGIS plugins in several places:  

1. **QGIS Plugin Repository**: This is the official repository where all approved QGIS plugins are listed. You can access it directly from your QGIS software by going to Plugins > Manage and Install Plugins. Here, you can search for plugins, read their descriptions, and install them.  
2. **QGIS Documentation**: The official QGIS documentation provides information about core plugins and how to use them. You can access it at <https://docs.qgis.org>.  
3. **Plugin Documentation**: Most plugins come with their own documentation that provides detailed information about their functionality and usage. This documentation is usually accessible from the plugin's page in the QGIS Plugin Repository.  
4. **QGIS Community**: The QGIS community is a great resource for information about plugins. You can ask questions and share experiences on the QGIS mailing list or on GIS Stack Exchange.  
Remember to always check the compatibility of the plugin with your QGIS version.

### **Step:** 4  

**Prompt:** Is IntelliGeo a QGIS plugin?  

**Expected output:** Confirmation that IntelliGeo is a QGIS plugin.  

**Example output:**  
Yes, IntelliGeo is a QGIS plugin designed to assist users with various GIS tasks within the QGIS environment. It provides guidance, troubleshooting advice, and support for creating processing workflows.

### **Step:** 5  

**Prompt:** What can I do with IntelliGeo?  

**Expected output:** A list of tasks that IntelliGeo can support.  

**Example output:**  
With IntelliGeo, you can:  

1. Get step-by-step instructions for various GIS tasks in QGIS.  
2. Receive troubleshooting advice for common issues and errors.  
3. Get support in designing and executing project workflows.  
4. Learn about the latest updates on QGIS features and plugins.  
5. Generate processing workflows for the model designer by creating .model3 files.  
6. Get assistance in using PyQGIS for scripting and automating GIS tasks.  
7. Retrieve detailed information about your current QGIS project environment, including layer details and attributes.  
Remember, IntelliGeo is designed to provide concise, straightforward, and actionable information to help you efficiently use QGIS for your spatial analysis and GIS project needs.

## Processing with a single data layer

In this section, you will generate scripts to process a single data layer.  

### **Step:** 6  

**Prompt:** Create a script to calculate the number of data points for each bat in the layer "bats_data," which is already loaded in the workspace.  

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
        # Get the bat id from the feature's attributes
        bat_id = feature['bat_id']

        # If the bat id is already in the dictionary, increment the count
        if bat_id in bat_counts:
            bat_counts[bat_id] += 1
        # If the bat id is not in the dictionary, add it with a count of 1
        else:
            bat_counts[bat_id] = 1

    # Print the count of data points for each bat
    for bat, count in bat_counts.items():
        print(f"Bat {bat} has {count} data points.")
```  
  
This script first gets the "bats_data" layer from the current QGIS project. It then iterates over each feature (data point) in the layer, getting the bat ID from the feature's attributes. The script keeps a count of the number of data points for each bat in a dictionary. Finally, it prints out the count of data points for each bat.  
  
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

### **Step:** 7  

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

### **Step:** 8  

**Prompt:** Modify the latest produced script to calculate the statistics for each individual bat, using the "bat_id" field.  

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

### **Step:** 9  

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
         alt="Flying trajectories" width="600px">
    <figcaption><strong>Figure 2:</strong> Individual bats trajectories.</figcaption>
</figure>

---

### **Step:** 10

**Prompt:** Create a script that generates a vector layer representing a regular grid of 0.05 degrees × 0.05 degrees cells covering the full extent of the "bats_data" layer, which is already loaded in the workspace. Then, aggregate the data from "bats_data" by counting the number of points that fall within each grid cell.  

**Expected output:** A script that produces a grid and aggregates the records from the "bats_data" layer.

**Example output:**

```python
# Import necessary modules
from qgis.core import QgsVectorLayer, QgsProcessing, QgsProcessingFeatureSourceDefinition
from qgis.analysis import QgsNativeAlgorithms
import processing

# Initialize QGIS's processing framework
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# Get the "bats_data" layer
bats_data_layer = QgsProject.instance().mapLayersByName('bats_data')[0]

# Define the grid size
grid_size = 0.05

# Define the parameters for the "Create grid" algorithm
grid_parameters = {
    'TYPE': 2,  # Rectangle (polygon)
    'EXTENT': bats_data_layer.extent(),  # Use the extent of the "bats_data" layer
    'HSPACING': grid_size,  # Horizontal spacing
    'VSPACING': grid_size,  # Vertical spacing
    'CRS': bats_data_layer.crs(),  # Coordinate reference system
    'OUTPUT': 'memory:'  # Output to memory
}

# Run the "Create grid" algorithm
grid_result = processing.run('native:creategrid', grid_parameters)

# Get the resulting grid layer
grid_layer = grid_result['OUTPUT']

# Define the parameters for the "Count points in polygon" algorithm
count_parameters = {
    'POLYGONS': grid_layer,  # Use the grid layer as the polygon layer
    'POINTS': QgsProcessingFeatureSourceDefinition(bats_data_layer.id()),  # Use the "bats_data" layer as the point layer
    'OUTPUT': 'memory:'  # Output to memory
}

# Run the "Count points in polygon" algorithm
count_result = processing.run('native:countpointsinpolygon', count_parameters)

# Get the resulting layer
result_layer = count_result['OUTPUT']

# Add the resulting layer to the map
QgsProject.instance().addMapLayer(result_layer)
```

**Example execution:**  

<figure>
    <img src="https://raw.githubusercontent.com/MahdiFarnaghi/intelli_geo/main/docs/img/QGIS_UC_2025/fig_grid_aggregation.png"
         alt="Data aggregated over a grid" width="600px">
    <figcaption><strong>Figure 3:</strong> Aggregated data over a grid.</figcaption>
</figure>

## Processing with two data layers

### **Step:** 11

**Prompt:** Create a script to count the number of points from the "bats_data" layer that fall within each polygon of the "Iberian_Peninsula_Level_1" layer. Both layers are already loaded in the workspace. The script must produce a new in-memory vector layer containing the polygons from "Iberian_Peninsula_Level_1", with a field named "COUNT" that indicates the number of points contained within each polygon.

**Expected output:** Script to calculate the number of records within each administrative division (level 1).

**Example output:**  

```python
# Import necessary modules
from qgis.core import *

# Define the names of the input layers
point_layer_name = "bats_data"
polygon_layer_name = "Iberian_Peninsula_Level_1"

# Retrieve the layers from the current project
point_layer = QgsProject.instance().mapLayersByName(point_layer_name)[0]
polygon_layer = QgsProject.instance().mapLayersByName(polygon_layer_name)[0]

# Create a new in-memory vector layer to store the results
result_layer = QgsVectorLayer("Polygon?crs=epsg:4326", "result", "memory")

# Start editing the result layer
result_layer.startEditing()

# Add a new field to the result layer to store the count of points
result_layer.dataProvider().addAttributes([QgsField("COUNT", QVariant.Int)])
result_layer.updateFields()

# Create a spatial index for the point layer to speed up the spatial query
index = QgsSpatialIndex(point_layer.getFeatures())

# Iterate over each feature (i.e., polygon) in the polygon layer
for polygon_feature in polygon_layer.getFeatures():
    # Create a new feature for the result layer
    result_feature = QgsFeature(result_layer.fields())
    # Copy the geometry from the polygon feature
    result_feature.setGeometry(polygon_feature.geometry())
    # Use the spatial index to find points within the polygon
    ids = index.intersects(polygon_feature.geometry().boundingBox())
    # Count the number of points that are actually within the polygon
    count = sum(polygon_feature.geometry().contains(point_layer.getFeature(id).geometry()) for id in ids)
    # Set the count field of the result feature
    result_feature["COUNT"] = count
    # Add the result feature to the result layer
    result_layer.addFeature(result_feature)

# Commit the changes to the result layer
result_layer.commitChanges()

# Add the result layer to the current project
QgsProject.instance().addMapLayer(result_layer)
```

**Example execution:**  

<figure>
    <img src="https://raw.githubusercontent.com/MahdiFarnaghi/intelli_geo/main/docs/img/QGIS_UC_2025/fig_level_1_aggregation.png"
         alt="Records aggregated based on administrative division level 1" width="600px">
    <figcaption><strong>Figure 4:</strong> Aggregated data over Administrative Division Level 1.</figcaption>
</figure>

---  

### **Step:** 12

**Prompt:** Create a script to extract values from the "50N_010W" layer, which is already loaded in the workspace. For each point in the "bats_data" layer (also loaded in the workspace), retrieve the corresponding value from "50N_010W" based on its coordinates and store it in a new field named "landcover".

**Expected output:** A script to extract landcover values for each feature in the "bats_data" layer.

**Example output:**  

```python
# Import necessary modules
from qgis.core import QgsProject, QgsFeatureRequest

# Get the layers
project = QgsProject.instance()
raster_layer = project.mapLayersByName('50N_010W')[0]
vector_layer = project.mapLayersByName('bats_data')[0]

# Check if the 'landcover' field already exists in the vector layer
# If not, create it
if 'landcover' not in [field.name() for field in vector_layer.fields()]:
    vector_layer.dataProvider().addAttributes([QgsField('landcover', QVariant.Double)])
    vector_layer.updateFields()

# Get the index of the 'landcover' field
field_index = vector_layer.fields().indexFromName('landcover')

# Start editing the vector layer
vector_layer.startEditing()

# For each feature (point) in the vector layer
for feature in vector_layer.getFeatures():
    # Get the point's coordinates
    point = feature.geometry().asPoint()

    # Get the corresponding value from the raster layer
    value = raster_layer.dataProvider().sample(point, 1)[0]

    # Update the 'landcover' field with the value
    feature.setAttribute(field_index, value)
    vector_layer.updateFeature(feature)

# Commit the changes
vector_layer.commitChanges()
```

**Example execution:**  

<figure>
    <img src="https://raw.githubusercontent.com/MahdiFarnaghi/intelli_geo/main/docs/img/QGIS_UC_2025/fig_landcover.png"
         alt="Landcover values" width="600px">
    <figcaption><strong>Figure 5:</strong> Land cover values for records in the "bats_data" layer.</figcaption>
</figure>

---  

## References

**[O’Mara et al., 2021]** O'Mara MT, Amorim F, Scacco M, McCracken GF, Safi K, Mata V, Tomé R, Swartz S, Wikelski M, Beja P, Rebelo H, Dechmann DKN. 2021. Bats use topography and nocturnal updrafts to fly high and fast. Curr Biol. https://doi.org/10.1016/j.cub.2020.12.042
