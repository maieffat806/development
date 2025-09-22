import xml.etree.ElementTree as ET
import json


class XMLtoJSONConverter:
    def __init__(self, xml_file):
        self.xml_file = xml_file

    def parse_xml(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        return self._element_to_dict(root)

    def _element_to_dict(self, element):
        data = {}

        for child in element:
            data[child.tag] = self._element_to_dict(child)

        if element.text and element.text.strip():
            data["text"] = element.text.strip()
        return data

    def convert_to_json(self, output_file):
        data = self.parse_xml()
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
