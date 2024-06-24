"""
Model exported as python.
Name : dissolve
Group : 
With QGIS : 33602
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Dissolve(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterField('attribute', 'Attribute', type=QgsProcessingParameterField.Any, parentLayerParameterName='input_layer', allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('input_layer', 'Input layer', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output', 'Output', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Dissolve
        alg_params = {
            'FIELD': parameters['attribute'],
            'INPUT': parameters['input_layer'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': parameters['Output']
        }
        outputs['Dissolve'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output'] = outputs['Dissolve']['OUTPUT']
        return results

    def name(self):
        return 'dissolve'

    def displayName(self):
        return 'dissolve'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Dissolve()
