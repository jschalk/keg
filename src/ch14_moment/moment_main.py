from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch00_py.dict_toolbox import get_0_if_None, get_empty_set_if_None
from src.ch00_py.file_toolbox import create_path, get_dir_file_strs, open_json, set_dir
from src.ch01_allot.allot import default_grain_num_if_None
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch09_person_lesson._ref.ch09_path import (
    create_moment_dir_path,
    create_moment_json_path,
)
from src.ch09_person_lesson.lasso import LassoUnit, lassounit_shop
from src.ch09_person_lesson.lesson_filehandler import (
    gut_file_exists,
    open_gut_file,
    save_gut_file,
)
from src.ch10_person_listen.basis_person import create_listen_basis
from src.ch10_person_listen.keep_tool import (
    create_treasury_db_file,
    open_job_file,
    save_duty_person,
    save_job_file,
)
from src.ch10_person_listen.listen_main import (
    listen_to_agendas_create_init_job_from_guts,
    listen_to_debtors_roll_jobs_into_job,
)
from src.ch11_bud._ref.ch11_path import create_cell_dir_path
from src.ch11_bud.bud_filehandler import cellunit_save_to_dir
from src.ch11_bud.bud_main import (
    BudUnit,
    PersonBudHistory,
    TranBook,
    TranUnit,
    get_personbudhistory_from_dict,
    get_tranbook_from_dict,
    personbudhistory_shop,
    tranbook_shop,
)
from src.ch11_bud.cell_main import cellunit_shop
from src.ch13_time.epoch_main import (
    EpochUnit,
    TimeNum,
    add_epoch_planunit,
    epochunit_shop,
)
from src.ch14_moment._ref.ch14_semantic_types import (
    FundGrain,
    FundNum,
    KnotTerm,
    ManaGrain,
    MomentRope,
    PartnerName,
    PersonName,
    RespectGrain,
    SparkInt,
    default_knot_if_None,
)


def get_default_job_listen_count() -> int:
    return 3


class BudUnitError(Exception):
    pass


class SetOffiTimeMaxError(Exception):
    pass


@dataclass
class MomentUnit:
    """Data pipelines:
    pipeline1: lessons->gut
    pipeline2: gut->dutys
    pipeline3: duty->vision
    pipeline4: vision->job
    pipeline5: gut->job (direct)
    pipeline6: gut->vision->job (through visions)
    pipeline7: lessons->job (could be 5 of 6)
    """

    moment_rope: MomentRope = None
    moment_mstr_dir: str = None
    epoch: EpochUnit = None
    personbudhistorys: dict[PersonName, PersonBudHistory] = None
    paybook: TranBook = None
    offi_times: set[TimeNum] = None
    knot: KnotTerm = None
    fund_grain: FundGrain = None
    respect_grain: RespectGrain = None
    mana_grain: ManaGrain = None
    job_listen_rotations: int = None
    # calculated fields
    offi_time_max: TimeNum = None
    moment_dir: str = None
    persons_dir: str = None
    lessons_dir: str = None
    all_tranbook: TranBook = None

    # directory setup
    def get_lasso(self) -> LassoUnit:
        return lassounit_shop(self.moment_rope, self.knot)

    def _set_moment_dirs(self):
        self.moment_dir = create_moment_dir_path(self.moment_mstr_dir, self.get_lasso())
        self.persons_dir = create_path(self.moment_dir, "persons")
        self.lessons_dir = create_path(self.moment_dir, "lessons")
        set_dir(x_path=self.moment_dir)
        set_dir(x_path=self.persons_dir)
        set_dir(x_path=self.lessons_dir)

    def _get_person_dir(self, person_name) -> str:
        return create_path(self.persons_dir, person_name)

    def _get_person_dir_names(self) -> set:
        persons = get_dir_file_strs(
            self.persons_dir, include_dirs=True, include_files=False
        )
        return sorted(list(persons.keys()))

    # person administration
    def _set_all_healer_dutys(self, person_name: PersonName):
        x_gut = open_gut_file(self.moment_mstr_dir, self.get_lasso(), person_name)
        x_gut.conpute()
        for healer_name, healer_dict in x_gut._healers_dict.items():
            for keep_rope in healer_dict.keys():
                create_treasury_db_file(
                    self.moment_mstr_dir,
                    person_name=person_name,
                    moment_rope=self.moment_rope,
                    keep_rope=keep_rope,
                    knot=self.knot,
                )
                save_duty_person(
                    moment_mstr_dir=self.moment_mstr_dir,
                    person_name=healer_name,
                    moment_rope=self.moment_rope,
                    keep_rope=keep_rope,
                    knot=None,
                    duty_person=x_gut,
                )

    # job person administration
    def create_empty_person_from_moment(self, person_name: PersonName) -> PersonUnit:
        return personunit_shop(
            person_name,
            self.moment_rope,
            knot=self.knot,
            fund_grain=self.fund_grain,
            respect_grain=self.respect_grain,
            mana_grain=self.mana_grain,
        )

    def create_gut_file_if_none(self, person_name: PersonName) -> None:
        if not gut_file_exists(self.moment_mstr_dir, self.get_lasso(), person_name):
            empty_person = self.create_empty_person_from_moment(person_name)
            save_gut_file(self.moment_mstr_dir, empty_person)

    def create_init_job_from_guts(self, person_name: PersonName) -> None:
        self.create_gut_file_if_none(person_name)
        x_gut = open_gut_file(self.moment_mstr_dir, self.get_lasso(), person_name)
        x_job = create_listen_basis(x_gut)
        listen_to_agendas_create_init_job_from_guts(self.moment_mstr_dir, x_job)
        save_job_file(self.moment_mstr_dir, x_job)

    def rotate_job(self, person_name: PersonName) -> PersonUnit:
        x_job = open_job_file(self.moment_mstr_dir, self.get_lasso(), person_name)
        x_job.conpute()
        # # if personunit has healers create job from healers.
        # create personunit from debtors roll
        mstr_dir = self.moment_mstr_dir
        return listen_to_debtors_roll_jobs_into_job(
            mstr_dir, self.get_lasso(), person_name
        )

    def generate_all_jobs(self) -> None:
        person_names = self._get_person_dir_names()
        for person_name in person_names:
            self.create_init_job_from_guts(person_name)

        for _ in range(self.job_listen_rotations):
            for person_name in person_names:
                save_job_file(self.moment_mstr_dir, self.rotate_job(person_name))

    def get_job_file_person(self, person_name: PersonName) -> PersonUnit:
        return open_job_file(self.moment_mstr_dir, self.get_lasso(), person_name)

    # personbudhistorys
    def set_personbudhistory(self, x_personbudhistory: PersonBudHistory) -> None:
        self.personbudhistorys[x_personbudhistory.person_name] = x_personbudhistory

    def personbudhistory_exists(self, x_person_name: PersonName) -> bool:
        return self.personbudhistorys.get(x_person_name) != None

    def get_personbudhistory(self, x_person_name: PersonName) -> PersonBudHistory:
        return self.personbudhistorys.get(x_person_name)

    def del_personbudhistory(self, x_person_name: PersonName) -> None:
        self.personbudhistorys.pop(x_person_name)

    def add_budunit(
        self,
        person_name: PersonName,
        bud_time: TimeNum,
        quota: int,
        allow_prev_to_offi_time_max_entry: bool = False,
        celldepth: int = None,
    ):
        self.offi_time_max = get_0_if_None(self.offi_time_max)
        if bud_time < self.offi_time_max and not allow_prev_to_offi_time_max_entry:
            exception_str = f"Cannot set budunit because bud_time {bud_time} is less than MomentUnit.offi_time_max {self.offi_time_max}."
            raise BudUnitError(exception_str)
        if self.personbudhistory_exists(person_name) is False:
            self.set_personbudhistory(personbudhistory_shop(person_name))
        x_personbudhistory = self.get_personbudhistory(person_name)
        x_personbudhistory.add_bud(bud_time, quota, celldepth)

    def bud_quota_exists(
        self,
        person_name: PersonName,
        bud_time: TimeNum,
        quota: int,
    ) -> bool:
        personbudhistory = self.get_personbudhistory(person_name)
        if not personbudhistory:
            return False
        budunit = personbudhistory.get_bud(bud_time)
        return budunit.quota == quota if budunit else False

    def get_budunit(self, person_name: PersonName, bud_time: TimeNum) -> BudUnit:
        if not self.get_personbudhistory(person_name):
            return None
        x_personbudhistory = self.get_personbudhistory(person_name)
        return x_personbudhistory.get_bud(bud_time)

    def to_dict(self, include_paybook: bool = True) -> dict:
        """Returns dict that is serializable to JSON."""

        x_dict = {
            "moment_rope": self.moment_rope,
            "moment_mstr_dir": self.moment_mstr_dir,
            "knot": self.knot,
            "fund_grain": self.fund_grain,
            "mana_grain": self.mana_grain,
            "personbudhistorys": self._get_personbudhistorys_dict(),
            "respect_grain": self.respect_grain,
            "epoch": self.epoch.to_dict(),
            "offi_times": list(self.offi_times),
        }
        if include_paybook:
            x_dict["paybook"] = self.paybook.to_dict()
        return x_dict

    def _get_personbudhistorys_dict(self) -> dict[PersonName, dict]:
        return {
            x_bud.person_name: x_bud.to_dict()
            for x_bud in self.personbudhistorys.values()
        }

    def get_personbudhistorys_bud_times(self) -> set[TimeNum]:
        all_budunit_bud_times = set()
        for x_personbudhistory in self.personbudhistorys.values():
            all_budunit_bud_times.update(x_personbudhistory.get_bud_times())
        return all_budunit_bud_times

    def set_paypurchase(self, x_paypurchase: TranUnit):
        self.paybook.set_tranunit(
            tranunit=x_paypurchase,
            blocked_tran_times=self.get_personbudhistorys_bud_times(),
            offi_time_max=self.offi_time_max,
        )

    def add_paypurchase(
        self,
        person_name: PersonName,
        partner_name: PartnerName,
        tran_time: TimeNum,
        amount: FundNum,
        blocked_tran_times: set[TimeNum] = None,
        offi_time_max: TimeNum = None,
    ) -> None:
        self.paybook.add_tranunit(
            person_name=person_name,
            partner_name=partner_name,
            tran_time=tran_time,
            amount=amount,
            blocked_tran_times=blocked_tran_times,
            offi_time_max=offi_time_max,
        )

    def paypurchase_exists(
        self, src: PersonName, dst: PartnerName, x_tran_time: TimeNum
    ) -> bool:
        return self.paybook.tranunit_exists(src, dst, x_tran_time)

    def get_paypurchase(
        self, src: PersonName, dst: PartnerName, x_tran_time: TimeNum
    ) -> TranUnit:
        return self.paybook.get_tranunit(src, dst, x_tran_time)

    def del_paypurchase(
        self, src: PersonName, dst: PartnerName, x_tran_time: TimeNum
    ) -> TranUnit:
        return self.paybook.del_tranunit(src, dst, x_tran_time)

    def clear_paypurchases(self):
        self.paybook = tranbook_shop(self.moment_rope)

    # def set_offi_time(self, offi_time: TimeNum):
    #     self.offi_time = offi_time
    #     if self.offi_time_max < self.offi_time:
    #         self.offi_time_max = self.offi_time

    def set_offi_time_max(self, x_offi_time_max: TimeNum):
        x_tran_times = self.paybook.get_tran_times()
        if x_tran_times != set() and max(x_tran_times) >= x_offi_time_max:
            exception_str = f"Cannot set offi_time_max {x_offi_time_max}, paypurchase with greater tran_time exists"
            raise SetOffiTimeMaxError(exception_str)
        # if self.offi_time > x_offi_time_max:
        #     exception_str = f"Cannot set offi_time_max={x_offi_time_max} because it is less than offi_time={self.offi_time}"
        #     raise SetOffiTimeMaxError(exception_str)
        self.offi_time_max = x_offi_time_max

    # def set_offi_time(
    #     self, offi_time: TimeNum, offi_time_max: TimeNum
    # ):
    #     self.set_offi_time(offi_time)
    #     self.set_offi_time_max(_offi_time_max)

    def set_all_tranbook(self) -> None:
        x_tranunits = copy_deepcopy(self.paybook.tranunits)
        x_tranbook = tranbook_shop(self.moment_rope, x_tranunits)
        for person_name, x_personbudhistory in self.personbudhistorys.items():
            for x_bud_time, x_budunit in x_personbudhistory.buds.items():
                for partner_name, x_amount in x_budunit.bud_partner_nets.items():
                    x_tranbook.add_tranunit(
                        person_name, partner_name, x_bud_time, x_amount
                    )
        self.all_tranbook = x_tranbook

    def create_buds_root_cells(
        self,
        ote1_dict: dict[PersonName, dict[TimeNum, SparkInt]],
    ) -> None:
        for person_name, personbudhistory in self.personbudhistorys.items():
            for bud_time in personbudhistory.buds.keys():
                self._create_bud_root_cell(person_name, ote1_dict, bud_time)

    def _create_bud_root_cell(
        self,
        person_name: PersonName,
        ote1_dict: dict[PersonName, dict[TimeNum, SparkInt]],
        bud_time: TimeNum,
    ) -> None:
        past_spark_num = _get_ote1_max_past_spark_num(person_name, ote1_dict, bud_time)
        budunit = self.get_budunit(person_name, bud_time)
        cellunit = cellunit_shop(
            bud_person_name=person_name,
            ancestors=[],
            spark_num=past_spark_num,
            celldepth=budunit.celldepth,
            quota=budunit.quota,
            mana_grain=self.mana_grain,
        )
        root_cell_dir = create_cell_dir_path(
            self.moment_mstr_dir, self.get_lasso(), person_name, bud_time, []
        )
        cellunit_save_to_dir(root_cell_dir, cellunit)

    def get_epoch_config(self) -> dict:
        return self.epoch.to_dict()

    def add_epoch_to_gut(self, person_name: PersonName) -> None:
        """Adds the epoch to the gut file for the given person."""
        x_gut = open_gut_file(self.moment_mstr_dir, self.get_lasso(), person_name)
        add_epoch_planunit(x_gut, self.get_epoch_config())
        save_gut_file(self.moment_mstr_dir, x_gut)

    def add_epoch_to_guts(self) -> None:
        """Adds the epoch to all gut files."""
        person_names = self._get_person_dir_names()
        for person_name in person_names:
            self.add_epoch_to_gut(person_name)


def _get_ote1_max_past_spark_num(
    person_name: str, ote1_dict: dict[str, dict[str, int]], bud_time: int
) -> SparkInt:
    """Using the grab most recent ote1 spark int before a given bud_time"""
    ote1_person_dict = ote1_dict.get(person_name)
    if not ote1_person_dict:
        return None
    spark_timenums = set(ote1_person_dict.keys())
    if past_timenums := {tp for tp in spark_timenums if int(tp) <= bud_time}:
        max_past_timenum = max(past_timenums)
        return ote1_person_dict.get(max_past_timenum)


def momentunit_shop(
    moment_rope: MomentRope,
    moment_mstr_dir: str,
    epoch: EpochUnit = None,
    offi_times: set[TimeNum] = None,
    knot: KnotTerm = None,
    fund_grain: float = None,
    respect_grain: float = None,
    mana_grain: float = None,
    job_listen_rotations: int = None,
) -> MomentUnit:
    if epoch is None:
        epoch = epochunit_shop()
    if not job_listen_rotations:
        job_listen_rotations = get_default_job_listen_count()
    x_momentunit = MomentUnit(
        moment_rope=moment_rope,
        moment_mstr_dir=moment_mstr_dir,
        epoch=epoch,
        personbudhistorys={},
        paybook=tranbook_shop(moment_rope),
        offi_times=get_empty_set_if_None(offi_times),
        knot=default_knot_if_None(knot),
        fund_grain=default_grain_num_if_None(fund_grain),
        respect_grain=default_grain_num_if_None(respect_grain),
        mana_grain=default_grain_num_if_None(mana_grain),
        all_tranbook=tranbook_shop(moment_rope),
        job_listen_rotations=job_listen_rotations,
    )
    if x_momentunit.moment_mstr_dir:
        x_momentunit._set_moment_dirs()
    return x_momentunit


def _get_personbudhistorys_from_dict(
    personbudhistorys_dict: dict,
) -> dict[PersonName, PersonBudHistory]:
    return {
        x_person_name: get_personbudhistory_from_dict(personbudhistory_dict)
        for x_person_name, personbudhistory_dict in personbudhistorys_dict.items()
    }


def get_momentunit_from_dict(moment_dict: dict) -> MomentUnit:
    x_moment_rope = moment_dict.get("moment_rope")
    x_moment = momentunit_shop(
        moment_rope=x_moment_rope,
        moment_mstr_dir=moment_dict.get("moment_mstr_dir"),
        offi_times=set(moment_dict.get("offi_times")),
        knot=moment_dict.get("knot"),
        fund_grain=moment_dict.get("fund_grain"),
        respect_grain=moment_dict.get("respect_grain"),
        mana_grain=moment_dict.get("mana_grain"),
    )
    moment_dict_epoch_value = moment_dict.get("epoch")
    if moment_dict_epoch_value:
        x_moment.epoch = epochunit_shop(moment_dict_epoch_value)
    else:
        x_moment.epoch = epochunit_shop(None)
    x_moment.personbudhistorys = _get_personbudhistorys_from_dict(
        moment_dict.get("personbudhistorys")
    )
    x_moment.paybook = get_tranbook_from_dict(moment_dict.get("paybook"))
    return x_moment


def get_default_path_momentunit(
    moment_mstr_dir: str, moment_lasso: LassoUnit
) -> MomentUnit:
    moment_json_path = create_moment_json_path(moment_mstr_dir, moment_lasso)
    x_momentunit = get_momentunit_from_dict(open_json(moment_json_path))
    x_momentunit.moment_mstr_dir = moment_mstr_dir
    x_momentunit._set_moment_dirs()
    return x_momentunit
