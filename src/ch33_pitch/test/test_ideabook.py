from ch33_pitch.ideabook import IdeaBook
from ch99_glossary.ch_keyword import Ch23Keywords as kw, ExampleStrs as exx

# # get a list of all prime tables
# def test_IdeaPrime_Exists():
#     # ESTABLISH / WHEN
#     ideaprime = IdeaPrime()
#     # THEN
#     assert not ideaprime
#     assert set(ideaprime.__dict__.keys()) == {f"{kw.}s"}


def test_IdeaBook_Exists():
    # ESTABLISH / WHEN
    ideabook = IdeaBook()
    # THEN
    assert not ideabook.ideas
    assert set(ideabook.__dict__.keys()) == {f"{kw.idea}s"}
    # assert 1 == 2
