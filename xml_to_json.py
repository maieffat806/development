import xml.etree.ElementTree as ET
import json

# convert element to dict
def element_to_dict(element):
    node = {}
    
    # add attribute
    if element.attrib:
        node["attributes"] = element.attrib
    # add text if exists
    if element.text and element.text.strip():
        node["text"] = element.text.strip()
    # add children
    for child in element:
        child_dict = element_to_dict(child)
        if child.tag not in node:
            node[child.tag] = child_dict
        else:
            # handle multiple children with same tag
            if isinstance(node[child.tag], list):
                node[child.tag].append(child_dict)
            else:
                node[child.tag] = [node[child.tag], child_dict]
    
    return node
# read xml file
tree = ET.parse("SOUND_Short_eHorizon_Pdu.arxml")
root = tree.getroot()
# convert to dict
xml_dict = {root.tag: element_to_dict(root)}
# save in json file
with open("filename_updated.json", "w", encoding="utf-8") as f:
    json.dump(xml_dict, f, indent=4)


