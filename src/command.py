from flask_script import Command

from src.services.GetSourceDocs import GetSourceDocFiles
from src.services.PreProcessData import PreProcessDataToDB
from src.services.ProcessKeywords import ProcessKeywordsFromDB

from src.models import db

# TODO Really wanted this to be a broken-down luigi data-pipeline
def data_load_command():
    db.create_all()
    # TODO These should be .env file or cmd line args
    path = 'data/'
    doc_file_glob = '*.txt'
    source = GetSourceDocFiles(path, doc_file_glob)
    pre_processor = PreProcessDataToDB(source, db.session)
    pre_processor.pre_process()
    processor = ProcessKeywordsFromDB(db.session)
    processor.process()