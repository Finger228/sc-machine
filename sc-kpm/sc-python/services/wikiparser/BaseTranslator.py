import json
from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    def __init__(self):
        self._info = {}
        self._info['entities'] = {}
        self._info['relations'] = {}
        self._info['triplets'] = []

    @abstractmethod
    def getEntity(self, entity):
        pass

    @abstractmethod
    def getEntities(self, entities):
        pass

    def getJson(self):
        return json.dumps(self._info)
