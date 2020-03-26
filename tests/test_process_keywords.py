import os
from pathlib import Path
from src.services.GetSourceDocs import GetSourceDocFiles
from src.services.PreProcessData import PreProcessDataToDB
from src.services.ProcessKeywords import ProcessKeywordsFromDB
from src.models import db
from src.models import Sentence, Document, Keyword

def test_process_keywords(session):
    # TODO Should not be relying on previous tasks
    processor = ProcessKeywordsFromDB(session)
    corpus = processor.build_corpus(Document.query.all())
    keywords = processor.get_keywords(corpus, 5)
    assert keywords == [('language', 2), ('science', 1), ('music', 1), ('sport', 1), ('etc', 1)]
    processor.store_and_link_keywords(keywords)
    for sentence in Sentence.query.all():
        for sentence_keywords in sentence.keywords:
            assert sentence_keywords.word in sentence.content