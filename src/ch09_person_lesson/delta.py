from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.ch00_py.dict_toolbox import (
    get_0_if_None,
    get_all_nondictionary_objs,
    get_empty_dict_if_None,
    get_from_nested_dict,
    set_in_nested_dict,
)
from src.ch02_partner.group import MemberShip
from src.ch02_partner.partner import MemberShip, PartnerName, PartnerUnit
from src.ch05_reason.reason_main import FactUnit, ReasonUnit
from src.ch06_plan.plan import PlanUnit
from src.ch07_person_logic.person_main import PersonUnit, personunit_shop
from src.ch08_person_atom.atom_config import CRUD_command
from src.ch08_person_atom.atom_main import (
    PersonAtom,
    get_personatom_from_dict,
    jvalues_different,
    modify_person_with_personatom,
    personatom_shop,
    sift_personatom,
)
from src.ch09_person_lesson._ref.ch09_semantic_types import RopeTerm, TitleTerm


class InvalidPersonAtomError(Exception):
    pass


@dataclass
class PersonDelta:
    personatoms: dict[CRUD_command : dict[str, PersonAtom]] = None
    person_build_validated: bool = None

    def _get_crud_personatoms_list(self) -> dict[CRUD_command, list[PersonAtom]]:
        return get_all_nondictionary_objs(self.personatoms)

    def get_dimen_sorted_personatoms_list(self) -> list[PersonAtom]:
        atoms_list = []
        for crud_list in self._get_crud_personatoms_list().values():
            atoms_list.extend(iter(crud_list))

        atom_order_key_dict = {}
        for x_atom in atoms_list:
            atom_order_list = atom_order_key_dict.get(x_atom.atom_order)
            if atom_order_list is None:
                atom_order_key_dict[x_atom.atom_order] = [x_atom]
            else:
                atom_order_list.append(x_atom)

        ordered_list = []
        for x_list in atom_order_key_dict.values():
            if x_list[0].jkeys.get("plan_rope") is not None:
                x_list = sorted(x_list, key=lambda x: x.jkeys.get("plan_rope"))
            ordered_list.extend(x_list)
        return ordered_list

    def get_sorted_personatoms(self) -> list[PersonAtom]:
        personatoms_list = self.get_dimen_sorted_personatoms_list()
        return sorted(personatoms_list, key=lambda x: x.atom_order)

    def get_atom_edited_person(self, before_person: PersonUnit) -> PersonUnit:
        edited_person = copy_deepcopy(before_person)
        for x_personatom in self.get_sorted_personatoms():
            modify_person_with_personatom(edited_person, x_personatom)
        return edited_person

    def set_personatom(self, x_personatom: PersonAtom):
        if x_personatom.is_valid() is False:
            raise InvalidPersonAtomError(
                f"""'{x_personatom.dimen}' {x_personatom.crud_str} PersonAtom is invalid
                {x_personatom.is_jkeys_valid()=}
                {x_personatom.is_jvalues_valid()=}"""
            )

        x_personatom.set_atom_order()
        x_keylist = [
            x_personatom.crud_str,
            x_personatom.dimen,
            *x_personatom.get_nesting_order_args(),
        ]
        set_in_nested_dict(self.personatoms, x_keylist, x_personatom)

    def c_personatom_exists(self, x_personatom: PersonAtom) -> bool:
        if x_personatom.is_valid() is False:
            raise InvalidPersonAtomError(
                f"""'{x_personatom.dimen}' {x_personatom.crud_str} PersonAtom is invalid
                {x_personatom.is_jkeys_valid()=}
                {x_personatom.is_jvalues_valid()=}"""
            )

        x_personatom.set_atom_order()
        x_keylist = [
            x_personatom.crud_str,
            x_personatom.dimen,
            *list(x_personatom.get_nesting_order_args()),
        ]
        nested_personatom = get_from_nested_dict(self.personatoms, x_keylist, True)
        return nested_personatom == x_personatom

    def add_personatom(
        self,
        dimen: str,
        crud_str: str,
        jkeys: dict[str, str] = None,
        jvalues: dict[str, str] = None,
    ):
        x_personatom = personatom_shop(
            dimen=dimen,
            crud_str=crud_str,
            jkeys=jkeys,
            jvalues=jvalues,
        )
        self.set_personatom(x_personatom)

    def get_personatom(self, crud_str: str, dimen: str, jkeys: list[str]) -> PersonAtom:
        x_keylist = [crud_str, dimen, *jkeys]
        return get_from_nested_dict(self.personatoms, x_keylist)

    def add_all_personatoms(self, after_person: PersonUnit):
        before_person = personunit_shop(
            after_person.person_name, after_person.planroot.get_plan_rope()
        )
        self.add_all_different_personatoms(before_person, after_person)

    def add_all_different_personatoms(
        self, before_person: PersonUnit, after_person: PersonUnit
    ):
        before_person.conpute()
        after_person.conpute()
        self.add_personatoms_personunit_simple_attrs(before_person, after_person)
        self.add_personatoms_partners(before_person, after_person)
        self.add_personatoms_plans(before_person, after_person)

    def add_personatoms_personunit_simple_attrs(
        self, before_person: PersonUnit, after_person: PersonUnit
    ):
        if not jvalues_different("personunit", before_person, after_person):
            return
        x_personatom = personatom_shop("personunit", "UPDATE")
        if before_person.max_tree_traverse != after_person.max_tree_traverse:
            x_personatom.set_jvalue("max_tree_traverse", after_person.max_tree_traverse)
        if before_person.credor_respect != after_person.credor_respect:
            x_personatom.set_jvalue("credor_respect", after_person.credor_respect)
        if before_person.debtor_respect != after_person.debtor_respect:
            x_personatom.set_jvalue("debtor_respect", after_person.debtor_respect)
        if before_person.fund_pool != after_person.fund_pool:
            x_personatom.set_jvalue("fund_pool", after_person.fund_pool)
        if before_person.fund_grain != after_person.fund_grain:
            x_personatom.set_jvalue("fund_grain", after_person.fund_grain)
        if before_person.respect_grain != after_person.respect_grain:
            x_personatom.set_jvalue("respect_grain", after_person.respect_grain)
        self.set_personatom(x_personatom)

    def add_personatoms_partners(
        self, before_person: PersonUnit, after_person: PersonUnit
    ):
        before_partner_names = set(before_person.partners.keys())
        after_partner_names = set(after_person.partners.keys())

        self.add_personatom_partnerunit_inserts(
            after_person=after_person,
            insert_partner_names=after_partner_names.difference(before_partner_names),
        )
        self.add_personatom_partnerunit_deletes(
            before_person=before_person,
            delete_partner_names=before_partner_names.difference(after_partner_names),
        )
        self.add_personatom_partnerunit_updates(
            before_person=before_person,
            after_person=after_person,
            update_partner_names=before_partner_names & (after_partner_names),
        )

    def add_personatom_partnerunit_inserts(
        self, after_person: PersonUnit, insert_partner_names: set
    ):
        for insert_partner_name in insert_partner_names:
            insert_partnerunit = after_person.get_partner(insert_partner_name)
            x_personatom = personatom_shop("person_partnerunit", "INSERT")
            x_personatom.set_jkey("partner_name", insert_partnerunit.partner_name)
            if insert_partnerunit.partner_cred_lumen is not None:
                x_personatom.set_jvalue(
                    "partner_cred_lumen", insert_partnerunit.partner_cred_lumen
                )
            if insert_partnerunit.partner_debt_lumen is not None:
                x_personatom.set_jvalue(
                    "partner_debt_lumen", insert_partnerunit.partner_debt_lumen
                )
            self.set_personatom(x_personatom)
            all_group_titles = set(insert_partnerunit.memberships.keys())
            self.add_personatom_memberships_inserts(
                after_partnerunit=insert_partnerunit,
                insert_membership_group_titles=all_group_titles,
            )

    def add_personatom_partnerunit_updates(
        self,
        before_person: PersonUnit,
        after_person: PersonUnit,
        update_partner_names: set,
    ):
        for partner_name in update_partner_names:
            after_partnerunit = after_person.get_partner(partner_name)
            before_partnerunit = before_person.get_partner(partner_name)
            if jvalues_different(
                "person_partnerunit", after_partnerunit, before_partnerunit
            ):
                x_personatom = personatom_shop("person_partnerunit", "UPDATE")
                x_personatom.set_jkey("partner_name", after_partnerunit.partner_name)
                if (
                    before_partnerunit.partner_cred_lumen
                    != after_partnerunit.partner_cred_lumen
                ):
                    x_personatom.set_jvalue(
                        "partner_cred_lumen", after_partnerunit.partner_cred_lumen
                    )
                if (
                    before_partnerunit.partner_debt_lumen
                    != after_partnerunit.partner_debt_lumen
                ):
                    x_personatom.set_jvalue(
                        "partner_debt_lumen", after_partnerunit.partner_debt_lumen
                    )
                self.set_personatom(x_personatom)
            self.add_personatom_partnerunit_update_memberships(
                after_partnerunit=after_partnerunit,
                before_partnerunit=before_partnerunit,
            )

    def add_personatom_partnerunit_deletes(
        self, before_person: PersonUnit, delete_partner_names: set
    ):
        for delete_partner_name in delete_partner_names:
            x_personatom = personatom_shop("person_partnerunit", "DELETE")
            x_personatom.set_jkey("partner_name", delete_partner_name)
            self.set_personatom(x_personatom)
            delete_partnerunit = before_person.get_partner(delete_partner_name)
            non_mirror_group_titles = {
                x_group_title
                for x_group_title in delete_partnerunit.memberships.keys()
                if x_group_title != delete_partner_name
            }
            self.add_personatom_memberships_delete(
                delete_partner_name, non_mirror_group_titles
            )

    def add_personatom_partnerunit_update_memberships(
        self, after_partnerunit: PartnerUnit, before_partnerunit: PartnerUnit
    ):
        # before_non_mirror_group_titles
        before_group_titles = {
            x_group_title
            for x_group_title in before_partnerunit.memberships.keys()
            if x_group_title != before_partnerunit.partner_name
        }
        # after_non_mirror_group_titles
        after_group_titles = {
            x_group_title
            for x_group_title in after_partnerunit.memberships.keys()
            if x_group_title != after_partnerunit.partner_name
        }

        self.add_personatom_memberships_inserts(
            after_partnerunit=after_partnerunit,
            insert_membership_group_titles=after_group_titles.difference(
                before_group_titles
            ),
        )

        self.add_personatom_memberships_delete(
            before_partner_name=after_partnerunit.partner_name,
            before_group_titles=before_group_titles.difference(after_group_titles),
        )

        update_group_titles = before_group_titles & (after_group_titles)
        for update_partner_name in update_group_titles:
            before_membership = before_partnerunit.get_membership(update_partner_name)
            after_membership = after_partnerunit.get_membership(update_partner_name)
            if jvalues_different(
                "person_partner_membership", before_membership, after_membership
            ):
                self.add_personatom_membership_update(
                    partner_name=after_partnerunit.partner_name,
                    before_membership=before_membership,
                    after_membership=after_membership,
                )

    def add_personatom_memberships_inserts(
        self,
        after_partnerunit: PartnerUnit,
        insert_membership_group_titles: list[TitleTerm],
    ):
        after_partner_name = after_partnerunit.partner_name
        for insert_group_title in insert_membership_group_titles:
            after_membership = after_partnerunit.get_membership(insert_group_title)
            x_personatom = personatom_shop("person_partner_membership", "INSERT")
            x_personatom.set_jkey("partner_name", after_partner_name)
            x_personatom.set_jkey("group_title", after_membership.group_title)
            if after_membership.group_cred_lumen is not None:
                x_personatom.set_jvalue(
                    "group_cred_lumen", after_membership.group_cred_lumen
                )
            if after_membership.group_debt_lumen is not None:
                x_personatom.set_jvalue(
                    "group_debt_lumen", after_membership.group_debt_lumen
                )
            self.set_personatom(x_personatom)

    def add_personatom_membership_update(
        self,
        partner_name: PartnerName,
        before_membership: MemberShip,
        after_membership: MemberShip,
    ):
        x_personatom = personatom_shop("person_partner_membership", "UPDATE")
        x_personatom.set_jkey("partner_name", partner_name)
        x_personatom.set_jkey("group_title", after_membership.group_title)
        if after_membership.group_cred_lumen != before_membership.group_cred_lumen:
            x_personatom.set_jvalue(
                "group_cred_lumen", after_membership.group_cred_lumen
            )
        if after_membership.group_debt_lumen != before_membership.group_debt_lumen:
            x_personatom.set_jvalue(
                "group_debt_lumen", after_membership.group_debt_lumen
            )
        self.set_personatom(x_personatom)

    def add_personatom_memberships_delete(
        self, before_partner_name: PartnerName, before_group_titles: TitleTerm
    ):
        for delete_group_title in before_group_titles:
            x_personatom = personatom_shop("person_partner_membership", "DELETE")
            x_personatom.set_jkey("partner_name", before_partner_name)
            x_personatom.set_jkey("group_title", delete_group_title)
            self.set_personatom(x_personatom)

    def add_personatoms_plans(
        self, before_person: PersonUnit, after_person: PersonUnit
    ):
        before_plan_ropes = set(before_person._plan_dict.keys())
        after_plan_ropes = set(after_person._plan_dict.keys())

        self.add_personatom_plan_inserts(
            after_person=after_person,
            insert_plan_ropes=after_plan_ropes.difference(before_plan_ropes),
        )
        self.add_personatom_plan_deletes(
            before_person=before_person,
            delete_plan_ropes=before_plan_ropes.difference(after_plan_ropes),
        )
        self.add_personatom_plan_updates(
            before_person=before_person,
            after_person=after_person,
            update_ropes=before_plan_ropes & (after_plan_ropes),
        )

    def add_personatom_plan_inserts(
        self, after_person: PersonUnit, insert_plan_ropes: set
    ):
        for insert_plan_rope in insert_plan_ropes:
            insert_planunit = after_person.get_plan_obj(insert_plan_rope)
            x_personatom = personatom_shop("person_planunit", "INSERT")
            x_personatom.set_jkey("plan_rope", insert_planunit.get_plan_rope())
            x_personatom.set_jvalue("addin", insert_planunit.addin)
            x_personatom.set_jvalue("begin", insert_planunit.begin)
            x_personatom.set_jvalue("close", insert_planunit.close)
            x_personatom.set_jvalue("denom", insert_planunit.denom)
            x_personatom.set_jvalue("numor", insert_planunit.numor)
            x_personatom.set_jvalue("morph", insert_planunit.morph)
            x_personatom.set_jvalue("star", insert_planunit.star)
            x_personatom.set_jvalue("pledge", insert_planunit.pledge)
            self.set_personatom(x_personatom)

            self.add_personatom_plan_factunit_inserts(
                planunit=insert_planunit,
                insert_factunit_reason_contexts=set(insert_planunit.factunits.keys()),
            )
            self.add_personatom_plan_awardunit_inserts(
                after_planunit=insert_planunit,
                insert_awardunit_awardee_titles=set(insert_planunit.awardunits.keys()),
            )
            self.add_personatom_plan_reasonunit_inserts(
                after_planunit=insert_planunit,
                insert_reasonunit_reason_contexts=set(
                    insert_planunit.reasonunits.keys()
                ),
            )
            self.add_personatom_plan_laborunit_insert(
                plan_rope=insert_plan_rope,
                insert_laborunit_labor_titles=insert_planunit.workforceunit.labors,
            )
            self.add_personatom_plan_healerunit_insert(
                plan_rope=insert_plan_rope,
                insert_healerunit_healer_names=insert_planunit.healerunit.healer_names,
            )

    def add_personatom_plan_updates(
        self,
        before_person: PersonUnit,
        after_person: PersonUnit,
        update_ropes: set,
    ):
        for plan_rope in update_ropes:
            after_planunit = after_person.get_plan_obj(plan_rope)
            before_planunit = before_person.get_plan_obj(plan_rope)
            if jvalues_different("person_planunit", before_planunit, after_planunit):
                x_personatom = personatom_shop("person_planunit", "UPDATE")
                x_personatom.set_jkey("plan_rope", after_planunit.get_plan_rope())
                if before_planunit.addin != after_planunit.addin:
                    x_personatom.set_jvalue("addin", after_planunit.addin)
                if before_planunit.begin != after_planunit.begin:
                    x_personatom.set_jvalue("begin", after_planunit.begin)
                if before_planunit.close != after_planunit.close:
                    x_personatom.set_jvalue("close", after_planunit.close)
                if before_planunit.denom != after_planunit.denom:
                    x_personatom.set_jvalue("denom", after_planunit.denom)
                if before_planunit.numor != after_planunit.numor:
                    x_personatom.set_jvalue("numor", after_planunit.numor)
                if before_planunit.morph != after_planunit.morph:
                    x_personatom.set_jvalue("morph", after_planunit.morph)
                if before_planunit.star != after_planunit.star:
                    x_personatom.set_jvalue("star", after_planunit.star)
                if before_planunit.pledge != after_planunit.pledge:
                    x_personatom.set_jvalue("pledge", after_planunit.pledge)
                self.set_personatom(x_personatom)

            # insert / update / delete factunits
            before_factunit_reason_contexts = set(before_planunit.factunits.keys())
            after_factunit_reason_contexts = set(after_planunit.factunits.keys())
            self.add_personatom_plan_factunit_inserts(
                planunit=after_planunit,
                insert_factunit_reason_contexts=after_factunit_reason_contexts.difference(
                    before_factunit_reason_contexts
                ),
            )
            self.add_personatom_plan_factunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_factunit_reason_contexts=before_factunit_reason_contexts
                & (after_factunit_reason_contexts),
            )
            self.add_personatom_plan_factunit_deletes(
                plan_rope=plan_rope,
                delete_factunit_reason_contexts=before_factunit_reason_contexts.difference(
                    after_factunit_reason_contexts
                ),
            )

            # insert / update / delete awardunits
            before_awardunits_awardee_titles = set(before_planunit.awardunits.keys())
            after_awardunits_awardee_titles = set(after_planunit.awardunits.keys())
            self.add_personatom_plan_awardunit_inserts(
                after_planunit=after_planunit,
                insert_awardunit_awardee_titles=after_awardunits_awardee_titles.difference(
                    before_awardunits_awardee_titles
                ),
            )
            self.add_personatom_plan_awardunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_awardunit_awardee_titles=before_awardunits_awardee_titles
                & (after_awardunits_awardee_titles),
            )
            self.add_personatom_plan_awardunit_deletes(
                plan_rope=plan_rope,
                delete_awardunit_awardee_titles=before_awardunits_awardee_titles.difference(
                    after_awardunits_awardee_titles
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_reason_contexts = set(before_planunit.reasonunits.keys())
            after_reasonunit_reason_contexts = set(after_planunit.reasonunits.keys())
            self.add_personatom_plan_reasonunit_inserts(
                after_planunit=after_planunit,
                insert_reasonunit_reason_contexts=after_reasonunit_reason_contexts.difference(
                    before_reasonunit_reason_contexts
                ),
            )
            self.add_personatom_plan_reasonunit_updates(
                before_planunit=before_planunit,
                after_planunit=after_planunit,
                update_reasonunit_reason_contexts=before_reasonunit_reason_contexts
                & (after_reasonunit_reason_contexts),
            )
            self.add_personatom_plan_reasonunit_deletes(
                before_planunit=before_planunit,
                delete_reasonunit_reason_contexts=before_reasonunit_reason_contexts.difference(
                    after_reasonunit_reason_contexts
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_case
            # update reasonunits_permises update_case
            # update reasonunits_permises delete_case

            # insert / update / delete laborunits
            before_labors_labor_titles = set(before_planunit.workforceunit.labors)
            after_labors_labor_titles = set(after_planunit.workforceunit.labors)
            self.add_personatom_plan_laborunit_insert(
                plan_rope=plan_rope,
                insert_laborunit_labor_titles=after_labors_labor_titles.difference(
                    before_labors_labor_titles
                ),
            )
            self.add_personatom_plan_laborunit_deletes(
                plan_rope=plan_rope,
                delete_laborunit_labor_titles=before_labors_labor_titles.difference(
                    after_labors_labor_titles
                ),
            )

            # insert / update / delete healerunits
            before_healerunits_healer_names = set(
                before_planunit.healerunit.healer_names
            )
            after_healerunits_healer_names = set(after_planunit.healerunit.healer_names)
            self.add_personatom_plan_healerunit_insert(
                plan_rope=plan_rope,
                insert_healerunit_healer_names=after_healerunits_healer_names.difference(
                    before_healerunits_healer_names
                ),
            )
            self.add_personatom_plan_healerunit_deletes(
                plan_rope=plan_rope,
                delete_healerunit_healer_names=before_healerunits_healer_names.difference(
                    after_healerunits_healer_names
                ),
            )

    def add_personatom_plan_deletes(
        self, before_person: PersonUnit, delete_plan_ropes: set
    ):
        for delete_plan_rope in delete_plan_ropes:
            x_personatom = personatom_shop("person_planunit", "DELETE")
            x_personatom.set_jkey("plan_rope", delete_plan_rope)
            self.set_personatom(x_personatom)

            delete_planunit = before_person.get_plan_obj(delete_plan_rope)
            self.add_personatom_plan_factunit_deletes(
                plan_rope=delete_plan_rope,
                delete_factunit_reason_contexts=set(delete_planunit.factunits.keys()),
            )

            self.add_personatom_plan_awardunit_deletes(
                plan_rope=delete_plan_rope,
                delete_awardunit_awardee_titles=set(delete_planunit.awardunits.keys()),
            )
            self.add_personatom_plan_reasonunit_deletes(
                before_planunit=delete_planunit,
                delete_reasonunit_reason_contexts=set(
                    delete_planunit.reasonunits.keys()
                ),
            )
            self.add_personatom_plan_laborunit_deletes(
                plan_rope=delete_plan_rope,
                delete_laborunit_labor_titles=delete_planunit.workforceunit.labors,
            )
            self.add_personatom_plan_healerunit_deletes(
                plan_rope=delete_plan_rope,
                delete_healerunit_healer_names=delete_planunit.healerunit.healer_names,
            )

    def add_personatom_plan_reasonunit_inserts(
        self, after_planunit: PlanUnit, insert_reasonunit_reason_contexts: set
    ):
        for insert_reasonunit_reason_context in insert_reasonunit_reason_contexts:
            after_reasonunit = after_planunit.get_reasonunit(
                insert_reasonunit_reason_context
            )
            x_personatom = personatom_shop("person_plan_reasonunit", "INSERT")
            x_personatom.set_jkey("plan_rope", after_planunit.get_plan_rope())
            x_personatom.set_jkey("reason_context", after_reasonunit.reason_context)
            if after_reasonunit.active_requisite is not None:
                x_personatom.set_jvalue(
                    "active_requisite",
                    after_reasonunit.active_requisite,
                )
            self.set_personatom(x_personatom)

            self.add_personatom_plan_reason_caseunit_inserts(
                plan_rope=after_planunit.get_plan_rope(),
                after_reasonunit=after_reasonunit,
                insert_case_reason_states=set(after_reasonunit.cases.keys()),
            )

    def add_personatom_plan_reasonunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_reasonunit_reason_contexts: set,
    ):
        for update_reasonunit_reason_context in update_reasonunit_reason_contexts:
            before_reasonunit = before_planunit.get_reasonunit(
                update_reasonunit_reason_context
            )
            after_reasonunit = after_planunit.get_reasonunit(
                update_reasonunit_reason_context
            )
            if jvalues_different(
                "person_plan_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_personatom = personatom_shop("person_plan_reasonunit", "UPDATE")
                x_personatom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_personatom.set_jkey("reason_context", after_reasonunit.reason_context)
                if (
                    before_reasonunit.active_requisite
                    != after_reasonunit.active_requisite
                ):
                    x_personatom.set_jvalue(
                        "active_requisite",
                        after_reasonunit.active_requisite,
                    )
                self.set_personatom(x_personatom)

            before_case_reason_states = set(before_reasonunit.cases.keys())
            after_case_reason_states = set(after_reasonunit.cases.keys())
            self.add_personatom_plan_reason_caseunit_inserts(
                plan_rope=before_planunit.get_plan_rope(),
                after_reasonunit=after_reasonunit,
                insert_case_reason_states=after_case_reason_states.difference(
                    before_case_reason_states
                ),
            )
            self.add_personatom_plan_reason_caseunit_updates(
                plan_rope=before_planunit.get_plan_rope(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_case_reason_states=after_case_reason_states
                & (before_case_reason_states),
            )
            self.add_personatom_plan_reason_caseunit_deletes(
                plan_rope=before_planunit.get_plan_rope(),
                reasonunit_reason_context=update_reasonunit_reason_context,
                delete_case_reason_states=before_case_reason_states.difference(
                    after_case_reason_states
                ),
            )

    def add_personatom_plan_reasonunit_deletes(
        self, before_planunit: PlanUnit, delete_reasonunit_reason_contexts: set
    ):
        for delete_reasonunit_reason_context in delete_reasonunit_reason_contexts:
            x_personatom = personatom_shop("person_plan_reasonunit", "DELETE")
            x_personatom.set_jkey("plan_rope", before_planunit.get_plan_rope())
            x_personatom.set_jkey("reason_context", delete_reasonunit_reason_context)
            self.set_personatom(x_personatom)

            before_reasonunit = before_planunit.get_reasonunit(
                delete_reasonunit_reason_context
            )
            self.add_personatom_plan_reason_caseunit_deletes(
                plan_rope=before_planunit.get_plan_rope(),
                reasonunit_reason_context=delete_reasonunit_reason_context,
                delete_case_reason_states=set(before_reasonunit.cases.keys()),
            )

    def add_personatom_plan_reason_caseunit_inserts(
        self,
        plan_rope: RopeTerm,
        after_reasonunit: ReasonUnit,
        insert_case_reason_states: set,
    ):
        for insert_case_reason_state in insert_case_reason_states:
            after_caseunit = after_reasonunit.get_case(insert_case_reason_state)
            x_personatom = personatom_shop("person_plan_reason_caseunit", "INSERT")
            x_personatom.set_jkey("plan_rope", plan_rope)
            x_personatom.set_jkey("reason_context", after_reasonunit.reason_context)
            x_personatom.set_jkey("reason_state", after_caseunit.reason_state)
            if after_caseunit.reason_lower is not None:
                x_personatom.set_jvalue("reason_lower", after_caseunit.reason_lower)
            if after_caseunit.reason_upper is not None:
                x_personatom.set_jvalue("reason_upper", after_caseunit.reason_upper)
            if after_caseunit.reason_divisor is not None:
                x_personatom.set_jvalue("reason_divisor", after_caseunit.reason_divisor)
            self.set_personatom(x_personatom)

    def add_personatom_plan_reason_caseunit_updates(
        self,
        plan_rope: RopeTerm,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_case_reason_states: set,
    ):
        for update_case_reason_state in update_case_reason_states:
            before_caseunit = before_reasonunit.get_case(update_case_reason_state)
            after_caseunit = after_reasonunit.get_case(update_case_reason_state)
            if jvalues_different(
                "person_plan_reason_caseunit",
                before_caseunit,
                after_caseunit,
            ):
                x_personatom = personatom_shop("person_plan_reason_caseunit", "UPDATE")
                x_personatom.set_jkey("plan_rope", plan_rope)
                x_personatom.set_jkey(
                    "reason_context", before_reasonunit.reason_context
                )
                x_personatom.set_jkey("reason_state", after_caseunit.reason_state)
                if after_caseunit.reason_lower != before_caseunit.reason_lower:
                    x_personatom.set_jvalue("reason_lower", after_caseunit.reason_lower)
                if after_caseunit.reason_upper != before_caseunit.reason_upper:
                    x_personatom.set_jvalue("reason_upper", after_caseunit.reason_upper)
                if after_caseunit.reason_divisor != before_caseunit.reason_divisor:
                    x_personatom.set_jvalue(
                        "reason_divisor", after_caseunit.reason_divisor
                    )
                self.set_personatom(x_personatom)

    def add_personatom_plan_reason_caseunit_deletes(
        self,
        plan_rope: RopeTerm,
        reasonunit_reason_context: RopeTerm,
        delete_case_reason_states: set,
    ):
        for delete_case_reason_state in delete_case_reason_states:
            x_personatom = personatom_shop("person_plan_reason_caseunit", "DELETE")
            x_personatom.set_jkey("plan_rope", plan_rope)
            x_personatom.set_jkey("reason_context", reasonunit_reason_context)
            x_personatom.set_jkey("reason_state", delete_case_reason_state)
            self.set_personatom(x_personatom)

    def add_personatom_plan_laborunit_insert(
        self, plan_rope: RopeTerm, insert_laborunit_labor_titles: set
    ):
        for insert_laborunit_labor_title in insert_laborunit_labor_titles:
            x_personatom = personatom_shop("person_plan_laborunit", "INSERT")
            x_personatom.set_jkey("plan_rope", plan_rope)
            x_personatom.set_jkey("labor_title", insert_laborunit_labor_title)
            self.set_personatom(x_personatom)

    def add_personatom_plan_laborunit_deletes(
        self, plan_rope: RopeTerm, delete_laborunit_labor_titles: set
    ):
        for delete_laborunit_labor_title in delete_laborunit_labor_titles:
            x_personatom = personatom_shop("person_plan_laborunit", "DELETE")
            x_personatom.set_jkey("plan_rope", plan_rope)
            x_personatom.set_jkey("labor_title", delete_laborunit_labor_title)
            self.set_personatom(x_personatom)

    def add_personatom_plan_healerunit_insert(
        self, plan_rope: RopeTerm, insert_healerunit_healer_names: set
    ):
        for insert_healerunit_healer_name in insert_healerunit_healer_names:
            x_personatom = personatom_shop("person_plan_healerunit", "INSERT")
            x_personatom.set_jkey("plan_rope", plan_rope)
            x_personatom.set_jkey("healer_name", insert_healerunit_healer_name)
            self.set_personatom(x_personatom)

    def add_personatom_plan_healerunit_deletes(
        self, plan_rope: RopeTerm, delete_healerunit_healer_names: set
    ):
        for delete_healerunit_healer_name in delete_healerunit_healer_names:
            x_personatom = personatom_shop("person_plan_healerunit", "DELETE")
            x_personatom.set_jkey("plan_rope", plan_rope)
            x_personatom.set_jkey("healer_name", delete_healerunit_healer_name)
            self.set_personatom(x_personatom)

    def add_personatom_plan_awardunit_inserts(
        self, after_planunit: PlanUnit, insert_awardunit_awardee_titles: set
    ):
        for after_awardunit_awardee_title in insert_awardunit_awardee_titles:
            after_awardunit = after_planunit.awardunits.get(
                after_awardunit_awardee_title
            )
            x_personatom = personatom_shop("person_plan_awardunit", "INSERT")
            x_personatom.set_jkey("plan_rope", after_planunit.get_plan_rope())
            x_personatom.set_jkey("awardee_title", after_awardunit.awardee_title)
            x_personatom.set_jvalue("give_force", after_awardunit.give_force)
            x_personatom.set_jvalue("take_force", after_awardunit.take_force)
            self.set_personatom(x_personatom)

    def add_personatom_plan_awardunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_awardunit_awardee_titles: set,
    ):
        for update_awardunit_awardee_title in update_awardunit_awardee_titles:
            before_awardunit = before_planunit.awardunits.get(
                update_awardunit_awardee_title
            )
            after_awardunit = after_planunit.awardunits.get(
                update_awardunit_awardee_title
            )
            if jvalues_different(
                "person_plan_awardunit", before_awardunit, after_awardunit
            ):
                x_personatom = personatom_shop("person_plan_awardunit", "UPDATE")
                x_personatom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_personatom.set_jkey("awardee_title", after_awardunit.awardee_title)
                if before_awardunit.give_force != after_awardunit.give_force:
                    x_personatom.set_jvalue("give_force", after_awardunit.give_force)
                if before_awardunit.take_force != after_awardunit.take_force:
                    x_personatom.set_jvalue("take_force", after_awardunit.take_force)
                self.set_personatom(x_personatom)

    def add_personatom_plan_awardunit_deletes(
        self, plan_rope: RopeTerm, delete_awardunit_awardee_titles: set
    ):
        for delete_awardunit_awardee_title in delete_awardunit_awardee_titles:
            x_personatom = personatom_shop("person_plan_awardunit", "DELETE")
            x_personatom.set_jkey("plan_rope", plan_rope)
            x_personatom.set_jkey("awardee_title", delete_awardunit_awardee_title)
            self.set_personatom(x_personatom)

    def add_personatom_plan_factunit_inserts(
        self, planunit: PlanUnit, insert_factunit_reason_contexts: set
    ):
        for insert_factunit_reason_context in insert_factunit_reason_contexts:
            insert_factunit = planunit.factunits.get(insert_factunit_reason_context)
            x_personatom = personatom_shop("person_plan_factunit", "INSERT")
            x_personatom.set_jkey("plan_rope", planunit.get_plan_rope())
            x_personatom.set_jkey("fact_context", insert_factunit.fact_context)
            if insert_factunit.fact_state is not None:
                x_personatom.set_jvalue("fact_state", insert_factunit.fact_state)
            if insert_factunit.fact_lower is not None:
                x_personatom.set_jvalue("fact_lower", insert_factunit.fact_lower)
            if insert_factunit.fact_upper is not None:
                x_personatom.set_jvalue("fact_upper", insert_factunit.fact_upper)
            self.set_personatom(x_personatom)

    def add_personatom_plan_factunit_updates(
        self,
        before_planunit: PlanUnit,
        after_planunit: PlanUnit,
        update_factunit_reason_contexts: set,
    ):
        for update_factunit_reason_context in update_factunit_reason_contexts:
            before_factunit = before_planunit.factunits.get(
                update_factunit_reason_context
            )
            after_factunit = after_planunit.factunits.get(
                update_factunit_reason_context
            )
            if jvalues_different(
                "person_plan_factunit", before_factunit, after_factunit
            ):
                x_personatom = personatom_shop("person_plan_factunit", "UPDATE")
                x_personatom.set_jkey("plan_rope", before_planunit.get_plan_rope())
                x_personatom.set_jkey("fact_context", after_factunit.fact_context)
                if before_factunit.fact_state != after_factunit.fact_state:
                    x_personatom.set_jvalue("fact_state", after_factunit.fact_state)
                if before_factunit.fact_lower != after_factunit.fact_lower:
                    x_personatom.set_jvalue("fact_lower", after_factunit.fact_lower)
                if before_factunit.fact_upper != after_factunit.fact_upper:
                    x_personatom.set_jvalue("fact_upper", after_factunit.fact_upper)
                self.set_personatom(x_personatom)

    def add_personatom_plan_factunit_deletes(
        self, plan_rope: RopeTerm, delete_factunit_reason_contexts: FactUnit
    ):
        for delete_factunit_reason_context in delete_factunit_reason_contexts:
            x_personatom = personatom_shop("person_plan_factunit", "DELETE")
            x_personatom.set_jkey("plan_rope", plan_rope)
            x_personatom.set_jkey("fact_context", delete_factunit_reason_context)
            self.set_personatom(x_personatom)

    def atoms_empty(self) -> bool:
        return self.personatoms == {}

    def get_ordered_personatoms(self, x_count: int = None) -> dict[int, PersonAtom]:
        x_count = get_0_if_None(x_count)
        x_dict = {}
        for x_atom in self.get_sorted_personatoms():
            x_dict[x_count] = x_atom
            x_count += 1
        return x_dict

    def get_ordered_dict(self, x_count: int = None) -> dict[int, str]:
        atom_tuples = self.get_ordered_personatoms(x_count).items()
        return {atom_num: atom_obj.to_dict() for atom_num, atom_obj in atom_tuples}


def persondelta_shop(personatoms: dict[str, PersonAtom] = None) -> PersonDelta:
    return PersonDelta(
        personatoms=get_empty_dict_if_None(personatoms),
        person_build_validated=False,
    )


def person_built_from_delta_is_valid(
    x_delta: PersonDelta, x_person: PersonUnit = None
) -> bool:
    x_person = personunit_shop() if x_person is None else x_person
    x_person = x_delta.get_atom_edited_person(x_person)
    try:
        x_person.conpute()
    except Exception:
        return False
    return True


def get_dimens_cruds_persondelta(
    x_persondelta: PersonDelta, dimen_set: set[str], curd_set: set[str]
) -> PersonDelta:
    new_persondelta = persondelta_shop()
    for x_personatom in x_persondelta.get_sorted_personatoms():
        if x_personatom.crud_str in curd_set and x_personatom.dimen in dimen_set:
            new_persondelta.set_personatom(x_personatom)
    return new_persondelta


def get_minimal_persondelta(
    x_persondelta: PersonDelta, x_person: PersonUnit
) -> PersonDelta:
    """Creates new PersonDelta with only PersonAtoms that would actually change the PersonUnit"""
    new_persondelta = persondelta_shop()
    for x_atom in x_persondelta.get_sorted_personatoms():
        sifted_atom = sift_personatom(x_person, x_atom)
        if sifted_atom != None:
            new_persondelta.set_personatom(sifted_atom)
    return new_persondelta


def get_persondelta_from_ordered_dict(x_dict: dict) -> PersonDelta:
    x_persondelta = persondelta_shop()
    for x_atom_dict in x_dict.values():
        x_persondelta.set_personatom(get_personatom_from_dict(x_atom_dict))
    return x_persondelta
