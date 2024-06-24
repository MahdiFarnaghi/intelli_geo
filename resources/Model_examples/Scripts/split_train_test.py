"""
Model exported as python.
Name : split_train_test
Group : 
With QGIS : 33602
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Split_train_test(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('percentage_train', 'Percentage train', type=QgsProcessingParameterNumber.Integer, minValue=1, maxValue=99, defaultValue=70))
        self.addParameter(QgsProcessingParameterVectorLayer('samples', 'Samples', types=[QgsProcessing.TypeVectorAnyGeometry], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TestSubset', 'Test subset', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('TrainSubset', 'Train subset', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Extract train subset
        alg_params = {
            'INPUT': parameters['samples'],
            'METHOD': 1,  # Percentage of features
            'NUMBER': parameters['percentage_train'],
            'OUTPUT': parameters['TrainSubset']
        }
        outputs['ExtractTrainSubset'] = processing.run('native:randomextract', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TrainSubset'] = outputs['ExtractTrainSubset']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Difference
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': parameters['samples'],
            'OVERLAY': outputs['ExtractTrainSubset']['OUTPUT'],
            'OUTPUT': parameters['TestSubset']
        }
        outputs['Difference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['TestSubset'] = outputs['Difference']['OUTPUT']
        return results

    def name(self):
        return 'split_train_test'

    def displayName(self):
        return 'split_train_test'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Split_train_test()
