from antlr4 import InputStream, ParseTreeListener, CommonTokenStream, ParseTreeWalker
from loguru import logger
from .KotlinLexer import KotlinLexer
from .KotlinParser import KotlinParser


def setup_kotlin_parser():
    """
    Set up and initialize the ANTLR4 parser for Kotlin.

    Returns:
        None: ANTLR4 doesn't require explicit setup like tree-sitter
    """
    return None


class KotlinListener(ParseTreeListener):
    def __init__(self, source):
        self.source = source
        self.class_info = []
        self.current_class = None
        self.nesting_level = 0

    def enterClassDeclaration(self, ctx):
        # Track nesting level
        self.nesting_level += 1

        # Look for class or interface declaration
        found_type = False
        is_interface = False
        is_data_class = False
        class_name = None
        annotations = []

        # First pass: collect annotations from ModifierList
        for child in ctx.getChildren():
            if isinstance(child, KotlinParser.ModifierListContext):
                for modifier in child.getChildren():
                    if isinstance(modifier, KotlinParser.AnnotationsContext):
                        # Extract annotation name directly from modifier text
                        annotation = modifier.getText().strip("@")
                        annotations.append(annotation)
                    elif modifier.getText() == "data":
                        # Mark as data class if data modifier is found
                        is_data_class = True

        # Second pass: find class type and name
        for child in ctx.getChildren():
            text = child.getText()
            if text in ["class", "interface"]:
                found_type = True
                is_interface = text == "interface"
                continue
            if found_type and isinstance(child, KotlinParser.SimpleIdentifierContext):
                class_name = child.getText()
                break

        if class_name and self.nesting_level == 1:
            # For nested classes, we want to capture their methods too
            # but only store them in the top-level class
            self.current_class = {
                "name": class_name,
                "constants": [],
                "methods": [],
                "companion_objects": [],
                "properties": [],
                "annotations": annotations,
                "is_enum": False,
                "is_interface": is_interface,
                "is_data_class": is_data_class,
                "enum_values": [],
            }
            logger.debug(
                f"Created new {'interface' if is_interface else 'class'}: {class_name}"
            )

    def enterClassParameter(self, ctx):
        if self.current_class and self.current_class.get("is_data_class"):
            # Look for parameter name in class constructor
            name = None
            is_private = False

            # Check modifiers first
            for child in ctx.getChildren():
                if isinstance(child, KotlinParser.ModifierListContext):
                    for modifier in child.getChildren():
                        if modifier.getText() == "private":
                            is_private = True
                            break
                elif isinstance(child, KotlinParser.SimpleIdentifierContext):
                    name = child.getText()
                    break

            if name and not is_private:
                # Add as property for data class parameters
                self.current_class["properties"].append({"name": name, "comment": ""})
                logger.debug(
                    f"Added data class parameter '{name}' as property to class {self.current_class['name']}"
                )

    def enterEnumClassBody(self, ctx):
        if self.current_class:
            self.current_class["is_enum"] = True
            logger.debug(f"Marked class {self.current_class['name']} as enum class")

    def enterEnumEntry(self, ctx):
        if self.current_class and self.current_class["is_enum"]:
            # Look for enum entry name
            for child in ctx.getChildren():
                if isinstance(child, KotlinParser.SimpleIdentifierContext):
                    # Found an enum entry name
                    self.current_class["enum_values"].append(
                        {"name": child.getText(), "comment": ""}
                    )
                    logger.debug(
                        f"Added enum value '{child.getText()}' to enum class {self.current_class['name']}"
                    )
                    break

    def enterCompanionObject(self, ctx):
        if self.current_class:
            # Look for companion object name
            name = None
            for child in ctx.getChildren():
                text = child.getText()
                if text not in ["companion", "object"] and not text.startswith("@"):
                    name = text
                    break

            # If no explicit name is found, use default name "Companion"
            if not name:
                name = "Companion"

            # Add companion object to current class
            self.current_class["companion_objects"].append(
                {"name": name, "comment": ""}
            )
            logger.debug(
                f"Added companion object '{name}' to class {self.current_class['name']}"
            )

    def exitClassDeclaration(self, ctx):
        if self.nesting_level == 1 and self.current_class:
            self.class_info.append(self.current_class)
            self.current_class = None
        self.nesting_level -= 1

    def enterPropertyDeclaration(self, ctx):
        if self.current_class:
            # Check if this property is directly under class body
            parent = ctx.parentCtx
            while parent is not None:
                if isinstance(parent, KotlinParser.BlockContext):
                    # If we find a block before class body, this is a local property
                    return
                if isinstance(parent, KotlinParser.ClassBodyContext):
                    # Found class body, this is a class-level property
                    break
                parent = parent.parentCtx

            # If we didn't find class body, this is not a class-level property
            if not isinstance(parent, KotlinParser.ClassBodyContext):
                return

            is_const = False
            is_val = False
            is_private = False
            name = None
            for child in ctx.getChildren():
                text = child.getText()
                if isinstance(child, KotlinParser.ModifierListContext):
                    for modifier_child in child.getChildren():
                        modifier_text = modifier_child.getText()
                        if modifier_text == "private":
                            is_private = True
                        elif modifier_text == "const":
                            is_const = True
                elif text in ["var", "val"]:
                    is_val = True
                else:
                    # Look for the property name
                    for sibling in ctx.getChildren():
                        if isinstance(sibling, KotlinParser.VariableDeclarationContext):
                            for sibling_child in sibling.getChildren():
                                if isinstance(
                                    sibling_child,
                                    KotlinParser.SimpleIdentifierContext,
                                ):
                                    name = sibling_child.getText()
                                    break
                            break
                    if name:
                        break
            if name and not is_private:
                if is_const:
                    self.current_class["constants"].append(
                        {"name": name, "comment": ""}
                    )
                elif is_val:
                    self.current_class["properties"].append(
                        {"name": name, "comment": ""}
                    )

    def enterFunctionDeclaration(self, ctx):
        if self.current_class:
            # Collect all child nodes first
            children = list(ctx.getChildren())
            found_fun = False
            name = None
            receiver_type = None

            logger.debug(
                f"Processing function declaration in class {self.current_class['name']}"
            )
            logger.debug(f"Total children nodes: {len(children)}")

            for i, child in enumerate(children):
                text = child.getText()
                logger.debug(f"Processing node {i}: '{text}'")

                if text == "fun":
                    found_fun = True
                    logger.debug("Found 'fun' keyword")
                    continue

                if found_fun:
                    # Skip annotations and modifiers
                    if text.startswith("@") or text in [
                        "private",
                        "public",
                        "protected",
                        "internal",
                    ]:
                        logger.debug(f"Skipping modifier/annotation: {text}")
                        continue

                    # Skip generic type parameters
                    if text.startswith("<"):
                        logger.debug(f"Skipping generic parameter: {text}")
                        continue

                    # Look for receiver type and function name
                    if not name:
                        # Check for extension function pattern
                        next_text = (
                            children[i + 1].getText() if i + 1 < len(children) else ""
                        )
                        next_next_text = (
                            children[i + 2].getText() if i + 2 < len(children) else ""
                        )
                        logger.debug(
                            f"Checking for extension function. Current text: '{text}', Next text: '{next_text}', Next next text: '{next_next_text}'"
                        )

                        if "." in text or (text and next_text == "."):
                            # This is an extension function
                            if "." in text:
                                parts = text.split(".")
                                receiver_type = parts[0]
                                if next_text and not next_text.startswith("("):
                                    name = next_text
                            else:
                                receiver_type = text
                                if next_next_text and not next_next_text.startswith(
                                    "("
                                ):
                                    name = next_next_text

                            if name:
                                logger.debug(
                                    f"Found extension function - Receiver: {receiver_type}, Name: {name}"
                                )
                                break
                        elif (
                            not text.startswith("(")
                            and not text.startswith("<")
                            and not text.startswith("@")
                            and text not in ["fun", ":"]
                        ):
                            name = text
                            logger.debug(f"Found regular function name: {name}")
                            break

            if name:
                logger.debug(
                    f"Adding method '{name}' to class {self.current_class['name']}"
                )
                self.current_class["methods"].append({"name": name, "comment": ""})
            else:
                logger.debug("No function name found in this declaration")


def parse_kotlin_file(content, parser=None):
    """
    Parse Kotlin source code and extract class information using ANTLR4.

    Args:
        content (str): The content of the Kotlin source file.
        parser (None): Not used in ANTLR4 implementation.

    Returns:
        list: A list of dictionaries containing class information.
    """
    try:
        # Create the lexer and stream
        input_stream = InputStream(content)
        lexer = KotlinLexer(input_stream)
        stream = CommonTokenStream(lexer)

        # Create the parser
        parser = KotlinParser(stream)
        tree = parser.kotlinFile()

        # Create and run the listener
        listener = KotlinListener(content)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.class_info
    except Exception as e:
        logger.error(f"Error parsing Kotlin file: {e}")
        return []
