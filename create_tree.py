from openplc_parser import OpenPlcParser


parser=OpenPlcParser("D://export.xml")
#parser.showPouAttributes()
#parser.savePous("D://parse//pous")
#parser.saveCopyObjTree()
# parser.showPous()
# parser.parsePous()
# parser.clearPous("D://parse//clear.xml")
parser.createNewTree()
# parser.createStructure("D://parse")