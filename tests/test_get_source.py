import unittest
from src.services.GetSourceDocs import GetSourceDocFiles
from pathlib import Path
import os

documents = [
    ('The European languages are members of the same family. Their separate existence is a myth.', 'doc1.txt'), 
    ('For science, music, sport, etc, Europe uses the same vocabulary. The languages only differ in their grammar, their pronunciation and their most common words.', 'doc2.txt')
]

class TestGettingSourceFiles(unittest.TestCase):

    def test_getting_source_file(self):
        path = os.path.join(os.getcwd(), 'tests', 'exampledocs')
        source = GetSourceDocFiles(path, '*.txt')
        docs = list(source.get_docs())
        assert sorted(docs) == sorted(documents)

if __name__ == '__main__':
    unittest.main()