from ch00_py.dict_toolbox import get_from_nested_dict
from ch07_person_logic.person_main import PersonUnit
from ch08_person_atom.atom_main import PersonAtom
from ch09_person_lesson.delta import PersonDelta


def get_leg_obj(x_dict: dict, x_keylist) -> any:
    return get_from_nested_dict(x_dict, x_keylist, if_missing_return_None=True)


def create_legible_list(x_delta: PersonDelta, x_person: PersonUnit) -> list[str]:
    atoms_dict = x_delta.personatoms
    personunit_atom = get_leg_obj(atoms_dict, ["UPDATE", "personunit"])

    contactunit_insert_dict = get_leg_obj(atoms_dict, ["INSERT", "person_contactunit"])
    contactunit_update_dict = get_leg_obj(atoms_dict, ["UPDATE", "person_contactunit"])
    contactunit_delete_dict = get_leg_obj(atoms_dict, ["DELETE", "person_contactunit"])

    x_list = ["INSERT", "person_contact_membership"]
    contact_membership_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "person_contact_membership"]
    contact_membership_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "person_contact_membership"]
    contact_membership_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "person_planunit"]
    person_planunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "person_planunit"]
    person_planunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "person_planunit"]
    person_planunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "person_plan_awardunit"]
    person_plan_awardunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "person_plan_awardunit"]
    person_plan_awardunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "person_plan_awardunit"]
    person_plan_awardunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "person_plan_reasonunit"]
    person_plan_reasonunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "person_plan_reasonunit"]
    person_plan_reasonunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "person_plan_reasonunit"]
    person_plan_reasonunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "person_plan_reason_caseunit"]
    person_plan_reason_caseunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "person_plan_reason_caseunit"]
    person_plan_reason_caseunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "person_plan_reason_caseunit"]
    person_plan_reason_caseunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "person_plan_laborunit"]
    person_plan_laborunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "person_plan_laborunit"]
    person_plan_laborunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "person_plan_healerunit"]
    person_plan_healerunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "person_plan_healerunit"]
    person_plan_healerunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    x_list = ["INSERT", "person_plan_factunit"]
    person_plan_factunit_insert_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["UPDATE", "person_plan_factunit"]
    person_plan_factunit_update_dict = get_leg_obj(atoms_dict, x_list)
    x_list = ["DELETE", "person_plan_factunit"]
    person_plan_factunit_delete_dict = get_leg_obj(atoms_dict, x_list)

    leg_list = []
    if personunit_atom is not None:
        add_personunit_legible_list(leg_list, personunit_atom, x_person)
    if contactunit_insert_dict is not None:
        add_person_contactunit_insert_to_legible_list(
            leg_list, contactunit_insert_dict, x_person
        )
    if contactunit_update_dict is not None:
        add_person_contactunit_update_to_legible_list(
            leg_list, contactunit_update_dict, x_person
        )
    if contactunit_delete_dict is not None:
        add_person_contactunit_delete_to_legible_list(
            leg_list, contactunit_delete_dict, x_person
        )

    if contact_membership_insert_dict is not None:
        add_person_contact_membership_insert_to_legible_list(
            leg_list, contact_membership_insert_dict, x_person
        )
    if contact_membership_update_dict is not None:
        add_person_contact_membership_update_to_legible_list(
            leg_list, contact_membership_update_dict, x_person
        )
    if contact_membership_delete_dict is not None:
        add_person_contact_membership_delete_to_legible_list(
            leg_list, contact_membership_delete_dict, x_person
        )

    if person_planunit_insert_dict is not None:
        add_person_planunit_insert_to_legible_list(
            leg_list, person_planunit_insert_dict, x_person
        )
    if person_planunit_update_dict is not None:
        add_person_planunit_update_to_legible_list(
            leg_list, person_planunit_update_dict, x_person
        )
    if person_planunit_delete_dict is not None:
        add_person_planunit_delete_to_legible_list(
            leg_list, person_planunit_delete_dict, x_person
        )

    if person_plan_awardunit_insert_dict is not None:
        add_person_plan_awardunit_insert_to_legible_list(
            leg_list, person_plan_awardunit_insert_dict, x_person
        )
    if person_plan_awardunit_update_dict is not None:
        add_person_plan_awardunit_update_to_legible_list(
            leg_list, person_plan_awardunit_update_dict, x_person
        )
    if person_plan_awardunit_delete_dict is not None:
        add_person_plan_awardunit_delete_to_legible_list(
            leg_list, person_plan_awardunit_delete_dict, x_person
        )

    if person_plan_reasonunit_insert_dict is not None:
        add_person_plan_reasonunit_insert_to_legible_list(
            leg_list, person_plan_reasonunit_insert_dict, x_person
        )
    if person_plan_reasonunit_update_dict is not None:
        add_person_plan_reasonunit_update_to_legible_list(
            leg_list, person_plan_reasonunit_update_dict, x_person
        )
    if person_plan_reasonunit_delete_dict is not None:
        add_person_plan_reasonunit_delete_to_legible_list(
            leg_list, person_plan_reasonunit_delete_dict, x_person
        )

    if person_plan_reason_caseunit_insert_dict is not None:
        add_person_reason_caseunit_insert_to_legible_list(
            leg_list, person_plan_reason_caseunit_insert_dict, x_person
        )
    if person_plan_reason_caseunit_update_dict is not None:
        add_person_reason_caseunit_update_to_legible_list(
            leg_list, person_plan_reason_caseunit_update_dict, x_person
        )
    if person_plan_reason_caseunit_delete_dict is not None:
        add_person_reason_caseunit_delete_to_legible_list(
            leg_list, person_plan_reason_caseunit_delete_dict, x_person
        )

    if person_plan_laborunit_insert_dict is not None:
        add_person_plan_laborunit_insert_to_legible_list(
            leg_list, person_plan_laborunit_insert_dict, x_person
        )
    if person_plan_laborunit_delete_dict is not None:
        add_person_plan_laborunit_delete_to_legible_list(
            leg_list, person_plan_laborunit_delete_dict, x_person
        )

    if person_plan_healerunit_insert_dict is not None:
        add_person_plan_healerunit_insert_to_legible_list(
            leg_list, person_plan_healerunit_insert_dict, x_person
        )
    if person_plan_healerunit_delete_dict is not None:
        add_person_plan_healerunit_delete_to_legible_list(
            leg_list, person_plan_healerunit_delete_dict, x_person
        )

    if person_plan_factunit_insert_dict is not None:
        add_person_plan_factunit_insert_to_legible_list(
            leg_list, person_plan_factunit_insert_dict, x_person
        )
    if person_plan_factunit_update_dict is not None:
        add_person_plan_factunit_update_to_legible_list(
            leg_list, person_plan_factunit_update_dict, x_person
        )
    if person_plan_factunit_delete_dict is not None:
        add_person_plan_factunit_delete_to_legible_list(
            leg_list, person_plan_factunit_delete_dict, x_person
        )

    return leg_list


def add_personunit_legible_list(
    legible_list: list[str], x_atom: PersonAtom, x_person: PersonUnit
):
    jvalues = x_atom.jvalues
    _max_tree_traverse_str = "max_tree_traverse"
    _max_tree_traverse_value = jvalues.get(_max_tree_traverse_str)
    credor_respect_value = jvalues.get("credor_respect")
    debtor_respect_value = jvalues.get("debtor_respect")

    if _max_tree_traverse_value is not None:
        x_str = f"{x_person.person_name}'s maximum number of Person evaluations set to {_max_tree_traverse_value}"
        legible_list.append(x_str)
    if (
        credor_respect_value is not None
        and debtor_respect_value is not None
        and credor_respect_value == debtor_respect_value
    ):
        x_str = f"{x_person.person_name}'s total pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif credor_respect_value is not None:
        x_str = f"{x_person.person_name}'s credor pool is now {credor_respect_value}"
        legible_list.append(x_str)
    elif debtor_respect_value is not None:
        x_str = f"{x_person.person_name}'s debtor pool is now {debtor_respect_value}"
        legible_list.append(x_str)


def add_person_contactunit_insert_to_legible_list(
    legible_list: list[str], contactunit_dict: PersonAtom, x_person: PersonUnit
):
    for contactunit_atom in contactunit_dict.values():
        contact_name = contactunit_atom.get_value("contact_name")
        contact_cred_lumen_value = contactunit_atom.get_value("contact_cred_lumen")
        contact_debt_lumen_value = contactunit_atom.get_value("contact_debt_lumen")
        x_str = f"{contact_name} was added with {contact_cred_lumen_value} score credit and {contact_debt_lumen_value} score debt"
        legible_list.append(x_str)


def add_person_contactunit_update_to_legible_list(
    legible_list: list[str], contactunit_dict: PersonAtom, x_person: PersonUnit
):
    for contactunit_atom in contactunit_dict.values():
        contact_name = contactunit_atom.get_value("contact_name")
        contact_cred_lumen_value = contactunit_atom.get_value("contact_cred_lumen")
        contact_debt_lumen_value = contactunit_atom.get_value("contact_debt_lumen")
        if (
            contact_cred_lumen_value is not None
            and contact_debt_lumen_value is not None
        ):
            x_str = f"{contact_name} now has {contact_cred_lumen_value} score credit and {contact_debt_lumen_value} score debt."
        elif contact_cred_lumen_value is not None:
            x_str = f"{contact_name} now has {contact_cred_lumen_value} score credit."
        elif contact_debt_lumen_value is not None:
            x_str = f"{contact_name} now has {contact_debt_lumen_value} score debt."
        legible_list.append(x_str)


def add_person_contactunit_delete_to_legible_list(
    legible_list: list[str], contactunit_dict: PersonAtom, x_person: PersonUnit
):
    for contactunit_atom in contactunit_dict.values():
        contact_name = contactunit_atom.get_value("contact_name")
        x_str = f"{contact_name} was removed from score contacts."
        legible_list.append(x_str)


def add_person_contact_membership_insert_to_legible_list(
    legible_list: list[str],
    contact_membership_insert_dict: dict,
    x_person: PersonUnit,
):
    for contact_membership_dict in contact_membership_insert_dict.values():
        for contact_membership_atom in contact_membership_dict.values():
            group_title = contact_membership_atom.get_value("group_title")
            contact_name = contact_membership_atom.get_value("contact_name")
            group_cred_lumen_value = contact_membership_atom.get_value(
                "group_cred_lumen"
            )
            group_debt_lumen_value = contact_membership_atom.get_value(
                "group_debt_lumen"
            )
            x_str = f"Group '{group_title}' has new membership {contact_name} with group_cred_lumen_value{group_cred_lumen_value} and group_debt_lumen_value={group_debt_lumen_value}."
            legible_list.append(x_str)


def add_person_contact_membership_update_to_legible_list(
    legible_list: list[str],
    contact_membership_update_dict: dict,
    x_person: PersonUnit,
):
    for contact_membership_dict in contact_membership_update_dict.values():
        for contact_membership_atom in contact_membership_dict.values():
            group_title = contact_membership_atom.get_value("group_title")
            contact_name = contact_membership_atom.get_value("contact_name")
            group_cred_lumen_value = contact_membership_atom.get_value(
                "group_cred_lumen"
            )
            group_debt_lumen_value = contact_membership_atom.get_value(
                "group_debt_lumen"
            )
            if (
                group_cred_lumen_value is not None
                and group_debt_lumen_value is not None
            ):
                x_str = f"Group '{group_title}' membership {contact_name} has new group_cred_lumen_value{group_cred_lumen_value} and group_debt_lumen_value={group_debt_lumen_value}."
            elif group_cred_lumen_value is not None:
                x_str = f"Group '{group_title}' membership {contact_name} has new group_cred_lumen_value{group_cred_lumen_value}."
            elif group_debt_lumen_value is not None:
                x_str = f"Group '{group_title}' membership {contact_name} has new group_debt_lumen_value={group_debt_lumen_value}."
            legible_list.append(x_str)


def add_person_contact_membership_delete_to_legible_list(
    legible_list: list[str],
    contact_membership_delete_dict: dict,
    x_person: PersonUnit,
):
    for contact_membership_dict in contact_membership_delete_dict.values():
        for contact_membership_atom in contact_membership_dict.values():
            group_title = contact_membership_atom.get_value("group_title")
            contact_name = contact_membership_atom.get_value("contact_name")
            x_str = f"Group '{group_title}' no longer has membership {contact_name}."
            legible_list.append(x_str)


def add_person_planunit_insert_to_legible_list(
    legible_list: list[str], planunit_insert_dict: dict, x_person: PersonUnit
):
    _problem_bool_str = "problem_bool"
    for planunit_atom in planunit_insert_dict.values():
        rope_value = planunit_atom.get_value("plan_rope")
        _addin_value = planunit_atom.get_value("addin")
        _begin_value = planunit_atom.get_value("begin")
        _close_value = planunit_atom.get_value("close")
        _denom_value = planunit_atom.get_value("denom")
        _numor_value = planunit_atom.get_value("numor")
        _problem_bool_value = planunit_atom.get_value(_problem_bool_str)
        _morph_value = planunit_atom.get_value("morph")
        _star_value = planunit_atom.get_value("star")
        pledge_value = planunit_atom.get_value("pledge")
        x_str = f"Created Plan '{rope_value}'. "
        if _addin_value is not None:
            x_str += f"addin={_addin_value}."
        if _begin_value is not None:
            x_str += f"begin={_begin_value}."
        if _close_value is not None:
            x_str += f"close={_close_value}."
        if _denom_value is not None:
            x_str += f"denom={_denom_value}."
        if _numor_value is not None:
            x_str += f"numor={_numor_value}."
        if _problem_bool_value is not None:
            x_str += f"problem_bool={_problem_bool_value}."
        if _morph_value is not None:
            x_str += f"morph={_morph_value}."
        if _star_value is not None:
            x_str += f"star={_star_value}."
        if pledge_value is not None:
            x_str += f"pledge={pledge_value}."

        legible_list.append(x_str)


def add_person_planunit_update_to_legible_list(
    legible_list: list[str], planunit_update_dict: dict, x_person: PersonUnit
):
    _problem_bool_str = "problem_bool"
    for planunit_atom in planunit_update_dict.values():
        rope_value = planunit_atom.get_value("plan_rope")
        addin_value = planunit_atom.get_value("addin")
        begin_value = planunit_atom.get_value("begin")
        close_value = planunit_atom.get_value("close")
        denom_value = planunit_atom.get_value("denom")
        numor_value = planunit_atom.get_value("numor")
        problem_bool_value = planunit_atom.get_value(_problem_bool_str)
        morph_value = planunit_atom.get_value("morph")
        star_value = planunit_atom.get_value("star")
        pledge_value = planunit_atom.get_value("pledge")
        x_str = f"Plan '{rope_value}' set these attrs: "
        if addin_value is not None:
            x_str += f"addin={addin_value}."
        if begin_value is not None:
            x_str += f"begin={begin_value}."
        if close_value is not None:
            x_str += f"close={close_value}."
        if denom_value is not None:
            x_str += f"denom={denom_value}."
        if numor_value is not None:
            x_str += f"numor={numor_value}."
        if problem_bool_value is not None:
            x_str += f"problem_bool={problem_bool_value}."
        if morph_value is not None:
            x_str += f"morph={morph_value}."
        if star_value is not None:
            x_str += f"star={star_value}."
        if pledge_value is not None:
            x_str += f"pledge={pledge_value}."

        legible_list.append(x_str)


def add_person_planunit_delete_to_legible_list(
    legible_list: list[str], planunit_delete_dict: dict, x_person: PersonUnit
):
    for planunit_atom in planunit_delete_dict.values():
        rope_value = planunit_atom.get_value("plan_rope")
        x_str = f"Plan '{rope_value}' was deleted."
        legible_list.append(x_str)


def add_person_plan_awardunit_insert_to_legible_list(
    legible_list: list[str], plan_awardunit_insert_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_awardunit_insert_dict.values():
        for plan_awardunit_atom in rope_dict.values():
            awardee_title_value = plan_awardunit_atom.get_value("awardee_title")
            rope_value = plan_awardunit_atom.get_value("plan_rope")
            give_force_value = plan_awardunit_atom.get_value("give_force")
            take_force_value = plan_awardunit_atom.get_value("take_force")
            x_str = f"AwardUnit created for group {awardee_title_value} for plan '{rope_value}' with give_force={give_force_value} and take_force={take_force_value}."
            legible_list.append(x_str)


def add_person_plan_awardunit_update_to_legible_list(
    legible_list: list[str], plan_awardunit_update_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_awardunit_update_dict.values():
        for plan_awardunit_atom in rope_dict.values():
            awardee_title_value = plan_awardunit_atom.get_value("awardee_title")
            rope_value = plan_awardunit_atom.get_value("plan_rope")
            give_force_value = plan_awardunit_atom.get_value("give_force")
            take_force_value = plan_awardunit_atom.get_value("take_force")
            if give_force_value is not None and take_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value} and take_force={take_force_value}."
            elif give_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now give_force={give_force_value}."
            elif take_force_value is not None:
                x_str = f"AwardUnit has been set for group {awardee_title_value} for plan '{rope_value}'. Now take_force={take_force_value}."
            legible_list.append(x_str)


def add_person_plan_awardunit_delete_to_legible_list(
    legible_list: list[str], plan_awardunit_delete_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_awardunit_delete_dict.values():
        for plan_awardunit_atom in rope_dict.values():
            awardee_title_value = plan_awardunit_atom.get_value("awardee_title")
            rope_value = plan_awardunit_atom.get_value("plan_rope")
            x_str = f"AwardUnit for group {awardee_title_value}, plan '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_person_plan_reasonunit_insert_to_legible_list(
    legible_list: list[str], plan_reasonunit_insert_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_reasonunit_insert_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            reason_context_value = plan_reasonunit_atom.get_value("reason_context")
            active_requisite_value = plan_reasonunit_atom.get_value("active_requisite")
            x_str = f"ReasonUnit created for plan '{rope_value}' with reason_context '{reason_context_value}'."
            if active_requisite_value is not None:
                x_str += f" active_requisite={active_requisite_value}."
            legible_list.append(x_str)


def add_person_plan_reasonunit_update_to_legible_list(
    legible_list: list[str], plan_reasonunit_update_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_reasonunit_update_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            reason_context_value = plan_reasonunit_atom.get_value("reason_context")
            active_requisite_value = plan_reasonunit_atom.get_value("active_requisite")
            if active_requisite_value is not None:
                x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' set with active_requisite={active_requisite_value}."
            else:
                x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' and no longer checks reason_context active mode."
            legible_list.append(x_str)


def add_person_plan_reasonunit_delete_to_legible_list(
    legible_list: list[str], plan_reasonunit_delete_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_reasonunit_delete_dict.values():
        for plan_reasonunit_atom in rope_dict.values():
            rope_value = plan_reasonunit_atom.get_value("plan_rope")
            reason_context_value = plan_reasonunit_atom.get_value("reason_context")
            x_str = f"ReasonUnit reason_context='{reason_context_value}' for plan '{rope_value}' has been deleted."
            legible_list.append(x_str)


def add_person_reason_caseunit_insert_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_insert_dict: dict,
    x_person: PersonUnit,
):
    for rope_dict in plan_reason_caseunit_insert_dict.values():
        for reason_context_dict in rope_dict.values():
            for plan_reason_caseunit_atom in reason_context_dict.values():
                rope_value = plan_reason_caseunit_atom.get_value("plan_rope")
                reason_context_value = plan_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = plan_reason_caseunit_atom.get_value("reason_state")
                reason_divisor_value = plan_reason_caseunit_atom.get_value(
                    "reason_divisor"
                )
                reason_upper_value = plan_reason_caseunit_atom.get_value("reason_upper")
                reason_lower_value = plan_reason_caseunit_atom.get_value("reason_lower")
                x_str = f"CaseUnit '{reason_state_value}' created for reason '{reason_context_value}' for plan '{rope_value}'."
                if reason_lower_value is not None:
                    x_str += f" reason_lower={reason_lower_value}."
                if reason_upper_value is not None:
                    x_str += f" reason_upper={reason_upper_value}."
                if reason_divisor_value is not None:
                    x_str += f" reason_divisor={reason_divisor_value}."
                legible_list.append(x_str)


def add_person_reason_caseunit_update_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_update_dict: dict,
    x_person: PersonUnit,
):
    for rope_dict in plan_reason_caseunit_update_dict.values():
        for reason_context_dict in rope_dict.values():
            for plan_reason_caseunit_atom in reason_context_dict.values():
                rope_value = plan_reason_caseunit_atom.get_value("plan_rope")
                reason_context_value = plan_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = plan_reason_caseunit_atom.get_value("reason_state")
                reason_divisor_value = plan_reason_caseunit_atom.get_value(
                    "reason_divisor"
                )
                reason_upper_value = plan_reason_caseunit_atom.get_value("reason_upper")
                reason_lower_value = plan_reason_caseunit_atom.get_value("reason_lower")
                x_str = f"CaseUnit '{reason_state_value}' updated for reason '{reason_context_value}' for plan '{rope_value}'."
                if reason_lower_value is not None:
                    x_str += f" reason_lower={reason_lower_value}."
                if reason_upper_value is not None:
                    x_str += f" reason_upper={reason_upper_value}."
                if reason_divisor_value is not None:
                    x_str += f" reason_divisor={reason_divisor_value}."
                legible_list.append(x_str)


def add_person_reason_caseunit_delete_to_legible_list(
    legible_list: list[str],
    plan_reason_caseunit_delete_dict: dict,
    x_person: PersonUnit,
):
    for rope_dict in plan_reason_caseunit_delete_dict.values():
        for reason_context_dict in rope_dict.values():
            for plan_reason_caseunit_atom in reason_context_dict.values():
                rope_value = plan_reason_caseunit_atom.get_value("plan_rope")
                reason_context_value = plan_reason_caseunit_atom.get_value(
                    "reason_context"
                )
                reason_state_value = plan_reason_caseunit_atom.get_value("reason_state")
                x_str = f"CaseUnit '{reason_state_value}' deleted from reason '{reason_context_value}' for plan '{rope_value}'."
                legible_list.append(x_str)


def add_person_plan_laborunit_insert_to_legible_list(
    legible_list: list[str], plan_laborunit_insert_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_laborunit_insert_dict.values():
        for plan_laborunit_atom in rope_dict.values():
            labor_title_value = plan_laborunit_atom.get_value("labor_title")
            rope_value = plan_laborunit_atom.get_value("plan_rope")
            x_str = f"laborunit '{labor_title_value}' created for plan '{rope_value}'."
            legible_list.append(x_str)


def add_person_plan_laborunit_delete_to_legible_list(
    legible_list: list[str], plan_laborunit_delete_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_laborunit_delete_dict.values():
        for plan_laborunit_atom in rope_dict.values():
            labor_title_value = plan_laborunit_atom.get_value("labor_title")
            rope_value = plan_laborunit_atom.get_value("plan_rope")
            x_str = f"laborunit '{labor_title_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)


def add_person_plan_healerunit_insert_to_legible_list(
    legible_list: list[str], plan_healerunit_insert_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_healerunit_insert_dict.values():
        for plan_healerunit_atom in rope_dict.values():
            healer_name_value = plan_healerunit_atom.get_value("healer_name")
            rope_value = plan_healerunit_atom.get_value("plan_rope")
            x_str = f"HealerUnit '{healer_name_value}' created for plan '{rope_value}'."
            legible_list.append(x_str)


def add_person_plan_healerunit_delete_to_legible_list(
    legible_list: list[str], plan_healerunit_delete_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_healerunit_delete_dict.values():
        for plan_healerunit_atom in rope_dict.values():
            healer_name_value = plan_healerunit_atom.get_value("healer_name")
            rope_value = plan_healerunit_atom.get_value("plan_rope")
            x_str = f"HealerUnit '{healer_name_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)


def add_person_plan_factunit_insert_to_legible_list(
    legible_list: list[str], plan_factunit_insert_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_factunit_insert_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fact_context_value = plan_factunit_atom.get_value("fact_context")
            fact_state_value = plan_factunit_atom.get_value("fact_state")
            fact_upper_value = plan_factunit_atom.get_value("fact_upper")
            fact_lower_value = plan_factunit_atom.get_value("fact_lower")
            x_str = f"FactUnit '{fact_state_value}' created for reason_context '{fact_context_value}' for plan '{rope_value}'."
            if fact_lower_value is not None:
                x_str += f" fact_lower={fact_lower_value}."
            if fact_upper_value is not None:
                x_str += f" fact_upper={fact_upper_value}."
            legible_list.append(x_str)


def add_person_plan_factunit_update_to_legible_list(
    legible_list: list[str], plan_factunit_update_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_factunit_update_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fact_context_value = plan_factunit_atom.get_value("fact_context")
            fact_state_value = plan_factunit_atom.get_value("fact_state")
            fact_upper_value = plan_factunit_atom.get_value("fact_upper")
            fact_lower_value = plan_factunit_atom.get_value("fact_lower")
            x_str = f"FactUnit '{fact_state_value}' updated for reason_context '{fact_context_value}' for plan '{rope_value}'."
            if fact_lower_value is not None:
                x_str += f" fact_lower={fact_lower_value}."
            if fact_upper_value is not None:
                x_str += f" fact_upper={fact_upper_value}."
            legible_list.append(x_str)


def add_person_plan_factunit_delete_to_legible_list(
    legible_list: list[str], plan_factunit_delete_dict: dict, x_person: PersonUnit
):
    for rope_dict in plan_factunit_delete_dict.values():
        for plan_factunit_atom in rope_dict.values():
            rope_value = plan_factunit_atom.get_value("plan_rope")
            fact_context_value = plan_factunit_atom.get_value("fact_context")
            fact_state_value = plan_factunit_atom.get_value("fact_state")
            x_str = f"FactUnit reason_context '{fact_context_value}' deleted for plan '{rope_value}'."
            legible_list.append(x_str)
