"""
Model exported as python.
Name : reproject
Group : 
With QGIS : 33602
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterCrs
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Reproject(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('input_layer', 'Input layer', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterCrs('target_crs', 'Target CRS', defaultValue='EPSG:28992'))
        self.addParameter(QgsProcessingParameterFeatureSink('Output', 'Output', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Reproject layer
        alg_params = {
            'CONVERT_CURVED_GEOMETRIES': False,
            'INPUT': parameters['input_layer'],
            'OPERATION': None,
            'TARGET_CRS': parameters['target_crs'],
            'OUTPUT': parameters['Output']
        }
        outputs['ReprojectLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output'] = outputs['ReprojectLayer']['OUTPUT']
        return results

    def name(self):
        return 'reproject'

    def displayName(self):
        return 'reproject'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Reproject()
