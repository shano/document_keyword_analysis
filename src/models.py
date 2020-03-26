from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

migrate = Migrate()
db = SQLAlchemy()

class KeywordSentence(db.Model):
    __tablename__ = 'keyword_sentence'
    sentence_id = Column(
        Integer, 
        ForeignKey('sentence.id'), 
        primary_key = True)

    keyword_id = Column(
        Integer, 
        ForeignKey('keyword.id'), 
        primary_key = True)

class Document(db.Model):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    content = Column(Text) # TODO V2 - Migrate to elasticsearch or postgres FTS
    sentences = relationship('Sentence', lazy=True)
    name = Column(String)

    def __repr__(self):
        return '<Document %r>' % self.id

class Sentence(db.Model):
    __tablename__ = 'sentence'
    id = Column(Integer, primary_key=True)
    content = Column(Text) # TODO V2 - Migrate to elasticsearch or postgres FTS
    document_id = Column(Integer, ForeignKey('document.id'), nullable=False)
    keywords = relationship('Keyword', secondary='keyword_sentence', lazy=True)
    document = relationship("Document", back_populates="sentences")

    def __repr__(self):
        return '<Sentence %r>' % self.id

class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    word = Column(Text)
    frequency = Column(Integer)
    sentences = relationship('Sentence', secondary='keyword_sentence', lazy=True)

    def __repr__(self):
        return '<Keyword %r>' % self.id

    # TODO both sentences and docs are really inefficient
    # Probably move to a /documents endpoint with direct pagination on each
    def as_dict(self):

        sentence_content = []
        document_names = set()
        for sentence in self.sentences:
            sentence_content.append(sentence.content)
            document_names.add(sentence.document.name)

        return {
            'id': self.id,
            'word': self.word,
            'frequency': self.frequency,
            'sentences': sentence_content,
            'documents': list(document_names)
        }
