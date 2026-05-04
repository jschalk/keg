from ch00_py.file_toolbox import create_path
from ch26_world.world import WorldName
from ch27_pitch._ref.ch27_semantic_types import PitchID


def create_pitch_dir_path(pitch_mstr_dir: str, pitch_id: PitchID) -> str:
    """Returns path: pitch_mstr_dir\\pitchs\\pitch_id"""
    pitchs_dir = create_path(pitch_mstr_dir, "pitchs")
    return create_path(pitchs_dir, pitch_id)


def create_world_dir_path(
    pitch_mstr_dir: str, pitch_id: PitchID, world_name: WorldName
) -> str:
    """Returns path: pitch_mstr_dir\\pitchs\\pitch_id\\worlds\\world_name"""
    pitchs_dir = create_path(pitch_mstr_dir, "pitchs")
    pitch_dir = create_path(pitchs_dir, pitch_id)
    worlds_dir = create_path(pitch_dir, "worlds")
    return create_path(worlds_dir, world_name)


def create_moment_mstr_dir_path(
    pitch_mstr_dir: str, pitch_id: PitchID, world_name: WorldName
) -> str:
    """Returns path: pitch_mstr_dir\\pitchs\\pitch_id\\worlds\\world_name\\moment_mstr_dir"""
    pitchs_dir = create_path(pitch_mstr_dir, "pitchs")
    pitch_dir = create_path(pitchs_dir, pitch_id)
    worlds_dir = create_path(pitch_dir, "worlds")
    world_name_dir = create_path(worlds_dir, world_name)
    return create_path(world_name_dir, "moment_mstr_dir")
