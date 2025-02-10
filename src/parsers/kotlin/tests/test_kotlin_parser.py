import pytest
from pathlib import Path
from src.parsers.kotlin.kotlin_parser import parse_kotlin_file


@pytest.fixture
def kt_test_file():
    test_file = Path(__file__).parent / "test_data" / "TestClass.kt"
    with open(test_file, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def kt_extension_test_file():
    test_file = Path(__file__).parent / "test_data" / "ExtensionFunction.kt"
    with open(test_file, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def kt_complex_test_file():
    test_file = Path(__file__).parent / "test_data" / "KotlinTest.kt"
    with open(test_file, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def kt_general_settings_file():
    test_file = Path(__file__).parent / "test_data" / "GeneralSettings.kt"
    with open(test_file, "r", encoding="utf-8") as f:
        return f.read()


def test_parse_general_settings(kt_general_settings_file):
    # Parse the file
    result = parse_kotlin_file(kt_general_settings_file)

    # Verify the parsing results
    assert len(result) == 3, "Should parse main class, data class and enum class"

    # Verify expected class names are present
    class_names = [c["name"] for c in result]
    expected_class_names = [
        "GeneralSettings",
        "GeneralSettingsState",
        # "PropertyNames", # nested class
        "ProcessCloseConfirmation",
    ]
    assert set(class_names) == set(expected_class_names), (
        f"Expected classes {expected_class_names}, but found {class_names}"
    )

    # Find the main GeneralSettings class
    general_settings = next(c for c in result if c["name"] == "GeneralSettings")

    # Check class annotations
    assert any("State" in a for a in general_settings.get("annotations", [])), (
        "Should have @State annotation"
    )

    # Check properties
    properties = general_settings["properties"]
    expected_properties = [
        "browserPath",
        "isShowTipsOnStartup",
        "isReopenLastProject",
        "isSyncOnFrameActivation",
        "isBackgroundSync",
        "isSaveOnFrameDeactivation",
        "isAutoSaveIfInactive",
        "isUseSafeWrite",
        "isUseDefaultBrowser",
        "isSearchInBackground",
        "isConfirmExit",
        "isShowWelcomeScreen",
        "confirmOpenNewProject",
        "processCloseConfirmation",
        "isSupportScreenReaders",
        "inactiveTimeout",
        "defaultProjectDirectory",
        "SAVE_FILES_AFTER_IDLE_SEC",
    ]
    for prop in expected_properties:
        assert any(p["name"] == prop for p in properties), f"Missing property {prop}"

    # Check companion object constants
    companion = general_settings.get("constants", [])
    assert len(companion) > 0, "Should have companion object"

    constants = general_settings.get("constants", [])
    expected_constants = [
        "IDE_GENERAL_XML",
        "OPEN_PROJECT_ASK",
        "OPEN_PROJECT_NEW_WINDOW",
        "OPEN_PROJECT_SAME_WINDOW",
        "OPEN_PROJECT_SAME_WINDOW_ATTACH",
        "SUPPORT_SCREEN_READERS",
    ]
    for const in expected_constants:
        assert any(c["name"] == const for c in constants), f"Missing constant {const}"

    # Check nested enum classes
    property_names = next(c for c in result if c["name"] == "ProcessCloseConfirmation")
    assert property_names.get("is_enum", False), (
        "ProcessCloseConfirmation should be an enum class"
    )
    assert len(property_names.get("enum_values", [])) == 3, (
        "ProcessCloseConfirmation should have 3 enum values"
    )

    # Check data class
    settings_state = next(c for c in result if c["name"] == "GeneralSettingsState")
    assert settings_state.get("is_data_class", False), (
        "GeneralSettingsState should be a data class"
    )
    assert len(settings_state.get("properties", [])) > 0, (
        "GeneralSettingsState should have properties"
    )


def test_parse_kotlin_file(kt_test_file):
    # Parse the file
    result = parse_kotlin_file(kt_test_file)

    # Verify the parsing results
    assert len(result) == 1, "Should parse one top-level class"

    # Check the main class
    class_info = result[0]
    assert class_info["name"] == "TestClass", "Should parse class name correctly"

    # Check constants
    constants = class_info["constants"]
    expected_constants = [
        {"name": "MAX_COUNT", "comment": ""},
        {"name": "DEFAULT_NAME", "comment": ""},
        {"name": "VERSION", "comment": ""},
        {"name": "NESTED_CONSTANT", "comment": ""},
    ]
    assert len(constants) == len(expected_constants), "Should parse all constants"
    for expected in expected_constants:
        assert any(c["name"] == expected["name"] for c in constants), (
            f"Missing constant {expected['name']}"
        )

    # Check methods
    methods = class_info["methods"]
    expected_methods = [
        "basicFunction",
        "parameterizedFunction",
        "genericFunction",
        "addPrefix",
        "nestedFunction",
        "interfaceMethod",
    ]
    assert len(methods) == len(expected_methods), "Should parse all methods"
    for expected in expected_methods:
        assert any(m["name"] == expected for m in methods), f"Missing method {expected}"


def test_parse_kotlin_extension_function(kt_extension_test_file):
    # Parse the file
    result = parse_kotlin_file(kt_extension_test_file)

    # Verify the parsing results
    assert len(result) == 1, "Should parse one top-level class"

    # Check the main class
    class_info = result[0]
    assert class_info["name"] == "TestExtensions", "Should parse class name correctly"

    # Check extension functions
    methods = class_info["methods"]
    expected_methods = ["addPrefix", "double"]

    assert len(methods) == len(expected_methods), "Should parse all extension functions"
    for expected in expected_methods:
        assert any(m["name"] == expected for m in methods), (
            f"Missing extension function '{expected}'"
        )


def test_parse_complex_kotlin_file(kt_complex_test_file):
    # Parse the file
    result = parse_kotlin_file(kt_complex_test_file)

    # Verify multiple class declarations
    assert len(result) > 1, "Should parse multiple top-level classes"

    # Check specific classes
    class_names = [c["name"] for c in result]
    expected_classes = ["Foo", "Runnable", "A", "Color", "My", "Outer"]
    for expected in expected_classes:
        assert expected in class_names, f"Missing class {expected}"

    # Find class A with companion objects
    class_a = next(c for c in result if c["name"] == "A")
    assert "companion_objects" in class_a, "Class A should have companion objects"

    # Find enum class Color
    color_class = next(c for c in result if c["name"] == "Color" and "is_enum" in c)
    assert color_class["is_enum"], "Color should be an enum class"
    assert "methods" in color_class, "Color should have methods"

    # Check interface
    interface_foo = next(
        c for c in result if c["name"] == "FooInterface" and "is_interface" in c
    )
    assert interface_foo["is_interface"], "Foo should be an interface"
    assert "methods" in interface_foo, "Interface should have methods"
    assert "properties" in interface_foo, "Interface should have properties"
