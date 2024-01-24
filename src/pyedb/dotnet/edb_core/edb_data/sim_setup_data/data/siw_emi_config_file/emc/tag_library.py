from pyedb.dotnet.edb_core.edb_data.sim_setup_data.data.siw_emi_config_file.emc.xml_generic import XmlGeneric


class TagType(XmlGeneric):
    def __init__(self, element):
        super().__init__(element)

        if element is not None:
            self.name = self._element.attrib["name"]
        else:
            self.name = None


class TagConfig(XmlGeneric):
    def __init__(self, element):
        super().__init__(element)


class Tag(XmlGeneric):
    CLS_MAPPING = {
        "TagType": TagType,
        "TagConfig": TagConfig
    }

    def __init__(self, element):
        super().__init__(element)

        if element is not None:
            self.label = self._element.attrib["label"]
            self.name = self._element.attrib["name"]
            self.sub_elements = []

            for el in self._element.findall("TagType"):
                temp = TagType(el)
                self.sub_elements.append(temp)

            for el in self._element.findall("TagConfig"):
                temp = TagConfig(el)
                self.sub_elements.append(temp)
        else:
            self.label = None
            self.name = None
            self.sub_elements = []


class TagLibrary(XmlGeneric):
    CLS_MAPPING = {
        "Tag": Tag,
    }

    def __init__(self, element):
        super().__init__(element)
        self._element = element

        if element:
            for el in self._element.findall("Tag"):
                tag = Tag(el)
                self.sub_elements.append(tag)
