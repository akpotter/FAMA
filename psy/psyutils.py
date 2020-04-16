import logging

from java.util import UUID
from java.util.logging import Level
from org.sleuthkit.autopsy.casemodule import Case
from org.sleuthkit.autopsy.casemodule.services import Blackboard
from org.sleuthkit.autopsy.ingest import ModuleDataEvent
from org.sleuthkit.autopsy.ingest import IngestServices
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.autopsy.ingest import IngestMessage

from psy.progress import ProgressUpdater

class PsyUtils:
    def __init__(self):
        self._logger = Logger.getLogger("Ingest Logger")
        

        

    def log(self, level, msg):
        self._logger.logp(level, self.__class__.__name__, inspect.stack()[1][3], msg)

    @staticmethod
    def add_to_fileset(name, folder, device_id = UUID.randomUUID()):
        fileManager = Case.getCurrentCase().getServices().getFileManager()
        skcase_data = Case.getCurrentCase()
        #skcase_data.notifyAddingDataSource(device_id)
        progress_updater = ProgressUpdater() 
        
        fileManager.addLocalFilesDataSource(device_id.toString(), name, "", folder, progress_updater)
        
        files_added = progress_updater.getFiles()
        
        for file_added in files_added:
            skcase_data.notifyDataSourceAdded(file_added, device_id)

    @staticmethod
    def create_attribute_type(att_name, type, att_desc):
        try:
            Case.getCurrentCase().getSleuthkitCase().addArtifactAttributeType(att_name, type, att_desc)
        except:
            self.log(Level.INFO, "[Project] Error creating attribute type: " + att_desc)
        return Case.getCurrentCase().getSleuthkitCase().getAttributeType(att_name)
    
    @staticmethod
    def create_artifact_type(base_name, art_name, art_desc):
        try:
            Case.getCurrentCase().getSleuthkitCase().addBlackboardArtifactType(art_name, base_name.capitalize() + art_desc)
        except:
            self.log(Level.INFO, "[Project]  Error creating artifact type: " + art_desc)
        art = Case.getCurrentCase().getSleuthkitCase().getArtifactType(art_name)
        return art
    
    @staticmethod
    def index_artifact(artifact, artifact_type):
        IngestServices.getInstance().fireModuleDataEvent(ModuleDataEvent("test",artifact_type, None))

    @staticmethod
    def add_relationship(node1, node2, art, relationship_type, timestamp):
        Case.getCurrentCase().getSleuthkitCase().getCommunicationsManager().addRelationships(node1, node2, art, relationship_type, timestamp)
                    
    @staticmethod
    def blackboard_attribute(attribute):
        return {
            "byte": BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.BYTE,
            "datetime": BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DATETIME,
            "double": BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.DOUBLE,
            "integer": BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.INTEGER,
            "long": BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.LONG,
            "string": BlackboardAttribute.TSK_BLACKBOARD_ATTRIBUTE_VALUE_TYPE.STRING
        }.get(attribute)
    
    @staticmethod
    def get_or_create_account(self, account_type,  file, uniqueid):
        return Case.getCurrentCase().getSleuthkitCase().getCommunicationsManager().createAccountFileInstance(account_type, uniqueid, "test", file.getDataSource())
