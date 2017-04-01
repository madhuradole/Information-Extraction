import nltk
from nltk.tag.stanford import StanfordNERTagger
import os


class namedEntityUnit:
    def __init__(self, inputText):
        self.rawText = inputText
        self.sentences = nltk.sent_tokenize(self.rawText)
        self.tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in self.sentences]
        self.tagged_sentences = [nltk.pos_tag(sentence) for sentence in self.tokenized_sentences]
        self.chunked_sentences = nltk.ne_chunk_sents(self.tagged_sentences, binary=True)

    def extract_entity_names(self, t):
        entity_names = []
        if hasattr(t, 'label') and t.label:
            if t.label() == 'NE':
                entity_names.append(' '.join([child[0] for child in t]))
            else:
                for child in t:
                    entity_names.extend(self.extract_entity_names(child))

        return entity_names

    def returnEntityNames(self):
        if os.environ.get("JAVA_HOME") is not None and "/bin" not in os.environ["JAVA_HOME"]:
            os.environ["JAVAHOME"] = os.path.normpath(os.path.join(os.environ["JAVA_HOME"], "bin"))
        # model = "C:\Users\Maddy\PycharmProjects\InformationExtraction\Stanford\english.all.3class.distsim.crf.ser.gz"
        # model = "C:\Users\Maddy\PycharmProjects\InformationExtraction\Stanford\english.conll.4class.distsim.crf.ser.gz"
        model = os.getcwd() + "\Stanford\english.muc.7class.distsim.crf.ser.gz"
        # model = "C:\Users\Maddy\PycharmProjects\InformationExtraction\Stanford\english.muc.7class.distsim.crf.ser.gz"
        jar = os.getcwd() + "\Stanford\stanford-ner.jar"
        st = StanfordNERTagger(model_filename=model, path_to_jar=jar)
        stanfordTagged = st.tag(self.rawText.split())
        return stanfordTagged
        # entity_names = []
        # for tree in self.chunked_sentences:
        #     entity_names.extend(self.extract_entity_names(tree))
        # return set(entity_names)
