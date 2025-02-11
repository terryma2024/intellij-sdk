from antlr4 import InputStream, ParseTreeListener, CommonTokenStream, ParseTreeWalker
from antlr4.error.DiagnosticErrorListener import DiagnosticErrorListener
from antlr4.Token import Token
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
    def __init__(self, source, comments):
        self.source = source
        self.class_info = []
        self.current_class = None
        self.nesting_level = 0
        self.comments = comments
        self.last_processed_line = -1

    def _clean_comment(self, comment):
        """Clean up comment by removing comment markers."""
        cleaned = comment
        if cleaned.startswith("/*") and cleaned.endswith("*/"):
            cleaned = cleaned[2:-2].strip()
        elif cleaned.startswith("//"):
            cleaned = cleaned[2:].strip()
        return cleaned

    def _is_class_level_property(self, ctx):
        """Check if a property is directly under class body."""
        parent = ctx.parentCtx
        while parent is not None:
            if isinstance(parent, KotlinParser.BlockContext):
                return False
            if isinstance(parent, KotlinParser.ClassBodyContext):
                return True
            parent = parent.parentCtx
        return False

    def _extract_annotations(self, modifier_list_ctx):
        """Extract annotations from ModifierList context."""
        annotations = []
        for modifier in modifier_list_ctx.getChildren():
            if isinstance(modifier, KotlinParser.AnnotationsContext):
                annotation = modifier.getText().strip("@")
                annotations.append(annotation)
        return annotations

    def _extract_property_info(self, ctx):
        """Extract property information from property declaration context."""
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
            elif isinstance(child, KotlinParser.VariableDeclarationContext):
                for sibling_child in child.getChildren():
                    if isinstance(sibling_child, KotlinParser.SimpleIdentifierContext):
                        name = sibling_child.getText()
                        break

        return name, is_const, is_val, is_private

    def find_nearest_comment(self, target_line):
        """Find and return the nearest comment before the target line."""
        nearest_comment = None
        for comment, line in reversed(self.comments):
            if self.last_processed_line < line < target_line:
                nearest_comment = self._clean_comment(comment)
                break
        self.last_processed_line = target_line
        return nearest_comment or "No Comment"

    def _create_class_info(
        self, class_name, annotations, is_interface, is_data_class, line
    ):
        """Create a new class info dictionary with default values."""
        return {
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
            "comment": self.find_nearest_comment(line),
        }

    def _process_class_modifiers(self, ctx):
        """Process class modifiers to extract annotations and class type."""
        annotations = []
        is_data_class = False

        for child in ctx.getChildren():
            if isinstance(child, KotlinParser.ModifierListContext):
                for modifier in child.getChildren():
                    if isinstance(modifier, KotlinParser.AnnotationsContext):
                        annotations.append(modifier.getText().strip("@"))
                    elif modifier.getText() == "data":
                        is_data_class = True

        return annotations, is_data_class

    def _find_class_name_and_type(self, ctx):
        """Find class name and determine if it's an interface."""
        found_type = False
        is_interface = False
        class_name = None

        for child in ctx.getChildren():
            text = child.getText()
            if text in ["class", "interface"]:
                found_type = True
                is_interface = text == "interface"
            elif found_type and isinstance(child, KotlinParser.SimpleIdentifierContext):
                class_name = child.getText()
                break

        return class_name, is_interface

    def enterClassDeclaration(self, ctx):
        self.nesting_level += 1

        annotations, is_data_class = self._process_class_modifiers(ctx)
        class_name, is_interface = self._find_class_name_and_type(ctx)

        if class_name and self.nesting_level == 1:
            self.current_class = self._create_class_info(
                class_name, annotations, is_interface, is_data_class, ctx.start.line
            )
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
                self.current_class["properties"].append(
                    {"name": name, "comment": self.find_nearest_comment(ctx.start.line)}
                )
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
                        {
                            "name": child.getText(),
                            "comment": self.find_nearest_comment(ctx.start.line),
                        }
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
                {"name": name, "comment": self.find_nearest_comment(ctx.start.line)}
            )
            logger.debug(
                f"Added companion object '{name}' to class {self.current_class['name']}"
            )

    def exitClassDeclaration(self, ctx):
        if self.nesting_level == 1 and self.current_class:
            self.class_info.append(self.current_class)
            self.current_class = None
        self.nesting_level -= 1

    def _add_property_to_class(self, name, is_const, line):
        """Add a property to the current class."""
        property_info = {"name": name, "comment": self.find_nearest_comment(line)}
        if is_const:
            self.current_class["constants"].append(property_info)
        else:
            self.current_class["properties"].append(property_info)

    def enterPropertyDeclaration(self, ctx):
        if not self.current_class or not self._is_class_level_property(ctx):
            return

        name, is_const, is_val, is_private = self._extract_property_info(ctx)
        if name and not is_private and (is_const or is_val):
            self._add_property_to_class(name, is_const, ctx.start.line)

    def _is_modifier_or_annotation(self, text):
        """Check if the text is a modifier or annotation."""
        return text.startswith("@") or text in [
            "private",
            "public",
            "protected",
            "internal",
        ]

    def _extract_extension_function_info(self, text, next_text, next_next_text):
        """Extract extension function information."""
        name = None
        receiver_type = None

        if "." in text:
            parts = text.split(".")
            receiver_type = parts[0]
            if next_text and not next_text.startswith("("):
                name = next_text
        else:
            receiver_type = text
            if next_next_text and not next_next_text.startswith("("):
                name = next_next_text

        return name, receiver_type

    def _is_valid_function_name(self, text):
        """Check if the text could be a valid function name."""
        return not any(
            [
                text.startswith("("),
                text.startswith("<"),
                text.startswith("@"),
                text in ["fun", ":"],
            ]
        )

    def enterFunctionDeclaration(self, ctx):
        if not self.current_class:
            return

        children = list(ctx.getChildren())
        found_fun = False
        name = None

        for i, child in enumerate(children):
            text = child.getText()

            if text == "fun":
                found_fun = True
                continue

            if not found_fun:
                continue

            if self._is_modifier_or_annotation(text) or text.startswith("<"):
                continue

            if name is None:
                next_text = children[i + 1].getText() if i + 1 < len(children) else ""
                next_next_text = (
                    children[i + 2].getText() if i + 2 < len(children) else ""
                )

                if "." in text or (text and next_text == "."):
                    name, _ = self._extract_extension_function_info(
                        text, next_text, next_next_text
                    )
                    if name:
                        break
                elif self._is_valid_function_name(text):
                    name = text
                    break

        if name:
            self.current_class["methods"].append(
                {"name": name, "comment": self.find_nearest_comment(ctx.start.line)}
            )


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

        # Extract comments before parsing
        stream.fill()
        comments = []
        for token in stream.tokens:
            if token.channel == Token.HIDDEN_CHANNEL and token.type in [
                KotlinLexer.DelimitedComment,
                KotlinLexer.LineComment,
            ]:
                comments.append((token.text.strip(), token.line))

        # Create the parser
        parser = KotlinParser(stream)
        parser.removeErrorListeners()  # Remove default error listeners
        parser.addErrorListener(DiagnosticErrorListener())  # Add diagnostic listener
        tree = parser.kotlinFile()

        # Create and run the listener with comments
        listener = KotlinListener(content, comments)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.class_info
    except Exception as e:
        logger.error(f"Error parsing Kotlin file: {e}")
        return []
