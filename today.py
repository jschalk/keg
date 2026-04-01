# from os import getcwd as os_getcwd
# from os.path import isdir as os_path_isdir
# from src.ch00_py.file_toolbox import create_path, open_json, save_file
from src.ch00_py.file_toolbox import create_path

# from src.ch20_kpi.gcalendar import get_gcal_day_punch_from_personunit

# HOW TO USE:
# Open up CMD, change directory to repo
# Enter this: python today.py


def main():
    print("jih")
    test_file_path = input("test_file_path: ").strip()
    test_name = input("test_name: ").strip()
    dest_dir = input("dest_dir (default ch18): ").strip()
    if dest_dir in {None, ""}:
        dest_dir = "src/ch19_etl_steps/test/z_notebooks"
    dest_filename = input("dest_filename (default test_name): ").strip()
    if dest_filename in {None, ""}:
        dest_filename = f"{test_name[5:]}.py"
    dest_file_path = create_path(dest_dir, dest_filename)
    print(f"{test_file_path=}")
    print(f"{dest_file_path=}")
    print("")
    print(f"marimo edit {dest_file_path}")
    # save_marimo_notebook_from_test_file(test_file_path, test_name, dest_file_path)

    # find_str = input("Find string: ").strip()
    # replace_str = input("Replace string: ").strip()
    # print(f"Goal is to move {find_str} to {replace_str}")

    # if not os_path_isdir(src_dir):
    #     print("Error: directory does not exist.")
    #     return


if __name__ == "__main__":
    main()
