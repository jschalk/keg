from dataclasses import dataclass
from datetime import datetime
from os.path import exists as os_path_exists
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect
from src.ch00_py.file_toolbox import create_path, delete_dir, set_dir
from src.ch17_idea.idea_db_tool import export_db_to_excel
from src.ch18_etl_config._ref.ch18_path import (
    create_moment_mstr_path,
    create_world_db_path,
)
from src.ch18_etl_config.belief_tool import create_belief0001_file
from src.ch19_etl_steps.belief2idea import beliefs_sheets_to_idea_sheets
from src.ch19_etl_steps.etl_main import (
    add_moment_epoch_to_guts,
    calc_moment_bud_contact_mandate_net_ledgers,
    create_last_run_metrics_json,
    etl_heard_agg_tables_to_heard_vld_tables,
    etl_heard_raw_tables_to_heard_agg_tables,
    etl_heard_raw_tables_to_moment_ote1_agg,
    etl_heard_vld_tables_to_moment_jsons,
    etl_heard_vld_to_spark_person_csvs,
    etl_idea_dfs_to_ideax_raw_tables,
    etl_ideax_agg_tables_to_ideax_vld_tables,
    etl_ideax_agg_tables_to_sparks_ideax_agg_table,
    etl_ideax_raw_tables_to_ideax_agg_tables,
    etl_ideax_vld_tables_to_sound_raw_tables,
    etl_moment_guts_to_moment_jobs,
    etl_moment_job_jsons_to_job_tables,
    etl_moment_json_contact_nets_to_moment_contact_nets_table,
    etl_moment_ote1_agg_csvs_to_jsons,
    etl_moment_ote1_agg_table_to_moment_ote1_agg_csvs,
    etl_sound_agg_tables_to_sound_vld_tables,
    etl_sound_raw_tables_to_sound_agg_tables,
    etl_sound_vld_tables_to_heard_raw_tables,
    etl_spark_inherited_personunits_to_moment_gut,
    etl_spark_lesson_json_to_spark_inherited_personunits,
    etl_spark_person_csvs_to_lesson_json,
    etl_sparks_ideax_agg_table_to_sparks_ideax_vld_table,
    etl_translate_sound_agg_tables_to_translate_sound_vld_tables,
    get_max_ideax_agg_spark_num,
)
from src.ch20_kpi.gcalendar import (
    copy_person_day_punches_to_dst_dir,
    save_person_gcal_day_punchs,
)
from src.ch20_kpi.kpi_mstr import create_calendar_markdown_files, populate_kpi_bundle
from src.ch21_world._ref.ch21_semantic_types import GroupTitle, PersonName, WorldName


def create_beliefs(
    world_dir: str,
    output_dir: str,
    world_name: str,
    moment_mstr_dir: str,
    prettify_excel_bool=True,
):
    create_belief0001_file(world_dir, output_dir, world_name, prettify_excel_bool)
    create_calendar_markdown_files(moment_mstr_dir, output_dir)


def idea_sheets_to_lynx_with_cursor(
    cursor: sqlite3_Cursor, ideas_src_dir: str, moment_mstr_dir: str
):
    delete_dir(moment_mstr_dir)
    set_dir(moment_mstr_dir)

    # collect excel file data into central location
    etl_idea_dfs_to_ideax_raw_tables(cursor, ideas_src_dir)
    # idea raw to sound raw, check by spark_nums
    etl_ideax_raw_tables_to_ideax_agg_tables(cursor)
    etl_ideax_agg_tables_to_sparks_ideax_agg_table(cursor)
    etl_sparks_ideax_agg_table_to_sparks_ideax_vld_table(cursor)
    etl_ideax_agg_tables_to_ideax_vld_tables(cursor)
    etl_ideax_vld_tables_to_sound_raw_tables(cursor)
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
    calc_moment_bud_contact_mandate_net_ledgers(moment_mstr_dir)
    etl_moment_job_jsons_to_job_tables(cursor, moment_mstr_dir)
    etl_moment_json_contact_nets_to_moment_contact_nets_table(cursor, moment_mstr_dir)
    populate_kpi_bundle(cursor)
    create_last_run_metrics_json(cursor, moment_mstr_dir)


@dataclass
class WorldDir:
    world_name: WorldName = None
    worlds_dir: str = None
    output_dir: str = None
    ideas_src_dir: str = None
    beliefs_src_dir: str = None
    # calculated dirs
    world_dir: str = None
    db_path: str = None
    moment_mstr_dir: str = None

    def get_world_db_path(self) -> str:
        "Returns path: world_dir/world.db"
        return create_world_db_path(self.world_dir)

    def delete_world_db(self):
        delete_dir(self.get_world_db_path())

    def set_ideas_src_dir(self, x_dir: str):
        self.ideas_src_dir = x_dir
        set_dir(self.ideas_src_dir)

    def set_beliefs_src_dir(self, x_dir: str):
        self.beliefs_src_dir = x_dir
        set_dir(self.beliefs_src_dir)

    def _set_world_dirs(self):
        self.world_dir = create_path(self.worlds_dir, self.world_name)
        self.moment_mstr_dir = create_moment_mstr_path(self.world_dir)
        set_dir(self.world_dir)
        set_dir(self.moment_mstr_dir)


def worlddir_shop(
    world_name: WorldName,
    worlds_dir: str,
    output_dir: str = None,
    ideas_src_dir: str = None,
    beliefs_src_dir: str = None,
) -> WorldDir:
    x_worlddir = WorldDir(
        world_name=world_name,
        worlds_dir=worlds_dir,
        output_dir=output_dir,
        ideas_src_dir=ideas_src_dir,
        beliefs_src_dir=beliefs_src_dir,
    )
    x_worlddir._set_world_dirs()
    x_worlddir.db_path = x_worlddir.get_world_db_path()
    if not x_worlddir.output_dir:
        x_worlddir.output_dir = create_path(x_worlddir.world_dir, "output")
    if not x_worlddir.ideas_src_dir:
        x_worlddir.set_ideas_src_dir(create_path(x_worlddir.world_dir, "ideas_src"))
    if not x_worlddir.beliefs_src_dir:
        x_worlddir.set_beliefs_src_dir(create_path(x_worlddir.world_dir, "beliefs_src"))
    return x_worlddir


def idea_sheets_to_lynx_mstr(worlddir: WorldDir, export_db: bool = False):
    with sqlite3_connect(worlddir.db_path) as db_conn:
        cursor = db_conn.cursor()
        idea_sheets_to_lynx_with_cursor(
            cursor, worlddir.ideas_src_dir, worlddir.moment_mstr_dir
        )
        if export_db and worlddir.output_dir:
            set_dir(worlddir.output_dir)
            excel_path = create_path(worlddir.output_dir, "db_export.xlsx")
            export_db_to_excel(cursor, excel_path, True)

        db_conn.commit()
    db_conn.close()


def belief_sheets_to_lynx_mstr(worlddir: WorldDir, export_db: bool = False):
    max_ideax_agg_spark_num = 0
    if os_path_exists(worlddir.db_path):
        with sqlite3_connect(worlddir.db_path) as db_conn0:
            cursor0 = db_conn0.cursor()
            max_ideax_agg_spark_num = get_max_ideax_agg_spark_num(cursor0)
        db_conn0.close()
    beliefs_sheets_to_idea_sheets(
        worlddir.beliefs_src_dir, worlddir.ideas_src_dir, max_ideax_agg_spark_num
    )
    idea_sheets_to_lynx_mstr(worlddir, export_db)


def idea_sheets_to_gcal_day_punchs(
    worlddir: WorldDir,
    person_name: PersonName,
    day: datetime,
    focus_group_title: GroupTitle = None,
):
    belief_sheets_to_lynx_mstr(worlddir, export_db=True)
    save_person_gcal_day_punchs(
        moment_mstr_dir=worlddir.moment_mstr_dir,
        person_name=person_name,
        day=day,
        focus_group_title=focus_group_title,
    )


def create_today_punchs(
    person_name: PersonName,
    world_name: WorldName,
    worlds_dir: str,
    output_dir: str = None,
    ideas_src_dir: str = None,
    beliefs_src_dir: str = None,
    focus_group_title: GroupTitle = None,
):
    worlddir = worlddir_shop(
        world_name=world_name,
        worlds_dir=worlds_dir,
        output_dir=output_dir,
        ideas_src_dir=ideas_src_dir,
        beliefs_src_dir=beliefs_src_dir,
    )
    idea_sheets_to_gcal_day_punchs(
        worlddir=worlddir,
        person_name=person_name,
        day=datetime.now(),
        focus_group_title=focus_group_title,
    )
    copy_person_day_punches_to_dst_dir(
        worlddir.moment_mstr_dir, worlddir.output_dir, person_name
    )
