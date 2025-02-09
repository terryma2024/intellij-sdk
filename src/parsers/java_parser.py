from antlr4 import InputStream, ParseTreeListener, CommonTokenStream, ParseTreeWalker
from loguru import logger
from .Java20Lexer import Java20Lexer
from .Java20Parser import Java20Parser


def setup_java_parser():
    """
    Set up and initialize the ANTLR4 parser for Java.

    Returns:
        None: ANTLR4 doesn't require explicit setup like tree-sitter
    """
    return None


class JavaListener(ParseTreeListener):
    def __init__(self, source):
        self.source = source
        self.class_info = []
        self.class_stack = []
        self.current_class = None
        self.nesting_level = 0

    def enterNormalClassDeclaration(self, ctx):
        # Track nesting level
        self.nesting_level += 1

        # Find the class name
        identifier = None
        logger.debug("Processing normal class declaration...")
        for child in ctx.getChildren():
            logger.debug(f"Child type: {type(child).__name__}, text: {child.getText()}")
            if isinstance(child, Java20Parser.TypeIdentifierContext):
                identifier = child.getText()
                logger.debug(f"Found class identifier: {identifier}")
                break

        if identifier:
            # Push current class to stack before creating new one
            if self.current_class:
                self.class_stack.append(self.current_class)

            # Create new class context
            self.current_class = {"name": identifier, "constants": [], "methods": []}
            logger.debug(f"Created new class context for: {identifier}")

            # Only add top-level classes to class_info immediately
            if self.nesting_level == 1:
                self.class_info.append(self.current_class)
        else:
            logger.debug("No class identifier found")

    def exitNormalClassDeclaration(self, ctx):
        if self.current_class:
            # Only append nested classes to class_info when exiting
            if self.nesting_level > 1:
                self.class_info.append(self.current_class)

            # Restore parent class from stack
            self.current_class = self.class_stack.pop() if self.class_stack else None
        self.nesting_level -= 1

    def enterNormalInterfaceDeclaration(self, ctx):
        # Track nesting level
        self.nesting_level += 1

        # Find the interface name
        identifier = None
        for child in ctx.getChildren():
            if isinstance(child, Java20Parser.TypeIdentifierContext):
                identifier = child.getText()
                break

        if identifier:
            # Push current class to stack before creating new one
            if self.current_class:
                self.class_stack.append(self.current_class)

            # Create new class context
            self.current_class = {"name": identifier, "constants": [], "methods": []}

            # Only add top-level interfaces to class_info immediately
            if self.nesting_level == 1:
                self.class_info.append(self.current_class)
        else:
            logger.debug("No interface identifier found")

    def exitNormalInterfaceDeclaration(self, ctx):
        if self.current_class:
            # Only append nested interfaces to class_info when exiting
            if self.nesting_level > 1:
                self.class_info.append(self.current_class)

            # Restore parent class from stack
            self.current_class = self.class_stack.pop() if self.class_stack else None
        self.nesting_level -= 1

    def enterMethodDeclaration(self, ctx):
        if self.current_class:
            logger.debug(
                f"Processing method declaration in class: {self.current_class['name']}"
            )
            identifier = None

            # First try to find the method identifier directly in the method declarator
            for child in ctx.getChildren():
                if isinstance(child, Java20Parser.MethodHeaderContext):
                    for header_child in child.getChildren():
                        if isinstance(
                            header_child, Java20Parser.MethodDeclaratorContext
                        ):
                            # Get the first identifier that appears before a parenthesis
                            method_text = header_child.getText()
                            method_parts = method_text.split("(")
                            if len(method_parts) > 0:
                                # Extract the method name by taking the last part before the parenthesis
                                # and removing any annotations or type parameters
                                method_name = method_parts[0].strip()
                                # Remove any annotations (starting with @)
                                while "@" in method_name:
                                    method_name = method_name[method_name.find("@") :]
                                    method_name = method_name[
                                        method_name.find(" ") + 1 :
                                    ]
                                # Remove any generic type parameters
                                if "<" in method_name:
                                    method_name = method_name[: method_name.find("<")]
                                # Get the final part which should be the method name
                                identifier = method_name.split()[-1]
                                logger.debug(f"Found method identifier: {identifier}")
                                break
                    if identifier:
                        break

            # Add the method if an identifier was found
            if identifier:
                # Filter out modifiers and annotations
                modifiers_and_annotations = [
                    "public",
                    "private",
                    "protected",
                    "static",
                    "final",
                    "abstract",
                    "synchronized",
                    "native",
                    "strictfp",
                    "default",
                    "transient",
                    "volatile",
                    "class",
                    "interface",
                ]
                if identifier not in modifiers_and_annotations:
                    # Check if method already exists
                    if not any(
                        method["name"] == identifier
                        for method in self.current_class["methods"]
                    ):
                        self.current_class["methods"].append(
                            {"name": identifier, "comment": ""}
                        )
                        logger.debug(
                            f"Added method '{identifier}' to class {self.current_class['name']}"
                        )
            else:
                logger.debug("No method identifier found")

    def enterConstructorDeclaration(self, ctx):
        if self.current_class:
            logger.debug(
                f"Processing constructor declaration in class: {self.current_class['name']}"
            )
            identifier = None
            for child in ctx.getChildren():
                logger.debug(
                    f"Constructor child type: {type(child).__name__}, text: {child.getText()}"
                )
                if isinstance(child, Java20Parser.ConstructorDeclaratorContext):
                    logger.debug("Found constructor declarator")
                    for decl_child in child.getChildren():
                        logger.debug(
                            f"Declarator child type: {type(decl_child).__name__}, text: {decl_child.getText()}"
                        )
                        if isinstance(decl_child, Java20Parser.TypeIdentifierContext):
                            identifier = decl_child.getText()
                            logger.debug(f"Found constructor identifier: {identifier}")
                            break
                    if identifier:
                        break

            if identifier:
                self.current_class["methods"].append(
                    {"name": identifier, "comment": ""}
                )
                logger.debug(
                    f"Added constructor '{identifier}' to class {self.current_class['name']}"
                )
            else:
                logger.debug("No constructor identifier found")

    def enterInterfaceMethodDeclaration(self, ctx):
        if self.current_class:
            logger.debug(
                f"Processing interface method declaration in: {self.current_class['name']}"
            )
            identifier = None
            for child in ctx.getChildren():
                logger.debug(
                    f"Interface method child type: {type(child).__name__}, text: {child.getText()}"
                )
                if isinstance(child, Java20Parser.InterfaceMethodModifierContext):
                    logger.debug("Found interface method modifier")
                elif isinstance(child, Java20Parser.MethodHeaderContext):
                    logger.debug("Found method header")
                    for header_child in child.getChildren():
                        logger.debug(
                            f"Header child type: {type(header_child).__name__}, text: {header_child.getText()}"
                        )
                        if isinstance(
                            header_child, Java20Parser.MethodDeclaratorContext
                        ):
                            logger.debug("Found method declarator")
                            for method_child in header_child.getChildren():
                                logger.debug(
                                    f"Declarator child type: {type(method_child).__name__}, text: {method_child.getText()}"
                                )
                                if isinstance(
                                    method_child, Java20Parser.IdentifierContext
                                ):
                                    identifier = method_child.getText()
                                    logger.debug(
                                        f"Found interface method identifier: {identifier}"
                                    )
                                    break
                            if identifier:
                                break
                    if identifier:
                        break

            if identifier:
                self.current_class["methods"].append(
                    {"name": identifier, "comment": ""}
                )
                logger.debug(
                    f"Added interface method '{identifier}' to interface {self.current_class['name']}"
                )
            else:
                logger.debug("No interface method identifier found")


def parse_java_file(content, parser=None):
    """
    Parse Java source code and extract class information using ANTLR4.

    Args:
        content (str): The content of the Java source file.
        parser (None): Not used in ANTLR4 implementation.

    Returns:
        list: A list of dictionaries containing class information.
    """
    try:
        # Create the lexer and stream
        input_stream = InputStream(content)
        lexer = Java20Lexer(input_stream)
        stream = CommonTokenStream(lexer)

        # Create the parser
        parser = Java20Parser(stream)
        tree = parser.compilationUnit()

        # Create and run the listener
        listener = JavaListener(content)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.class_info
    except Exception as e:
        logger.error(f"Error parsing Java file: {e}")
        return []
