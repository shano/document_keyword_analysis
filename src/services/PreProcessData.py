from abc import ABC, abstractmethod
from src.services.GetSourceDocs import AbstractGetSourceDocs
from src.models import Document, Sentence
import nltk.data
import os

class AbstractPreProcessData(ABC):
    @abstractmethod
    def pre_process(self):
        pass


class PreProcessDataToDB(AbstractPreProcessData):
    # TODO Type hinting
    def __init__(self, source: AbstractGetSourceDocs, session):
        self.source = source
        self.session = session
        nltk.download('punkt')

    def pre_process(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        for (document, filename) in self.source.get_docs():
            doc = Document()
            doc.content = document
            doc.name = str(filename)
            self.session.add(doc)
            self.session.flush()

            for doc_sentence in tokenizer.tokenize(document):
                sentence = Sentence()
                sentence.content = doc_sentence
                sentence.document_id = doc.id
                self.session.add(sentence)
            self.session.commit()
