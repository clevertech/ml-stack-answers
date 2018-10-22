from xml.etree import ElementTree as ET

import pprint

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

        pp.pprint(self.root)

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
