from ch00_py.dict_toolbox import get_0_if_None, get_1_if_None
from ch02_allot.allot import allot_scale, default_grain_num_if_None
from ch03_contact._ref.ch03_semantic_types import (
    BossMass,
    ContactName,
    FundNum,
    GroupMark,
    NameTerm,
    RespectGrain,
    RespectNum,
    TrustMass,
    default_groupmark_if_None,
)
from ch03_contact.group import (
    GroupTitle,
    MemberShip,
    membership_shop,
    memberships_get_from_dict,
)
from dataclasses import dataclass


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


class InvalidContactNameMemberShipError(Exception):
    pass


@dataclass
class ContactUnit:
    """This represents the object's opinion of the ContactUnit.contact_name
    ContactUnit.contact_cred_mass represents how much contact_cred_mass the object projects to the contact_name
    ContactUnit.contact_debt_mass represents how much contact_debt_mass the object projects to the contact_name
    """

    contact_name: ContactName = None
    groupmark: str = None
    respect_grain: RespectGrain = None
    contact_cred_mass: BossMass = None
    contact_debt_mass: TrustMass = None
    # special attribute: static in json, in memory it is deleted after loading and recalculated during saving.
    memberships: dict[ContactName, MemberShip] = None
    # calculated fields
    credor_pool: RespectNum = None
    debtor_pool: RespectNum = None
    irrational_contact_debt_mass: TrustMass = None  # set by listening process
    inallocable_contact_debt_mass: TrustMass = None  # set by listening process
    # set by thinkout()
    fund_give: FundNum = None
    fund_take: FundNum = None
    fund_agenda_give: FundNum = None
    fund_agenda_take: FundNum = None
    fund_agenda_ratio_give: FundNum = None
    fund_agenda_ratio_take: FundNum = None

    def set_name(self, x_contact_name: ContactName):
        self.contact_name = validate_nameterm(x_contact_name, self.groupmark)

    def set_respect_grain(self, x_respect_grain: float):
        self.respect_grain = x_respect_grain

    def set_credor_contact_debt_mass(
        self,
        contact_cred_mass: BossMass = None,
        contact_debt_mass: TrustMass = None,
    ):
        if contact_cred_mass is not None:
            self.set_contact_cred_mass(contact_cred_mass)
        if contact_debt_mass is not None:
            self.set_contact_debt_mass(contact_debt_mass)

    def set_contact_cred_mass(self, contact_cred_mass: BossMass):
        self.contact_cred_mass = contact_cred_mass

    def set_contact_debt_mass(self, contact_debt_mass: TrustMass):
        self.contact_debt_mass = contact_debt_mass

    def get_contact_cred_mass(self):
        return get_1_if_None(self.contact_cred_mass)

    def get_contact_debt_mass(self):
        return get_1_if_None(self.contact_debt_mass)

    def clear_fund_give_take(self):
        self.fund_give = 0
        self.fund_take = 0
        self.fund_agenda_give = 0
        self.fund_agenda_take = 0
        self.fund_agenda_ratio_give = 0
        self.fund_agenda_ratio_take = 0

    def add_irrational_contact_debt_mass(
        self, x_irrational_contact_debt_mass: TrustMass
    ):
        self.irrational_contact_debt_mass += x_irrational_contact_debt_mass

    def add_inallocable_contact_debt_mass(
        self, x_inallocable_contact_debt_mass: TrustMass
    ):
        self.inallocable_contact_debt_mass += x_inallocable_contact_debt_mass

    def reset_listen_calculated_attrs(self):
        self.irrational_contact_debt_mass = 0
        self.inallocable_contact_debt_mass = 0

    def add_fund_give(self, fund_give: float):
        self.fund_give += fund_give

    def add_fund_take(self, fund_take: float):
        self.fund_take += fund_take

    def add_fund_agenda_give(self, fund_agenda_give: float):
        self.fund_agenda_give += fund_agenda_give

    def add_fund_agenda_take(self, fund_agenda_take: float):
        self.fund_agenda_take += fund_agenda_take

    def add_contact_fund_give_take(
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
        contactunits_contact_cred_mass_sum: float,
        contactunits_contact_debt_mass_sum: float,
    ):
        total_contact_cred_mass = contactunits_contact_cred_mass_sum
        ratio_give_sum = fund_agenda_ratio_give_sum
        self.fund_agenda_ratio_give = (
            self.get_contact_cred_mass() / total_contact_cred_mass
            if fund_agenda_ratio_give_sum == 0
            else self.fund_agenda_give / ratio_give_sum
        )
        if fund_agenda_ratio_take_sum == 0:
            total_contact_debt_mass = contactunits_contact_debt_mass_sum
            self.fund_agenda_ratio_take = (
                self.get_contact_debt_mass() / total_contact_debt_mass
            )
        else:
            ratio_take_sum = fund_agenda_ratio_take_sum
            self.fund_agenda_ratio_take = self.fund_agenda_take / ratio_take_sum

    def add_membership(
        self,
        group_title: GroupTitle,
        group_cred_mass: BossMass = None,
        group_debt_mass: TrustMass = None,
    ):
        x_membership = membership_shop(group_title, group_cred_mass, group_debt_mass)
        self.set_membership(x_membership)

    def set_membership(self, x_membership: MemberShip):
        x_group_title = x_membership.group_title
        group_title_is_contact_name = is_nameterm(x_group_title, self.groupmark)
        if group_title_is_contact_name and self.contact_name != x_group_title:
            exception_str = f"ContactUnit with contact_name='{self.contact_name}' cannot have link to '{x_group_title}'."
            raise InvalidContactNameMemberShipError(exception_str)

        x_membership.contact_name = self.contact_name
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
            x_membership.group_title: x_membership.group_cred_mass
            for x_membership in self.memberships.values()
        }
        allot_dict = allot_scale(ledger_dict, self.credor_pool, self.respect_grain)
        for x_group_title, alloted_pool in allot_dict.items():
            self.get_membership(x_group_title).credor_pool = alloted_pool

    def set_debtor_pool(self, debtor_pool: RespectNum):
        self.debtor_pool = debtor_pool
        ledger_dict = {
            x_membership.group_title: x_membership.group_debt_mass
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
            "contact_name": self.contact_name,
            "contact_cred_mass": self.contact_cred_mass,
            "contact_debt_mass": self.contact_debt_mass,
            "memberships": self.get_memberships_dict(),
        }
        if self.irrational_contact_debt_mass not in [None, 0]:
            x_dict["irrational_contact_debt_mass"] = self.irrational_contact_debt_mass
        if self.inallocable_contact_debt_mass not in [None, 0]:
            x_dict["inallocable_contact_debt_mass"] = self.inallocable_contact_debt_mass

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


def contactunits_get_from_dict(
    x_dict: dict, groupmark: str = None
) -> dict[str, ContactUnit]:
    contactunits = {}
    for contactunit_dict in x_dict.values():
        x_contactunit = contactunit_get_from_dict(contactunit_dict, groupmark)
        contactunits[x_contactunit.contact_name] = x_contactunit
    return contactunits


def contactunit_get_from_dict(contactunit_dict: dict, groupmark: str) -> ContactUnit:
    x_contact_name = contactunit_dict["contact_name"]
    x_contact_cred_mass = contactunit_dict["contact_cred_mass"]
    x_contact_debt_mass = contactunit_dict["contact_debt_mass"]
    x_memberships_dict = contactunit_dict["memberships"]
    x_contactunit = contactunit_shop(
        x_contact_name, x_contact_cred_mass, x_contact_debt_mass, groupmark
    )
    x_contactunit.memberships = memberships_get_from_dict(
        x_memberships_dict, x_contact_name
    )
    irrational_contact_debt_mass = contactunit_dict.get(
        "irrational_contact_debt_mass", 0
    )
    inallocable_contact_debt_mass = contactunit_dict.get(
        "inallocable_contact_debt_mass", 0
    )
    x_contactunit.add_irrational_contact_debt_mass(
        get_0_if_None(irrational_contact_debt_mass)
    )
    x_contactunit.add_inallocable_contact_debt_mass(
        get_0_if_None(inallocable_contact_debt_mass)
    )

    return x_contactunit


def contactunit_shop(
    contact_name: ContactName,
    contact_cred_mass: BossMass = None,
    contact_debt_mass: TrustMass = None,
    groupmark: str = None,
    respect_grain: float = None,
) -> ContactUnit:
    x_contactunit = ContactUnit(
        contact_cred_mass=get_1_if_None(contact_cred_mass),
        contact_debt_mass=get_1_if_None(contact_debt_mass),
        memberships={},
        credor_pool=0,
        debtor_pool=0,
        irrational_contact_debt_mass=0,
        inallocable_contact_debt_mass=0,
        fund_give=0,
        fund_take=0,
        fund_agenda_give=0,
        fund_agenda_take=0,
        fund_agenda_ratio_give=0,
        fund_agenda_ratio_take=0,
        groupmark=default_groupmark_if_None(groupmark),
        respect_grain=default_grain_num_if_None(respect_grain),
    )
    x_contactunit.set_name(x_contact_name=contact_name)
    return x_contactunit


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
