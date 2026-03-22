from src.ch00_py.file_toolbox import create_path
from src.ch09_person_lesson.lasso import LassoUnit
from src.ch11_bud._ref.ch11_path import create_bud_dir_path
from src.ch14_moment._ref.ch14_semantic_types import PersonName

BUD_MANDATE_FILENAME = "bud_partner_mandate_ledger.json"


def create_bud_partner_mandate_ledger_path(
    moment_mstr_dir: str,
    moment_lasso: LassoUnit,
    person_name: PersonName,
    bud_time: int,
) -> str:
    """Returns path: moment_mstr_dir\\moments\\moment_rope\\persons\\person_name\\buds\n\\bud_time\\bud_partner_mandate_ledger.json"""
    timenum_dir = create_bud_dir_path(
        moment_mstr_dir, moment_lasso, person_name, bud_time
    )
    return create_path(timenum_dir, "bud_partner_mandate_ledger.json")
