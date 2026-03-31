from dataclasses import dataclass
from src.ch00_py.dict_toolbox import get_0_if_None, get_empty_dict_if_None
from src.ch01_allot.allot import (
    allot_scale,
    default_grain_num_if_None,
    validate_pool_num,
)
from src.ch07_person_logic.person_main import PersonUnit
from src.ch12_keep._ref.ch12_semantic_types import (
    ContactName,
    ManaGrain,
    ManaNum,
    MomentRope,
    PersonName,
    RespectNum,
    RopeTerm,
)


def get_patientledger(x_person: PersonUnit) -> dict[ContactName, RespectNum]:
    return {
        contactunit.contact_name: contactunit.contact_cred_lumen
        for contactunit in x_person.contacts.values()
        if contactunit.contact_cred_lumen > 0
    }


def get_doctorledger(x_person: PersonUnit) -> dict[ContactName, RespectNum]:
    return {
        contactunit.contact_name: contactunit.contact_debt_lumen
        for contactunit in x_person.contacts.values()
        if contactunit.contact_debt_lumen > 0
    }


@dataclass
class RiverBook:
    person_name: PersonName = None
    rivercares: dict[ContactName, float] = None
    mana_grain: ManaGrain = None


def riverbook_shop(person_name: PersonName, mana_grain: ManaGrain = None):
    x_riverbook = RiverBook(person_name)
    x_riverbook.rivercares = {}
    x_riverbook.mana_grain = default_grain_num_if_None(mana_grain)
    return x_riverbook


def create_riverbook(
    person_name: PersonName,
    keep_patientledger: dict,
    book_point_amount: int,
    mana_grain: ManaGrain = None,
) -> RiverBook:
    x_riverbook = riverbook_shop(person_name, mana_grain)
    x_riverbook.rivercares = allot_scale(
        ledger=keep_patientledger,
        scale_number=book_point_amount,
        grain_unit=x_riverbook.mana_grain,
    )
    return x_riverbook


@dataclass
class RiverCycle:
    healer_name: PersonName = None
    number: int = None
    keep_patientledgers: dict[PersonName : dict[ContactName, float]] = None
    riverbooks: dict[ContactName, RiverBook] = None
    mana_grain: ManaGrain = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.person_name] = x_riverbook

    def set_riverbook(
        self,
        book_contact_name: ContactName,
        book_point_amount: float,
    ):
        person_patientledger = self.keep_patientledgers.get(book_contact_name)
        if person_patientledger is not None:
            x_riverbook = create_riverbook(
                person_name=book_contact_name,
                keep_patientledger=person_patientledger,
                book_point_amount=book_point_amount,
                mana_grain=default_grain_num_if_None(self.mana_grain),
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[ContactName, float]:
        x_dict = {}
        for x_riverbook in self.riverbooks.values():
            for caree, charge_amount in x_riverbook.rivercares.items():
                if x_dict.get(caree) is None:
                    x_dict[caree] = charge_amount
                else:
                    x_dict[caree] = x_dict[caree] + charge_amount
        return x_dict


def rivercycle_shop(
    healer_name: PersonName,
    number: int,
    keep_patientledgers: dict[PersonName : dict[ContactName, float]] = None,
    mana_grain: ManaGrain = None,
):
    return RiverCycle(
        healer_name=healer_name,
        number=number,
        keep_patientledgers=get_empty_dict_if_None(keep_patientledgers),
        riverbooks=get_empty_dict_if_None(),
        mana_grain=default_grain_num_if_None(mana_grain),
    )


def create_init_rivercycle(
    healer_name: PersonName,
    keep_patientledgers: dict[PersonName : dict[ContactName, float]],
    keep_point_magnitude: ManaNum = None,
    mana_grain: ManaGrain = None,
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(
        healer_name, 0, keep_patientledgers, mana_grain=mana_grain
    )
    x_rivercycle.set_riverbook(healer_name, validate_pool_num(keep_point_magnitude))
    return x_rivercycle


def create_next_rivercycle(
    prev_rivercycle: RiverCycle,
    prev_cycle_cycleledger_post_need: dict[ContactName, float],
) -> RiverCycle:
    next_rivercycle = rivercycle_shop(
        healer_name=prev_rivercycle.healer_name,
        number=prev_rivercycle.number + 1,
        keep_patientledgers=prev_rivercycle.keep_patientledgers,
        mana_grain=prev_rivercycle.mana_grain,
    )
    for carer_id, chargeing_amount in prev_cycle_cycleledger_post_need.items():
        next_rivercycle.set_riverbook(carer_id, chargeing_amount)
    return next_rivercycle


@dataclass
class RiverGrade:
    moment_rope: MomentRope = None
    person_name: PersonName = None
    keep_rope: RopeTerm = None
    contact_name: ContactName = None
    number: int = None
    need_bill_amount: float = None
    care_amount: float = None
    doctor_rank_num: float = None
    patient_rank_num: float = None
    need_paid_amount: float = None
    need_paid_bool: float = None
    need_paid_rank_num: float = None
    need_paid_rank_percent: float = None
    doctor_count: float = None
    patient_count: float = None
    doctor_rank_percent: float = None
    patient_rank_percent: float = None
    rewards_count: float = None
    rewards_magnitude: float = None

    def set_need_bill_amount(self, x_need_bill_amount: float):
        self.need_bill_amount = x_need_bill_amount
        self.set_need_paid_bool()

    def set_need_paid_amount(self, x_need_paid_amount: float):
        self.need_paid_amount = x_need_paid_amount
        self.set_need_paid_bool()

    def set_need_paid_bool(self):
        self.need_paid_bool = (
            self.need_bill_amount is not None
            and self.need_bill_amount == self.need_paid_amount
        )

    def to_dict(self) -> dict:
        """Returns dict that is serializable to JSON."""

        return {
            "moment_rope": self.moment_rope,
            "healer_name": self.person_name,
            "keep_rope": self.keep_rope,
            "need_bill_amount": self.need_bill_amount,
            "care_amount": self.care_amount,
            "doctor_rank_num": self.doctor_rank_num,
            "patient_rank_num": self.patient_rank_num,
            "need_paid_amount": self.need_paid_amount,
            "need_paid_bool": self.need_paid_bool,
            "need_paid_rank_num": self.need_paid_rank_num,
            "need_paid_rank_percent": self.need_paid_rank_percent,
            "doctor_count": self.doctor_count,
            "patient_count": self.patient_count,
            "doctor_rank_percent": self.doctor_rank_percent,
            "patient_rank_percent": self.patient_rank_percent,
            "rewards_count": self.rewards_count,
            "rewards_magnitude": self.rewards_magnitude,
        }


def rivergrade_shop(
    moment_rope: MomentRope,
    person_name: PersonName,
    keep_rope: RopeTerm,
    contact_name: ContactName,
    number: float = None,
    doctor_count: int = None,
    patient_count: int = None,
):
    return RiverGrade(
        moment_rope=moment_rope,
        person_name=person_name,
        keep_rope=keep_rope,
        contact_name=contact_name,
        number=get_0_if_None(number),
        doctor_count=doctor_count,
        patient_count=patient_count,
    )
