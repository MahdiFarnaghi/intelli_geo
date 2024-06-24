"""
Model exported as python.
Name : points_in_polygons
Group : 
With QGIS : 33602
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Points_in_polygons(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('points', 'Points', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('polygons', 'Polygons', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output', 'Output', type=QgsProcessing.TypeVectorPolygon, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Count points in polygon
        alg_params = {
            'CLASSFIELD': None,
            'FIELD': 'NUMPOINTS',
            'POINTS': parameters['points'],
            'POLYGONS': parameters['polygons'],
            'WEIGHT': None,
            'OUTPUT': parameters['Output']
        }
        outputs['CountPointsInPolygon'] = processing.run('native:countpointsinpolygon', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output'] = outputs['CountPointsInPolygon']['OUTPUT']
        return results

    def name(self):
        return 'points_in_polygons'

    def displayName(self):
        return 'points_in_polygons'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Points_in_polygons()
