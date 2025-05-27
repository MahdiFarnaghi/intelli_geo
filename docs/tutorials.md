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
    <img src="./img/QGIS_UC_2025/fig_new_conversation.png"
         alt="New conversation" width="600px">
    <figcaption><strong>Figure 1:</strong> Creating a new conversation.</figcaption>
</figure>



### Requesting general information

In this section, you will interact with **IntelliGeo** to request general information about **QGIS**, the plugin, and the data available at your working space. You are encourage to experiment with the provided prompts:

| No.   | Prompt   | Expected output   |
| ----- | -------- | ----------------- |
| 1     | What is QGIS? | Description of the QGIS software. |
| 2     | What is a QGIS plugin? | Description of a plugin for QGIS. |
| 3     | Where can I get information about QGIS plugins? | Information about QGIS Plugin Repository. |
| 4     | Is IntelliGeo a QGIS plugin? | Confirmation that IntelliGeo is a QGIS plugin. |
| 5     | What can I do with IntelliGeo? | A list of tasks that IntelliGeo can support. |

### Processing with a single data layer

### Processing with two data layers

### References 

**[O’Mara et al., 2021]** O'Mara MT, Amorim F, Scacco M, McCracken GF, Safi K, Mata V, Tomé R, Swartz S, Wikelski M, Beja P, Rebelo H, Dechmann DKN. 2021. Bats use topography and nocturnal updrafts to fly high and fast. Curr Biol. doi:10.1016/j.cub.2020.12.042 