import nltk
import sys
import NamedEntityRecognition
import DateTimeExtractor
import RelationExtraction
from nltk import PorterStemmer
from nltk.corpus import wordnet as wn
from itertools import chain
import datetime


class ControllerUnit:
    def __init__(self, inputText):
        self.rawText = inputText

    def performNER(self):
        nerObj = NamedEntityRecognition.namedEntityUnit(self.rawText)
        return nerObj.returnEntityNames()

    def performDateTimeExtraction(self):
        dateTimeObj = DateTimeExtractor.dateTimeUnit(self.rawText)
        taggedText = dateTimeObj.tag()
        return dateTimeObj.ground(taggedText, datetime.date)

    def orgLocRelationExtraction(self):
        orgLocObj = RelationExtraction.relationExtractionUnit(self.rawText)
        return orgLocObj.returnOrgLocationRelation()

    def perOrgRelationExtraction(self):
        perOrgObj=RelationExtraction.relationExtractionUnit(self.rawText)
        return perOrgObj.returnPerOrgRelation()
