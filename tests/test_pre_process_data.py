import os
from pathlib import Path
from src.services.GetSourceDocs import GetSourceDocFiles
from src.services.PreProcessData import PreProcessDataToDB # MOVE TO TOP AFTER BOOTSTRAP
from src.models import db
from src.models import Sentence, Document

def test_pre_processing_data(session):
    path = os.path.join(os.getcwd(), 'tests', 'exampledocs')
    source = GetSourceDocFiles(path, '*.txt')
    pre_processor = PreProcessDataToDB(source, session)
    pre_processor.pre_process()
    assert Document.query.count() == 2
    assert Sentence.query.count() == 4
    # TODO Test relationships exist too
