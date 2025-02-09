import pytest
from pathlib import Path
from src.parsers.java_parser import parse_java_file


@pytest.fixture
def java_test_file():
    test_file = Path(__file__).parent / "test_data" / "AllInOne8.java"
    with open(test_file, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def java_anno_test_file():
    test_file = Path(__file__).parent / "test_data" / "Annos.java"
    with open(test_file, "r", encoding="utf-8") as f:
        return f.read()


def test_parse_java_classes(java_test_file):
    # Parse the test file
    result = parse_java_file(java_test_file)

    # Expected class names in the file
    expected_classes = [
        "Lambdas",
        "Formula",
        "For",
        "Annotations",
        "CallableProcessingInterceptor",
        "RouterFunction",
        "Unicode",
        "Annos",
        "Gen",
        "A",
    ]

    # Verify all expected classes are found
    found_classes = [cls["name"] for cls in result]
    assert set(found_classes) == set(expected_classes), (
        f"Expected classes {expected_classes}, but found {found_classes}"
    )


def test_parse_java_methods(java_test_file):
    result = parse_java_file(java_test_file)

    # Test methods in Lambdas class
    lambdas_class = next(cls for cls in result if cls["name"] == "Lambdas")
    assert any(method["name"] == "main" for method in lambdas_class["methods"]), (
        "Expected 'main' method in Lambdas class"
    )

    # Test methods in For class
    for_class = next(cls for cls in result if cls["name"] == "For")
    assert any(method["name"] == "bar" for method in for_class["methods"]), (
        "Expected 'bar' method in For class"
    )

    # Test methods in Unicode class
    unicode_class = next(cls for cls in result if cls["name"] == "Unicode")
    assert any(method["name"] == "main" for method in unicode_class["methods"]), (
        "Expected 'main' method in Unicode class"
    )


def test_parse_java_interfaces(java_test_file):
    import time

    start_time = time.time()
    result = parse_java_file(java_test_file)
    end_time = time.time()
    print(
        f"\nParsing time for test_parse_java_interfaces: {end_time - start_time:.3f} seconds"
    )

    # Test Formula interface methods
    formula_interface = next(cls for cls in result if cls["name"] == "Formula")
    assert any(
        method["name"] == "calculate" for method in formula_interface["methods"]
    ), "Expected 'calculate' method in Formula interface"
    assert any(method["name"] == "sqrt" for method in formula_interface["methods"]), (
        "Expected 'sqrt' default method in Formula interface"
    )

    # Test RouterFunction interface methods
    router_interface = next(cls for cls in result if cls["name"] == "RouterFunction")
    assert any(method["name"] == "filter" for method in router_interface["methods"]), (
        "Expected 'filter' method in RouterFunction interface"
    )


def test_parse_java_annotations(java_anno_test_file):
    result = parse_java_file(java_anno_test_file)

    # Test annotation class methods
    annos_class = next(cls for cls in result if cls["name"] == "Annos")
    assert any(method["name"] == "foo" for method in annos_class["methods"]), (
        "Expected 'foo' method in Annos class"
    )
    assert any(method["name"] == "foo2" for method in annos_class["methods"]), (
        "Expected 'foo2' method in Annos class"
    )
    assert any(method["name"] == "foo3" for method in annos_class["methods"]), (
        "Expected 'foo3' method in Annos class"
    )
    assert any(method["name"] == "foo33" for method in annos_class["methods"]), (
        "Expected 'foo33' method in Annos class"
    )
    assert any(method["name"] == "foo333" for method in annos_class["methods"]), (
        "Expected 'foo333' method in Annos class"
    )
    assert any(method["name"] == "f" for method in annos_class["methods"]), (
        "Expected 'f' method in Annos class"
    )
