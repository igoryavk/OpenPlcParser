import bs4
from bs4 import BeautifulSoup as Soup
import os
from shutil import rmtree
from bs4 import NavigableString


class OpenPlcParser:

    def __init__(self,path):
        self.__path=path
        with open(path,encoding="utf-8",mode="r") as openxml:
            content=openxml.read()
        self.__parsing_tree=Soup(content,"xml")
        self.__project=self.__parsing_tree.project
        self.__pous = [pou for pou in self.__project.types.pous.children if pou.name is not None]
        # with open("D://parse//111.xml",encoding="utf-8",mode="w") as file:
        #     file.write(str(self.__parsing_tree))
        #     file.close()


    def showTopLevel(self):
        topLevelNames=[element.name for element in self.__project.children if element.name is not None]
        self.__topLevelTags=[element for element in self.__project.children if element.name is not None]
        print(topLevelNames)

    def showTags(self):
        for tag in self.__topLevelTags:
            print(f"The elements name is {tag.name} and its type is {type(tag)}")

    def showTypes(self):
        types=[type for type in self.__project.types.children if type.name is not None]
        for type in types:
            print(type.name)

    def showDataTypes(self):
        datatypes = [type for type in self.__project.types.datatypes.children if type.name is not None]
        for type in datatypes:
            print(type.get("name"))

    def showPouStructure(self):
        #self.__pous=[pou for pou in self.__project.types.pous.children if pou.name is not None]
        elements=[element for element in self.__project.types.pous.pou.children if element.name is not None]
        for element in elements:
            print(element.name)

    def savePous(self,path):
        self.__createRootDirectory(dir_path=path)
        for pou in self.__pous:
            with open(f'{path}//{pou.get("name")}.xml','w',encoding='utf-8') as file:
                file.write(str(pou))
                file.flush()
                file.close()
    def showPouAttributes(self):
        for pou in self.__pous:
            print(pou.attrs)

    def getPouChildren(self,pou):
        return [element for element in pou.children if element.name is not None]

    def __getVariables(self,var_area):
        return [el for el in var_area.children if el.name is not None]

    def __createRootDirectory(self,dir_path):
        self.__dir_path=dir_path
        if os.path.exists(dir_path):
            rmtree(dir_path)
        os.makedirs(dir_path)



    def clearPous(self,clearxml_path):
        pous=self.__parsing_tree.types.pous
        pous.decompose()
        self.__parsing_tree.prettify()
        # list_pous=[pou for pou in self.__pous if pou.name is not None]
        # for pou in list_pous:
        #     pou.decompose()
        # self.__parsing_tree.prettify()
        with open(clearxml_path,encoding="utf-8",mode="w") as clearxml:
             clearxml.write(str(self.__parsing_tree))
             clearxml.close()





if __name__ == '__main__':
    parser=OpenPlcParser("D://export.xml")
    parser.savePous("D://parse//pous")
    # parser.showPous()
    # parser.parsePous()
    # parser.clearPous("D://parse//clear.xml")
    # parser.createStructure("D://parse")