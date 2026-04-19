from ch00_py.dict_toolbox import (
    create_csv,
    del_in_nested_dict,
    exists_in_nested_dict,
    get_0_if_None,
    get_empty_dict_if_None,
    get_empty_set_if_None,
    get_from_nested_dict,
    set_in_nested_dict,
)
from ch01_allot.allot import default_pool_num
from ch11_bud._ref.ch11_semantic_types import (
    ContactName,
    FundNum,
    MomentRope,
    PersonName,
    TimeNum,
)
from dataclasses import dataclass


class CalcMagnitudeError(Exception):
    pass


class TranTimeError(Exception):
    pass


DEFAULT_CELLDEPTH = 2


@dataclass
class TranUnit:
    src: PersonName = None
    dst: ContactName = None
    tran_time: TimeNum = None
    amount: FundNum = None


def tranunit_shop(
    src: PersonName, dst: ContactName, tran_time: TimeNum, amount: FundNum
) -> TranUnit:
    return TranUnit(src=src, dst=dst, tran_time=tran_time, amount=amount)


@dataclass
class TranBook:
    moment_rope: MomentRope = None
    tranunits: dict[PersonName, dict[ContactName, dict[TimeNum, FundNum]]] = None
    _contacts_net: dict[PersonName, dict[ContactName, FundNum]] = None

    def set_tranunit(
        self,
        tranunit: TranUnit,
        blocked_tran_times: set[TimeNum] = None,
        offi_time_max: TimeNum = None,
    ):
        self.add_tranunit(
            person_name=tranunit.src,
            contact_name=tranunit.dst,
            tran_time=tranunit.tran_time,
            amount=tranunit.amount,
            blocked_tran_times=blocked_tran_times,
            offi_time_max=offi_time_max,
        )

    def add_tranunit(
        self,
        person_name: PersonName,
        contact_name: ContactName,
        tran_time: TimeNum,
        amount: FundNum,
        blocked_tran_times: set[TimeNum] = None,
        offi_time_max: TimeNum = None,
    ):
        if tran_time in get_empty_set_if_None(blocked_tran_times):
            exception_str = (
                f"Cannot set tranunit for tran_time={tran_time}, TimeNum is blocked"
            )
            raise TranTimeError(exception_str)
        if offi_time_max != None and tran_time >= offi_time_max:
            exception_str = f"Cannot set tranunit for tran_time={tran_time}, TimeNum is greater than current time={offi_time_max}"
            raise TranTimeError(exception_str)
        x_keylist = [person_name, contact_name, tran_time]
        set_in_nested_dict(self.tranunits, x_keylist, amount)

    def tranunit_exists(
        self, src: PersonName, dst: ContactName, tran_time: TimeNum
    ) -> bool:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True) != None

    def get_tranunit(
        self, src: PersonName, dst: ContactName, tran_time: TimeNum
    ) -> TranUnit:
        x_amount = get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)
        if x_amount != None:
            return tranunit_shop(src, dst, tran_time, x_amount)

    def get_amount(
        self, src: PersonName, dst: ContactName, tran_time: TimeNum
    ) -> TranUnit:
        return get_from_nested_dict(self.tranunits, [src, dst, tran_time], True)

    def del_tranunit(
        self, src: PersonName, dst: ContactName, tran_time: TimeNum
    ) -> TranUnit:
        x_keylist = [src, dst, tran_time]
        if exists_in_nested_dict(self.tranunits, x_keylist):
            del_in_nested_dict(self.tranunits, x_keylist)

    def get_tran_times(self) -> set[TimeNum]:
        x_set = set()
        for dst_dict in self.tranunits.values():
            for tran_time_dict in dst_dict.values():
                x_set.update(set(tran_time_dict.keys()))
        return x_set

    def get_persons_contacts_net(
        self,
    ) -> dict[PersonName, dict[ContactName, FundNum]]:
        persons_contacts_net_dict = {}
        for person_name, person_dict in self.tranunits.items():
            for contact_name, contact_dict in person_dict.items():
                if persons_contacts_net_dict.get(person_name) is None:
                    persons_contacts_net_dict[person_name] = {}
                person_net_dict = persons_contacts_net_dict.get(person_name)
                person_net_dict[contact_name] = sum(contact_dict.values())
        return persons_contacts_net_dict

    def get_contacts_net_dict(self) -> dict[ContactName, FundNum]:
        contacts_net_dict = {}
        for person_dict in self.tranunits.values():
            for contact_name, contact_dict in sorted(person_dict.items()):
                if contacts_net_dict.get(contact_name) is None:
                    contacts_net_dict[contact_name] = sum(contact_dict.values())
                else:
                    contacts_net_dict[contact_name] += sum(contact_dict.values())
        return contacts_net_dict

    def _get_contacts_headers(self) -> list:
        return ["contact_name", "net_amount"]

    def _get_contacts_net_array(self) -> list[list]:
        x_plans = self.get_contacts_net_dict().items()
        return [[contact_name, net_amount] for contact_name, net_amount in x_plans]

    def get_contacts_net_csv(self) -> str:
        return create_csv(self._get_contacts_headers(), self._get_contacts_net_array())

    def join(self, x_tranbook):
        sorted_tranunits = sorted(
            x_tranbook.tranunits.items(),
            key=lambda x: next(iter(next(iter(x[1].values())).keys())),
        )
        for src_contact_name, dst_dict in sorted_tranunits:
            for dst_contact_name, tran_time_dict in dst_dict.items():
                for x_tran_time, x_amount in tran_time_dict.items():
                    self.add_tranunit(
                        src_contact_name, dst_contact_name, x_tran_time, x_amount
                    )

    def to_dict(
        self,
    ) -> dict[MomentRope, dict[PersonName, dict[ContactName, dict[TimeNum, FundNum]]]]:
        """Returns dict that is serializable to JSON."""

        return {"moment_rope": self.moment_rope, "tranunits": self.tranunits}


def tranbook_shop(
    x_moment_rope: MomentRope,
    x_tranunits: dict[PersonName, dict[ContactName, dict[TimeNum, FundNum]]] = None,
):
    return TranBook(
        moment_rope=x_moment_rope,
        tranunits=get_empty_dict_if_None(x_tranunits),
        _contacts_net={},
    )


def get_tranbook_from_dict(x_dict: dict) -> TranBook:
    x_tranunits = x_dict.get("tranunits")
    new_tranunits = {}
    for x_person_name, x_contact_dict in x_tranunits.items():
        for x_contact_name, x_tran_time_dict in x_contact_dict.items():
            for x_tran_time, x_amount in x_tran_time_dict.items():
                x_key_list = [x_person_name, x_contact_name, int(x_tran_time)]
                set_in_nested_dict(new_tranunits, x_key_list, x_amount)
    return tranbook_shop(x_dict.get("moment_rope"), new_tranunits)


@dataclass
class BudUnit:
    bud_time: TimeNum = None
    quota: FundNum = None
    celldepth: int = None  # non-negative
    # Calculated
    magnitude: FundNum = None  # how much of the actual quota is distributed
    bud_contact_nets: dict[ContactName, FundNum] = None  # ledger of bud outcome

    def set_bud_contact_net(
        self, x_contact_name: ContactName, bud_contact_net: FundNum
    ):
        self.bud_contact_nets[x_contact_name] = bud_contact_net

    def bud_contact_net_exists(self, x_contact_name: ContactName) -> bool:
        return self.bud_contact_nets.get(x_contact_name) != None

    def get_bud_contact_net(self, x_contact_name: ContactName) -> FundNum:
        return self.bud_contact_nets.get(x_contact_name)

    def del_bud_contact_net(self, x_contact_name: ContactName):
        self.bud_contact_nets.pop(x_contact_name)

    def calc_magnitude(self):
        bud_contact_nets = self.bud_contact_nets.values()
        x_cred_sum = sum(da_net for da_net in bud_contact_nets if da_net > 0)
        x_debt_sum = sum(da_net for da_net in bud_contact_nets if da_net < 0)
        if x_cred_sum + x_debt_sum != 0:
            exception_str = f"magnitude cannot be calculated: debt_bud_contact_net={x_debt_sum}, cred_bud_contact_net={x_cred_sum}"
            raise CalcMagnitudeError(exception_str)
        self.magnitude = x_cred_sum

    def to_dict(self) -> dict[str, FundNum | int]:
        """Returns dict that is serializable to JSON."""

        x_dict = {"bud_time": self.bud_time, "quota": self.quota}
        if self.bud_contact_nets:
            x_dict["bud_contact_nets"] = self.bud_contact_nets
        if self.magnitude:
            x_dict["magnitude"] = self.magnitude
        if self.celldepth != DEFAULT_CELLDEPTH:
            x_dict["celldepth"] = self.celldepth
        return x_dict


def budunit_shop(
    bud_time: TimeNum,
    quota: FundNum = None,
    bud_contact_nets: dict[ContactName, FundNum] = None,
    magnitude: FundNum = None,
    celldepth: int = None,
) -> BudUnit:
    if quota is None:
        quota = default_pool_num()
    if celldepth is None:
        celldepth = DEFAULT_CELLDEPTH

    return BudUnit(
        bud_time=bud_time,
        quota=quota,
        celldepth=celldepth,
        bud_contact_nets=get_empty_dict_if_None(bud_contact_nets),
        magnitude=get_0_if_None(magnitude),
    )


@dataclass
class PersonBudHistory:
    person_name: PersonName = None
    buds: dict[TimeNum, BudUnit] = None
    # calculated fields
    sum_budunit_quota: FundNum = None
    sum_contact_bud_nets: int = None
    bud_time_min: TimeNum = None
    bud_time_max: TimeNum = None

    def set_bud(self, x_bud: BudUnit):
        self.buds[x_bud.bud_time] = x_bud

    def add_bud(self, x_bud_time: TimeNum, x_quota: FundNum, celldepth: int = None):
        budunit = budunit_shop(bud_time=x_bud_time, quota=x_quota, celldepth=celldepth)
        self.set_bud(budunit)

    def bud_time_exists(self, x_bud_time: TimeNum) -> bool:
        return self.buds.get(x_bud_time) != None

    def get_bud(self, x_bud_time: TimeNum) -> BudUnit:
        return self.buds.get(x_bud_time)

    def del_bud(self, x_bud_time: TimeNum):
        self.buds.pop(x_bud_time)

    def get_2d_array(self) -> list[list]:
        return [
            [self.person_name, x_bud.bud_time, x_bud.quota]
            for x_bud in self.buds.values()
        ]

    def get_headers(self) -> list[str]:
        return ["person_name", "bud_time", "quota"]

    def to_dict(self) -> dict[ContactName,]:
        """Returns dict that is serializable to JSON."""

        return {"person_name": self.person_name, "buds": self._get_buds_dict()}

    def _get_buds_dict(self) -> dict[TimeNum, dict[str, FundNum | int]]:
        return {x_bud.bud_time: x_bud.to_dict() for x_bud in self.buds.values()}

    def get_bud_times(self) -> set[TimeNum]:
        return set(self.buds.keys())

    def get_tranbook(self, moment_rope: MomentRope) -> TranBook:
        x_tranbook = tranbook_shop(moment_rope)
        for x_bud_time, x_bud in self.buds.items():
            for dst_contact_name, x_quota in x_bud.bud_contact_nets.items():
                x_tranbook.add_tranunit(
                    person_name=self.person_name,
                    contact_name=dst_contact_name,
                    tran_time=x_bud_time,
                    amount=x_quota,
                )
        return x_tranbook


def personbudhistory_shop(person_name: PersonName) -> PersonBudHistory:
    return PersonBudHistory(person_name=person_name, buds={}, sum_contact_bud_nets={})


def get_budunit_from_dict(x_dict: dict) -> BudUnit:
    x_bud_time = x_dict.get("bud_time")
    x_quota = x_dict.get("quota")
    x_bud_net = x_dict.get("bud_contact_nets")
    x_magnitude = x_dict.get("magnitude")
    x_celldepth = x_dict.get("celldepth")
    return budunit_shop(
        x_bud_time, x_quota, x_bud_net, x_magnitude, celldepth=x_celldepth
    )


def get_personbudhistory_from_dict(x_dict: dict) -> PersonBudHistory:
    x_person_name = x_dict.get("person_name")
    x_personbudhistory = personbudhistory_shop(x_person_name)
    x_personbudhistory.buds = get_buds_from_dict(x_dict.get("buds"))
    return x_personbudhistory


def get_buds_from_dict(buds_dict: dict) -> dict[TimeNum, BudUnit]:
    x_dict = {}
    for x_bud_dict in buds_dict.values():
        x_budunit = get_budunit_from_dict(x_bud_dict)
        x_dict[x_budunit.bud_time] = x_budunit
    return x_dict
