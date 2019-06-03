from xml.etree import ElementTree as ET
import pprint
import spacy
import re
import nltk

nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


MAX_LEN = 10
pp = pprint.PrettyPrinter(indent=4)
spacy_nlp = spacy.load('en_core_web_sm')
ps = PorterStemmer()

class Extractor:
    """
    Take in the path to an XML file and parse out the tree and the root element, make them class variables
    """
    def __init__(self, dataFilePath):
        print("Extracting Tree")
        self.tree = self.getTree(dataFilePath)
        print("Grabbing root")
        self.root = self.getRoot(self.tree)

        return

    """
    getTree(dataFilePath)
    
    Take in a path to an XML data file and return an ElementTree representation
    """
    def getTree(self, dataFilePath):
        return ET.parse(dataFilePath)

    """
    getRoot(tree)
    
    Take in an ElementTree and return the root element
    """
    def getRoot(self, tree):
        return tree.getroot()

class PostExtractor(Extractor):
    def __init__(self, file):
        print("Prepping PostExtractor")
        super().__init__(file)
        self.posts = {}

        # extract
        print("Extracting Posts")
        self.posts = self.writeOut()

        print("Extracted")
        return

    def getRawQuestions(self):
        return self.root.findall(".//*[@AcceptedAnswerId]")

    def getRawAnswersByParent(self, parent_id):
        return self.root.findall(".//*[@ParentId='" + parent_id + "']")

    def processText(self, text):
        # Given body of question or answer as original string,
        # 1. compile a regex to find all <code> blocks
        codeblock_regex = re.compile(r"<code>(.*)</code>")
        original_question_body = text

        # 2. execute the regex on the original string and get a match object
        codeblocks = codeblock_regex.finditer(original_question_body)
        codeblock_count = 0

        # 3. count the code blocks
        for codeblock in codeblocks:
            codeblock_count += 1

        # 3a. remove the codeblocks
        codeless_question_body = codeblock_regex.sub(' ', original_question_body)

        # 3b. remove all remaining html tags
        htmlfree_regex = re.compile(r"<[^>]+>")
        htmlfree_body = htmlfree_regex.sub(' ', codeless_question_body)

        # 4. replace all non-alpha chars in the code-free string with a space
        nonalpha_regex = re.compile(r"[^A-Za-z]")
        alpha_string = nonalpha_regex.sub(' ', htmlfree_body)

        # 5. replace all uppercase chars in the alphabetic string  w/ lowercase
        lowercase_string = alpha_string.lower()

        # 6. remove all stopwords from the lowercase string, stemming remaining words at the same time
        split_string = lowercase_string.split(' ')
        stemmed_stopwordless_list = [ps.stem(word) for word in split_string if not word in set(stopwords.words('english'))]
        normalized_body = " ".join(stemmed_stopwordless_list)

        spacy_result = spacy_nlp(normalized_body)

        # Analyze syntax
        spacy_noun_phrases = [chunk.text for chunk in spacy_result.noun_chunks]
        spacy_verbs = [token.lemma_ for token in spacy_result if token.pos_ == "VERB"]
        spacy_entity_chunks = spacy_result.ents

        spacy_entity_string = ''
        for entity in spacy_entity_chunks:
            spacy_entity_string += entity.text + ','
        spacy_entity_string = spacy_entity_string[:-1]

        result_map = {
            'noun_phrases': spacy_noun_phrases,
            'verbs': spacy_verbs,
            'entity_chunks': spacy_entity_string,
            'codeblock_count': codeblock_count
        }

        return result_map

    def addTextProcessingToXmlEntity(self, xml_entity):
        text_processing_results = self.processText(xml_entity.attrib.get('Body'))
        xml_entity.set('NounPhrases', ','.join(text_processing_results['noun_phrases']))
        xml_entity.set('Verbs', ','.join(text_processing_results['verbs']))
        xml_entity.set('EntityChunks', text_processing_results['entity_chunks'])
        xml_entity.set('CodeblockCount', str(text_processing_results['codeblock_count']))
        return xml_entity


    def writeOut(self):

        questions = self.getRawQuestions() 
        root = ET.Element('posts')
        count = 0
        max = MAX_LEN

        print('shortening question list')
        for question_index in range(len(questions)):

            # 1. install and import spacy
            # 2. run chunking and/or parsing on question body
            # 3. add chunked data to question element

            question = questions[question_index]
            question_id = question.attrib.get('Id')

            # QUESTION BODY
            self.addTextProcessingToXmlEntity(question)

            answers = self.getRawAnswersByParent(question_id)
            for answer in answers:
                self.addTextProcessingToXmlEntity(answer)

            root.insert(1,question)
            root.extend(answers)

            count += 1
            if (count > max):
                break
            # return result

            # add the new features to the XML object:  code count, stemmed string, noun phrases, verb phrases, entity chunks
            # -- the following steps should be done in the extractor --
            # 1. run count vectorizer on stemmed string to get our first bag of words sparse matrix
            # 2. run count vectorizer on the noun phrases, verb phrases, and entity chunks respectively and get three more sparse matricies
            # 3. run the random forest algorithm on each sparse matrix and get 4 classification results
            # 4. assess the results of each of the random forests, determining which is the best or if we should combine them together somehow
            # 9. add the new features to the XML object:  code count, stemmed string, noun phrases, verb phrases, entity chunks
            # 8. additionally, run spacy on the *html-free*, *codefree-string* string

        limited_questions = questions[:MAX_LEN]

        print('here')
        ET.ElementTree(root).write('extracted.xml')

extractor = PostExtractor('Posts.xml')
