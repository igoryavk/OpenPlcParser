import bs4
from bs4 import BeautifulSoup as Soup
import os
from shutil import rmtree


class OpenPlcParser:
    def __init__(self,path):
        self.__path=path
        with open(path,encoding="utf-8",mode="r") as openxml:
            content=openxml.read()
        self.__parsing_tree=Soup(content,"lxml")
        self.__project=self.__parsing_tree.project
        self.__pous = [pou for pou in self.__project.types.pous.children if pou.name is not None]

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
    def showPous(self):
       # self.__pous=[pou for pou in self.__project.types.pous.children if pou.name is not None]
        for pou in self.__pous:
            print(f"The pou name is {pou.get('name')} and its type is {pou.get('poutype')}")
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
    def __createCatalogStructure(self):
        for pou in self.__pous:
            for element in self.getPouChildren(pou):
                catalog_structure=f"{self.__dir_path}//{pou.get('poutype')}//{pou.get('name')}//{element.name}"
                if not os.path.exists(catalog_structure):
                    os.makedirs(catalog_structure)
            interface = pou.interface
            areas = [area for area in interface.children if area.name is not None]
            for area in areas:
                if (area.name!="documentation"):
                    interface_path=f"{self.__dir_path}//{pou.get('poutype')}//{pou.get('name')}//interface//{area.name}"
                    if not os.path.exists(interface_path):
                        os.makedirs(interface_path)
                    vars=self.__getVariables(area)
                    for var in vars:
                        if (area.name!="adddata"):
                            with open(f"{interface_path}//{var.get('name')}.txt",encoding="utf-8",mode="a") as varfile:
                                varfile.write(str(var))
                                varfile.close()
                        elif(area.name=="adddata"):
                            with open(f"{interface_path}//{var.name}.txt",encoding="utf-8",mode="a") as varfile:
                                varfile.write(str(var))
                                varfile.close()
                elif(area.name=="documentation"):
                    with open(f"{self.__dir_path}//{pou.get('poutype')}//{pou.get('name')}//interface//documentation.txt",encoding="utf-8",mode="a") as docfile:
                        docfile.write(str(area))
                        docfile.close()
            with open(f"{self.__dir_path}//{pou.get('poutype')}//{pou.get('name')}//st//st.txt",encoding="utf-8", mode="a") as stfile:
                stfile.write(str(pou.st))

    def parsePous(self):
        self.__createRootDirectory("D://parse")
        self.__createCatalogStructure()
    def clearPous(self,clearxml_path):
        list_pous=[pou for pou in self.__pous if pou.name is not None]
        for pou in list_pous:
            pou.decompose()
        self.__parsing_tree.prettify()
        with open(clearxml_path,encoding="utf-8",mode="w") as clearxml:
            clearxml.write(str(self.__parsing_tree))
            clearxml.close()
    def showDirectories(self):
        for level_1 in os.listdir("D://parse"):
            path=f"D://parse"+level_1
            if os.path.isdir(f"{path}"):
                print(path)

                for level_2 in os.listdir(f"{path}"):
                    path = path + level_2
                    if os.path.isdir(f"{path}"):
                        print(f"    {level_2}")
                        for level_3 in os.listdir(f"D://parse//{level_1}//{level_2}"):
                            if os.path.isdir(f"D://parse//{level_1}//{level_2}"):
                                print(f"        {level_3}")
                                for level_4 in os.listdir(f"D://parse//{level_1}//{level_2}//{level_3}"):
                                    if os.path.isdir(f"D://parse//{level_1}//{level_2}//{level_3}"):
                                        print(f"         {level_4}")
    def createStructure(self,path):
        bss=Soup()
        pous=bss.new_tag("pous")
        bss.append(pous)
        for level_1 in os.listdir(path):
            path_l1=f"{path}//{level_1}";
            if os.path.isdir(path_l1):
                for level_2 in os.listdir(path_l1):
                    path_l2=f"{path}//{level_1}//{level_2}"
                    if os.path.isdir(path_l2):
                        pou=bss.new_tag(name="pou")
                        pou["name"]=level_2
                        pou["poutype"]=level_1
                        bss.pous.append(pou)
        bss.prettify()
        with open("D://parse//newblock.xml",encoding="utf-8",mode="w") as newblock:
            newblock.write(str(bss))
            newblock.close()

if __name__ == '__main__':
    parser=OpenPlcParser("C://json//myexport.xml")
    #parser.showTopLevel()
    #parser.showPous()
    #parser.parsePous()
    #parser.clearPous("D://parse//clear.xml")
    parser.createStructure("D://parse")