# IntelliGeo Quick Start

Welcome to the **IntelliGeo Quick Start** documentation! This guide showcases various examples and common use cases to help you understand how to use the plugin effectively for your geospatial tasks in QGIS. Whether you're a beginner or an advanced user, this document aims to provide clear and concise examples to get you started and expand your knowledge.

## Table of Contents

1. Introduction
2. Getting Started
3. Example Use Cases
   - Use Case 1: Automating Layer Styling
   - Use Case 2: Batch Processing
   - Use Case 3: Spatial Analysis
4. Advanced Examples
5. Troubleshooting and Tips



## Getting Started

Before diving into the examples, ensure you have the following prerequisites:
- QGIS Installed: *Download and install the latest version of QGIS from QGIS.org.*
- Plugin Installation: *Install intelliGeo from the QGIS Plugin Repository or your custom source.*
- API Key Ready: Make sure you have activated OpenAI's or Cohere's API key.
- Sample Data:* Some examples use sample datasets.

*Once installed IntelliGeo, you should see the plugin's toolbar or menu added to your QGIS interface. You’re now ready to follow along with the examples!*



## Examples Use Cases

### Use Case 1: Generating Attribute Lists from a Vector Layer

This example demonstrates how to generate a model that lists the attributes from a vector layer in the workspace by selecting the layer by name.

**Prompt**: Generate a model to list the attributes from a vector layer in the workspace. Select the layer by name.

**Note**: Replace the layer's name.

### Use Case 2: Producing Attribute Descriptions for a Vector Layer

**Prompt**: Generate a model to produce a description for the attributes in a vector layer. The summary should include the attributes name, data type, number of NULL values, number of unique values. Select the layer by name.

**Note**: Replace the layer's name.

### Use Case 3: Producing Statistics for Polygon Areas

**Prompt**: I need to produce statistics for the area of the polygons in a layer loaded in the workspace. The statistics should include minimum, maximum, average, standard deviation, and number of features. Generate a model for this purpose. Select the layer by name.

**Note**: Replace the layer's name.



## Advanced Examples

### Use Case 1: Calculating Buffers Around Features

**Prompt**: Create a buffer area of 5000 meters and 40 segments around the features of a vector layer from the workspace. The layer should be selected by name.

**Note**: Replace the layer's name

### Use Case 2: Random selection and buffer

**Prompt**: Create a workflow that:

1. Selects 10 percent of the features in a vector layer loaded in the workspace. Select the layer by name. Load the result as a temporal in-memory layer.
2. Calculate buffers of 5000 meters and 50 segments around the temporal layer.

### Use Case 3: Random Points

**Prompt**: Create a model that generates 1000 random points over the current map extent. The coordinate system is EPSG:28992.



## Troubleshooting and Tips

One of the most frequent issues users encounter when working with the plugin is the problem of "hallucinated imports." This occurs when the script or model references imports or modules that do not exist in your QGIS environment or Python installation. To avoid this issue:



