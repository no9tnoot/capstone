# Molly Ryan, Peter Berens, Sian Wood
# 31 August 2023
# ISQLQuery

from abc import ABC, abstractmethod

class ISQLQuery(ABC):
    
    @abstractmethod
    def setAttr(self):
        pass
    
    