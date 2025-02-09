import javalang


def parse_java_file(content):
    """
    Parse Java source code and extract class information.

    Args:
        content (str): The content of the Java source file.

    Returns:
        list: A list of dictionaries containing class information.
    """
    try:
        tree = javalang.parse.parse(content)
        class_info = []

        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            class_data = {"name": node.name, "constants": [], "methods": []}

            # Extract constants (fields with final modifier)
            for field in node.fields:
                if "final" in field.modifiers:
                    for declarator in field.declarators:
                        class_data["constants"].append(
                            {
                                "name": declarator.name,
                                "comment": field.documentation or "",
                            }
                        )

            # Extract methods
            for method in node.methods:
                class_data["methods"].append(
                    {"name": method.name, "comment": method.documentation or ""}
                )

            class_info.append(class_data)
        return class_info
    except Exception as e:
        print(f"Error parsing Java file: {e}")
        return []
