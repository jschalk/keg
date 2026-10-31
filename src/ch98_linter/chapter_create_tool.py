from json import dumps as json_dumps
from pathlib import Path
from ch00_py.file_toolbox import save_json
from ch01_keyword.keyword_class_builder import (
    get_keywords_src_config,
    create_src_keywords_src_path,
)
from ch97_docs_builder.glossary_definition import (
    get_keywords_definitions,
    save_keg_descriptions_json,
)


def create_chapter_files(chapter_dict: dict) -> None:
    src_dir = Path(chapter_dict["src_dir"])
    chapter_number = chapter_dict["chapter_number"]
    chapter_name = chapter_dict["chapter_description"].lower()
    chapter_dir = src_dir / f"ch{chapter_number:02}_{chapter_name}"

    if chapter_dir.exists():
        raise FileExistsError(f"Chapter directory already exists: {chapter_dir}")

    ref_dir = chapter_dir / "_ref"
    chapter_dir.mkdir(parents=True, exist_ok=True)
    ref_dir.mkdir(parents=True, exist_ok=True)
    chapter_init_py_path = chapter_dir / "__init__.py"
    chapter_init_py_path.write_text("pass", encoding="utf-8")
    ref_init_path = ref_dir / "__init__.py"
    ref_init_path.write_text("pass", encoding="utf-8")
    ref_ai_summary_1min_path = ref_dir / f"ch{chapter_number:02}_ai_summary_1min.md"
    ref_ai_summary_1min_path.write_text("", encoding="utf-8")
    ref_ch_json_path = ref_dir / f"ch{chapter_number:02}_ref.json"
    chapter_dict["chapter_description"] = f"ch{chapter_number}_{chapter_name}"
    chapter_dict.pop("src_dir")
    ref_ch_json_path.write_text(json_dumps(chapter_dict, indent=2), encoding="utf-8")
    ref_semantic_types_path = ref_dir / f"ch{chapter_number:02}_semantic_types.py"
    ref_semantic_types_path.write_text("", encoding="utf-8")


def add_ch_to_keywords_src_config(chapter_dict: dict):
    keywords_src_config = get_keywords_src_config()
    chapter_number = chapter_dict["chapter_number"]
    valid_ch_dict = {"valid_ch": f"{chapter_number}"}
    keywords_src_config[f"ch{chapter_number:02}"] = valid_ch_dict
    src_keywords_src_path = create_src_keywords_src_path("src")
    save_json(src_keywords_src_path, None, keywords_src_config)


def add_ch_to_keyword_definitions(chapter_dict: dict):
    chapter_number = chapter_dict["chapter_number"]
    chapter_blurb = chapter_dict.get("chapter_blurb")
    keywords_definitions_dict = get_keywords_definitions()
    keywords_definitions_dict[f"ch{chapter_number:02}"] = chapter_blurb
    save_keg_descriptions_json("src", keywords_definitions_dict)


def main():
    ontology_summary_str = "All chapters get checked for following style rules."
    chapter_dict = {
        "src_dir": input("Source directory [c:/dev/keg/src]: ") or "c:/dev/keg/src",
        "chapter_blurb": input("Chapter blurb [Linter for repo.]: ")
        or "Linter for repo.",
        "chapter_content": input("Chapter content [Linter for repo.]: ")
        or "Linter for repo.",
        "chapter_description": input("Chapter description [linter]: ") or "linter",
        "chapter_number": int(input("Chapter number [98]: ") or "98"),
        "chapter_ref_catalogue": input("Chapter ref catalogue [n]: ") or "n",
        "ontology summary": input(f"Ontology summary [{ontology_summary_str}]: ")
        or ontology_summary_str,
    }
    create_chapter_files(chapter_dict)
    add_ch_to_keywords_src_config(chapter_dict)
    add_ch_to_keyword_definitions(chapter_dict)


if __name__ == "__main__":
    main()
