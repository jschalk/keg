from ch01_keyword.keyword_class_builder import get_keywords_src_config
from ch97_docs_builder.glossary_ranking import get_tiered_questionunits


# CUT / EXAM2
def test_tiered_questionunits_ReturnsObj():
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH / WHEN
    tiered_questionunits = get_tiered_questionunits()
    # THEN
    keywords_src_config = get_keywords_src_config()
    keywords_set = set(keywords_src_config.keys())
    for keg_term, keg_qu in tiered_questionunits.items():
        # check chxx terms
        if len(keg_term) == 4 and keg_term.startswith("ch"):
            # print(f"{keg_term=} {keg_qu.question_tier=}")
            assert keg_qu.question_tier == 6
        # check non ch terms
        if keg_qu.init_ch is None and keg_term in keywords_set:
            print(f"{keg_term=} {keg_qu.init_ch=} {keg_qu.question_tier=}")
            assert keg_qu.question_tier == 10, keg_term
