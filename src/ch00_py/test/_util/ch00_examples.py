from enum import Enum


class DictToolExampleStrs(str, Enum):
    bob = "Bob"
    sue = "Sue"
    SueZia = "SueZia"
    yao = "Yao"
    xio = "Xio"
    zia = "Zia"
    SueAndZia = "SueAndZia"
    casa = "casa"
    clean_str = "clean"
    dirtyness_str = "dirtyness"
    slash_str = "/"
    bowl = "bowl"
    wk_str = "wk"

    def __str__(self):
        return self.value
