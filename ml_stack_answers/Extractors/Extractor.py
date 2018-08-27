from xml.etree import ElementTree as ET

class Extractor:
    """
    Take in the path to an XML file and parse out the tree and the root element, make them class variables
    """
    def __init__(self, dataFilePath):
        self.tree = self.getTree(dataFilePath)
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
