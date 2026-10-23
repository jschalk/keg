from src.ch00_py.file_toolbox import save_file
from src.ch38_article_tool.article_toolbox import (
    get_markdown_file_metadata,
    create_markdown_table_of_contents,
)
from os.path import join as os_path_join
from os import makedirs as os_makedirs


def test_get_markdown_file_metadata_ReturnsDict_Scenario0_EmptyDir(temp3_dir):
    # ESTABLISH
    # WHEN
    x_metadata = get_markdown_file_metadata(temp3_dir)

    # THEN
    assert x_metadata == {}


def test_get_markdown_file_metadata_ReturnsDict_Scenario1_ValidMetadata(temp3_dir):
    # ESTABLISH
    temp_file_path = os_path_join(temp3_dir, "article.md")
    temp_file_str = """
# Big Clause Little Clause

**Author:** Hans Christen Anderson<br>
**Date:** 1844<br>

Article content.
"""
    save_file(temp_file_path, None, temp_file_str)

    # WHEN
    x_metadata = get_markdown_file_metadata(temp3_dir)

    # THEN
    expected_metadata = {
        "article.md": {
            "author": "Hans Christen Anderson",
            "date": "1844",
        }
    }
    assert x_metadata == expected_metadata


def test_get_markdown_file_metadata_ReturnsDict_Scenario2_DifferentDateFormat(
    temp3_dir,
):
    # ESTABLISH
    temp_file_path = os_path_join(temp3_dir, "article.md")
    temp_file_str = """
**Author:** Jane Smith<br>
**Date:** October 23, 2026<br>
"""
    save_file(temp_file_path, None, temp_file_str)

    # WHEN
    x_metadata = get_markdown_file_metadata(temp3_dir)

    # THEN
    expected_metadata = {
        "article.md": {
            "author": "Jane Smith",
            "date": "October 23, 2026",
        }
    }
    assert x_metadata == expected_metadata


def test_get_markdown_file_metadata_ReturnsDict_Scenario3_MissingMetadata(
    temp3_dir,
):
    # ESTABLISH
    temp_file_path = os_path_join(temp3_dir, "article.md")
    temp_file_str = """
# An Article

Article content without metadata.
"""
    save_file(temp_file_path, None, temp_file_str)

    # WHEN
    x_metadata = get_markdown_file_metadata(temp3_dir)

    # THEN
    expected_metadata = {
        "article.md": {
            "author": None,
            "date": None,
        }
    }
    assert x_metadata == expected_metadata


def test_get_markdown_file_metadata_ReturnsDict_Scenario4_ExcludesCatalogue(
    temp3_dir,
):
    # ESTABLISH
    article_file_path = os_path_join(temp3_dir, "article.md")
    catalogue_file_path = os_path_join(temp3_dir, "article_catalogue.md")

    temp_file_str = """
**Author:** Jane Smith<br>
**Date:** 2026-10-23<br>
"""
    save_file(article_file_path, None, temp_file_str)
    save_file(catalogue_file_path, None, temp_file_str)

    # WHEN
    x_metadata = get_markdown_file_metadata(temp3_dir)

    # THEN
    expected_metadata = {
        "article.md": {
            "author": "Jane Smith",
            "date": "2026-10-23",
        }
    }
    assert x_metadata == expected_metadata


def test_get_markdown_file_metadata_ReturnsDict_Scenario5_OnlyFirstLevelFiles(
    temp3_dir,
):
    # ESTABLISH
    article_file_path = os_path_join(temp3_dir, "article.md")
    subdirectory_path = os_path_join(temp3_dir, "subdirectory")
    os_makedirs(subdirectory_path)

    nested_file_path = os_path_join(subdirectory_path, "nested.md")
    temp_file_str = """
**Author:** Jane Smith<br>
**Date:** 2026<br>
"""
    save_file(article_file_path, None, temp_file_str)
    save_file(nested_file_path, None, temp_file_str)

    # WHEN
    x_metadata = get_markdown_file_metadata(temp3_dir)

    # THEN
    expected_metadata = {
        "article.md": {
            "author": "Jane Smith",
            "date": "2026",
        }
    }
    assert x_metadata == expected_metadata


def test_create_markdown_table_of_contents_ReturnsStr_Scenario0_Empty():
    # ESTABLISH
    metadata = {}

    # WHEN
    x_markdown = create_markdown_table_of_contents(metadata)

    # THEN
    assert x_markdown == "# Table of Contents\n"


def test_create_markdown_table_of_contents_ReturnsStr_Scenario1_OneArticle():
    # ESTABLISH
    metadata = {
        "big_clause.md": {
            "author": "Hans Christen Anderson",
            "date": "1844",
        }
    }

    # WHEN
    x_markdown = create_markdown_table_of_contents(metadata)

    # THEN
    expected_markdown = """# Table of Contents

## Big Clause Little Clause

*Hans Christen Anderson · 1844*

[Read article](./big_clause.md)

---
"""
    assert x_markdown == expected_markdown


def test_create_markdown_table_of_contents_ReturnsStr_Scenario2_MultipleArticles():
    # ESTABLISH
    metadata = {
        "zebra_article.md": {
            "author": "Jane Smith",
            "date": "October 23, 2026",
        },
        "apple_article.md": {
            "author": "John Doe",
            "date": "2025-01-15",
        },
    }

    # WHEN
    x_markdown = create_markdown_table_of_contents(metadata)

    # THEN
    expected_markdown = """# Table of Contents

## Apple Article

*John Doe · 2025-01-15*

[Read article](./apple_article.md)

---

## Zebra Article

*Jane Smith · October 23, 2026*

[Read article](./zebra_article.md)

---
"""
    assert x_markdown == expected_markdown


def test_create_markdown_table_of_contents_ReturnsStr_Scenario3_MissingMetadata():
    # ESTABLISH
    metadata = {
        "untitled.md": {
            "author": None,
            "date": None,
        }
    }

    # WHEN
    x_markdown = create_markdown_table_of_contents(metadata)

    # THEN
    expected_markdown = """# Table of Contents

## Untitled

*Unknown author · Undated*

[Read article](./untitled.md)

---
"""
    assert x_markdown == expected_markdown


def test_create_markdown_table_of_contents_ReturnsStr_Scenario4_FormatsFileName():
    # ESTABLISH
    metadata = {
        "my-interesting_article-name.md": {
            "author": "Jane Smith",
            "date": "2026",
        }
    }

    # WHEN
    x_markdown = create_markdown_table_of_contents(metadata)

    # THEN
    expected_markdown = """# Table of Contents

## My Interesting Article Name

*Jane Smith · 2026*

[Read article](./my-interesting_article-name.md)

---
"""
    assert x_markdown == expected_markdown


def test_create_markdown_table_of_contents_ReturnsStr_Scenario5_MissingKeys():
    # ESTABLISH
    metadata = {"article.md": {}}

    # WHEN
    x_markdown = create_markdown_table_of_contents(metadata)

    # THEN
    expected_markdown = """# Table of Contents

## Article

*Unknown author · Undated*

[Read article](./article.md)

---
"""
    assert x_markdown == expected_markdown
