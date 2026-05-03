from ch00_py.file_toolbox import create_path
from ch09_person_lesson._ref.ch09_path import create_moments_dir_path
from ch09_person_lesson.lasso import LassoUnit
from ch24_idea_dst._ref.ch24_semantic_types import PersonName


def create_mind0001_path(output_dir: str) -> str:
    """Returns path: output_dir\\mind0001.xlsx"""
    return create_path(output_dir, "mind0001.xlsx")
