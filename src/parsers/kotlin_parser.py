from antlr4 import InputStream, ParseTreeListener, CommonTokenStream, ParseTreeWalker
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

        found_class = False
        for child in ctx.getChildren():
            text = child.getText()
            if text == "class":
                found_class = True
                continue
            if found_class and not text.startswith("<") and not text.startswith("@"):
                # For nested classes, we want to capture their methods too
                # but only store them in the top-level class
                if self.nesting_level == 1:
                    self.current_class = {
                        "name": text,
                        "constants": [],
                        "methods": [],
                    }
                break

    def exitClassDeclaration(self, ctx):
        if self.nesting_level == 1 and self.current_class:
            self.class_info.append(self.current_class)
            self.current_class = None
        self.nesting_level -= 1

    def enterPropertyDeclaration(self, ctx):
        if self.current_class:
            is_const = False
            name = None
            for child in ctx.getChildren():
                if child.getText() == "const":
                    is_const = True
                elif child.getText() == "val" and is_const:
                    for sibling in ctx.getChildren():
                        if sibling.getText() not in ["const", "val", "="]:
                            name = sibling.getText()
                            break

            if is_const and name:
                self.current_class["constants"].append({"name": name, "comment": ""})

    def enterFunctionDeclaration(self, ctx):
        if self.current_class:
            # Collect all child nodes first
            children = list(ctx.getChildren())
            found_fun = False
            name = None
            receiver_type = None

            print(
                f"Processing function declaration in class {self.current_class['name']}"
            )
            print(f"Total children nodes: {len(children)}")

            for i, child in enumerate(children):
                text = child.getText()
                print(f"Processing node {i}: '{text}'")

                if text == "fun":
                    found_fun = True
                    print("Found 'fun' keyword")
                    continue

                if found_fun:
                    # Skip annotations and modifiers
                    if text.startswith("@") or text in [
                        "private",
                        "public",
                        "protected",
                        "internal",
                    ]:
                        print(f"Skipping modifier/annotation: {text}")
                        continue

                    # Skip generic type parameters
                    if text.startswith("<"):
                        print(f"Skipping generic parameter: {text}")
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
                        print(
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
                                print(
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
                            print(f"Found regular function name: {name}")
                            break

            if name:
                print(f"Adding method '{name}' to class {self.current_class['name']}")
                self.current_class["methods"].append({"name": name, "comment": ""})
            else:
                print("No function name found in this declaration")


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
        print(f"Error parsing Kotlin file: {e}")
        return []
