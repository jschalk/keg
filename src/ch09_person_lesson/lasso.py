from dataclasses import dataclass
from src.ch00_py.file_toolbox import create_directory_path
from src.ch04_rope.rope import get_all_rope_labels, get_default_rope
from src.ch09_person_lesson._ref.ch09_semantic_types import (
    KnotTerm,
    MomentRope,
    default_knot_if_None,
)


class Lasso_init_knot_not_presentException(Exception):
    pass


@dataclass
class LassoUnit:
    moment_rope: MomentRope = None
    knot: KnotTerm = None

    def make_path(self) -> str:
        rope_labels = get_all_rope_labels(self.moment_rope, self.knot)
        return create_directory_path(x_list=[*rope_labels])


def lassounit_shop(moment_rope: MomentRope = None, knot: KnotTerm = None) -> LassoUnit:
    if moment_rope is None:
        moment_rope = get_default_rope()
    knot = default_knot_if_None(knot)
    if moment_rope.find(knot) != 0:
        exception_str = f"moment_rope '{moment_rope}' must have knot '{knot}' at position 0 in string"
        raise Lasso_init_knot_not_presentException(exception_str)

    return LassoUnit(moment_rope=moment_rope, knot=knot)
