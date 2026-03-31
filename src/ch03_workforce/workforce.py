from dataclasses import dataclass
from src.ch00_py.dict_toolbox import get_empty_dict_if_None, get_False_if_None
from src.ch02_partner.group import GroupTitle, GroupUnit
from src.ch02_partner.partner import PartnerName


@dataclass
class LaborUnit:
    labor_title: GroupTitle = None
    solo: bool = None

    def to_dict(self) -> dict[str,]:
        """Returns dict that is serializable to JSON."""

        x_dict = {"labor_title": self.labor_title}
        if self.solo is True:
            x_dict["solo"] = self.solo
        return x_dict


def laborunit_shop(labor_title: GroupTitle, solo: bool = None) -> LaborUnit:
    return LaborUnit(labor_title=labor_title, solo=get_False_if_None(solo))


def laborunit_get_from_dict(x_dict: dict) -> LaborUnit:
    return laborunit_shop(x_dict.get("labor_title"), solo=x_dict.get("solo"))


@dataclass
class LaborHeir:
    labor_title: GroupTitle = None
    solo: bool = None
    parent_solo: bool = None


def laborheir_shop(labor_title: GroupTitle, solo: bool) -> LaborHeir:
    return LaborHeir(labor_title=labor_title, solo=solo)


@dataclass
class WorkforceUnit:
    labors: dict[GroupTitle, LaborUnit] = None

    def to_dict(self) -> dict[str, str]:
        """Returns dict that is serializable to JSON."""

        labors_dict = {
            labor_title: laborunit.to_dict()
            for labor_title, laborunit in self.labors.items()
        }
        return {"labors": labors_dict}

    def add_labor(self, labor_title: GroupTitle, solo: bool = None):
        self.labors[labor_title] = laborunit_shop(labor_title, solo)

    def laborunit_exists(self, labor_title: GroupTitle):
        return labor_title in self.labors

    def del_laborunit(self, labor_title: GroupTitle):
        self.labors.pop(labor_title)

    def get_laborunit(self, labor_title: GroupTitle) -> LaborUnit:
        if self.laborunit_exists(labor_title):
            return self.labors.get(labor_title)


def workforceunit_shop(labors: dict[GroupTitle, LaborUnit] = None) -> WorkforceUnit:
    return WorkforceUnit(get_empty_dict_if_None(labors))


def get_workforceunit_from_dict(workforceunit_dict: dict) -> WorkforceUnit:
    x_workforceunit = workforceunit_shop()
    labors_dict = workforceunit_dict.get("labors")
    for labor_dict in labors_dict.values():
        x_workforceunit.add_labor(
            labor_title=labor_dict.get("labor_title"), solo=labor_dict.get("solo")
        )
    return x_workforceunit


@dataclass
class WorkforceHeir:
    labors: dict[GroupTitle, LaborHeir] = None
    person_name_is_workforce: bool = None

    def labors_empty(self) -> bool:
        return self.labors == {}

    def set_person_name_is_workforce(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        person_name: PartnerName,
    ):
        self.person_name_is_workforce = self.get_person_name_is_workforce_bool(
            groupunits=groupunits, person_name=person_name
        )

    def get_person_name_is_workforce_bool(
        self,
        groupunits: dict[GroupTitle, GroupUnit],
        person_name: PartnerName,
    ) -> bool:
        if self.labors == {}:
            return True

        for x_labor_title, x_groupunit in groupunits.items():
            if x_labor_title in self.labors:
                for x_partner_name in x_groupunit.memberships.keys():
                    if x_partner_name == person_name:
                        return True
        return False

    def set_labors(
        self,
        parent_workforceheir,
        workforceunit: WorkforceUnit,
        groupunits: dict[GroupTitle, GroupUnit],
    ):
        self.labors = {}
        # there is no parent workforceheir or parent workforceheir is empty
        if parent_workforceheir is None or parent_workforceheir.labors == {}:
            for laborunit in workforceunit.labors.values():
                _set_labor_to_labors(self.labors, laborunit)
        # current workforceunit is not empty and parent workforceheir is empty
        elif workforceunit.labors == {}:
            for parent_laborheir in parent_workforceheir.labors.values():
                _set_labor_to_labors(self.labors, parent_laborheir)
        # current workforceunit is not empty and parent workforceheir is not empty
        else:
            # grab all parent heirs first
            for parent_laborheir in parent_workforceheir.labors.values():
                _set_labor_to_labors(self.labors, parent_laborheir)
            # if it doesn't exist add current workforceunit
            for laborunit in workforceunit.labors.values():
                if self.labors.get(laborunit.labor_title) is None:
                    _set_labor_to_labors(self.labors, laborunit)

    def has_labor(self, labor_titles: set[GroupTitle]):
        return self.labors_empty() or any(gn_x in self.labors for gn_x in labor_titles)


def _set_labor_to_labors(labors: dict, x_labor):
    x_laborheir = laborheir_shop(labor_title=x_labor.labor_title, solo=x_labor.solo)
    labors[x_laborheir.labor_title] = x_laborheir


def workforceheir_shop(
    labors: dict[GroupTitle, LaborHeir] = None, person_name_is_workforce: bool = None
) -> WorkforceHeir:
    labors = get_empty_dict_if_None(labors)
    person_name_is_workforce = get_False_if_None(person_name_is_workforce)
    return WorkforceHeir(
        labors=labors, person_name_is_workforce=person_name_is_workforce
    )
