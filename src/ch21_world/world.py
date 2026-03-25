from dataclasses import dataclass
from os.path import exists as os_path_exists
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.ch00_py.file_toolbox import create_path, delete_dir, set_dir
from src.ch17_idea.idea_db_tool import update_spark_num_in_excel_files
from src.ch18_etl_config._ref.ch18_path import (
    create_moment_mstr_path,
    create_world_db_path,
)
from src.ch18_etl_config.stance_tool import create_stance0001_file
from src.ch19_etl_main.etl_main import (
    add_moment_epoch_to_guts,
    calc_moment_bud_partner_mandate_net_ledgers,
    create_last_run_metrics_json,
    etl_brick_agg_tables_to_brick_valid_tables,
    etl_brick_agg_tables_to_sparks_brick_agg_table,
    etl_brick_raw_tables_to_brick_agg_tables,
    etl_brick_valid_tables_to_sound_raw_tables,
    etl_heard_agg_tables_to_heard_vld_tables,
    etl_heard_raw_tables_to_heard_agg_tables,
    etl_heard_raw_tables_to_moment_ote1_agg,
    etl_heard_vld_tables_to_moment_jsons,
    etl_heard_vld_to_spark_person_csvs,
    etl_input_dfs_to_brick_raw_tables,
    etl_moment_guts_to_moment_jobs,
    etl_moment_job_jsons_to_job_tables,
    etl_moment_json_partner_nets_to_moment_partner_nets_table,
    etl_moment_ote1_agg_csvs_to_jsons,
    etl_moment_ote1_agg_table_to_moment_ote1_agg_csvs,
    etl_sound_agg_tables_to_sound_vld_tables,
    etl_sound_raw_tables_to_sound_agg_tables,
    etl_sound_vld_tables_to_heard_raw_tables,
    etl_spark_inherited_personunits_to_moment_gut,
    etl_spark_lesson_json_to_spark_inherited_personunits,
    etl_spark_person_csvs_to_lesson_json,
    etl_sparks_brick_agg_table_to_sparks_brick_valid_table,
    etl_translate_sound_agg_tables_to_translate_sound_vld_tables,
    get_max_brick_agg_spark_num,
)
from src.ch20_kpi.kpi_mstr import create_calendar_markdown_files, populate_kpi_bundle
from src.ch21_world._ref.ch21_semantic_types import WorldName


def create_stances(
    world_dir: str,
    output_dir: str,
    world_name: str,
    moment_mstr_dir: str,
    prettify_excel_bool=True,
):
    # TODO why is create_stance0001_file not drawing from world db instead of files?
    # it should be the database because that's the end of the core pipeline so it should
    # be the source of truth.
    create_stance0001_file(world_dir, output_dir, world_name, prettify_excel_bool)
    create_calendar_markdown_files(moment_mstr_dir, output_dir)


def sheets_input_to_lynx_with_cursor(
    cursor: sqlite3_Cursor, input_dir: str, moment_mstr_dir: str
):
    delete_dir(moment_mstr_dir)
    set_dir(moment_mstr_dir)

    # collect excel file data into central location
    etl_input_dfs_to_brick_raw_tables(cursor, input_dir)
    # brick raw to sound raw, check by spark_nums
    etl_brick_raw_tables_to_brick_agg_tables(cursor)
    etl_brick_agg_tables_to_sparks_brick_agg_table(cursor)
    etl_sparks_brick_agg_table_to_sparks_brick_valid_table(cursor)
    etl_brick_agg_tables_to_brick_valid_tables(cursor)
    etl_brick_valid_tables_to_sound_raw_tables(cursor)
    # sound raw to heard raw, filter through translates
    etl_sound_raw_tables_to_sound_agg_tables(cursor)
    etl_translate_sound_agg_tables_to_translate_sound_vld_tables(cursor)
    etl_sound_agg_tables_to_sound_vld_tables(cursor)
    etl_sound_vld_tables_to_heard_raw_tables(cursor)
    # heard raw stage to sparkized stage: moment/person jsons files
    etl_heard_raw_tables_to_heard_agg_tables(cursor)
    etl_heard_agg_tables_to_heard_vld_tables(cursor)
    etl_heard_vld_tables_to_moment_jsons(cursor, moment_mstr_dir)
    etl_heard_vld_to_spark_person_csvs(cursor, moment_mstr_dir)
    etl_spark_person_csvs_to_lesson_json(moment_mstr_dir)
    etl_spark_lesson_json_to_spark_inherited_personunits(moment_mstr_dir)
    # Sparkized files to Lynx stage
    etl_spark_inherited_personunits_to_moment_gut(moment_mstr_dir)
    add_moment_epoch_to_guts(moment_mstr_dir)
    etl_moment_guts_to_moment_jobs(moment_mstr_dir)
    etl_heard_raw_tables_to_moment_ote1_agg(cursor)
    etl_moment_ote1_agg_table_to_moment_ote1_agg_csvs(cursor, moment_mstr_dir)
    etl_moment_ote1_agg_csvs_to_jsons(moment_mstr_dir)
    calc_moment_bud_partner_mandate_net_ledgers(moment_mstr_dir)
    etl_moment_job_jsons_to_job_tables(cursor, moment_mstr_dir)
    etl_moment_json_partner_nets_to_moment_partner_nets_table(cursor, moment_mstr_dir)
    populate_kpi_bundle(cursor)
    create_last_run_metrics_json(cursor, moment_mstr_dir)


def sheets_input_to_lynx_mstr(world_db_path: str, input_dir: str, moment_mstr_dir: str):
    with sqlite3_connect(world_db_path) as db_conn:
        cursor = db_conn.cursor()
        sheets_input_to_lynx_with_cursor(cursor, input_dir, moment_mstr_dir)
        db_conn.commit()
    db_conn.close()


def stance_sheets_to_lynx_mstr(
    world_db_path: str, input_dir: str, moment_mstr_dir: str
):
    max_brick_agg_spark_num = 0
    if os_path_exists(world_db_path):
        with sqlite3_connect(world_db_path) as db_conn0:
            cursor0 = db_conn0.cursor()
            max_brick_agg_spark_num = get_max_brick_agg_spark_num(cursor0)
        db_conn0.close()
    next_spark_num = max_brick_agg_spark_num + 1
    update_spark_num_in_excel_files(input_dir, next_spark_num)
    sheets_input_to_lynx_mstr(
        world_db_path=world_db_path,
        input_dir=input_dir,
        moment_mstr_dir=moment_mstr_dir,
    )
    delete_dir(input_dir)


@dataclass
class WorldDir:
    world_name: WorldName = None
    worlds_dir: str = None
    output_dir: str = None
    _world_dir: str = None
    _input_dir: str = None
    _brick_dir: str = None
    _moment_mstr_dir: str = None

    def get_world_db_path(self) -> str:
        "Returns path: world_dir/world.db"
        return create_world_db_path(self._world_dir)

    def delete_world_db(self):
        delete_dir(self.get_world_db_path())

    def set_input_dir(self, x_dir: str):
        self._input_dir = x_dir
        set_dir(self._input_dir)

    def _set_world_dirs(self):
        self._world_dir = create_path(self.worlds_dir, self.world_name)
        self._brick_dir = create_path(self._world_dir, "brick")
        self._moment_mstr_dir = create_moment_mstr_path(self._world_dir)
        set_dir(self._world_dir)
        set_dir(self._brick_dir)
        set_dir(self._moment_mstr_dir)


def worlddir_shop(
    world_name: WorldName,
    worlds_dir: str,
    output_dir: str = None,
    input_dir: str = None,
) -> WorldDir:
    x_worlddir = WorldDir(
        world_name=world_name,
        worlds_dir=worlds_dir,
        output_dir=output_dir,
        _input_dir=input_dir,
    )
    x_worlddir._set_world_dirs()
    if not x_worlddir._input_dir:
        x_worlddir.set_input_dir(create_path(x_worlddir._world_dir, "input"))
    return x_worlddir


def sheets_to_gcal_day_reports():
    pass
