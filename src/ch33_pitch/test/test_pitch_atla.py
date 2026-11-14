from ch33_pitch.pitch import AtlaUnit, PitchUnit, pitchunit_shop
from ch99_glossary.ch_keyword import Ch33Keywords as kw, ExampleStrs as exx


def test_AtlaUnit_Exists():
    # ESTABLISH / WHEN
    x_atlaunit = AtlaUnit()

    # THEN
    assert not x_atlaunit.atla_name
    assert not x_atlaunit.pitch_id
    assert not x_atlaunit.old_world_dir
    assert not x_atlaunit.gift_world_dir
    assert not x_atlaunit.new_world_dir
    assert not x_atlaunit.difference_report
    assert set(x_atlaunit.__dict__.keys()) == {
        "atla_name",
        "pitch_id",
        "old_world_dir",
        "gift_world_dir",
        "new_world_dir",
        "difference_report",
    }
