from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


# Declare a base class
class Base(DeclarativeBase):
    pass


class PersonTable(Base):
    __tablename__ = "person"
    plan_uid = Column(Integer, primary_key=True)
    max_tree_traverse = Column(Integer)
    credor_respect = Column(Float)
    debtor_respect = Column(Float)
    fund_pool = Column(Float)
    fund_grain = Column(Float)
    respect_grain = Column(Float)
    mana_grain = Column(Float)


class PartnerUnitTable(Base):
    __tablename__ = "partnerunit"
    plan_uid = Column(Integer, primary_key=True)
    partner_name = Column(String)
    partner_cred_lumen = Column(Float)
    partner_debt_lumen = Column(Float)


class MemberShipTable(Base):
    __tablename__ = "membership"
    plan_uid = Column(Integer, primary_key=True)
    group_title = Column(String)
    partner_name = Column(String)
    group_cred_lumen = Column(Float)
    group_debt_lumen = Column(Float)


class PlanTable(Base):
    __tablename__ = "plan"
    plan_uid = Column(Integer, primary_key=True)
    plan_rope = Column(String)
    addin = Column(Float)
    begin = Column(Float)
    close = Column(Float)
    denom = Column(Integer)
    gogo_want = Column(Float)
    numor = Column(Integer)
    problem_bool = Column(Integer)
    morph = Column(Integer)
    star = Column(Integer)
    pledge = Column(Integer)
    stop_want = Column(Float)


class AwardUnitTable(Base):
    __tablename__ = "awardunit"
    plan_uid = Column(Integer, primary_key=True)
    awardee_title = Column(String)
    plan_rope = Column(String)
    give_force = Column(Float)
    take_force = Column(Float)


class ReasonTable(Base):
    __tablename__ = "reason"
    plan_uid = Column(Integer, primary_key=True)
    reason_context = Column(String)
    plan_rope = Column(String)
    active_requisite = Column(Integer)


class CaseTable(Base):
    __tablename__ = "case"
    plan_uid = Column(Integer, primary_key=True)
    reason_context = Column(String)
    reason_state = Column(String)
    plan_rope = Column(String)
    reason_divisor = Column(Integer)
    reason_upper = Column(Float)
    reason_lower = Column(Float)


class WorkforceLinkTable(Base):
    __tablename__ = "laborunit"
    plan_uid = Column(Integer, primary_key=True)
    labor_title = Column(String)
    plan_rope = Column(String)
    solo = Column(Integer)


class HealerUnitTable(Base):
    __tablename__ = "healerunit"
    plan_uid = Column(Integer, primary_key=True)
    healer_name = Column(String)
    plan_rope = Column(String)


class FactTable(Base):
    __tablename__ = "fact"
    plan_uid = Column(Integer, primary_key=True)
    fact_context = Column(String)
    plan_rope = Column(String)
    fact_upper = Column(Float)
    fact_lower = Column(Float)
    fact_state = Column(String)
