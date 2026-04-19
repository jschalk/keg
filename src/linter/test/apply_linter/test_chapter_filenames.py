from ch00_py.file_toolbox import get_dir_file_strs
from linter.style import get_chapter_descs, get_filenames_with_wrong_style


def get_filenamebase_mapping(filenamebases: list[str]) -> dict:
    base_map = {}
    for focus_filenamebase in filenamebases:
        for check_filenamebase in filenamebases:
            if check_filenamebase.find(focus_filenamebase) > -1:
                if base_map.get(focus_filenamebase) is None:
                    base_map[focus_filenamebase] = []
                base_map[focus_filenamebase].append(check_filenamebase)
    return base_map


def get_file_collisions_set(filenames: list[str]) -> list[str]:
    base_map = get_filenamebase_mapping(filenames)
    collisions = []
    for name_group in base_map.values():
        if len(name_group) > 1:
            collisions.extend(name_group)
    return collisions


def test_check_Chapters_filenames_FollowFileNameConventions_NoNamingCollision():
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    all_level1_file_bases = set()
    all_level1_filenames = set()
    for chapter_desc, chapter_dir in get_chapter_descs().items():
        level1_file_bases = get_dir_file_strs(chapter_dir, True, False, True)
        level1_file_bases = set(level1_file_bases.keys())
        all_level1_file_bases.update(level1_file_bases)

        level1_filenames = get_dir_file_strs(chapter_dir, None, False, True)
        level1_filenames = set(level1_filenames.keys())
        all_level1_filenames.update(level1_filenames)
        # print(f"{level1_files=}")
        collisions = get_file_collisions_set(level1_file_bases)
        if collisions:
            print(f"{chapter_desc} {collisions=}")
        assert not collisions

    # CHECK for collisions acress chapters
    all_collisions = get_file_collisions_set(all_level1_file_bases)
    if all_collisions:
        print(f"{all_collisions=}")
    assert not all_collisions
    assert get_filenames_with_wrong_style(all_level1_filenames) == set()
