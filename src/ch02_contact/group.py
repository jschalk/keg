from ch00_py.dict_toolbox import get_1_if_None
from ch01_allot.allot import allot_scale, default_grain_num_if_None
from ch02_contact._ref.ch02_semantic_types import ContactName, FundGrain, GroupTitle
from dataclasses import dataclass


class MembershipGroupTitleError(Exception):
    pass


@dataclass
class GroupCore:
    group_title: GroupTitle = None


@dataclass
class MemberShip(GroupCore):
    group_cred_lumen: float = 1.0
    group_debt_lumen: float = 1.0
    # calculated fields
    credor_pool: float = None
    debtor_pool: float = None
    fund_give: float = None
    fund_take: float = None
    fund_agenda_give: float = None
    fund_agenda_take: float = None
    fund_agenda_ratio_give: float = None
    fund_agenda_ratio_take: float = None
    contact_name: ContactName = None

    def set_group_cred_lumen(self, x_group_cred_lumen: float):
        if x_group_cred_lumen is not None:
            self.group_cred_lumen = x_group_cred_lumen

    def set_group_debt_lumen(self, x_group_debt_lumen: float):
        if x_group_debt_lumen is not None:
            self.group_debt_lumen = x_group_debt_lumen

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        return {
            "group_title": self.group_title,
            "group_cred_lumen": self.group_cred_lumen,
            "group_debt_lumen": self.group_debt_lumen,
        }

    def clear_membership_fund_give_take(self):
        self.fund_give = 0
        self.fund_take = 0
        self.fund_agenda_give = 0
        self.fund_agenda_take = 0
        self.fund_agenda_ratio_give = 0
        self.fund_agenda_ratio_take = 0


def membership_shop(
    group_title: GroupTitle,
    group_cred_lumen: float = None,
    group_debt_lumen: float = None,
    contact_name: ContactName = None,
) -> MemberShip:
    return MemberShip(
        group_title=group_title,
        group_cred_lumen=get_1_if_None(group_cred_lumen),
        group_debt_lumen=get_1_if_None(group_debt_lumen),
        credor_pool=0,
        debtor_pool=0,
        contact_name=contact_name,
    )


def membership_get_from_dict(x_dict: dict, x_contact_name: ContactName) -> MemberShip:
    return membership_shop(
        group_title=x_dict.get("group_title"),
        group_cred_lumen=x_dict.get("group_cred_lumen"),
        group_debt_lumen=x_dict.get("group_debt_lumen"),
        contact_name=x_contact_name,
    )


def memberships_get_from_dict(
    x_dict: dict, x_contact_name: ContactName
) -> dict[GroupTitle, MemberShip]:
    return {
        x_group_title: membership_get_from_dict(x_membership_dict, x_contact_name)
        for x_group_title, x_membership_dict in x_dict.items()
    }


@dataclass
class AwardCore:
    awardee_title: GroupTitle = None


@dataclass
class AwardUnit(AwardCore):
    give_force: float = 1.0
    take_force: float = 1.0

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        return {
            "awardee_title": self.awardee_title,
            "give_force": self.give_force,
            "take_force": self.take_force,
        }


def get_awardunits_from_dict(x_dict: dict) -> dict[GroupTitle, AwardUnit]:
    awardunits = {}
    for awardunits_dict in x_dict.values():
        x_group = awardunit_shop(
            awardee_title=awardunits_dict["awardee_title"],
            give_force=awardunits_dict["give_force"],
            take_force=awardunits_dict["take_force"],
        )
        awardunits[x_group.awardee_title] = x_group
    return awardunits


def awardunit_shop(
    awardee_title: GroupTitle,
    give_force: float = None,
    take_force: float = None,
) -> AwardUnit:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardUnit(awardee_title, give_force, take_force=take_force)


@dataclass
class AwardHeir(AwardCore):
    give_force: float = 1.0
    take_force: float = 1.0
    fund_give: float = None
    fund_take: float = None


def awardheir_shop(
    awardee_title: GroupTitle,
    give_force: float = None,
    take_force: float = None,
    fund_give: float = None,
    fund_take: float = None,
) -> AwardHeir:
    give_force = get_1_if_None(give_force)
    take_force = get_1_if_None(take_force)
    return AwardHeir(awardee_title, give_force, take_force, fund_give, fund_take)


@dataclass
class AwardLine(AwardCore):
    fund_give: float = None
    fund_take: float = None

    def add_fund_give_take(self, fund_give: float, fund_take: float):
        self.validate_fund_give_fund_take()
        self.fund_give += fund_give
        self.fund_take += fund_take

    def validate_fund_give_fund_take(self):
        if self.fund_give is None:
            self.fund_give = 0
        if self.fund_take is None:
            self.fund_take = 0


def awardline_shop(awardee_title: GroupTitle, fund_give: float, fund_take: float):
    return AwardLine(awardee_title, fund_give=fund_give, fund_take=fund_take)


@dataclass
class GroupUnit(GroupCore):
    memberships: dict[ContactName, MemberShip] = None
    # calculated by Parent Object method "conpute"
    fund_give: float = None
    fund_take: float = None
    fund_agenda_give: float = None
    fund_agenda_take: float = None
    credor_pool: float = None
    debtor_pool: float = None
    fund_grain: FundGrain = None

    def set_g_membership(self, x_membership: MemberShip):
        if x_membership.group_title != self.group_title:
            raise MembershipGroupTitleError(
                f"GroupUnit.group_title={self.group_title} cannot set membership.group_title={x_membership.group_title}"
            )
        if x_membership.contact_name is None:
            raise MembershipGroupTitleError(
                f"membership group_title={x_membership.group_title} cannot be set when _contact_name is None."
            )

        self.memberships[x_membership.contact_name] = x_membership
        self._add_credor_pool(x_membership.credor_pool)
        self._add_debtor_pool(x_membership.debtor_pool)

    def _add_credor_pool(self, x_credor_pool: float):
        self.credor_pool += x_credor_pool

    def _add_debtor_pool(self, x_debtor_pool: float):
        self.debtor_pool += x_debtor_pool

    def get_contact_membership(self, x_contact_name: ContactName) -> MemberShip:
        return self.memberships.get(x_contact_name)

    def group_membership_exists(self, x_contact_name: ContactName) -> bool:
        return self.get_contact_membership(x_contact_name) is not None

    def del_membership(self, contact_name):
        self.memberships.pop(contact_name)

    def clear_group_fund_give_take(self):
        self.fund_give = 0
        self.fund_take = 0
        self.fund_agenda_give = 0
        self.fund_agenda_take = 0
        for membership in self.memberships.values():
            membership.clear_membership_fund_give_take()

    def _set_membership_fund_give_fund_take(self):
        credit_ledger = {}
        debt_ledger = {}
        for x_contact_name, x_membership in self.memberships.items():
            credit_ledger[x_contact_name] = x_membership.group_cred_lumen
            debt_ledger[x_contact_name] = x_membership.group_debt_lumen
        fund_give_allot = allot_scale(credit_ledger, self.fund_give, self.fund_grain)
        fund_take_allot = allot_scale(debt_ledger, self.fund_take, self.fund_grain)
        for contact_name, x_membership in self.memberships.items():
            x_membership.fund_give = fund_give_allot.get(contact_name)
            x_membership.fund_take = fund_take_allot.get(contact_name)
        x_a_give = self.fund_agenda_give
        x_a_take = self.fund_agenda_take
        fund_agenda_give_allot = allot_scale(credit_ledger, x_a_give, self.fund_grain)
        fund_agenda_take_allot = allot_scale(debt_ledger, x_a_take, self.fund_grain)
        for contact_name, x_membership in self.memberships.items():
            x_membership.fund_agenda_give = fund_agenda_give_allot.get(contact_name)
            x_membership.fund_agenda_take = fund_agenda_take_allot.get(contact_name)


def groupunit_shop(group_title: GroupTitle, fund_grain: FundGrain = None) -> GroupUnit:
    return GroupUnit(
        group_title=group_title,
        memberships={},
        fund_give=0,
        fund_take=0,
        fund_agenda_give=0,
        fund_agenda_take=0,
        credor_pool=0,
        debtor_pool=0,
        fund_grain=default_grain_num_if_None(fund_grain),
    )
    # x_groupunit.set_group_title(group_title=group_title)
    # return x_groupunit
