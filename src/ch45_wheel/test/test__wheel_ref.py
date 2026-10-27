# Warsaw Pact slaves
# USSR slaves
# Russia Federal Districts
# Russia Federal Subjects
# Central District Oblasts
# Moscow Okrugs
# Central Okrug Districts
def get_warsaw_pact_slaves() -> set[str]:
    return {
        "USSR": "house",
        "Albania": "field",
        "Poland": "field",
        "Czechoslovakia": "field",
        "Hungary": "field",
        "Bulgaria": "field",
        "Romania": "field",
        "East Germany": "field1",
    }


def test_get_warsaw_pact_slaves_ReturnsObj():
    # ESTABLISH / WHEN
    warsaw_pact_slaves = get_warsaw_pact_slaves()
    # THEN
    expected_warsaw_pact_slaves = {
        "USSR": "house",
        "Albania": "field",
        "Poland": "field",
        "Czechoslovakia": "field",
        "Hungary": "field",
        "Bulgaria": "field",
        "Romania": "field",
        "East Germany": "field1",
    }
    assert warsaw_pact_slaves == expected_warsaw_pact_slaves
    assert list(warsaw_pact_slaves.values()).count("house") == 1
    assert list(warsaw_pact_slaves.values()).count("field1") == 1


def get_ussr_slaves() -> set[str]:
    return {
        "Russia": "house",
        "Ukraine": "field1",
        "Belarus": "field",
        "Uzbekistan": "field",
        "Kazakhstan": "field",
        "Georgia": "field",
        "Azerbaijan": "field",
        "Lithuania": "field",
        "Moldova": "field",
        "Latvia": "field",
        "Kyrgyzstan": "field",
        "Tajikistan": "field",
        "Armenia": "field",
        "Turkmenistan": "field",
        "Estonia": "field",
    }


def test_get_ussr_slaves_ReturnsObj():
    # ESTABLISH / WHEN
    ussr_slaves = get_ussr_slaves()
    # THEN
    expected_ussr_slaves = {
        "Russia": "house",
        "Ukraine": "field1",
        "Belarus": "field",
        "Uzbekistan": "field",
        "Kazakhstan": "field",
        "Georgia": "field",
        "Azerbaijan": "field",
        "Lithuania": "field",
        "Moldova": "field",
        "Latvia": "field",
        "Kyrgyzstan": "field",
        "Tajikistan": "field",
        "Armenia": "field",
        "Turkmenistan": "field",
        "Estonia": "field",
    }
    assert ussr_slaves == expected_ussr_slaves
    assert list(ussr_slaves.values()).count("house") == 1
    assert list(ussr_slaves.values()).count("field1") == 1


def get_russia_slaves() -> set[str]:
    return {
        "Central Federal District": "house",
        "Northwestern Federal District": "field",
        "Southern Federal District": "field",
        "North Caucasian Federal District": "field",
        "Volga Federal District": "field1",
        "Ural Federal District": "field",
        "Siberian Federal District": "field",
        "Far Eastern Federal District": "field",
    }


def test_get_russia_slaves_ReturnsObj():
    # ESTABLISH / WHEN
    russia_slaves = get_russia_slaves()
    # THEN
    expected_russia_slaves = {
        "Central Federal District": "house",
        "Northwestern Federal District": "field",
        "Southern Federal District": "field",
        "North Caucasian Federal District": "field",
        "Volga Federal District": "field1",
        "Ural Federal District": "field",
        "Siberian Federal District": "field",
        "Far Eastern Federal District": "field",
    }
    assert russia_slaves == expected_russia_slaves
    assert list(russia_slaves.values()).count("house") == 1
    assert list(russia_slaves.values()).count("field1") == 1


def get_central_fed_slaves() -> set[str]:
    return {
        "Belgorod Oblast": "field",
        "Bryansk Oblast": "field",
        "Vladimir Oblast": "field",
        "Voronezh Oblast": "field1",
        "Ivanovo Oblast": "field",
        "Kaluga Oblast": "field",
        "Kostroma Oblast": "field",
        "Kursk Oblast": "field",
        "Lipetsk Oblast": "field",
        "Moscow Oblast": "field",
        "Oryol Oblast": "field",
        "Ryazan Oblast": "field",
        "Smolensk Oblast": "field",
        "Tambov Oblast": "field",
        "Tver Oblast": "field",
        "Tula Oblast": "field",
        "Yaroslavl Oblast": "field",
        "Moscow City": "house",
    }


def test_get_central_fed_slaves_ReturnsObj():
    # ESTABLISH / WHEN
    central_fed_slaves = get_central_fed_slaves()
    # THEN
    expected_central_fed_slaves = {
        "Belgorod Oblast": "field",
        "Bryansk Oblast": "field",
        "Vladimir Oblast": "field",
        "Voronezh Oblast": "field1",
        "Ivanovo Oblast": "field",
        "Kaluga Oblast": "field",
        "Kostroma Oblast": "field",
        "Kursk Oblast": "field",
        "Lipetsk Oblast": "field",
        "Moscow Oblast": "field",
        "Oryol Oblast": "field",
        "Ryazan Oblast": "field",
        "Smolensk Oblast": "field",
        "Tambov Oblast": "field",
        "Tver Oblast": "field",
        "Tula Oblast": "field",
        "Yaroslavl Oblast": "field",
        "Moscow City": "house",
    }
    assert central_fed_slaves == expected_central_fed_slaves
    assert list(central_fed_slaves.values()).count("house") == 1
    assert list(central_fed_slaves.values()).count("field1") == 1


def get_moscow_city_slaves() -> set[str]:
    return {
        "Eastern Administrative Okrug": "field",
        "Southeastern Administrative Okrug": "field",
        "Southern Administrative Okrug": "field",
        "Southwestern Administrative Okrug": "field",
        "Western Administrative Okrug": "field",
        "Northwestern Administrative Okrug": "field1",
        "Zelenograd Administrative Okrug": "field",
        "Novomoskovsky Administrative Okrug": "field",
        "Troitsky Administrative Okrug": "house",
    }


def test_get_moscow_city_slaves_ReturnsObj():
    # ESTABLISH / WHEN
    moscow_city_slaves = get_moscow_city_slaves()
    # THEN
    expected_moscow_city_slaves = {
        "Eastern Administrative Okrug": "field",
        "Southeastern Administrative Okrug": "field",
        "Southern Administrative Okrug": "field",
        "Southwestern Administrative Okrug": "field",
        "Western Administrative Okrug": "field",
        "Northwestern Administrative Okrug": "field1",
        "Zelenograd Administrative Okrug": "field",
        "Novomoskovsky Administrative Okrug": "field",
        "Troitsky Administrative Okrug": "house",
    }
    assert moscow_city_slaves == expected_moscow_city_slaves
    assert list(moscow_city_slaves.values()).count("house") == 1
    assert list(moscow_city_slaves.values()).count("field1") == 1
