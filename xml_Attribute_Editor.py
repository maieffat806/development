import xml.etree.ElementTree as ET


class ARXMLAttributeEditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    def _find_elements_recursive(self, element, tag, found=None):
        if found is None:
            found = []
        if tag in element.tag:
            found.append(element)
        for child in element:
            self._find_elements_recursive(child, tag, found)
        return found

    def find_elements(self, tag):

        return self._find_elements_recursive(self.root, tag)

    def add_attribute(self, element_tag, attribute_name, attribute_value):
        elements = self.find_elements(element_tag)
        if not elements:
            print(f"Error: No elements found with tag '{element_tag}'")
            return

        for elem in elements:
            if attribute_name in elem.attrib:
                print(
                    f"Skipped: Attribute '{attribute_name}' already exists in element '{elem.tag}'"
                )
            else:
                elem.set(attribute_name, attribute_value)
                print(
                    f"Added: Attribute '{attribute_name}'='{attribute_value}' to element '{elem.tag}'"
                )

    def edit_attribute(self, element_tag, attribute_name, new_value):
        elements = self.find_elements(element_tag)
        if not elements:
            print(f"Error: No elements found with tag '{element_tag}'")
            return

        for elem in elements:
            if attribute_name not in elem.attrib:
                print(
                    f"Skipped: Attribute '{attribute_name}' not found in element '{elem.tag}'"
                )
            else:
                old_value = elem.attrib[attribute_name]
                elem.set(attribute_name, new_value)
                print(
                    f"Edited: Attribute '{attribute_name}' in element '{elem.tag}' from '{old_value}' to '{new_value}'"
                )

    def delete_attribute(self, element_tag, attribute_name):
        elements = self.find_elements(element_tag)
        if not elements:
            print(f"Error: No elements found with tag '{element_tag}'")
            return

        for elem in elements:
            if attribute_name in elem.attrib:
                del elem.attrib[attribute_name]
                print(
                    f"Deleted: Attribute '{attribute_name}' from element '{elem.tag}'"
                )
            else:
                print(
                    f"Skipped: Attribute '{attribute_name}' not found in element '{elem.tag}'"
                )

    def save(self, output_file=None):
        if output_file is None:
            output_file = self.file_path
        self.tree.write(output_file, encoding="utf-8", xml_declaration=True)
