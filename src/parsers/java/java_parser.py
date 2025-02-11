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
        self.comments = comments
        self.last_processed_line = -1
        logger.debug("Initialized JavaListener")

    def _clean_comment(self, comment):
        """Clean up comment by removing comment markers."""
        cleaned = comment
        if cleaned.startswith("/*") and cleaned.endswith("*/"):
            cleaned = cleaned[2:-2].strip()
        elif cleaned.startswith("//"):
            cleaned = cleaned[2:].strip()
        return cleaned

    def _is_valid_identifier(self, text, excluded_keywords=None):
        """Check if the text is a valid identifier."""
        if not text or text.startswith("@"):
            return False

        default_keywords = ["class", "interface", "enum"]
        excluded = excluded_keywords if excluded_keywords else default_keywords
        return text not in excluded

    def _create_class_info(self, identifier, line):
        """Create a new class info dictionary with default values."""
        return {
            "name": identifier,
            "constants": [],
            "methods": [],
            "comment": self.find_nearest_comment(line),
        }

    def _handle_class_stack(self):
        """Handle class stack operations when entering a new class context."""
        if self.current_class:
            self.class_stack.append(self.current_class)

    def find_nearest_comment(self, target_line):
        """Find and return the nearest comment before the target line."""
        nearest_comment = None
        for comment, line in reversed(self.comments):
            if self.last_processed_line < line < target_line:
                nearest_comment = self._clean_comment(comment)
                break
        self.last_processed_line = target_line
        return nearest_comment or "No Comment"

    def _find_identifier(self, ctx, excluded_keywords=None):
        """Find a valid identifier from the context's children."""
        for child in ctx.getChildren():
            if isinstance(
                child, (JavaParser.TypeIdentifierContext, JavaParser.IdentifierContext)
            ):
                text = child.getText()
                if self._is_valid_identifier(text, excluded_keywords):
                    return text
        return None

    def _handle_declaration_entry(self, ctx, declaration_type="class"):
        """Handle entry of class-like declarations (class, enum, interface)."""
        self.nesting_level += 1
        identifier = self._find_identifier(ctx)

        if identifier:
            self._handle_class_stack()
            self.current_class = self._create_class_info(identifier, ctx.start.line)

            # Only add top-level declarations to class_info immediately
            if self.nesting_level == 1:
                self.class_info.append(self.current_class)

            logger.debug(f"Created new {declaration_type}: {identifier}")
        else:
            logger.debug(f"No {declaration_type} identifier found")

    def _handle_declaration_exit(self):
        """Handle exit of class-like declarations."""
        if self.current_class:
            # Only append nested declarations to class_info when exiting
            if self.nesting_level > 1:
                self.class_info.append(self.current_class)
            self.current_class = self.class_stack.pop() if self.class_stack else None
        self.nesting_level -= 1

    def enterClassDeclaration(self, ctx):
        self._handle_declaration_entry(ctx)

    def exitClassDeclaration(self, ctx):
        self._handle_declaration_exit()

    def enterEnumDeclaration(self, ctx):
        self._handle_declaration_entry(ctx, "enum")

    def exitEnumDeclaration(self, ctx):
        self._handle_declaration_exit()

    def enterNormalClassDeclaration(self, ctx):
        self._handle_declaration_entry(ctx, "normal class")

    def exitNormalClassDeclaration(self, ctx):
        self._handle_declaration_exit()

    def enterInterfaceDeclaration(self, ctx):
        self._handle_declaration_entry(ctx, "interface")

    def exitInterfaceDeclaration(self, ctx):
        self._handle_declaration_exit()

    def _handle_method_declaration(
        self, ctx, method_type="method", excluded_keywords=None
    ):
        """Handle method-like declarations (methods, constructors, interface methods)."""
        if not self.current_class:
            return

        logger.debug(
            f"Processing {method_type} declaration in: {self.current_class['name']}"
        )
        identifier = self._find_identifier(ctx, excluded_keywords)

        if identifier:
            # Check if method already exists
            if not any(
                method["name"] == identifier for method in self.current_class["methods"]
            ):
                self.current_class["methods"].append(
                    {
                        "name": identifier,
                        "comment": self.find_nearest_comment(ctx.start.line),
                    }
                )
                logger.debug(
                    f"Added {method_type} '{identifier}' to {self.current_class['name']}"
                )
        else:
            logger.debug(f"No {method_type} identifier found")

    def enterMethodDeclaration(self, ctx):
        excluded_keywords = [
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
        self._handle_method_declaration(ctx, excluded_keywords=excluded_keywords)

    def enterConstructorDeclaration(self, ctx):
        self._handle_method_declaration(ctx, "constructor")

    def enterInterfaceCommonBodyDeclaration(self, ctx):
        excluded_keywords = [
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
        ]
        self._handle_method_declaration(ctx, "interface method", excluded_keywords)


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

        # Extract comments
        stream.fill()
        comments = [
            (token.text.strip(), token.line)
            for token in stream.tokens
            if token.channel == Token.HIDDEN_CHANNEL
            and token.type in [JavaLexer.COMMENT, JavaLexer.LINE_COMMENT]
        ]

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
