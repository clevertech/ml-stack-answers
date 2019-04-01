from xml.etree import ElementTree as ET
import pprint

MAX_LEN = 1000
pp = pprint.PrettyPrinter(indent=4)

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

    def writeOut(self):

        questions = self.getRawQuestions() 
        root = ET.Element('posts')
        count = 0
        max = 1000

        print('shortening question list')
        for question_index in range(len(questions)):

            question = questions[question_index]
            question_id = question.attrib.get('Id')
            print('id: ' + str(question_id))

            answers = self.getRawAnswersByParent(question_id)
            print('answers: ' + str(len(answers)))

            root.insert(1,question)
            root.extend(answers)

            count += 1
            if (count > max):
                break

        limited_questions = questions[:1000]

        ET.ElementTree(root).write('extracted.xml')

extractor = PostExtractor('Posts.xml')
