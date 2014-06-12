

from XML import *
class Block:

    def __init__(self):
        pass

    @staticmethod
    def createBlock(xmlNode):

        node_kind = xmlNode.get('kind')
        print(node_kind)

        Block.load_class("./XML.XML")

    #function to dynamically load a new class

    @staticmethod
