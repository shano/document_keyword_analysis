from abc import ABC, abstractmethod
from src.services.GetSourceDocs import AbstractGetSourceDocs
from src.models import Document, Sentence, Keyword
import os
# Libraries for text preprocessing
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sqlalchemy import func

class AbstractProcessKeywords(ABC):
    # This could push to a queue etc
    @abstractmethod
    def process(self):
        pass


# TODO - This could be separated into more explicit tasks in luigi
class ProcessKeywordsFromDB(AbstractProcessKeywords):
    def __init__(self, session):
        self.session = session
        nltk.download('stopwords')
        nltk.download('wordnet') 
    
    def build_corpus(self, documents):
        corpus = []
        stop_words = set(stopwords.words("english"))
        for i in range(0, len(documents)):
            #Remove punctuations
            text = re.sub('[^a-zA-Z]', ' ', documents[i].content)
            #Convert to lowercase
            text = text.lower()
            #remove tags
            text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
            # remove special characters and digits
            text=re.sub("(\\d|\\W)+"," ",text)
            ##Convert to list from string
            text = text.split()
            ##Stemming
            lem = WordNetLemmatizer()
            text = [lem.lemmatize(word) for word in text if not word in  
                    stop_words] 
            text = " ".join(text)
            corpus.append(text)
        return corpus

    def get_keywords(self, corpus, n):
        #Most frequently occuring words
        vec = CountVectorizer().fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in      
                    vec.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], 
                        reverse=True)
        return words_freq[:n]
    
    # TODO Split up into multiple functions
    # A function with an and in it's function name is probably bad....
    def store_and_link_keywords(self, keywords):
        for keyword, frequency in keywords:
            new_keyword = Keyword()
            new_keyword.frequency = int(frequency)
            new_keyword.word = keyword
            self.session.add(new_keyword)
            self.session.flush()
            # TODO: Must be a more efficient way than this
            for keyword_sentence in Sentence.query.filter(func.lower(Sentence.content).contains(keyword)):
                keyword_sentence.keywords.append(new_keyword)
        self.session.commit()

    def process(self):
        corpus = self.build_corpus(self.session.query(Document).all())
        # TODO Should be in a .env or command line arg
        number_of_keywords = 20
        keywords = self.get_keywords(corpus, number_of_keywords)
        self.store_and_link_keywords(keywords)