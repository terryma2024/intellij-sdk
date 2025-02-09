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
