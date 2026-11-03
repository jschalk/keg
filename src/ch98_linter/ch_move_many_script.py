from ch98_linter.ch_move_single_script import move_chapters_given_ints
from time import sleep as time_sleep

# HOW TO USE:
# Open up CMD, change directory to repo
# Enter this: python -m src.linter.chapter_move_main


def ch_many_move_main():
    lower_chxx_str = input("Lower chapter (int): ").strip()
    upper_chxx_str = input("Upper chapter (int): ").strip()
    move_number = input("Move chapters how many? (int): ").strip()
    lower_chxx_int = int(lower_chxx_str)
    upper_chxx_int = int(upper_chxx_str)
    move_number_int = int(move_number)
    for src_ch_num in sorted(range(lower_chxx_int, upper_chxx_int + 1), reverse=True):
        dst_ch_num = src_ch_num + move_number_int
        print(f"from {src_ch_num} to {dst_ch_num}")
        move_chapters_given_ints(src_ch_num, dst_ch_num)
        time_sleep(3)
    print(f"Moved {lower_chxx_str}:{upper_chxx_str} by {move_number} chapters")


if __name__ == "__main__":
    ch_many_move_main()
