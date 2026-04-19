from ch11_bud.test._util.ch11_examples import (
    example_casa_clean_factunit,
    example_casa_dirty_factunit,
    example_sky_blue_factunit,
)
from ch11_bud.weighted_facts_tool import get_nodes_with_weighted_facts
from ref.keywords import ExampleStrs as exx


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario00_RootOnly_NoFacts():
    # ESTABLISH
    nodes_facts_dict = {}
    nodes_quota_ledger_dict = {}

    # WHEN
    nodes_weighted_facts = get_nodes_with_weighted_facts(
        nodes_facts_dict, nodes_quota_ledger_dict
    )

    # THEN
    assert nodes_weighted_facts == {}


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario01_Multiple_Nodes_NoFacts():
    # ESTABLISH
    root_addr = ()
    bob_addr = (exx.bob,)
    bob_yao_addr = (exx.bob, exx.yao)
    nodes_facts_dict = {root_addr: {}, bob_addr: {}, bob_yao_addr: {}}
    nodes_quota_dict = {
        root_addr: {exx.bob: 1},
        bob_addr: {exx.yao: 1},
        bob_yao_addr: {exx.sue: 1},
    }

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    assert nodes_wgt_facts == nodes_facts_dict


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario02_RootHasOneFact():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    root_facts = {clean_fact.fact_context: clean_fact}
    root_addr = ()
    nodes_facts_dict = {root_addr: root_facts}
    nodes_quota_dict = {root_addr: {exx.bob: 1}}

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    assert nodes_wgt_facts == nodes_facts_dict


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario03_ChildHasOneFact():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    root_facts = {}
    bob_facts = {clean_fact.fact_context: clean_fact}
    root_addr = ()
    bob_addr = (exx.bob,)
    nodes_facts_dict = {root_addr: root_facts, bob_addr: bob_facts}
    nodes_quota_dict = {root_addr: {exx.bob: 1}, bob_addr: {exx.yao: 1}}

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {(): bob_facts, (exx.bob,): bob_facts}
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario04_ChildHasOneFact():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    root_facts = {}
    bob_facts = {clean_fact.fact_context: clean_fact}
    root_addr = ()
    bob_addr = (exx.bob,)
    nodes_facts_dict = {root_addr: root_facts, bob_addr: bob_facts}
    nodes_quota_dict = {root_addr: {exx.bob: 1}, bob_addr: {exx.yao: 1}}
    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {(): bob_facts, (exx.bob,): bob_facts}
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario05_Level2ChildHasOneFact():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    root_addr = ()
    bob_addr = (exx.bob,)
    bob_yao_addr = (exx.bob, exx.yao)
    bob_yao_facts = {clean_fact.fact_context: clean_fact}
    nodes_facts_dict = {root_addr: {}, bob_addr: {}, bob_yao_addr: bob_yao_facts}
    nodes_quota_dict = {
        root_addr: {exx.bob: 1},
        bob_addr: {exx.yao: 1},
        bob_yao_addr: {exx.yao: 1},
    }

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {
        root_addr: bob_yao_facts,
        bob_addr: bob_yao_facts,
        bob_yao_addr: bob_yao_facts,
    }
    assert nodes_wgt_facts.get(bob_yao_addr) == bob_yao_facts
    assert nodes_wgt_facts.get(bob_addr) == bob_yao_facts
    assert nodes_wgt_facts.get(root_addr) == bob_yao_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario06_Level2ChildsHaveTwoFacts():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    sky_fact = example_sky_blue_factunit()
    root_addr = ()
    bob_addr = (exx.bob,)
    bob_yao_addr = (exx.bob, exx.yao)
    bob_facts = {sky_fact.fact_context: sky_fact}
    bob_yao_facts = {clean_fact.fact_context: clean_fact}
    nodes_facts_dict = {root_addr: {}, bob_addr: bob_facts, bob_yao_addr: bob_yao_facts}
    nodes_quota_dict = {
        root_addr: {exx.bob: 1},
        bob_addr: {exx.yao: 1},
        bob_yao_addr: {exx.yao: 1},
    }

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_bob_facts = {
        sky_fact.fact_context: sky_fact,
        clean_fact.fact_context: clean_fact,
    }
    expected_nodes_weighted_facts = {
        root_addr: expected_bob_facts,
        bob_addr: expected_bob_facts,
        bob_yao_addr: bob_yao_facts,
    }
    assert nodes_wgt_facts.get(bob_yao_addr) == bob_yao_facts
    assert nodes_wgt_facts.get(bob_addr) == expected_bob_facts
    assert nodes_wgt_facts.get(root_addr) == expected_bob_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario07_Level2ChildFactOverridesAncestorFact():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    dirty_fact = example_casa_dirty_factunit()
    root_addr = ()
    bob_addr = (exx.bob,)
    bob_yao_addr = (exx.bob, exx.yao)
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    bob_yao_facts = {clean_fact.fact_context: clean_fact}
    nodes_facts_dict = {
        root_addr: {},
        bob_addr: dirty_facts,
        bob_yao_addr: bob_yao_facts,
    }
    nodes_quota_dict = {
        root_addr: {exx.bob: 1},
        bob_addr: {exx.yao: 1},
        bob_yao_addr: {exx.yao: 1},
    }

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_clean_facts = {clean_fact.fact_context: clean_fact}
    expected_nodes_weighted_facts = {
        root_addr: expected_clean_facts,
        bob_addr: expected_clean_facts,
        bob_yao_addr: bob_yao_facts,
    }
    assert nodes_wgt_facts.get(bob_yao_addr) == bob_yao_facts
    assert nodes_wgt_facts.get(bob_addr) == expected_clean_facts
    assert nodes_wgt_facts.get(root_addr) == expected_clean_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario08_Level2ChildHasDiffentFacts():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    dirty_fact = example_casa_dirty_factunit()
    root_addr = ()
    bob_addr = (exx.bob,)
    bob_quota_sue = 7
    bob_quota_yao = 7
    bob_yao_addr = (exx.bob, exx.yao)
    bob_sue_addr = (exx.bob, exx.sue)
    bob_facts = {}
    bob_yao_facts = {clean_fact.fact_context: clean_fact}
    bob_sue_facts = {dirty_fact.fact_context: dirty_fact}
    nodes_facts_dict = {
        root_addr: {},
        bob_addr: bob_facts,
        bob_yao_addr: bob_yao_facts,
        bob_sue_addr: bob_sue_facts,
    }
    nodes_quota_dict = {
        root_addr: {exx.bob: 1},
        bob_addr: {exx.yao: bob_quota_sue, exx.sue: bob_quota_yao},
        bob_yao_addr: {exx.yao: 1},
        bob_sue_addr: {exx.yao: 1},
    }
    assert bob_quota_sue == bob_quota_yao

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    expected_clean_facts = {clean_fact.fact_context: clean_fact}
    expected_nodes_weighted_facts = {
        root_addr: expected_clean_facts,
        bob_addr: expected_clean_facts,
        bob_yao_addr: bob_yao_facts,
        bob_sue_addr: dirty_facts,
    }
    assert nodes_wgt_facts.get(bob_sue_addr) == dirty_facts
    assert nodes_wgt_facts.get(bob_yao_addr) == expected_clean_facts
    assert nodes_wgt_facts.get(bob_addr) == expected_clean_facts
    assert nodes_wgt_facts.get(root_addr) == expected_clean_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario09_Level2ChildThreeChildFacts():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    dirty_fact = example_casa_dirty_factunit()
    root_addr = ()
    bob_addr = (exx.bob,)
    bob_quota_yao = 7
    bob_quota_sue = 5
    bob_quota_zia = 5
    bob_yao_addr = (exx.bob, exx.yao)
    bob_sue_addr = (exx.bob, exx.sue)
    bob_zia_addr = (exx.bob, exx.zia)
    clean_facts = {clean_fact.fact_context: clean_fact}
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    nodes_facts_dict = {
        root_addr: {},
        bob_addr: {},
        bob_yao_addr: clean_facts,
        bob_sue_addr: dirty_facts,
        bob_zia_addr: dirty_facts,
    }
    nodes_quota_dict = {
        root_addr: {exx.bob: 1},
        bob_addr: {
            exx.yao: bob_quota_yao,
            exx.sue: bob_quota_sue,
            exx.zia: bob_quota_zia,
        },
        bob_yao_addr: {exx.yao: 1},
        bob_sue_addr: {exx.yao: 1},
        bob_zia_addr: {exx.yao: 1},
    }
    assert bob_quota_yao < bob_quota_sue + bob_quota_zia

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {
        root_addr: dirty_facts,
        bob_addr: dirty_facts,
        bob_yao_addr: clean_facts,
        bob_sue_addr: dirty_facts,
        bob_zia_addr: dirty_facts,
    }
    assert nodes_wgt_facts.get(bob_zia_addr) == dirty_facts
    assert nodes_wgt_facts.get(bob_sue_addr) == dirty_facts
    assert nodes_wgt_facts.get(bob_yao_addr) == clean_facts
    assert nodes_wgt_facts.get(bob_addr) == dirty_facts
    assert nodes_wgt_facts.get(root_addr) == dirty_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts


def test_get_nodes_with_weighted_facts_ReturnsObj_Scenario10_Level2ChildTwoChildFactsOneMissing():
    # ESTABLISH
    clean_fact = example_casa_clean_factunit()
    dirty_fact = example_casa_dirty_factunit()
    root_addr = ()
    bob_addr = (exx.bob,)
    bob_quota_yao = 7
    bob_quota_sue = 5
    bob_quota_zia = 5
    bob_yao_addr = (exx.bob, exx.yao)
    bob_sue_addr = (exx.bob, exx.sue)
    clean_facts = {clean_fact.fact_context: clean_fact}
    dirty_facts = {dirty_fact.fact_context: dirty_fact}
    nodes_facts_dict = {
        root_addr: {},
        bob_addr: dirty_facts,
        bob_yao_addr: clean_facts,
        bob_sue_addr: dirty_facts,
    }
    nodes_quota_dict = {
        root_addr: {exx.bob: 1},
        bob_addr: {
            exx.yao: bob_quota_yao,
            exx.sue: bob_quota_sue,
            exx.zia: bob_quota_zia,
        },
        bob_yao_addr: {exx.yao: 1},
        bob_sue_addr: {exx.yao: 1},
    }
    assert bob_quota_yao < bob_quota_sue + bob_quota_zia

    # WHEN
    nodes_wgt_facts = get_nodes_with_weighted_facts(nodes_facts_dict, nodes_quota_dict)

    # THEN
    expected_nodes_weighted_facts = {
        root_addr: dirty_facts,
        bob_addr: dirty_facts,
        bob_yao_addr: clean_facts,
        bob_sue_addr: dirty_facts,
    }
    assert nodes_wgt_facts.get(bob_sue_addr) == dirty_facts
    assert nodes_wgt_facts.get(bob_yao_addr) == clean_facts
    assert nodes_wgt_facts.get(bob_addr) == dirty_facts
    assert nodes_wgt_facts.get(root_addr) == dirty_facts
    assert nodes_wgt_facts == expected_nodes_weighted_facts
