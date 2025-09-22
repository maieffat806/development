import argparse
import sys
from xml_Attribute_Editor import ARXMLAttributeEditor
from xml_to_json import XMLtoJSONConverter

OUTPUT_FILE = "SOUND_Short_eHorizon_Pdu_updated.xml"

def parse_args():
    parser = argparse.ArgumentParser(description="ARXML Attribute Editor")
    parser.add_argument("input_file", help="Path to the input ARXML file")
    parser.add_argument("--tag", required=True, help="Element tag to find")
    parser.add_argument("--command", choices=["add", "edit", "delete"], required=True)
    parser.add_argument("--attr_name", required=True, help="Attribute name")
    parser.add_argument("--attr_value", help="Attribute value (required for add/edit)")
    parser.add_argument("--output", default=OUTPUT_FILE, help=f"Output file path (default: {OUTPUT_FILE})")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.command in ("add", "edit") and not args.attr_value:
        print(f"Error: --attr_value required for '{args.command}'")
        sys.exit(1)

    try:
        editor = ARXMLAttributeEditor(args.input_file)

        if args.command == "add":
            editor.add_attribute(args.tag, args.attr_name, args.attr_value)
        elif args.command == "edit":
            editor.edit_attribute(args.tag, args.attr_name, args.attr_value)
        elif args.command == "delete":
            editor.delete_attribute(args.tag, args.attr_name)
        else:
            print(f"Error: Unknown command '{args.command}'")
            sys.exit(1)

        # Save ARXML
        output_file = args.output if args.output else OUTPUT_FILE
        editor.save(output_file)
        print(f" Success! Saved to {output_file}")

        # Convert to JSON
        json_output_file = output_file.replace(".xml", ".json")
        converter = XMLtoJSONConverter(output_file)
        converter.convert_to_json(json_output_file)
        print(f" JSON saved to {json_output_file}")

    except Exception as e:
        print(f"Error editing XML: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
