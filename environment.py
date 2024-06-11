from qgis.core import QgsProject, QgsMapLayer


class QgisEnvironment():
    def __init__(self):
        self.project = QgsProject.instance()
        self.layers = self.project.mapLayers().values()

    def refresh(self):
        self.project = QgsProject.instance()
        self.layers = self.project.mapLayers().values()

    def getLayerAttributes(self):
        envInfo = ''
        envInfo += f'Total number of layers: {len(self.layers)}\n'
        for layer in self.layers:
            envInfo += '\n'
            layerName = layer.name()
            envInfo += f'Layer Name: {layerName};\n'
            envInfo += f'    Layer Type: {str(layer.type())};\n'
            if layer.type() == QgsMapLayer.VectorLayer:
                # get EPSG
                crs = layer.crs()
                epsgCode = crs.authid().split(':')[-1]
                envInfo += f'    EPSG Code: {epsgCode};\n'

                # get extent
                extent = layer.extent()
                xmin, ymin = extent.xMinimum(), extent.yMinimum()
                xmax, ymax = extent.xMaximum(), extent.yMaximum()
                envInfo += f'    Extent: {xmin}, {ymin}, {xmax}, {ymax};\n'

                # get geometry type
                geometryType = str(layer.geometryType())
                envInfo += f'    Geometry Type: {geometryType};\n'

            elif layer.type() == QgsMapLayer.RasterLayer:
                # get EPSG
                crs = layer.crs()
                epsgCode = crs.authid().split(':')[-1]
                envInfo += f'    EPSG Code: {epsgCode};\n'

                # get extent
                extent = layer.extent()
                xmin, ymin = extent.xMinimum(), extent.yMinimum()
                xmax, ymax = extent.xMaximum(), extent.yMaximum()
                envInfo += f'    Extent: {xmin}, {ymin}, {xmax}, {ymax};\n'

                # get resolution
                pixelSizeX = str(layer.rasterUnitsPerPixelX())
                pixelSizeY = str(layer.rasterUnitsPerPixelY())
                envInfo += f'    Resolution: {pixelSizeX}, {pixelSizeY};\n'

                # get attributes
                provider = layer.dataProvider()
                bandCount = provider.bandCount()
                envInfo += f'    Attributes:\n'
                for i in range(1, bandCount + 1):
                    bandType = provider.sourceDataType(i)
                    envInfo += f'        Band Number: {str(i)}, Data Type: {bandType};\n'

            else:
                envInfo += f"Layer name: {layerName} - Type: Unknown;"

        return envInfo

