from ch00_py.file_toolbox import create_path
from ch30_idea_dst._ref.ch30_semantic_types import PersonName


def create_mind0001_path(output_dir: str) -> str:
    """Returns path: output_dir\\mind0001.xlsx"""
    return create_path(output_dir, "mind0001.xlsx")


def create_mind0002_path(output_dir: str, person_name: PersonName) -> str:
    """Returns path: output_dir\\person_name\\person_name_ideas.xlsx"""
    person_punch_dir = create_path(output_dir, person_name)
    return create_path(person_punch_dir, f"{person_name}_ideas.xlsx")
