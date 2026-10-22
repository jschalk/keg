from src.ch38_article_tool.article_toolbox import get_articleunit_from_file
from pathlib import Path


def test_Ch40MarkDownFilesHaveRequiredStrings():
    # ESTABLISH
    current_ch_dir = Path(__file__).resolve().parent.parent
    author_str = "**Author:**"
    date_str = "**Date:**"
    source_str = "**Source:**"
    copied_str = "**Copied to Keg:**"
    required_strings = [author_str, date_str, source_str, copied_str]

    # WHEN / THEN
    for md_file_path in sorted(current_ch_dir.glob("*.md")):
        md_articleunit = get_articleunit_from_file(md_file_path, required_strings)
        assert not md_articleunit.missing_required, md_file_path
        assert not md_articleunit.out_of_order_req_str, md_file_path
