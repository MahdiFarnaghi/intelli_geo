from langchain.tools import tool
from typing import *

from .environment import QgisEnvironment


@tool
def readEnvironment() -> str:
    """
    Use this tool to retrieve detailed information about the currently opened project in QGIS.

    The tool provides comprehensive data for all types of layers, including:
        - Layer Name
        - Layer Type
        - Coordinate Reference System (CRS)
        - Extent

    For vector layers, additional information is included:
        - Geometry Type

    For raster layers, additional information is included:
        - Resolution
        - Attributes (including Band Names and Data Types)
    """
    environment = QgisEnvironment()
    environment.refresh()
    return environment.getLayerAttributes()
