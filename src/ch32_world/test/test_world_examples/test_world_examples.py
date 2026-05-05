from ch00_py.file_toolbox import (
    count_dirs_files,
    create_path,
    delete_dir,
    get_dir_filenames,
    get_level1_dirs,
)
from ch31_kpi.kpi_mstr import create_kpi_csvs
from ch32_world.world import brick_sheets_to_lego_mstr, create_ideas, worlddir_shop
from os.path import exists as os_path_exists
from ref.keywords import ExampleStrs as exx


def test_brick_sheets_to_lego_mstr_Examples(temp3_fs, run_big_tests):
    """Find examples in a example directory and run them through the pipeline."""
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH

    if not run_big_tests:
        return
    examples_dir = "src/ch32_world/test/test_world_examples"
    example_names = set(get_level1_dirs(examples_dir))
    if "__pycache__" in example_names:
        example_names.remove("__pycache__")  # Remove __pycache__ if it exists
    worlds_mstr_str = "worlds"
    output_str = "output"
    if worlds_mstr_str in example_names:
        example_names.remove(worlds_mstr_str)  # Remove __pycache__ if it exists
    if output_str in example_names:
        example_names.remove(output_str)  # Remove __pycache__ if it exists

    for example_name in example_names:
        worlds_dir = create_path(examples_dir, worlds_mstr_str)
        parent_output_dir = create_path(examples_dir, "output")
        output_dir = create_path(parent_output_dir, example_name)
        delete_dir(output_dir)  # Clean up output directory before test

        b_src_dir = create_path(examples_dir, example_name)
        print(f"{b_src_dir=} {get_dir_filenames(b_src_dir)}")
        example_worlddir = worlddir_shop(
            world_name=example_name,
            worlds_dir=worlds_dir,
            b_src_dir=b_src_dir,
            output_dir=output_dir,
        )
        example_worlddir.delete_world_db()
        assert count_dirs_files(output_dir) == 0
        print(f"before WHEN {os_path_exists(b_src_dir)=}")

        # WHEN
        brick_sheets_to_lego_mstr(example_worlddir)
        create_ideas(
            example_worlddir.world_dir,
            example_worlddir.output_dir,
            example_worlddir.world_name,
            example_worlddir.moment_mstr_dir,
            prettify_excel_bool=False,
        )
        create_kpi_csvs(
            example_worlddir.get_world_db_path(), example_worlddir.output_dir
        )

        # THEN
        print(f"after WHEN {os_path_exists(b_src_dir)=}")
        # print(f"{count_dirs_files(output_dir)=}")
        assert count_dirs_files(output_dir) > 0
        assert count_dirs_files(b_src_dir) > 0
