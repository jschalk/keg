from sqlalchemy import inspect
from src.ch08_person_atom.atom_config import get_normalized_person_table_build
from src.ch08_person_atom.normal_model import (
    AwardUnitTable,
    CaseTable,
    FactTable,
    HealerUnitTable,
    MemberShipTable,
    PartnerUnitTable,
    PersonTable,
    PlanTable,
    ReasonTable,
    WorkforceLinkTable,
)
from src.ref.keywords import Ch08Keywords as kw


def get_config_table_name(config_dimen) -> str:
    config_specs_dict = config_dimen.get(kw.normal_specs)
    return config_specs_dict.get(kw.normal_table_name)


def all_columns_are_as_config_requires(mapper, config_dimen):
    config_table_name = get_config_table_name(config_dimen)
    config_columns = config_dimen.get("columns")

    for config_column, column_dict in config_columns.items():
        table_column = mapper.columns.get(config_column)
        failed_assert_str = f"{config_column=} is missing from {config_table_name=}"
        assert table_column is not None, failed_assert_str
        config_type = column_dict.get(kw.sqlite_datatype)
        if config_type == "TEXT":
            config_type = "VARCHAR"
        elif config_type == "REAL":
            config_type = "FLOAT"
        failed_assert_str = f"Table '{config_table_name}' {config_column=} {str(table_column.type)==config_type=}"
        assert str(table_column.type) == config_type, failed_assert_str


def print_out_expected_class_attribute_declarations(config_dimen):
    config_table_name = get_config_table_name(config_dimen)
    config_columns = config_dimen.get("columns")

    print(f"Table {config_table_name}")
    for config_column, column_dict in config_columns.items():
        declare_type = column_dict.get(kw.sqlite_datatype)
        if declare_type == "TEXT":
            declare_type = "String"
        elif declare_type == "INTEGER":
            declare_type = "Integer"
        elif declare_type == "REAL":
            declare_type = "Float"
        if config_column == kw.plan_uid:
            declare_type = "Integer, primary_key=True"
        print(f"    {config_column} = Column({declare_type})")


def test_normalized_table_PersonTable_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.personunit)
    mapper = inspect(PersonTable)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "person"
    assert config_table_name == PersonTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_PartnerUnitTable_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.person_partnerunit)
    mapper = inspect(PartnerUnitTable)
    # print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "partnerunit"
    assert config_table_name == PartnerUnitTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_MemberShipTable_membership_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.person_partner_membership)
    mapper = inspect(MemberShipTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "membership"
    assert config_table_name == MemberShipTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_PlanTable_plan_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.person_planunit)
    mapper = inspect(PlanTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "plan"
    assert config_table_name == PlanTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_AwardUnitTable_awardunit_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.person_plan_awardunit)
    mapper = inspect(AwardUnitTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "awardunit"
    assert config_table_name == AwardUnitTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_ReasonTable_reason_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.person_plan_reasonunit)
    mapper = inspect(ReasonTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "reason"
    assert config_table_name == ReasonTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_CaseTable_case_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(
        kw.person_plan_reason_caseunit
    )
    mapper = inspect(CaseTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "case"
    assert config_table_name == CaseTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_WorkforceLinkTable_laborunit_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.person_plan_laborunit)
    mapper = inspect(WorkforceLinkTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "laborunit"
    assert config_table_name == WorkforceLinkTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_HealerUnitTable_healerunit_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.person_plan_healerunit)
    mapper = inspect(HealerUnitTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == kw.healerunit
    assert config_table_name == HealerUnitTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)


def test_normalized_table_FactTable_fact_Exists():
    # ESTABLISH
    config_dimen = get_normalized_person_table_build().get(kw.person_plan_factunit)
    mapper = inspect(FactTable)
    print_out_expected_class_attribute_declarations(config_dimen)

    # WHEN / THEN
    config_table_name = get_config_table_name(config_dimen)
    assert config_table_name == "fact"
    assert config_table_name == FactTable.__tablename__
    all_columns_are_as_config_requires(mapper, config_dimen)
