import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
import argparse
import sys

class XmlAttributeCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddAttributeCommand(XmlAttributeCommand):
    def __init__(self, element: ET.Element, attr_name: str, attr_value: str):
        self.element = element
        self.attr_name = attr_name
        self.attr_value = attr_value

    def execute(self):
        if self.attr_name in self.element.attrib:
            raise KeyError(f"Attribute '{self.attr_name}' already exists.")
        self.element.set(self.attr_name, self.attr_value)

class EditAttributeCommand(XmlAttributeCommand):
    def __init__(self, element: ET.Element, attr_name: str, new_value: str):
        self.element = element
        self.attr_name = attr_name
        self.new_value = new_value

    def execute(self):
        if self.attr_name not in self.element.attrib:
            raise KeyError(f"Attribute '{self.attr_name}' does not exist to edit.")
        self.element.set(self.attr_name, self.new_value)

class DeleteAttributeCommand(XmlAttributeCommand):
    def __init__(self, element: ET.Element, attr_name: str):
        self.element = element
        self.attr_name = attr_name

    def execute(self):
        if self.attr_name not in self.element.attrib:
            raise KeyError(f"Attribute '{self.attr_name}' does not exist to delete.")
        del self.element.attrib[self.attr_name]

class XmlEditor:
    def __init__(self, file_path: str):
        try:
            self.tree = ET.parse(file_path)
            self.root = self.tree.getroot()
            self.file_path = file_path
            self.remove_namespaces()  # <-- إزالة namespaces بعد تحميل الملف
        except ET.ParseError as e:
            raise RuntimeError(f"Failed to parse XML file '{file_path}': {e}")
        except FileNotFoundError:
            raise RuntimeError(f"File '{file_path}' not found.")

    def remove_namespaces(self):
        for elem in self.root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]

    def find_element(self, tag: str, attrib_key=None, attrib_value=None):
        for elem in self.root.iter(tag):
            if attrib_key is None:
                return elem
            elif elem.get(attrib_key) == attrib_value:
                return elem
        return None

    def execute_command(self, command: XmlAttributeCommand):
        command.execute()

    def save(self, new_file_path=None):
        path = new_file_path if new_file_path else self.file_path
        self.tree.write(path, encoding='utf-8', xml_declaration=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Edit XML attributes using commands (add, edit, delete).")

    parser.add_argument("input_file", help="Path to the input XML file.")
    parser.add_argument("output_file", nargs='?', default=None, help="Path to save the modified XML file. Defaults to overwriting input file.")

    parser.add_argument("--tag", required=True, help="Element tag to find.")
    parser.add_argument("--filter_key", help="Attribute key to filter element.")
    parser.add_argument("--filter_value", help="Attribute value to filter element.")

    parser.add_argument("--command", choices=["add", "edit", "delete"], required=True, help="Command to execute on attribute.")
    parser.add_argument("--attr_name", required=True, help="Attribute name to add/edit/delete.")
    parser.add_argument("--attr_value", help="Attribute value to add or edit. Required for add and edit commands.")

    return parser.parse_args()

def main():
    args = parse_args()

    # Validate attr_value presence for add/edit
    if args.command in ("add", "edit") and not args.attr_value:
        print(f"Error: --attr_value is required for '{args.command}' command.")
        sys.exit(1)

    try:
        editor = XmlEditor(args.input_file)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    elem = editor.find_element(args.tag, args.filter_key, args.filter_value)
    if elem is None:
        print(f"Error: Element with tag '{args.tag}'", end='')
        if args.filter_key and args.filter_value:
            print(f" and attribute [{args.filter_key}='{args.filter_value}']", end='')
        print(" not found.")
        sys.exit(1)

    try:
        if args.command == "add":
            cmd = AddAttributeCommand(elem, args.attr_name, args.attr_value)
        elif args.command == "edit":
            cmd = EditAttributeCommand(elem, args.attr_name, args.attr_value)
        elif args.command == "delete":
            cmd = DeleteAttributeCommand(elem, args.attr_name)
        else:
            print("Invalid command.")
            sys.exit(1)

        editor.execute_command(cmd)
    except KeyError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        editor.save(args.output_file)
    except Exception as e:
        print(f"Error saving file: {e}")
        sys.exit(1)

    print(f"Success! File saved to '{args.output_file or args.input_file}'")

if __name__ == "__main__":
    main()