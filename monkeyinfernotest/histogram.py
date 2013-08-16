
from collections import defaultdict
from simplejson import dumps
   
    
class WordsHistogram:
    """Creates words histogram from given text
    """
    
    
    def __init__(self, text):
        
        self.histogram = defaultdict(lambda: 0)
        for word in text.split():
            self.histogram[word.lower()]+=1
            
    def sortedwords(self):
        """sorted words by frequency
        """
        return sorted(self.histogram.items(), key=lambda x:x[1], reverse=1)
    
    def to_json(self):
        """creates json from histogram
        """
        data = [{'word': x, 'count':y} for x,y in self.sortedwords()]
        return dumps(data)