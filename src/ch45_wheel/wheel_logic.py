from dataclasses import dataclass

FAMU_STATUSES = {"winning", "losing", "stable", None}


class FamuStatusError(Exception):
    pass


@dataclass
class FamilyUnit:
    famu_name: str = None
    prestige: bool = None
    famu_status: str = None

    def set_famu_status(self, famu_status: str) -> None:
        if famu_status not in FAMU_STATUSES:
            error_str = f"FamilyUnit '{self.famu_name}': '{famu_status}' is not acceptable famu_status."
            raise FamuStatusError(error_str)
        self.famu_status = famu_status


def familyunit_shop(famu_name: str, famu_status: str = None) -> FamilyUnit:
    x_familyunit = FamilyUnit(famu_name, prestige=False)
    x_familyunit.set_famu_status(famu_status)
    return x_familyunit


@dataclass
class PillarUnit:
    pillar_name: str = None
    bearers: set[FamilyUnit] = None


def pillarunit_shop(pillar_name: str) -> PillarUnit:
    return PillarUnit(pillar_name=pillar_name, bearers={})


@dataclass
class WheelUnit:
    wheel_name: str = None
    familyunits: dict[str, FamilyUnit] = None
    stable_size: float = None
    moving_size: float = None

    def familyunit_exists(self, famu_name: str) -> bool:
        return self.familyunits.get(famu_name) is not None

    def set_familyunit(self, familyunit: FamilyUnit):
        if familyunit.famu_status not in FAMU_STATUSES:
            error_str = f"FamilyUnit '{familyunit.famu_name}': '{familyunit.famu_status}' is not acceptable famu_status."
            raise FamuStatusError(error_str)
        self.familyunits[familyunit.famu_name] = familyunit

    def del_familyunit(self, famu_name: str):
        self.familyunits.pop(famu_name)

    def get_familyunit(self, famu_name: str) -> FamilyUnit:
        return self.familyunits.get(famu_name)

    def get_famu_status_familyunits(self, famu_status: str) -> list[FamilyUnit]:
        stable_familyunits = []
        stable_familyunits.extend(
            familyunit
            for familyunit in self.familyunits.values()
            if familyunit.famu_status == famu_status
        )
        return stable_familyunits

    def get_stable_familyunits(self) -> list[FamilyUnit]:
        return self.get_famu_status_familyunits("stable")

    def get_winning_familyunits(self) -> list[FamilyUnit]:
        return self.get_famu_status_familyunits("winning")

    def get_losing_familyunits(self) -> list[FamilyUnit]:
        return self.get_famu_status_familyunits("losing")

    def get_no_prestige_familyunits(self) -> list[FamilyUnit]:
        return self.get_famu_status_familyunits(None)


def wheelunit_shop(wheel_name: str) -> WheelUnit:
    x_wheelunit = WheelUnit(wheel_name)
    x_wheelunit.familyunits = {}
    return x_wheelunit


@dataclass
class LandUnit:
    land_name: str = None
    pillars: set[PillarUnit] = None


def landunit_shop(land_name: str) -> LandUnit:
    return LandUnit(land_name=land_name, pillars=set())
