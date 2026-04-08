from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch00_py.dict_toolbox import (
    get_0_if_None,
    get_1_if_None,
    get_empty_dict_if_None,
    get_empty_list_if_None,
)
from src.ch01_allot.allot import allot_scale
from src.ch05_reason.reason_main import (
    FactUnit,
    get_dict_from_factunits,
    get_factunits_from_dict,
)
from src.ch07_person_logic.person_main import (
    PersonUnit,
    get_personunit_from_dict,
    personunit_shop,
)
from src.ch07_person_logic.person_tool import (
    clear_factunits_from_person,
    get_contact_mandate_ledger,
    get_credit_ledger,
    get_person_root_facts_dict as get_facts_dict,
)
from src.ch11_bud._ref.ch11_semantic_types import (
    FundNum,
    ManaGrain,
    PersonName,
    RopeTerm,
    SparkInt,
)

CELLNODE_QUOTA_DEFAULT = 1000


@dataclass
class CellUnit:
    ancestors: list[PersonName] = None
    spark_num: SparkInt = None
    celldepth: int = None
    bud_person_name: PersonName = None
    mana_grain: ManaGrain = None
    quota: float = None
    mandate: float = None
    personadjust: PersonUnit = None
    personspark_facts: dict[RopeTerm, FactUnit] = None
    found_facts: dict[RopeTerm, FactUnit] = None
    boss_facts: dict[RopeTerm, FactUnit] = None
    reason_contexts: set[RopeTerm] = None
    contact_mandate_ledger: dict[PersonName, FundNum] = None

    def get_cell_person_name(self) -> PersonName:
        return self.bud_person_name if self.ancestors == [] else self.ancestors[-1]

    def eval_personspark(self, x_person: PersonUnit):
        if not x_person:
            self.personadjust = None
            self.personspark_facts = {}
            self.reason_contexts = set()
        else:
            self._load_existing_personspark(x_person)

    def _load_existing_personspark(self, x_person: PersonUnit):
        self.reason_contexts = x_person.get_reason_contexts()
        self.personspark_facts = get_factunits_from_dict(get_facts_dict(x_person))
        y_person = copy_deepcopy(x_person)
        clear_factunits_from_person(y_person)
        y_person.conpute()
        self.personadjust = y_person

    def get_personsparks_credit_ledger(self) -> dict[PersonName, float]:
        return {} if self.personadjust is None else get_credit_ledger(self.personadjust)

    def get_personsparks_quota_ledger(self) -> dict[PersonName, float]:
        if not self.personadjust:
            return None
        credit_ledger = self.get_personsparks_credit_ledger()
        return allot_scale(credit_ledger, self.quota, self.mana_grain)

    def set_personspark_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.personspark_facts = get_factunits_from_dict(fact_dict)

    def set_found_facts_from_dict(self, fact_dict: dict[RopeTerm, dict]):
        self.found_facts = get_factunits_from_dict(fact_dict)

    def set_boss_facts_from_other_facts(self):
        self.boss_facts = copy_deepcopy(self.personspark_facts)
        for x_fact in self.found_facts.values():
            self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def add_other_facts_to_boss_facts(self):
        for x_fact in self.found_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)
        for x_fact in self.personspark_facts.values():
            if not self.boss_facts.get(x_fact.fact_context):
                self.boss_facts[x_fact.fact_context] = copy_deepcopy(x_fact)

    def filter_facts_by_reason_contexts(self):
        to_delete_personspark_fact_keys = set(self.personspark_facts.keys())
        to_delete_found_fact_keys = set(self.found_facts.keys())
        to_delete_boss_fact_keys = set(self.boss_facts.keys())
        to_delete_personspark_fact_keys.difference_update(self.reason_contexts)
        to_delete_found_fact_keys.difference_update(self.reason_contexts)
        to_delete_boss_fact_keys.difference_update(self.reason_contexts)
        for personspark_fact_key in to_delete_personspark_fact_keys:
            self.personspark_facts.pop(personspark_fact_key)
        for found_fact_key in to_delete_found_fact_keys:
            self.found_facts.pop(found_fact_key)
        for boss_fact_key in to_delete_boss_fact_keys:
            self.boss_facts.pop(boss_fact_key)

    def set_personadjust_facts(self):
        for fact in self.personspark_facts.values():
            self.personadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )
        for fact in self.found_facts.values():
            self.personadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )
        for fact in self.boss_facts.values():
            self.personadjust.add_fact(
                fact.fact_context,
                fact.fact_state,
                fact.fact_lower,
                fact.fact_upper,
                True,
            )

    def _set_contact_mandate_ledger(self):
        self.personadjust.set_fund_pool(self.mandate)
        self.contact_mandate_ledger = get_contact_mandate_ledger(
            self.personadjust, True
        )

    def calc_contact_mandate_ledger(self):
        self.reason_contexts = self.personadjust.get_reason_contexts()
        self.filter_facts_by_reason_contexts()
        self.set_personadjust_facts()
        self._set_contact_mandate_ledger()

    def to_dict(self) -> dict[str, str | dict]:
        """Returns dict that is serializable to JSON."""

        if not self.personadjust:
            self.personadjust = personunit_shop(self.get_cell_person_name())
        return {
            "ancestors": self.ancestors,
            "spark_num": self.spark_num,
            "celldepth": self.celldepth,
            "bud_person_name": self.bud_person_name,
            "mana_grain": self.mana_grain,
            "quota": self.quota,
            "mandate": self.mandate,
            "personadjust": self.personadjust.to_dict(),
            "personspark_facts": get_dict_from_factunits(self.personspark_facts),
            "found_facts": get_dict_from_factunits(self.found_facts),
            "boss_facts": get_dict_from_factunits(self.boss_facts),
        }


def cellunit_shop(
    bud_person_name: PersonName,
    ancestors: list[PersonName] = None,
    spark_num: SparkInt = None,
    celldepth: int = None,
    mana_grain: ManaGrain = None,
    quota: float = None,
    personadjust: PersonUnit = None,
    personspark_facts: dict[RopeTerm, FactUnit] = None,
    found_facts: dict[RopeTerm, FactUnit] = None,
    boss_facts: dict[RopeTerm, FactUnit] = None,
    mandate: float = None,
) -> CellUnit:
    if quota is None:
        quota = CELLNODE_QUOTA_DEFAULT
    if mandate is None:
        mandate = CELLNODE_QUOTA_DEFAULT
    if personadjust is None:
        personadjust = personunit_shop(bud_person_name)
    reason_contexts = personadjust.get_reason_contexts() if personadjust else set()
    if personadjust:
        personadjust = copy_deepcopy(personadjust)
        clear_factunits_from_person(personadjust)

    return CellUnit(
        ancestors=get_empty_list_if_None(ancestors),
        spark_num=spark_num,
        celldepth=get_0_if_None(celldepth),
        bud_person_name=bud_person_name,
        mana_grain=get_1_if_None(mana_grain),
        quota=quota,
        mandate=mandate,
        personadjust=personadjust,
        personspark_facts=get_empty_dict_if_None(personspark_facts),
        found_facts=get_empty_dict_if_None(found_facts),
        boss_facts=get_empty_dict_if_None(boss_facts),
        reason_contexts=reason_contexts,
        contact_mandate_ledger={},
    )


def cellunit_get_from_dict(x_dict: dict) -> CellUnit:
    bud_person_name = x_dict.get("bud_person_name")
    ancestors = x_dict.get("ancestors")
    spark_num = x_dict.get("spark_num")
    celldepth = x_dict.get("celldepth")
    mana_grain = x_dict.get("mana_grain")
    quota = x_dict.get("quota")
    mandate = x_dict.get("mandate")
    personadjust_dict = x_dict.get("personadjust")
    if personadjust_dict:
        personadjust_obj = get_personunit_from_dict(personadjust_dict)
    else:
        personadjust_obj = None
    personspark_fact_dict = get_empty_dict_if_None(x_dict.get("personspark_facts"))
    found_fact_dict = get_empty_dict_if_None(x_dict.get("found_facts"))
    boss_fact_dict = get_empty_dict_if_None(x_dict.get("boss_facts"))
    personspark_facts = get_factunits_from_dict(personspark_fact_dict)
    found_facts = get_factunits_from_dict(found_fact_dict)
    boss_facts = get_factunits_from_dict(boss_fact_dict)
    return cellunit_shop(
        bud_person_name=bud_person_name,
        ancestors=ancestors,
        spark_num=spark_num,
        celldepth=celldepth,
        mana_grain=mana_grain,
        quota=quota,
        personadjust=personadjust_obj,
        personspark_facts=personspark_facts,
        found_facts=found_facts,
        boss_facts=boss_facts,
        mandate=mandate,
    )


def create_child_cellunits(parent_cell: CellUnit) -> list[CellUnit]:
    parent_cell.calc_contact_mandate_ledger()
    x_list = []
    for child_person_name in sorted(parent_cell.contact_mandate_ledger):
        child_mandate = parent_cell.contact_mandate_ledger.get(child_person_name)
        if child_mandate > 0 and parent_cell.celldepth > 0:
            child_ancestors = copy_deepcopy(parent_cell.ancestors)
            child_ancestors.append(child_person_name)
            boss_facts = get_factunits_from_dict(
                get_facts_dict(parent_cell.personadjust)
            )
            child_cell = cellunit_shop(
                bud_person_name=parent_cell.bud_person_name,
                ancestors=child_ancestors,
                spark_num=parent_cell.spark_num,
                celldepth=parent_cell.celldepth - 1,
                mana_grain=parent_cell.mana_grain,
                mandate=child_mandate,
                boss_facts=boss_facts,
            )
            x_list.append(child_cell)
    return x_list
