import re
import nltk
from nltk import tree
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk.sem.relextract import tree2semi_rel, semi_rel2reldict
from collections import defaultdict
from nltk.compat import htmlentitydefs


class doc():
    pass


class relationExtractionUnit:
    def __init__(self, inputText):
        self.rawText = inputText
        self.sentences = nltk.sent_tokenize(self.rawText)
        self.tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in self.sentences]
        self.tagged_sentences = [nltk.pos_tag(sentence) for sentence in self.tokenized_sentences]
        # self.chunked_sentences = nltk.ne_chunk_sents(self.tagged_sentences, binary=True)

    def temp(self):
        # relation: Location of Organization
        IN = re.compile(r'.*\bin\b(?!\b.+ing)')
        OF = re.compile(r'.*\bof\b.*')
        relations = []
        for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
            for relation in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ieer', pattern=OF):
                relations.append(nltk.sem.rtuple(relation))
        print relations

    def returnOrgLocationRelation(self):
        # self.temp()
        # relation: Location of Organization
        pattern = re.compile(r'.*\bin\b(?!\b.+ing)')
        subjectClass = 'ORGANIZATION'
        objectClass = 'LOCATION'
        return self.relationExtraction(subjectClass, objectClass, pattern)

    def relationExtraction(self, subjectClass, objectClass, pattern):
        window = 5
        relations = []
        relfilter = lambda x: (x['subjclass'] == subjectClass and
                               len(x['filler'].split()) <= window and
                               pattern.match(x['filler']) and
                               x['objclass'] == objectClass)
        for sent in self.tagged_sentences:
            chunked = nltk.ne_chunk(sent)
            reldicts = self.semi_rel2reldict(tree2semi_rel(chunked))
            rels = list(filter(relfilter, reldicts))
            for rel in rels:
                relations.append(nltk.sem.relextract.rtuple(rel))
        return relations

    # def returnPerOrgRelation(self):
    #     OF = re.compile(r'.*\bof\b.*')
    #     relations = []
    #     for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
    #         for relation in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ace', pattern='OF'):
    #             relations.append(nltk.sem.rtuple(relation))
    #     return relations
    def returnPerOrgRelation(self):
        # relation: Person of Organization
        pattern = re.compile(r'.*\bof\b.*')
        subjectClass = 'PERSON'
        objectClass = 'ORGANIZATION'
        return self.relationExtraction(subjectClass, objectClass, pattern)

    def _join(self, lst, sep=' ', untag=False):
        try:
            return sep.join(lst)
        except TypeError:
            if untag:
                return sep.join(tup[0] for tup in lst)
            from nltk.tag import tuple2str
            return sep.join(tuple2str(tup) for tup in lst)

    def semi_rel2reldict(self, pairs, window=5, trace=False):
        result = []
        while len(pairs) >= 2:
            reldict = defaultdict(str)
            reldict['lcon'] = self._join(pairs[0][0][-window:])
            reldict['subjclass'] = pairs[0][1].label()
            reldict['subjtext'] = self._join(pairs[0][1].leaves())
            reldict['subjsym'] = self.list2sym(pairs[0][1].leaves())
            reldict['filler'] = self._join(pairs[1][0])
            reldict['untagged_filler'] = self._join(pairs[1][0], untag=True)
            reldict['objclass'] = pairs[1][1].label()
            reldict['objtext'] = self._join(pairs[1][1].leaves())
            reldict['objsym'] = self.list2sym(pairs[1][1].leaves())
            reldict['rcon'] = []
            if trace:
                print("(%s(%s, %s)" % (reldict['untagged_filler'], reldict['subjclass'], reldict['objclass']))
            result.append(reldict)
            pairs = pairs[1:]
        return result

    def list2sym(self, lst):
        """
        Convert a list of strings into a canonical symbol.
        :type lst: list
        :return: a Unicode string without whitespace
        :rtype: unicode
        """
        sym = self._join(lst, '_', untag=True)
        sym = sym.lower()
        ENT = re.compile("&(\w+?);")
        sym = ENT.sub(self.descape_entity, sym)
        sym = sym.replace('.', '')
        return sym

    def descape_entity(self, m, defs=htmlentitydefs.entitydefs):
        try:
            return defs[m.group(1)]

        except KeyError:
            return m.group(0)  # use as is
