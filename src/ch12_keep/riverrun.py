from ch00_py.dict_toolbox import (
    get_0_if_None,
    get_empty_dict_if_None,
    get_positive_int,
    set_in_nested_dict,
)
from ch00_py.file_toolbox import save_json
from ch01_allot.allot import allot_scale, default_grain_num_if_None, validate_pool_num
from ch10_person_listen._ref.ch10_path import create_keep_grade_path
from ch12_keep._ref.ch12_semantic_types import (
    ContactName,
    KnotTerm,
    LabelTerm,
    ManaGrain,
    ManaNum,
    PersonName,
    RopeTerm,
    default_knot_if_None,
)
from ch12_keep.rivercycle import (
    RiverGrade,
    create_init_rivercycle,
    create_next_rivercycle,
    rivergrade_shop,
)
from dataclasses import dataclass


@dataclass
class RiverRun:
    moment_mstr_dir: str = None
    moment_rope: RopeTerm = None
    person_name: PersonName = None
    keep_rope: RopeTerm = None
    knot: KnotTerm = None
    keep_point_magnitude: ManaNum = None
    mana_grain: ManaGrain = None
    number: int = None
    keep_patientledgers: dict[PersonName : dict[ContactName, float]] = None
    need_dues: dict[ContactName, float] = None
    cycle_max: int = None
    # calculated fields
    cares: dict[ContactName, float] = None
    need_yields: dict[ContactName, float] = None
    need_got_prev: float = None
    need_got_curr: float = None
    cycle_count: int = None
    cycle_carees_prev: set = None
    cycle_carees_curr: set = None
    doctor_count: int = None
    patient_count: int = None
    rivergrades: dict[ContactName, RiverGrade] = None

    def set_cycle_max(self, x_cycle_max: int):
        self.cycle_max = get_positive_int(x_cycle_max)

    def set_keep_patientledger(
        self,
        person_name: PersonName,
        contact_name: ContactName,
        mana_ledger: float,
    ):
        set_in_nested_dict(
            x_dict=self.keep_patientledgers,
            x_keylist=[person_name, contact_name],
            x_obj=mana_ledger,
        )

    def delete_keep_patientledgers_person(self, person_name: PersonName):
        self.keep_patientledgers.pop(person_name)

    def get_all_keep_patientledger_contact_names(self):
        x_set = set()
        for person_name, person_dict in self.keep_patientledgers.items():
            if person_name not in x_set:
                x_set.add(person_name)
            for contact_name in person_dict.keys():
                if contact_name not in x_set:
                    x_set.add(contact_name)
        return x_set

    def levy_need_dues(self, cycleledger: tuple[dict[ContactName, float], float]):
        delete_from_cycleledger = []
        need_got_total = 0
        for caree, caree_amount in cycleledger.items():
            if self.contact_has_need_due(caree):
                excess_carer_points, need_got = self.levy_need_due(caree, caree_amount)
                need_got_total += need_got
                if excess_carer_points == 0:
                    delete_from_cycleledger.append(caree)
                else:
                    cycleledger[caree] = excess_carer_points

        for caree_to_delete in delete_from_cycleledger:
            cycleledger.pop(caree_to_delete)
        return cycleledger, need_got_total

    def set_contact_need_due(self, x_contact_name: ContactName, need_due: float):
        self.need_dues[x_contact_name] = need_due

    def need_dues_unpaid(self) -> bool:
        return len(self.need_dues) != 0

    def set_need_dues(self, doctorledger: dict[ContactName, float]):
        x_amount = self.keep_point_magnitude
        self.need_dues = allot_scale(doctorledger, x_amount, self.mana_grain)

    def contact_has_need_due(self, x_contact_name: ContactName) -> bool:
        return self.need_dues.get(x_contact_name) is not None

    def get_contact_need_due(self, x_contact_name: ContactName) -> float:
        x_need_due = self.need_dues.get(x_contact_name)
        return 0 if x_need_due is None else x_need_due

    def delete_need_due(self, x_contact_name: ContactName):
        self.need_dues.pop(x_contact_name)

    def levy_need_due(self, x_contact_name: ContactName, carer_points: float) -> float:
        if self.contact_has_need_due(x_contact_name) is False:
            return carer_points, 0
        x_need_due = self.get_contact_need_due(x_contact_name)
        if x_need_due > carer_points:
            left_over_care = x_need_due - carer_points
            self.set_contact_need_due(x_contact_name, left_over_care)
            self.add_contact_need_yield(x_contact_name, carer_points)
            return 0, carer_points
        else:
            self.delete_need_due(x_contact_name)
            self.add_contact_need_yield(x_contact_name, x_need_due)
            return carer_points - x_need_due, x_need_due

    def get_ledger_dict(self) -> dict[ContactName, float]:
        return self.need_dues

    def set_contact_need_yield(self, x_contact_name: ContactName, need_yield: float):
        self.need_yields[x_contact_name] = need_yield

    def need_yields_is_empty(self) -> bool:
        return len(self.need_yields) == 0

    def reset_need_yields(self):
        self.need_yields = {}

    def contact_has_need_yield(self, x_contact_name: ContactName) -> bool:
        return self.need_yields.get(x_contact_name) is not None

    def get_contact_need_yield(self, x_contact_name: ContactName) -> float:
        x_need_yield = self.need_yields.get(x_contact_name)
        return 0 if x_need_yield is None else x_need_yield

    def delete_need_yield(self, x_contact_name: ContactName):
        self.need_yields.pop(x_contact_name)

    def add_contact_need_yield(self, x_contact_name: ContactName, x_need_yield: float):
        if self.contact_has_need_yield(x_contact_name):
            x_need_yield = self.get_contact_need_yield(x_contact_name) + x_need_yield
        self.set_contact_need_yield(x_contact_name, x_need_yield)

    def get_rivergrade(self, contact_name: ContactName) -> RiverGrade:
        return self.rivergrades.get(contact_name)

    def rivergrades_is_empty(self) -> bool:
        return self.rivergrades == {}

    def rivergrade_exists(self, contact_name: ContactName) -> bool:
        return self.rivergrades.get(contact_name) is not None

    def _get_contact_care(self, contact_name: ContactName) -> float:
        return get_0_if_None(self.cares.get(contact_name))

    def set_initial_rivergrade(self, contact_name: ContactName):
        x_rivergrade = rivergrade_shop(
            self.moment_rope,
            self.person_name,
            self.keep_rope,
            contact_name,
            self.number,
        )
        x_rivergrade.doctor_count = self.doctor_count
        x_rivergrade.patient_count = self.patient_count
        x_rivergrade.care_amount = self._get_contact_care(contact_name)
        self.rivergrades[contact_name] = x_rivergrade

    def set_all_initial_rivergrades(self):
        self.rivergrades = {}
        all_contact_names = self.get_all_keep_patientledger_contact_names()
        for contact_name in all_contact_names:
            self.set_initial_rivergrade(contact_name)

    def _set_post_loop_rivergrade_attrs(self):
        for x_contact_name, contact_rivergrade in self.rivergrades.items():
            need_due_leftover = self.get_contact_need_due(x_contact_name)
            need_due_paid = self.get_contact_need_yield(x_contact_name)
            contact_rivergrade.set_need_bill_amount(need_due_paid + need_due_leftover)
            contact_rivergrade.set_need_paid_amount(need_due_paid)

    def calc_metrics(self):
        self._set_doctor_count_patient_count()
        self._set_cares()
        self.set_all_initial_rivergrades()

        self.cycle_count = 0
        x_rivercyle = create_init_rivercycle(self.person_name, self.keep_patientledgers)
        x_cyclelegder = x_rivercyle.create_cylceledger()
        self.cycle_carees_curr = set(x_cyclelegder.keys())
        x_cyclelegder, need_got_curr = self.levy_need_dues(x_cyclelegder)
        self._set_need_got_attrs(need_got_curr)

        while self.cycle_max > self.cycle_count and self.cycles_vary():
            x_rivercyle = create_next_rivercycle(x_rivercyle, x_cyclelegder)
            x_cyclelegder, need_got_curr = self.levy_need_dues(x_cyclelegder)

            self._set_need_got_attrs(need_got_curr)
            self.cycle_carees_prev = self.cycle_carees_curr
            self.cycle_carees_curr = set(x_cyclelegder.keys())
            self.cycle_count += 1

        self._set_post_loop_rivergrade_attrs()

    def _set_doctor_count_patient_count(self):
        need_dues_contacts = set(self.need_dues.keys())
        need_yields_contacts = set(self.need_yields.keys())
        self.doctor_count = len(need_dues_contacts.union(need_yields_contacts))
        self.patient_count = len(self.keep_patientledgers.get(self.person_name))

    def _set_cares(self):
        care_patientledger = self.keep_patientledgers.get(self.person_name)
        self.cares = allot_scale(
            ledger=care_patientledger,
            scale_number=self.keep_point_magnitude,
            grain_unit=self.mana_grain,
        )

    def _save_rivergrade_file(self, contact_name: ContactName):
        rivergrade = self.get_rivergrade(contact_name)
        grade_path = create_keep_grade_path(
            moment_mstr_dir=self.moment_mstr_dir,
            person_name=self.person_name,
            moment_rope=self.moment_rope,
            keep_rope=self.keep_rope,
            knot=self.knot,
            grade_person_name=contact_name,
        )
        save_json(grade_path, None, rivergrade.to_dict())

    def save_rivergrade_files(self):
        for rivergrade_contact in self.rivergrades.keys():
            self._save_rivergrade_file(rivergrade_contact)

    def _cycle_carees_vary(self) -> bool:
        return self.cycle_carees_prev != self.cycle_carees_curr

    def _set_need_got_attrs(self, x_need_got_curr: float):
        self.need_got_prev = self.need_got_curr
        self.need_got_curr = x_need_got_curr

    def _need_gotten(self) -> bool:
        return max(self.need_got_prev, self.need_got_curr) > 0

    def cycles_vary(self) -> bool:
        return self._need_gotten() or self._cycle_carees_vary()


def riverrun_shop(
    moment_mstr_dir: str,
    moment_rope: RopeTerm,
    person_name: PersonName,
    keep_rope: RopeTerm = None,
    knot: KnotTerm = None,
    keep_point_magnitude: ManaNum = None,
    mana_grain: ManaGrain = None,
    number: int = None,
    keep_patientledgers: dict[PersonName : dict[ContactName, float]] = None,
    need_dues: dict[ContactName, float] = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        moment_mstr_dir=moment_mstr_dir,
        moment_rope=moment_rope,
        person_name=person_name,
        keep_rope=keep_rope,
        knot=default_knot_if_None(knot),
        keep_point_magnitude=validate_pool_num(keep_point_magnitude),
        mana_grain=default_grain_num_if_None(mana_grain),
        number=get_0_if_None(number),
        keep_patientledgers=get_empty_dict_if_None(keep_patientledgers),
        need_dues=get_empty_dict_if_None(need_dues),
        rivergrades={},
        cares={},
        need_yields={},
    )
    x_riverun.cycle_count = 0
    x_riverun.cycle_carees_prev = set()
    x_riverun.cycle_carees_curr = set()
    x_riverun.need_got_prev = 0
    x_riverun.need_got_curr = 0
    if cycle_max is None:
        cycle_max = 10
    x_riverun.set_cycle_max(cycle_max)
    return x_riverun
