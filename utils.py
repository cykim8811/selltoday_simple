import xml.etree.ElementTree as ET


import random
CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
used_ids = set()

class IdGenerator:
    def __init__(self):
        self.used_ids = set()
        self.last_id = {}
    
    def generate_id(self, element):
        tagname = element.tag.split('}')[-1]
        if tagname not in self.last_id:
            self.last_id[tagname] = 0
        self.last_id[tagname] += 1
        return f"{tagname}_{self.last_id[tagname]}"

def svg_to_json(svg_data):
    # Parse the SVG file
    # tree = ET.parse(svg_path)
    tree = ET.ElementTree(ET.fromstring(svg_data))
    root = tree.getroot()

    raw_strings = {}

    id_generator = IdGenerator()

    # Recursive function to process each element and its children
    def process_element(element):
        element_id = id_generator.generate_id(element)  # Generate a unique ID for each element
        # Set uuid to 0 if tag is svg
        if element.tag.split('}')[-1] == 'svg':
            element_id = "0"


        def toCamel(propName):  # Convert attribute names to camelCase
            if propName == 'class':
                return 'className'
            if propName.startswith('data-'):
                return propName
            return ''.join([word if i == 0 else word.capitalize() for i, word in enumerate(propName.split('-'))])
        
        # Element data to be returned
        element_data = {
            "id": element_id,  # Add the generated or existing ID
            "tag": element.tag.split('}')[-1],  # Clean up namespace if present
            "props": {toCamel(k.split('}')[-1]): v for k, v in element.attrib.items()},  # Clean up namespace in attributes
            "children": []
        }

        if 'style' in element_data['props']:
            element_data['props']['style'] = {toCamel(k): v for k, v in [prop.split(':') for prop in element_data['props']['style'].split(';') if prop]}

        # Process children if they exist
        if element.text and element.text.strip():
            text_id = id_generator.generate_id(element)
            raw_strings[text_id] = element.text
            element_data['children'].append(text_id)

        for child in element:
            child_data, child_id = process_element(child)  # Unpack the returned tuple
            element_data['children'].append(child_id)
            elements[child_id] = child_data
            if child.tail and child.tail.strip():
                text_id = id_generator.generate_id(child)
                raw_strings[text_id] = child.tail
                element_data['children'].append(text_id)

        return element_data, element_id

    # Initialize dictionary to hold all elements
    elements = {}

    # Start processing from root
    root_data, root_id = process_element(root)
    elements[root_id] = root_data

    # Add raw strings to the final JSON
    elements.update(raw_strings)

    # Final JSON structure
    json_data = {
        "elements": elements
    }

    return json_data

def json_to_svg(json_data):
    # Recursive function to convert JSON data to SVG
    elements = json_data['elements']
    
    def process_node(element_id):
        if type(elements[element_id]) == str:
            return elements[element_id]
        element_data = elements[element_id]
        element_tag = element_data['tag']
        element_props = element_data['props']
        element_children = element_data['children']

        res = f"<{element_tag} "
        element_props["data-idx"] = element_id
        for prop, value in element_props.items():
            prop = prop.replace('className', 'class')
            if prop == 'style':
                res += f"{prop}='"
                for style_prop, style_value in value.items():
                    res += f"{style_prop}: {style_value};"
                res += "' "
            else:
                res += f"{prop}='{value}' "
        res += ">"
        for child in element_children:
            res += process_node(child)
        res += f"</{element_tag}>"
        return res
    
    svg_data = process_node('0')
    svg_data = svg_data.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" ')
    return svg_data

def generate_filler(json_data):
    filler = "\ndef filler(view, data):\n    \n"
    for element_id, element_data in json_data['elements'].items():
        if type(element_data) == str:
            continue
        if element_data['tag'] == 'text' or element_data['tag'] == 'tspan':
            child = element_data['children'][0]
            text_data = json_data['elements'][child]
            filler += f"    view.elements['{child}'] = '{text_data}'\n"
        if element_data['tag'] == 'image':
            href = element_data['props']['href']
            filler += f"    view.elements['{element_id}'].props.href = '{href}'\n"
    filler += "    \n    return view\n"
    return filler