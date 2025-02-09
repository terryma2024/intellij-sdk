from antlr4 import InputStream, ParseTreeListener, CommonTokenStream, ParseTreeWalker
from antlr4.error.DiagnosticErrorListener import DiagnosticErrorListener
from antlr4.Token import Token
from loguru import logger
from .JavaLexer import JavaLexer
from .JavaParser import JavaParser


def setup_java_parser():
    """
    Set up and initialize the ANTLR4 parser for Java.

    Returns:
        None: ANTLR4 doesn't require explicit setup like tree-sitter
    """
    return None


class JavaListener(ParseTreeListener):
    def __init__(self, source, comments):
        self.source = source
        self.class_info = []
        self.class_stack = []
        self.current_class = None
        self.nesting_level = 0
        self.current_comment = ""
        self.last_processed_line = -1
        self.comments = comments
        logger.debug("Initialized JavaListener")

    def find_nearest_comment(self, target_line):
        # Search for comments between last processed line and current target line
        nearest_comment = None
        for comment, line in reversed(self.comments):
            if self.last_processed_line < line < target_line:
                # Clean up the comment by removing comment markers
                cleaned_comment = comment
                # Remove multi-line comment markers
                if cleaned_comment.startswith("/*") and cleaned_comment.endswith("*/"):
                    cleaned_comment = cleaned_comment[2:-2].strip()
                # Remove single-line comment markers
                elif cleaned_comment.startswith("//"):
                    cleaned_comment = cleaned_comment[2:].strip()
                nearest_comment = cleaned_comment
                break
        # Update last processed line
        self.last_processed_line = target_line
        return nearest_comment or "No Comment"

    def enterClassDeclaration(self, ctx):
        logger.debug("Entering class declaration")
        # Process the class declaration directly
        self.nesting_level += 1

        # Find the class name
        identifier = None
        for child in ctx.getChildren():
            if isinstance(
                child, (JavaParser.TypeIdentifierContext, JavaParser.IdentifierContext)
            ):
                text = child.getText()
                # Skip if the text is a Java keyword or starts with @ (annotation)
                if not text.startswith("@") and text not in [
                    "class",
                    "interface",
                    "enum",
                ]:
                    identifier = text
                    logger.debug(f"Found class identifier: {identifier}")
                    break

        if identifier:
            # Push current class to stack before creating new one
            if self.current_class:
                self.class_stack.append(self.current_class)

            # Create new class context
            self.current_class = {
                "name": identifier,
                "constants": [],
                "methods": [],
                "comment": self.find_nearest_comment(ctx.start.line),
            }
            logger.debug(f"Created new class context for: {identifier}")

            # Add class to class_info immediately
            self.class_info.append(self.current_class)
        else:
            logger.debug("No class identifier found")

    def exitClassDeclaration(self, ctx):
        if self.current_class:
            # Restore parent class from stack
            self.current_class = self.class_stack.pop() if self.class_stack else None
        self.nesting_level -= 1

    def enterEnumDeclaration(self, ctx):
        # Track nesting level
        self.nesting_level += 1

        # Find the enum name
        identifier = None
        for child in ctx.getChildren():
            if isinstance(
                child, (JavaParser.TypeIdentifierContext, JavaParser.IdentifierContext)
            ):
                text = child.getText()
                # Skip if the text is a Java keyword or starts with @ (annotation)
                if not text.startswith("@") and text not in [
                    "class",
                    "interface",
                    "enum",
                ]:
                    identifier = text
                    logger.debug(f"Found enum identifier: {identifier}")
                    break

        if identifier:
            # Push current class to stack before creating new one
            if self.current_class:
                self.class_stack.append(self.current_class)

            # Create new class context
            self.current_class = {
                "name": identifier,
                "constants": [],
                "methods": [],
                "comment": self.find_nearest_comment(ctx.start.line),
            }

            # Only add top-level enums to class_info immediately
            if self.nesting_level == 1:
                self.class_info.append(self.current_class)
        else:
            logger.debug("No enum identifier found")

    def exitEnumDeclaration(self, ctx):
        if self.current_class:
            # Only append nested enums to class_info when exiting
            if self.nesting_level > 1:
                self.class_info.append(self.current_class)

            # Restore parent class from stack
            self.current_class = self.class_stack.pop() if self.class_stack else None
        self.nesting_level -= 1

    def enterNormalClassDeclaration(self, ctx):
        # Track nesting level
        self.nesting_level += 1

        # Find the class name
        identifier = None
        logger.debug("Processing normal class declaration...")
        for child in ctx.getChildren():
            logger.debug(f"Child type: {type(child).__name__}, text: {child.getText()}")
            # Look for both TypeIdentifier and Identifier contexts since class names can appear in either
            if isinstance(
                child, (JavaParser.TypeIdentifierContext, JavaParser.IdentifierContext)
            ):
                text = child.getText()
                # Skip if the text is a Java keyword or starts with @ (annotation)
                if not text.startswith("@") and text not in [
                    "class",
                    "interface",
                    "enum",
                ]:
                    identifier = text
                    logger.debug(f"Found class identifier: {identifier}")
                    break

        if identifier:
            # Push current class to stack before creating new one
            if self.current_class:
                self.class_stack.append(self.current_class)

            # Create new class context
            self.current_class = {
                "name": identifier,
                "constants": [],
                "methods": [],
                "comment": self.find_nearest_comment(ctx.start.line),
            }
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

    def enterInterfaceDeclaration(self, ctx):
        # Track nesting level
        self.nesting_level += 1

        # Find the interface name
        identifier = None
        for child in ctx.getChildren():
            if isinstance(
                child, (JavaParser.TypeIdentifierContext, JavaParser.IdentifierContext)
            ):
                text = child.getText()
                # Skip if the text is a Java keyword or starts with @ (annotation)
                if not text.startswith("@") and text not in [
                    "class",
                    "interface",
                    "enum",
                ]:
                    identifier = text
                    logger.debug(f"Found interface identifier: {identifier}")
                    break

        if identifier:
            # Push current class to stack before creating new one
            if self.current_class:
                self.class_stack.append(self.current_class)

            # Create new class context
            self.current_class = {
                "name": identifier,
                "constants": [],
                "methods": [],
                "comment": self.find_nearest_comment(ctx.start.line),
            }
            logger.debug(f"Created new interface context for: {identifier}")

            # Add interface to class_info immediately
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

            # Look for the method identifier in the children
            for child in ctx.getChildren():
                if isinstance(
                    child,
                    (JavaParser.TypeIdentifierContext, JavaParser.IdentifierContext),
                ):
                    text = child.getText()
                    # Skip if the text is a Java keyword or starts with @ (annotation)
                    if not text.startswith("@") and text not in [
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
                    ]:
                        identifier = text
                        logger.debug(f"Found method identifier: {identifier}")
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
                            {
                                "name": identifier,
                                "comment": self.find_nearest_comment(ctx.start.line),
                            }
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
                if isinstance(child, JavaParser.ConstructorDeclarationContext):
                    logger.debug("Found constructor declarator")
                    for decl_child in child.getChildren():
                        logger.debug(
                            f"Declarator child type: {type(decl_child).__name__}, text: {decl_child.getText()}"
                        )
                        if isinstance(decl_child, JavaParser.TypeIdentifierContext):
                            identifier = decl_child.getText()
                            logger.debug(f"Found constructor identifier: {identifier}")
                            break
                    if identifier:
                        break

            if identifier:
                self.current_class["methods"].append(
                    {
                        "name": identifier,
                        "comment": self.find_nearest_comment(ctx.start.line),
                    }
                )
                logger.debug(
                    f"Added constructor '{identifier}' to class {self.current_class['name']}"
                )
            else:
                logger.debug("No constructor identifier found")

    def enterInterfaceCommonBodyDeclaration(self, ctx):
        if self.current_class:
            logger.debug(
                f"Processing interface method declaration in: {self.current_class['name']}"
            )
            identifier = None

            # Look for the method identifier in the children
            for child in ctx.getChildren():
                if isinstance(child, JavaParser.IdentifierContext):
                    text = child.getText()
                    # Skip if the text is a Java keyword or starts with @ (annotation)
                    if not text.startswith("@") and text not in [
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
                        "void",
                        "class",
                        "interface",
                        "double",
                        "int",
                        "boolean",
                        "char",
                        "byte",
                        "short",
                        "long",
                        "float",
                    ]:
                        identifier = text
                        logger.debug(f"Found interface method identifier: {identifier}")
                        break

            if identifier:
                self.current_class["methods"].append(
                    {
                        "name": identifier,
                        "comment": self.find_nearest_comment(ctx.start.line),
                    }
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
        lexer = JavaLexer(input_stream)
        stream = CommonTokenStream(lexer)

        # Create the parser with diagnostic logging
        parser = JavaParser(stream)
        parser.removeErrorListeners()  # Remove default error listeners
        parser.addErrorListener(DiagnosticErrorListener())  # Add diagnostic listener

        stream.fill()
        comments = []
        for token in stream.tokens:
            if token.channel == Token.HIDDEN_CHANNEL and token.type in [
                JavaLexer.COMMENT,
                JavaLexer.LINE_COMMENT,
            ]:
                comments.append((token.text.strip(), token.line))

        # Parse the compilation unit
        tree = parser.compilationUnit()

        # Create and run the listener
        listener = JavaListener(content, comments)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.class_info
    except Exception as e:
        logger.error(f"Error parsing Java file: {e}")
        return []
