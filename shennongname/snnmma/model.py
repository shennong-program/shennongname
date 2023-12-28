from pydantic import BaseModel


# Type alias
NmmsnNeList = list[list[str] | str]
'''
- Inner list[str] must be a list of two strings. 
- Inner str must be a logical operator: 'and' or 'or'.
- Must follow the format of: [list[str], str, list[str], str, list[str], ...]

Examples:
---------
[['root', '根'], 'and', ['stem', '茎'], 'or', ['leaf', '叶']]
'''


NmmsnSeq = list[list[str]]
'''
Examples:
---------
[["Ephedra equisetina vel intermedia vel sinica", "木贼麻黄或中麻黄或草麻黄"], ["Stem-herbaceous", "草质茎"], ["", ""], ["Segmented and Aquafried-honey", "蜜炙制段制"]]
'''


class NmmsnNameElement(BaseModel):
    nmm_type: str
    species_origins: NmmsnNeList
    medicinal_parts: NmmsnNeList
    special_descriptions: NmmsnNeList
    processing_methods: NmmsnNeList


class EnZh(BaseModel):
    en: str = ''
    zh: str = ''


class SnnmmaOutputFail(BaseModel):
    success: bool = False
    error_msg: str = ''
    error_msg_en_zh: EnZh = EnZh()


class NmmsnZh(BaseModel):
    zh: str
    pinyin: str


class Nmmsn(BaseModel):
    nmmsn: str
    nmmsn_zh: NmmsnZh
    nmmsn_name_element: NmmsnNameElement
    nmmsn_seq: NmmsnSeq


class SnnmmaOutputSuccess(BaseModel):
    success: bool = True
    error_msg: str = ''
    error_msg_en_zh: EnZh = EnZh()
    nmmsn: Nmmsn
