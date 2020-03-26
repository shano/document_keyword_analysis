from pathlib import Path
from abc import ABC, abstractmethod
import ntpath

class AbstractGetSourceDocs(ABC):
    @abstractmethod
    def get_docs(self, path, glob):
        pass


# Returns a list of document content
class GetSourceDocFiles(AbstractGetSourceDocs):
    def __init__(self, path, glob):
        self.path = path
        self.glob = glob

    def get_docs(self):
        files = Path(self.path).rglob(self.glob)
        for f in files:
            with open(f, 'r') as file:
                content = file.read()
            filename = ntpath.basename(f)
            file.close()
            yield (content, filename)