from ch00_py.file_toolbox import create_path, delete_dir, set_dir
from ch17_brick.brick_db_tool import export_db_to_excel
from ch18_etl_config._ref.ch18_path import create_moment_mstr_path, create_world_db_path
from ch18_etl_config.brick_collector import reorder_etl_db_sheets
from ch19_idea_src.idea2brick import ideas_sheets_to_brick_sheets
from ch20_etl_brick.etl_brick_main import (
    etl_brick_dfs_to_brixk_raw_tables,
    etl_brixk_agg_tables_to_brixk_vld_tables,
    etl_brixk_agg_tables_to_sparks_brixk_agg_table,
    etl_brixk_raw_tables_to_brixk_agg_tables,
    etl_brixk_vld_tables_to_sound_raw_tables,
    etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table,
)
from ch21_sound.sound import (
    etl_sound_agg_tables_to_sound_vld_tables,
    etl_sound_raw_tables_to_sound_agg_tables,
    etl_sound_vld_tables_to_heard_raw_tables,
    etl_translate_sound_agg_tables_to_translate_sound_vld_tables,
)
from ch22_heard.heard import (
    etl_heard_agg_tables_to_heard_vld_tables,
    etl_heard_raw_tables_to_heard_agg_tables,
    etl_heard_raw_tables_to_lego_moment_ote1_agg,
    etl_heard_vld_tables_to_mind_moment_jsons,
    etl_heard_vld_to_lego_spark_person_csvs,
    etl_moment_ote1_agg_table_to_moment_ote1_agg_csvs,
)
from ch27_lego.lego_core import (
    add_lego_epoch_to_mind_guts,
    calc_moment_bud_contact_mandate_net_ledgers,
    create_last_run_metrics_json,
    etl_lego_spark_lesson_json_to_spark_inherited_personunits,
    etl_lego_spark_person_csvs_to_lesson_json,
    etl_mind_guts_to_mind_jobs,
    etl_mind_job_jsons_to_job_tables,
    etl_moment_json_contact_nets_to_moment_tranbook_nets_table,
    etl_moment_ote1_agg_csvs_to_jsons,
    etl_spark_inherited_personunits_to_mind_gut,
    get_max_brixk_agg_spark_num,
)
from ch30_idea_dst.lego_db2df import create_lego0001_file, prettify_excel_file
from ch31_kpi.gcalendar import (
    copy_person_day_punches_to_dst_dir,
    get_day_punchs_persons,
    lego_to_person_gcal_day_punchs,
)
from ch31_kpi.kpi_mstr import create_calendar_markdown_files, populate_kpi_bundle
from ch32_world._ref.ch32_semantic_types import GroupTitle, PersonName, WorldName
from dataclasses import dataclass
from datetime import datetime
from os.path import exists as os_path_exists
from sqlite3 import Cursor as sqlite3_Cursor, connect as sqlite3_connect


def create_ideas(
    world_dir: str,
    output_dir: str,
    world_name: str,
    moment_mstr_dir: str,
    prettify_excel_bool=True,
):
    create_lego0001_file(world_dir, output_dir, world_name, prettify_excel_bool)
    create_calendar_markdown_files(moment_mstr_dir, output_dir)


def brick_sheets_to_lego_with_cursor(
    cursor: sqlite3_Cursor, bricks_src_dir: str, moment_mstr_dir: str
):
    delete_dir(moment_mstr_dir)
    set_dir(moment_mstr_dir)
    # collect excel file data into central location
    etl_brick_dfs_to_brixk_raw_tables(cursor, bricks_src_dir)
    # brick raw to sound raw, check by spark_nums
    etl_brixk_raw_tables_to_brixk_agg_tables(cursor)
    etl_brixk_agg_tables_to_sparks_brixk_agg_table(cursor)
    etl_sparks_brixk_agg_table_to_sparks_brixk_vld_table(cursor)
    etl_brixk_agg_tables_to_brixk_vld_tables(cursor)
    etl_brixk_vld_tables_to_sound_raw_tables(cursor)
    # sound raw to heard raw, filter through translates
    etl_sound_raw_tables_to_sound_agg_tables(cursor)
    etl_translate_sound_agg_tables_to_translate_sound_vld_tables(cursor)
    etl_sound_agg_tables_to_sound_vld_tables(cursor)
    etl_sound_vld_tables_to_heard_raw_tables(cursor)
    # heard raw stage to sparkized stage: moment/person jsons files
    etl_heard_raw_tables_to_heard_agg_tables(cursor)
    etl_heard_agg_tables_to_heard_vld_tables(cursor)
    etl_heard_vld_tables_to_mind_moment_jsons(cursor, moment_mstr_dir)
    etl_heard_vld_to_lego_spark_person_csvs(cursor, moment_mstr_dir)
    etl_lego_spark_person_csvs_to_lesson_json(moment_mstr_dir)
    etl_lego_spark_lesson_json_to_spark_inherited_personunits(moment_mstr_dir)
    # Sparkized files to lego stage
    etl_spark_inherited_personunits_to_mind_gut(moment_mstr_dir)
    add_lego_epoch_to_mind_guts(moment_mstr_dir)
    etl_mind_guts_to_mind_jobs(moment_mstr_dir)
    etl_heard_raw_tables_to_lego_moment_ote1_agg(cursor)
    etl_moment_ote1_agg_table_to_moment_ote1_agg_csvs(cursor, moment_mstr_dir)
    etl_moment_ote1_agg_csvs_to_jsons(moment_mstr_dir)
    calc_moment_bud_contact_mandate_net_ledgers(moment_mstr_dir)
    etl_mind_job_jsons_to_job_tables(cursor, moment_mstr_dir)
    etl_moment_json_contact_nets_to_moment_tranbook_nets_table(cursor, moment_mstr_dir)
    populate_kpi_bundle(cursor)
    create_last_run_metrics_json(cursor, moment_mstr_dir)


@dataclass
class WorldDir:
    world_name: WorldName = None
    worlds_dir: str = None
    output_dir: str = None
    bricks_src_dir: str = None
    ideas_src_dir: str = None
    # calculated dirs
    world_dir: str = None
    db_path: str = None
    moment_mstr_dir: str = None

    def get_world_db_path(self) -> str:
        "Returns path: world_dir/world.db"
        return create_world_db_path(self.world_dir)

    def delete_world_db(self):
        delete_dir(self.get_world_db_path())

    def set_bricks_src_dir(self, x_dir: str):
        self.bricks_src_dir = x_dir
        set_dir(self.bricks_src_dir)

    def set_ideas_src_dir(self, x_dir: str):
        self.ideas_src_dir = x_dir
        set_dir(self.ideas_src_dir)

    def _set_world_dirs(self):
        self.world_dir = create_path(self.worlds_dir, self.world_name)
        self.moment_mstr_dir = create_moment_mstr_path(self.world_dir)
        set_dir(self.world_dir)
        set_dir(self.moment_mstr_dir)


def worlddir_shop(
    world_name: WorldName,
    worlds_dir: str,
    output_dir: str = None,
    bricks_src_dir: str = None,
    ideas_src_dir: str = None,
) -> WorldDir:
    x_worlddir = WorldDir(
        world_name=world_name,
        worlds_dir=worlds_dir,
        output_dir=output_dir,
        bricks_src_dir=bricks_src_dir,
        ideas_src_dir=ideas_src_dir,
    )
    x_worlddir._set_world_dirs()
    x_worlddir.db_path = x_worlddir.get_world_db_path()
    if not x_worlddir.output_dir:
        x_worlddir.output_dir = create_path(x_worlddir.world_dir, "output")
    if not x_worlddir.bricks_src_dir:
        x_worlddir.set_bricks_src_dir(create_path(x_worlddir.world_dir, "bricks_src"))
    if not x_worlddir.ideas_src_dir:
        x_worlddir.set_ideas_src_dir(create_path(x_worlddir.world_dir, "ideas_src"))
    return x_worlddir


def brick_sheets_to_lego_mstr(worlddir: WorldDir, export_db: bool = False):
    with sqlite3_connect(worlddir.db_path) as db_conn:
        cursor = db_conn.cursor()
        brick_sheets_to_lego_with_cursor(
            cursor, worlddir.bricks_src_dir, worlddir.moment_mstr_dir
        )
        if export_db and worlddir.output_dir:
            set_dir(worlddir.output_dir)
            excel_path = create_path(worlddir.output_dir, "db_export.xlsx")
            export_db_to_excel(cursor, excel_path, True)
            reorder_etl_db_sheets(excel_path)
            prettify_excel_file(excel_path)

        db_conn.commit()
    db_conn.close()


def idea_sheets_to_lego_mstr(worlddir: WorldDir, export_db: bool = False):
    max_brixk_agg_spark_num = 0
    if os_path_exists(worlddir.db_path):
        with sqlite3_connect(worlddir.db_path) as db_conn0:
            cursor0 = db_conn0.cursor()
            max_brixk_agg_spark_num = get_max_brixk_agg_spark_num(cursor0)
        db_conn0.close()
    ideas_sheets_to_brick_sheets(
        worlddir.ideas_src_dir, worlddir.bricks_src_dir, max_brixk_agg_spark_num
    )
    brick_sheets_to_lego_mstr(worlddir, export_db)


def idea_sheets_to_gcal_day_punchs(
    worlddir: WorldDir,
    person_names: set[PersonName],
    day: datetime,
    focus_group_title: GroupTitle = None,
):
    idea_sheets_to_lego_mstr(worlddir, export_db=True)
    for person_name in sorted(person_names):
        lego_to_person_gcal_day_punchs(
            world_dir=worlddir.world_dir,
            person_name=person_name,
            day=day,
            focus_group_title=focus_group_title,
        )


def create_today_punchs(
    person_names: set[PersonName],
    world_name: WorldName,
    worlds_dir: str,
    output_dir: str = None,
    bricks_src_dir: str = None,
    ideas_src_dir: str = None,
    focus_group_title: GroupTitle = None,
) -> dict[PersonName, set]:
    worlddir = worlddir_shop(
        world_name=world_name,
        worlds_dir=worlds_dir,
        output_dir=output_dir,
        bricks_src_dir=bricks_src_dir,
        ideas_src_dir=ideas_src_dir,
    )
    idea_sheets_to_gcal_day_punchs(
        worlddir=worlddir,
        person_names=person_names,
        day=datetime.now(),
        focus_group_title=focus_group_title,
    )
    all_persons = get_day_punchs_persons(worlddir.moment_mstr_dir)
    dst_persons_punch_paths = {}
    for person_name in all_persons:
        dst_person_punch_paths = copy_person_day_punches_to_dst_dir(
            worlddir.moment_mstr_dir, worlddir.output_dir, person_name
        )
        dst_persons_punch_paths[person_name] = dst_person_punch_paths
    return dst_persons_punch_paths
