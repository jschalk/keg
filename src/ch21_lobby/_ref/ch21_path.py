from src.ch00_py.file_toolbox import create_path
from src.ch20_world_apex.world import WorldName
from src.ch21_lobby._ref.ch21_semantic_types import LobbyID


def create_lobby_dir_path(lobby_mstr_dir: str, lobby_id: LobbyID) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    return create_path(lobbys_dir, lobby_id)


def create_world_dir_path(
    lobby_mstr_dir: str, lobby_id: LobbyID, world_name: WorldName
) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id\\worlds\\world_name"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    lobby_dir = create_path(lobbys_dir, lobby_id)
    worlds_dir = create_path(lobby_dir, "worlds")
    return create_path(worlds_dir, world_name)


def create_moment_mstr_dir_path(
    lobby_mstr_dir: str, lobby_id: LobbyID, world_name: WorldName
) -> str:
    """Returns path: lobby_mstr_dir\\lobbys\\lobby_id\\worlds\\world_name\\moment_mstr_dir"""
    lobbys_dir = create_path(lobby_mstr_dir, "lobbys")
    lobby_dir = create_path(lobbys_dir, lobby_id)
    worlds_dir = create_path(lobby_dir, "worlds")
    world_name_dir = create_path(worlds_dir, world_name)
    return create_path(world_name_dir, "moment_mstr_dir")
