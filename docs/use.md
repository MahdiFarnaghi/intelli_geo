
# IntelliGeo Quick Start

Welcome to the **IntelliGeo Quick Start Guide**!

This guide provides a range of examples and common use cases to help you effectively utilize the IntelliGeo plugin for geospatial tasks in QGIS. Whether you're a beginner or an advanced user, this document offers clear and concise examples to get you started and deepen your knowledge.

---

## Getting Started

Before exploring the examples, ensure the following prerequisites are met:

- **QGIS Installed**: *Download and install the latest version of QGIS from [QGIS.org](https://www.qgis.org).*  
- **Plugin Installation**: *Install IntelliGeo from the QGIS Plugin Repository or a custom source.*  
- **API Key Ready**: Ensure you have an active API key for OpenAI or Cohere.  
- **Sample Data**: Some examples use preloaded sample datasets.

For a detailed guide on installation and obtaining API keys, visit the [Installation and API Keys page](https://www.intelligeo.org/installation/).

Once IntelliGeo is installed, the plugin's toolbar or menu should appear in your QGIS interface. You’re now ready to dive into the examples!

---

## Quick Start Video

Watch our [Quick Start Video](https://github.com/user-attachments/assets/0c85f177-c175-41a1-a96c-fff775ccdf1e).

<iframe width="560" height="315" src="https://github.com/user-attachments/assets/0c85f177-c175-41a1-a96c-fff775ccdf1e"></iframe>

---

## Example Use Cases

### Use Case 1: Generating Attribute Lists from a Vector Layer

Generate a model to list the attributes from a vector layer in the workspace by selecting the layer by name.

**Prompt**:  
*Generate a model to list the attributes from a vector layer in the workspace. Select the layer by name.*

**Note**: Replace the placeholder with your layer's name.

![Example Screenshot](https://github.com/user-attachments/assets/735a097d-605b-4b7e-a9f4-49ae3a040c3e)

---

### Use Case 2: Producing Attribute Descriptions for a Vector Layer

Generate a model that produces attribute descriptions for a vector layer, including attribute names, data types, counts of NULL values, and unique values.

**Prompt**:  
*Generate a model to describe the attributes of a vector layer. Include names, data types, NULL value counts, and unique value counts. Select the layer by name.*

**Note**: Replace the placeholder with your layer's name.

![Example Screenshot](https://github.com/user-attachments/assets/bd0a69ff-c009-44c7-b085-28c30e1610ba)

---

### Use Case 3: Producing Statistics for Polygon Areas

Generate a model that calculates area statistics for polygons in a loaded layer. The output includes minimum, maximum, average, standard deviation, and total feature count.

**Prompt**:  
*Produce area statistics for polygons in the selected layer, including minimum, maximum, mean, standard deviation, and total features.*

**Note**: Replace the placeholder with your layer's name.

![Example Screenshot](https://github.com/user-attachments/assets/ec65ef6b-106b-4ac7-a550-abed189ddd3a)

---

## Advanced Examples

### Use Case 1: Calculating Buffers Around Features

Generate a buffer area of 5000 meters with 40 segments around features in a vector layer.

**Prompt**:  
*Create a buffer area of 5000 meters and 40 segments around features in the selected layer.*

**Note**: Replace the placeholder with your layer's name.

![Example Screenshot](https://github.com/user-attachments/assets/d4927870-2057-4588-bc2d-9465a89e4450)

---

### Use Case 2: Generating Random Points

Create a model that generates 1000 random points over the current map extent in EPSG:28992.

**Prompt**:  
*Generate 1000 random points over the current map extent using EPSG:28992.*

![Example Screenshot](https://github.com/user-attachments/assets/8d972a92-73b5-4a25-9a2a-459e57eec87d)

---

### Use Case 3: Generating Random Lines

Create a model that generates 1000 random lines, each 5000 meters long, over the current map extent in EPSG:28992.

**Prompt**:  
*Generate 1000 random lines, each 5000 meters long, using EPSG:28992.*

![Example Screenshot](https://github.com/user-attachments/assets/d421b88a-00bc-403d-9870-4f205d556f17)

---

## Troubleshooting and Tips

A common issue when using the plugin is "hallucinated imports," where scripts reference non-existent imports or modules in your QGIS or Python environment. To avoid this:

- Verify all imported modules exist in your Python installation.  
- Ensure compatibility with the QGIS environment by testing custom scripts thoroughly.

--- 
