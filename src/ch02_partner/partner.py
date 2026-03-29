from dataclasses import dataclass
from src.ch00_py.dict_toolbox import get_0_if_None, get_1_if_None
from src.ch01_allot.allot import allot_scale, default_grain_num_if_None
from src.ch02_partner._ref.ch02_semantic_types import (
    FundNum,
    GroupMark,
    NameTerm,
    PartnerName,
    RespectGrain,
    RespectNum,
    default_groupmark_if_None,
)
from src.ch02_partner.group import (
    GroupTitle,
    MemberShip,
    membership_shop,
    memberships_get_from_dict,
)


def is_nameterm(x_nameterm: NameTerm, groupmark: GroupMark):
    x_nameterm = NameTerm(x_nameterm)
    return x_nameterm.is_name(groupmark=groupmark)


class ValidateNameTermError(Exception):
    pass


def validate_nameterm(
    x_nameterm: NameTerm, x_groupmark: str, not_nameterm_required: bool = False
) -> NameTerm:
    if is_nameterm(x_nameterm, x_groupmark) and not_nameterm_required:
        raise ValidateNameTermError(
            f"'{x_nameterm}' must not be a NameTerm. Must contain GroupMark: '{x_groupmark}'"
        )
    elif is_nameterm(x_nameterm, x_groupmark) is False and not not_nameterm_required:
        raise ValidateNameTermError(
            f"'{x_nameterm}' must be a NameTerm. Cannot contain GroupMark: '{x_groupmark}'"
        )
    return x_nameterm


class InvalidPartnerNameMemberShipError(Exception):
    pass


@dataclass
class PartnerUnit:
    """This represents the object's opinion of the PartnerUnit.partner_name
    PartnerUnit.partner_cred_lumen represents how much partner_cred_lumen the object projects to the partner_name
    PartnerUnit.partner_debt_lumen represents how much partner_debt_lumen the object projects to the partner_name
    """

    partner_name: PartnerName = None
    groupmark: str = None
    respect_grain: RespectGrain = None
    partner_cred_lumen: int = None
    partner_debt_lumen: int = None
    # special attribute: static in json, in memory it is deleted after loading and recalculated during saving.
    memberships: dict[PartnerName, MemberShip] = None
    # calculated fields
    credor_pool: RespectNum = None
    debtor_pool: RespectNum = None
    irrational_partner_debt_lumen: int = None  # set by listening process
    inallocable_partner_debt_lumen: int = None  # set by listening process
    # set by conpute()
    fund_give: FundNum = None
    fund_take: FundNum = None
    fund_agenda_give: FundNum = None
    fund_agenda_take: FundNum = None
    fund_agenda_ratio_give: FundNum = None
    fund_agenda_ratio_take: FundNum = None

    def set_name(self, x_partner_name: PartnerName):
        self.partner_name = validate_nameterm(x_partner_name, self.groupmark)

    def set_respect_grain(self, x_respect_grain: float):
        self.respect_grain = x_respect_grain

    def set_credor_partner_debt_lumen(
        self,
        partner_cred_lumen: float = None,
        partner_debt_lumen: float = None,
    ):
        if partner_cred_lumen is not None:
            self.set_partner_cred_lumen(partner_cred_lumen)
        if partner_debt_lumen is not None:
            self.set_partner_debt_lumen(partner_debt_lumen)

    def set_partner_cred_lumen(self, partner_cred_lumen: int):
        self.partner_cred_lumen = partner_cred_lumen

    def set_partner_debt_lumen(self, partner_debt_lumen: int):
        self.partner_debt_lumen = partner_debt_lumen

    def get_partner_cred_lumen(self):
        return get_1_if_None(self.partner_cred_lumen)

    def get_partner_debt_lumen(self):
        return get_1_if_None(self.partner_debt_lumen)

    def clear_fund_give_take(self):
        self.fund_give = 0
        self.fund_take = 0
        self.fund_agenda_give = 0
        self.fund_agenda_take = 0
        self.fund_agenda_ratio_give = 0
        self.fund_agenda_ratio_take = 0

    def add_irrational_partner_debt_lumen(self, x_irrational_partner_debt_lumen: float):
        self.irrational_partner_debt_lumen += x_irrational_partner_debt_lumen

    def add_inallocable_partner_debt_lumen(
        self, x_inallocable_partner_debt_lumen: float
    ):
        self.inallocable_partner_debt_lumen += x_inallocable_partner_debt_lumen

    def reset_listen_calculated_attrs(self):
        self.irrational_partner_debt_lumen = 0
        self.inallocable_partner_debt_lumen = 0

    def add_fund_give(self, fund_give: float):
        self.fund_give += fund_give

    def add_fund_take(self, fund_take: float):
        self.fund_take += fund_take

    def add_fund_agenda_give(self, fund_agenda_give: float):
        self.fund_agenda_give += fund_agenda_give

    def add_fund_agenda_take(self, fund_agenda_take: float):
        self.fund_agenda_take += fund_agenda_take

    def add_partner_fund_give_take(
        self,
        fund_give: float,
        fund_take,
        fund_agenda_give: float,
        fund_agenda_take,
    ):
        self.add_fund_give(fund_give)
        self.add_fund_take(fund_take)
        self.add_fund_agenda_give(fund_agenda_give)
        self.add_fund_agenda_take(fund_agenda_take)

    def set_fund_agenda_ratio_give_take(
        self,
        fund_agenda_ratio_give_sum: float,
        fund_agenda_ratio_take_sum: float,
        partnerunits_partner_cred_lumen_sum: float,
        partnerunits_partner_debt_lumen_sum: float,
    ):
        total_partner_cred_lumen = partnerunits_partner_cred_lumen_sum
        ratio_give_sum = fund_agenda_ratio_give_sum
        self.fund_agenda_ratio_give = (
            self.get_partner_cred_lumen() / total_partner_cred_lumen
            if fund_agenda_ratio_give_sum == 0
            else self.fund_agenda_give / ratio_give_sum
        )
        if fund_agenda_ratio_take_sum == 0:
            total_partner_debt_lumen = partnerunits_partner_debt_lumen_sum
            self.fund_agenda_ratio_take = (
                self.get_partner_debt_lumen() / total_partner_debt_lumen
            )
        else:
            ratio_take_sum = fund_agenda_ratio_take_sum
            self.fund_agenda_ratio_take = self.fund_agenda_take / ratio_take_sum

    def add_membership(
        self,
        group_title: GroupTitle,
        group_cred_lumen: float = None,
        group_debt_lumen: float = None,
    ):
        x_membership = membership_shop(group_title, group_cred_lumen, group_debt_lumen)
        self.set_membership(x_membership)

    def set_membership(self, x_membership: MemberShip):
        x_group_title = x_membership.group_title
        group_title_is_partner_name = is_nameterm(x_group_title, self.groupmark)
        if group_title_is_partner_name and self.partner_name != x_group_title:
            exception_str = f"PartnerUnit with partner_name='{self.partner_name}' cannot have link to '{x_group_title}'."
            raise InvalidPartnerNameMemberShipError(exception_str)

        x_membership.partner_name = self.partner_name
        self.memberships[x_membership.group_title] = x_membership

    def get_membership(self, group_title: GroupTitle) -> MemberShip:
        return self.memberships.get(group_title)

    def membership_exists(self, group_title: GroupTitle) -> bool:
        return self.memberships.get(group_title) is not None

    def delete_membership(self, group_title: GroupTitle):
        return self.memberships.pop(group_title)

    def memberships_exist(self):
        return len(self.memberships) != 0

    def clear_memberships(self):
        self.memberships = {}

    def set_credor_pool(self, credor_pool: RespectNum):
        self.credor_pool = credor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.group_cred_lumen
            for x_membership in self.memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self.credor_pool, self.respect_grain)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title).credor_pool = alloted_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self.debtor_pool = debtor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.group_debt_lumen
            for x_membership in self.memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self.debtor_pool, self.respect_grain)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title).debtor_pool = alloted_pool

    def get_memberships_dict(self) -> dict:
        return {
            x_membership.group_title: x_membership.to_dict()
            for x_membership in self.memberships.values()
        }

    def to_dict(self, all_attrs: bool = False) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        x_dict = {
            "partner_name": self.partner_name,
            "partner_cred_lumen": self.partner_cred_lumen,
            "partner_debt_lumen": self.partner_debt_lumen,
            "memberships": self.get_memberships_dict(),
        }
        if self.irrational_partner_debt_lumen not in [None, 0]:
            x_dict["irrational_partner_debt_lumen"] = self.irrational_partner_debt_lumen
        if self.inallocable_partner_debt_lumen not in [None, 0]:
            x_dict[
                "inallocable_partner_debt_lumen"
            ] = self.inallocable_partner_debt_lumen

        if all_attrs:
            self.all_attrs_necessary_in_dict(x_dict)
        return x_dict

    def all_attrs_necessary_in_dict(self, x_dict):
        x_dict["fund_give"] = self.fund_give
        x_dict["fund_take"] = self.fund_take
        x_dict["fund_agenda_give"] = self.fund_agenda_give
        x_dict["fund_agenda_take"] = self.fund_agenda_take
        x_dict["fund_agenda_ratio_give"] = self.fund_agenda_ratio_give
        x_dict["fund_agenda_ratio_take"] = self.fund_agenda_ratio_take


def partnerunits_get_from_dict(
    x_dict: dict, groupmark: str = None
) -> dict[str, PartnerUnit]:
    partnerunits = {}
    for partnerunit_dict in x_dict.values():
        x_partnerunit = partnerunit_get_from_dict(partnerunit_dict, groupmark)
        partnerunits[x_partnerunit.partner_name] = x_partnerunit
    return partnerunits


def partnerunit_get_from_dict(partnerunit_dict: dict, groupmark: str) -> PartnerUnit:
    x_partner_name = partnerunit_dict["partner_name"]
    x_partner_cred_lumen = partnerunit_dict["partner_cred_lumen"]
    x_partner_debt_lumen = partnerunit_dict["partner_debt_lumen"]
    x_memberships_dict = partnerunit_dict["memberships"]
    x_partnerunit = partnerunit_shop(
        x_partner_name, x_partner_cred_lumen, x_partner_debt_lumen, groupmark
    )
    x_partnerunit.memberships = memberships_get_from_dict(
        x_memberships_dict, x_partner_name
    )
    irrational_partner_debt_lumen = partnerunit_dict.get(
        "irrational_partner_debt_lumen", 0
    )
    inallocable_partner_debt_lumen = partnerunit_dict.get(
        "inallocable_partner_debt_lumen", 0
    )
    x_partnerunit.add_irrational_partner_debt_lumen(
        get_0_if_None(irrational_partner_debt_lumen)
    )
    x_partnerunit.add_inallocable_partner_debt_lumen(
        get_0_if_None(inallocable_partner_debt_lumen)
    )

    return x_partnerunit


def partnerunit_shop(
    partner_name: PartnerName,
    partner_cred_lumen: int = None,
    partner_debt_lumen: int = None,
    groupmark: str = None,
    respect_grain: float = None,
) -> PartnerUnit:
    x_partnerunit = PartnerUnit(
        partner_cred_lumen=get_1_if_None(partner_cred_lumen),
        partner_debt_lumen=get_1_if_None(partner_debt_lumen),
        memberships={},
        credor_pool=0,
        debtor_pool=0,
        irrational_partner_debt_lumen=0,
        inallocable_partner_debt_lumen=0,
        fund_give=0,
        fund_take=0,
        fund_agenda_give=0,
        fund_agenda_take=0,
        fund_agenda_ratio_give=0,
        fund_agenda_ratio_take=0,
        groupmark=default_groupmark_if_None(groupmark),
        respect_grain=default_grain_num_if_None(respect_grain),
    )
    x_partnerunit.set_name(x_partner_name=partner_name)
    return x_partnerunit


class CalcGiveTakeNetError(Exception):
    pass


def calc_give_take_net(x_give: float, x_take: float) -> float:
    x_give = get_0_if_None(x_give)
    x_take = get_0_if_None(x_take)
    if x_give < 0 or x_take < 0:
        if x_give < 0 and x_take >= 0:
            parameters_str = f"calc_give_take_net x_give={x_give}."
        elif x_give >= 0:
            parameters_str = f"calc_give_take_net x_take={x_take}."
        else:
            parameters_str = f"calc_give_take_net x_give={x_give} and x_take={x_take}."
        exception_str = f"{parameters_str} Only non-negative numbers allowed."
        raise CalcGiveTakeNetError(exception_str)
    return x_give - x_take
