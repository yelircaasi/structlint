"""
Top-level functions performing each check end-to-end.
"""

from functools import partial

from structlint.logic import sort_methods
from structlint.utils import deduplicate_ordered, sort_on_path

from .collection import Objects
from .configuration import Configuration, ImportsConfig
from .logic import (
    analyze_discrepancies,
    get_disallowed_imports,
    map_to_doc,
    map_to_test,
)
from .reporting import (
    make_discrepancy_report,
    make_imports_report,
    make_methods_report,
)


def check_method_order(cfg: Configuration, source_objects: Objects) -> tuple[str, bool]:
    out_of_order = []
    classes = source_objects.classes(include_inherited=False)

    for path, _, classname, methods, method_dict, __ in classes:
        if methods != (sorted_methods := sort_methods(method_dict, cfg.methods)):
            out_of_order.append((path, classname, methods, sorted_methods))

    return make_methods_report(out_of_order), bool(out_of_order)


def check_docs_structure(
    cfg: Configuration, source_objects: Objects, docs_objects: Objects
) -> tuple[str, bool]:
    actual: list[str] = sort_on_path(docs_objects.strings_without_methods)
    duplicated = source_objects.apply(
        partial(map_to_doc, cfg=cfg), cfg.docs.ignore, classes_only=True
    )
    expected: list[str] = sort_on_path(deduplicate_ordered(duplicated))
    missing, unexpected, overlap = analyze_discrepancies(
        expected, actual, allow_additional=cfg.docs.allow_additional
    )

    return (
        make_discrepancy_report(
            "DOCUMENTATION",
            actual,
            expected,
            missing,
            unexpected,
            overlap,
            cfg.docs.md_dir,
            cfg.root_dir,
            cfg.docs.order_ignore,
        ),
        any((missing, unexpected)),
    )


def check_tests_structure(
    cfg: Configuration, source_objects: Objects, tests_objects: Objects
) -> tuple[str, bool]:
    tests_objects = tests_objects.test_only
    actual: list[str] = sort_on_path(tests_objects.strings(include_inherited=True))
    expected: list[str] = sort_on_path(
        source_objects.apply(partial(map_to_test, cfg=cfg), cfg.tests.ignore)
    )
    missing, unexpected, overlap = analyze_discrepancies(
        expected, actual, allow_additional=cfg.tests.allow_additional
    )

    return (
        make_discrepancy_report(
            "TESTS",
            actual,
            expected,
            missing,
            unexpected,
            overlap,
            cfg.tests.unit_dir,
            cfg.root_dir,
            cfg.tests.order_ignore,
        ),
        any((missing, unexpected)),
    )


def check_imports(icfg: ImportsConfig, module_name: str) -> tuple[str, bool]:
    internal, external = get_disallowed_imports(icfg, module_name)

    return (
        make_imports_report(internal, external),
        any((internal, external)),
    )
