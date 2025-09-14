# XML Attribute Editor

This Python script allows you to **add, edit, and delete attributes** in an XML file.

It uses the built-in `xml.etree.ElementTree` module to handle XML files.

---

## Code Summary

- **XmlAttributeCommand**:  
  Abstract base class (interface) for attribute commands.

- **AddAttributeCommand**:  
  Adds a new attribute to an XML element.

- **EditAttributeCommand**:  
  Modifies an existing attribute’s value.

- **DeleteAttributeCommand**:  
  Removes an attribute from an XML element.

- **XmlEditor**:  
  Handles loading the XML file, executing attribute commands, and saving the updated XML file.

---
# XML to JSON Converter

This Python script converts an XML file into a JSON file by recursively transforming XML elements into nested dictionaries.

## Features

- Converts XML attributes to JSON under the key `"@attributes"`.
- Converts XML element text content to JSON under the key `"#text"`.
- Handles nested child elements.
- Repeated child elements with the same tag are converted into JSON arrays (lists).
- Saves the output as a pretty-printed JSON file.

## Usage

1. Place your XML file (e.g., `Autosar.arxml`) in the script directory.

2. Run the script:

   ```bash
   python xml_to_json.py
