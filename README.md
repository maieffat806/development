# XML Attribute Editor

A Python script to modify XML element attributes with commands to add, edit, or delete attributes.

---
## Features

- Add a new attribute to an XML element.
- Edit the value of an existing attribute.
- Delete an attribute from an element.

---

## Requirements

- Python 3.x

---

## Usage

```bash
python main.py <input_file> --tag TAG_NAME --command COMMAND --attr_name ATTR_NAME [--attr_value ATTR_VALUE] -- <output file>

```

---

## XML to JSON Converter

This Python script converts an XML file into a JSON file by recursively transforming XML elements into nested dictionaries.

## Features

- Converts XML attributes to JSON under the key `"@attributes"`.
- Converts XML element text content to JSON under the key `"#text"`.
- Handles nested child elements.
- Repeated child elements with the same tag are converted into JSON arrays (lists).
- Saves the output as a pretty-printed JSON file.

## Usage

1. Place your XML file (e.g., `SOUND_Short_eHorizon_Pdu.arxml`) in the script directory.

