from .fileUtility import FileUtilityBase
from .fileHandlerBase import FileConverter, FileCreator
import os

from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.objects.conversion.log import factory as conversion_factory #error msg
from pm4py.objects.log.util import sorting

# provides file import and export for .xes and .csv files
class FileUtility(FileUtilityBase):

    def __init__(self, defaultDirectory):
        super(FileUtility, self).__init__(defaultDirectory)
        self.registerImport('.xes', XESFileConverter())
        self.registerImport('.csv', CSVFileConverter())
        self.registerExport('.xes', XESFileCreator())

# provides .xes to event log conversion using pm4py
class XESFileConverter(FileConverter):
    def __init__(self):
        self._fileType = '.xes'

    def convert(self, filePath):
        return xes_importer.apply(filePath)

# provides .csv to event log converstion using pm4py
class CSVFileConverter(FileConverter):
    def __init__(self):
        self._fileType = '.csv'

    def convert(self, filePath):
        csvEventStream = csv_importer.import_event_stream(filePath)
        return conversion_factory.apply(csvEventStream)

# provides event log to .xes file creation using pm4py
class XESFileCreator(FileCreator): 

    def __init__(self):
        super(XESFileCreator, self).__init__()
        self._fileType = '.xes'

    def createFile(self, eventLog, fileName = "", filePath = ""):
        destinationPath = self.getDestinationPath()
        if filePath != "":
            destinationPath = filePath
        destinationPath = os.path.join(fileName, filePath)
        xes_exporter.export_log(eventLog, destinationPath)
        return destinationPath
        
        