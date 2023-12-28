import pytest

from shennongname.snnmma.model import NmmsnNameElement

from shennongname.snnmma.algorithm import (
    AsciiStr,
    convert_to_pinyin,
    split_sentence_by_words,
    Mapping,
    detect_species_inclusion,
    internationalize_error_msg,
    NmmsnNeData,
    construct_nmmsn_spe_ori,
    construct_nmmsn_med_par,
    construct_nmmsn_spe_des,
    construct_nmmsn_pro_met,
    construct_nmmsn,
)


class TestAsciiStr():
    def test_char_is_printable_ascii(self):
        assert AsciiStr.char_is_printable_ascii('a') == True
        # non-printable ascii
        assert AsciiStr.char_is_printable_ascii('\x00') == False
    
    
    def test_is_printable_ascii(self):
        assert AsciiStr("Hello World!").is_printable_ascii() == True
        assert AsciiStr("Hello \x00 World!").is_printable_ascii() == False
    
    
    def test_get_non_ascii_characters(self):
        assert AsciiStr("Hello 你 World! 你好，世界").get_non_ascii_characters() == set(['你', '你', '好', '，', '世', '界'])
        assert AsciiStr("Hello World!").get_non_ascii_characters() == set()
    
    
    def test_replace_non_printable_ascii(self):
        assert AsciiStr("Hello World!").replace_non_printable_ascii().str == "Hello World!"
        assert AsciiStr("Hello \x00 World!").replace_non_printable_ascii().str == "Hello World!"
        assert AsciiStr("Hello \x00 World!").replace_non_printable_ascii(replacement='?').str == "Hello ? World!"
    
    
    def test_remove_space(self):
        assert AsciiStr("  Hello    World!  ").remove_space().str == "HelloWorld!"
        
    
    def test_remove_zh_special_punctuation(self):
        assert AsciiStr("（原）板蓝").remove_zh_special_punctuation().str == "原板蓝"
    
    
    def test_char_is_alphabet_and_hyphen_and_space(self):
        assert AsciiStr.char_is_alphabet_and_hyphen_and_space('a') == True
        assert AsciiStr.char_is_alphabet_and_hyphen_and_space('A') == True
        assert AsciiStr.char_is_alphabet_and_hyphen_and_space('-') == True
        assert AsciiStr.char_is_alphabet_and_hyphen_and_space(' ') == True
        assert AsciiStr.char_is_alphabet_and_hyphen_and_space('1') == False
        assert AsciiStr.char_is_alphabet_and_hyphen_and_space('你') == True # python built-in isalpha() will return True for Chinese characters.
    
    
    def test_is_alphabet_and_hyphen_and_space(self):
        assert AsciiStr("Hello World").is_alphabet_and_hyphen_and_space() == True
        assert AsciiStr("Hello World!").is_alphabet_and_hyphen_and_space() == False
        assert AsciiStr("Hello 你 World").is_alphabet_and_hyphen_and_space() == True
        assert AsciiStr("Hello × World").is_alphabet_and_hyphen_and_space() == False
    
    
    def test_get_non_alphabet_and_hyphen_and_space_characters(self):
        assert AsciiStr("Hello × World").get_non_alphabet_and_hyphen_and_space_characters() == set(['×'])
        assert AsciiStr("Hello 你 World").get_non_alphabet_and_hyphen_and_space_characters() == set()
        assert AsciiStr("Hello World").get_non_alphabet_and_hyphen_and_space_characters() == set()
    
    
    def test_replace_non_alphabet_and_hyphen_and_space(self):
        assert AsciiStr("Hello × World").replace_non_alphabet_and_hyphen_and_space().str == "Hello World"
        assert AsciiStr("Hello × World").replace_non_alphabet_and_hyphen_and_space(replacement='?').str == "Hello ? World"


def test_convert_to_pinyin():
    assert convert_to_pinyin("青蒿") == "qīng hāo"
    assert convert_to_pinyin("人参") == "rén shēn"
    assert convert_to_pinyin("黄芪") == "huáng qí"
    assert convert_to_pinyin("当归") == "dāng guī"
    assert convert_to_pinyin("枸杞") == "gǒu qǐ"


@pytest.mark.parametrize("input_data, split_words, keep_sep, expected", [
    ("  a  and b   or c ", [' and ', ' or '], False, ['a', 'b', 'c']),
    ("  a and    b  or c ", [' and ', ' or '], True, ['a', 'and', 'b', 'or', 'c']),
    ("  a b c  ", [' and ', ' or '], False, ['a b c']),
])
def test_split_sentence_by_words(input_data, split_words, keep_sep, expected):
    assert split_sentence_by_words(input_data, split_words, keep_sep) == expected


class TestMapping:
    mapping_nn = []
    mapping_oo = [("apple", "苹果"), ("car", "汽车")]
    mapping_mo = [("apple", "苹果"), ("car", "汽车"), ("appla", "苹果")]
    mapping_om = [("apple", "苹果"), ("car", "汽车"), ("apple", "苹果果")]
    mapping_mm = [("apple", "苹果"), ("car", "汽车"), ("appla", "苹果"), ("apple", "苹果果")]
    
    
    def test_init(self):
        mappings = [
            [("carr", "car"), ("appla", "apple"), ("appla", "apple")],
        ]
        expected_mappings = [
            [("appla", "apple"), ("carr", "car")],
        ]
        for mapping, expected_mapping in zip(mappings, expected_mappings):
            mapping_cls = Mapping(mapping)
            assert mapping_cls.mapping == expected_mapping
        invalid_mappings = [
            [()],
            (),
            {},
            [{}],
        ]
        for invalid_mapping in invalid_mappings:
            with pytest.raises(ValueError):
                mapping_cls = Mapping(invalid_mapping)
        

    def test_verify_mapping_type(self):
        assert Mapping(self.mapping_nn).verify_mapping_type() == 'nn'
        assert Mapping(self.mapping_oo).verify_mapping_type() == 'oo'
        assert Mapping(self.mapping_mo).verify_mapping_type() == 'mo'
        assert Mapping(self.mapping_om).verify_mapping_type() == 'om'
        assert Mapping(self.mapping_mm).verify_mapping_type() == 'mm'
        

    def test_get_forward_mapping(self):
        mappings = [self.mapping_nn, self.mapping_oo, self.mapping_mo]
        expected_forward_mappings = [
            {},
            {'apple': '苹果', 'car': '汽车'}, 
            {'apple': '苹果', 'car': '汽车', 'appla': '苹果'}
        ]
        for mapping, expected_forward_mapping in zip(mappings, expected_forward_mappings):
            mapping_cls = Mapping(mapping)
            assert mapping_cls.get_forward_mapping() == expected_forward_mapping
        
        for mapping in [self.mapping_om, self.mapping_mm]:
            mapping_cls = Mapping(mapping)
            with pytest.raises(ValueError):
                mapping_cls.get_forward_mapping()
    
    
    def test_get_backward_mapping(self):
        mappings = [self.mapping_nn, self.mapping_oo, self.mapping_om]
        expected_backward_mappings = [
            {},
            {'苹果': 'apple', '汽车': 'car'}, 
            {'苹果': 'apple', '汽车': 'car', '苹果果': 'apple'}
        ]
        for mapping, expected_backward_mapping in zip(mappings, expected_backward_mappings):
            mapping_cls = Mapping(mapping)
            assert mapping_cls.get_backward_mapping() == expected_backward_mapping
        
        for mapping in [self.mapping_mo, self.mapping_mm]:
            mapping_cls = Mapping(mapping)
            with pytest.raises(ValueError):
                mapping_cls.get_backward_mapping()


    def test_get_multi_to_one_mappings(self):
        mapping = [("appla", "apple"), ("carr", "car"), ("appli", "apple")]
        mapping_cls = Mapping(mapping)
        expected_multi_to_one_mappings = [('appla', 'apple'), ('appli', 'apple')]
        mapping_cls.get_multi_to_one_mappings()
        assert mapping_cls.multi_to_one_mappings == expected_multi_to_one_mappings

        mapping = [("appla", "apple"), ("carr", "car")]
        mapping_cls = Mapping(mapping)
        with pytest.raises(ValueError):
            mapping_cls.get_multi_to_one_mappings()
            

    def test_report_multi_to_one_mappings(self, capsys):
        mapping = [("appla", "apple"), ("carr", "car"), ("appli", "apple")]
        mapping_cls = Mapping(mapping)
        expected_output = "The following multi-to-one mappings were found:\nappla -> apple\nappli -> apple\nPlease choose which mappings to keep.\n"
        mapping_cls.get_multi_to_one_mappings()
        mapping_cls.report_multi_to_one_mappings()
        captured = capsys.readouterr()
        assert captured.out == expected_output


def test_detect_species_inclusion():
    species = ["  Prinsepia uniflora ", "   Prinsepia uniflora var. serrata ", "  Prinsepia   "]
    expected_output = (True, ["Prinsepia"])
    assert detect_species_inclusion(species) == expected_output

    species = ["Prinsepia uniflora", "Prinsepia serrata", "Prinsepia"]
    expected_output = (True, ["Prinsepia"])
    assert detect_species_inclusion(species) == expected_output

    species = ["Prinsepia uniflora", "Prinsepia serrata", "Prinsepia sinensis"]
    expected_output = (False, ["Prinsepia serrata", "Prinsepia sinensis", "Prinsepia uniflora"])
    assert detect_species_inclusion(species) == expected_output

    species = ["Prinsepia uniflora", "  Prinsepia serrata  ", "Prinsepia"]
    expected_output = (True, ["Prinsepia"])
    assert detect_species_inclusion(species) == expected_output
    
    species = ["  Prinsepia uniflora ", "   Prinsepia uniflora var. serrata "]
    expected_output = (True, ["Prinsepia uniflora"])
    assert detect_species_inclusion(species) == expected_output


def test_internationalize_error_msg():
    error_msgs = [
        """
        Error message A.
        Pipe: xxx. Status: xxx. Reason: abc.
        Error message B.
        Pipe: xxx. Status: xxx. Reason: def.
        Pipe: xxx. Status: xxx. Reason: ghi.
        Miao miao miao.
        Wang wang wang.
        """,
        """
        Pipe: xxx. Status: xxx. Reason: abc.
        Hello, world!
        """   
    ]
    # Wang wang wang. Not in zh.po
    
    # expected_output should contain the translated strings that you have in your zh.po file.
    expected_outputs = [
        {
            'en': 'Error message A.\nabc.\nError message B.\ndef.\nghi.\nMiao miao miao.\nWang wang wang.',
            'zh': '错误信息A。\n甲乙丙。\n错误信息B。\n丁戊己。\n庚辛壬。\n喵喵喵。\nWang wang wang.',
        },
        {
            'en': 'abc.\nHello, world!',
            'zh': '甲乙丙。\n你好，世界！',
        }
    ]
    
    for error_msg, expected_output in zip(error_msgs, expected_outputs):
        assert internationalize_error_msg(error_msg).model_dump() == expected_output


class TestNmmsnNeData:
    # setup
    valid_ne_list = [
        [['a', 'A'], 'or', ['b', 'B'], 'and', ['c', 'C']],
        [[' a  ', ' A   '], 'OR', ['b', 'B'], '  and ', ['   c d', 'C D  ']],
        [['a', '甲'], 'or', ['b', '乙'], 'and', ['c', '丙']],
        [],
        # with only one logical operator
        [['a', 'A'], 'or', ['b', 'B'], 'or', ['c', 'C']],
        [['a', 'A'], 'and', ['b', 'B'], 'and', ['c', 'C']],
    ]
    expected_ne_list = [
        valid_ne_list[0],
        [['a', 'A'], 'or', ['b', 'B'], 'and', ['c d', 'C D']],
        valid_ne_list[2],
        valid_ne_list[3],
        valid_ne_list[4],
        valid_ne_list[5],
    ]
    invalid_ne_list = [
        [['a', 'A'], 'or', ['b', 'B'], 'and', ['c', 'C'], 'or'], # extra 'or'
        ['a', 'or', ['b', 'B'], 'and', ['c', 'C']], # first element is not a list
        [['a', 'A', '甲'], 'or', ['b', 'B'], 'and', ['c', 'C']], # extra element in first list
        [['a', 'A'], ['b', 'B'], 'and', ['c', 'C']], # missing logical operator
        [['a', 'A'], 'but', ['b', 'B'], 'and', ['c', 'C']], # invalid logical operator
    ]
    
    special_ne_list = [
        # duplicate NEs and unordered NEs
        [['c', 'C'], 'and', ['b', 'B'], 'and', ['c', 'C'], 'or', ['a', 'A'], 'or', ['c', 'C'], 'and', ['b', 'B']],
        
        # ne with non-ascii characters
        [['a', '甲'], 'or', ['b c.×', '乙 丙'], 'and', ['d', '丁']],
        
        # not oo mapping
        # om
        [['a', 'A'], 'or', ['a', 'B'], 'and', ['c', 'C']],
        # mo
        [['a', 'A'], 'or', ['b', 'A'], 'and', ['c', 'C']],
        # mm
        [['a', 'A'], 'or', ['b', 'B'], 'and', ['a', 'C'], 'and', ['b', 'C']],
    ]

    
    def test_init(self):
        for i in range(len(self.valid_ne_list)):
            ne_data = NmmsnNeData(self.valid_ne_list[i])
            assert ne_data.nmmsn_ne_list == self.expected_ne_list[i]
        for ne_list in self.invalid_ne_list:
            with pytest.raises(ValueError):
                ne_data = NmmsnNeData(ne_list)


    def test_str(self):
        # Test empty input data
        nmmsn_ne_list = []
        nmmsn_ne_data = NmmsnNeData(nmmsn_ne_list)
        assert str(nmmsn_ne_data) == ''

        # Test valid input data
        nmmsn_ne_list = [['  a ', '  b '], 'and', ['d', 'e  f']]
        nmmsn_ne_data = NmmsnNeData(nmmsn_ne_list)
        assert str(nmmsn_ne_data) == 'a | b and d | e f'
    
    
    def test_init_from_str(self):
        inputs = [
            '  a   | b and   d|e f   or   g |h i   ',
            'aandb | 甲and乙 and cord | 丙or丁 or eandforg | 戊and己or庚',
            ''
        ]
        expected_outputs = [
            [['a', 'b'], 'and', ['d', 'e f'], 'or', ['g', 'h i']],
            [['aandb', '甲and乙'], 'and', ['cord', '丙or丁'], 'or', ['eandforg', '戊and己or庚']],
            []
        ]
        for input, expected_output in zip(inputs, expected_outputs):
            ne_data = NmmsnNeData.init_from_str(input)
            assert ne_data.nmmsn_ne_list == expected_output
        
        invalid_inputs = [
            # start or end with logical operator
            'and  d | e f or g | h i',
            'a | b and d | e f or g | h i or',
            # consecutive logical operators
            'a | b and and d | e f or g | h i'
            'a | b and d | e f or or g | h i',
        ]
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError):
                ne_data = NmmsnNeData.init_from_str(invalid_input)
        
    
    def test_validate_empty(self):
        ne_data = NmmsnNeData(self.valid_ne_list[3])
        with pytest.raises(ValueError):
            ne_data.validate_empty()
    
    
    def test_validate_only_and_or_only_or(self):
        # should raise error
        ne_data = NmmsnNeData(self.valid_ne_list[0])
        with pytest.raises(ValueError):
            ne_data.validate_only_and_or_only_or()
            
        # would not raise error
        ne_data = NmmsnNeData(self.valid_ne_list[4])
        ne_data.validate_only_and_or_only_or()
        ne_data = NmmsnNeData(self.valid_ne_list[5])
        ne_data.validate_only_and_or_only_or()
    
    
    def test_validate_oo_mapping_type(self):
        # would not raise error
        ne_data = NmmsnNeData(self.valid_ne_list[0])
        ne_data.validate_oo_mapping_type()
        ne_data = NmmsnNeData(self.valid_ne_list[3]) # empty list
        
        # should raise error
        for ne_list in self.special_ne_list[2:]:
            ne_data = NmmsnNeData(ne_list)
            with pytest.raises(ValueError):
                ne_data.validate_oo_mapping_type()

    
    def test_convert_inner_list_to_tuple_and_convert_inner_tuple_to_list(self):
        ne_data = NmmsnNeData(self.valid_ne_list[0])
        tuple_ne_list = [('a', 'A'), 'or', ('b', 'B'), 'and', ('c', 'C')]
        assert ne_data.convert_inner_list_to_tuple() == tuple_ne_list
        assert ne_data.convert_inner_tuple_to_list(tuple_ne_list) == ne_data.nmmsn_ne_list
    
    
    def test_convert_nmmsn_ne_list_to_lower_case(self):
        # Test 1
        ne_list = [['A', 'B'], 'and', ['C', 'D'], 'or', ['E', 'F']]
        expected_output = [['a', 'b'], 'and', ['c', 'd'], 'or', ['e', 'f']]
        ne_data = NmmsnNeData(ne_list)
        assert ne_data.convert_nmmsn_ne_list_to_lower_case().nmmsn_ne_list == expected_output
        
        # Test 2
        ne_list = []
        expected_output = []
        ne_data = NmmsnNeData(ne_list)
        assert ne_data.convert_nmmsn_ne_list_to_lower_case().nmmsn_ne_list == expected_output
    
        
    def test_logic_order(self):
        # 1
        ordered_ne_list = [['a', 'A'], 'or', ['b', 'B'], 'and', ['c', 'C']]
        unordered_ne_data = NmmsnNeData(self.special_ne_list[0])
        assert unordered_ne_data.logic_order().nmmsn_ne_list == ordered_ne_list
        
        # 2
        unordered_ne_list = []
        unordered_ne_data = NmmsnNeData(unordered_ne_list)
        assert unordered_ne_data.logic_order().nmmsn_ne_list == []
        
        # Test 3: 1. exclude_and = True; 2. Whether removed the duplicated NEs with "or" logic; 3. Whether correctly order the NEs with "or" logic.
        unordered_ne_list = [['b', '乙'], 'and', ['a', '甲'], 'and', ['a', '甲'], 'or', ['a', '甲'], 'or', ['a', '甲']]
        ordered_ne_list = [['a', '甲'], 'or', ['b', '乙'], 'and', ['a', '甲'], 'and', ['a', '甲']] # 1. Duplicate NEs ['a', '甲'] are removed; 2. The order of the NEs with "or" logic is correctly ordered by the order of alphabetical order; 3. The order of the NEs with "and" logic is not changed; 4. The duplicated NEs with "and" logic are not removed.
        unordered_ne_data = NmmsnNeData(unordered_ne_list)
        assert unordered_ne_data.logic_order(exclude_and=True).nmmsn_ne_list == ordered_ne_list
        

    def test_stringify(self):
        # 1
        ne_data = NmmsnNeData(self.valid_ne_list[0])
        str_1, str_2 = ne_data.stringify()
        assert str_1 == 'a or b and c'
        assert str_2 == 'A or B and C'
        # 2
        ne_data = NmmsnNeData([])
        str_1, str_2 = ne_data.stringify()
        assert str_1 == ''
        assert str_2 == ''
        # 3
        ne_data = NmmsnNeData(
            [[' a ', 'A  A'], 'or', ['b  ', 'B B  '], 'and', ['c', 'C  C']]
        )
        str_1, str_2 = ne_data.stringify(reverse_second_str=True)
        assert str_1 == 'a or b and c'
        assert str_2 == 'C C and B B or A A'
    
    
    def test_stringify_en_zh(self):
        # Test 1
        ne_data = NmmsnNeData(self.special_ne_list[1])
        str_1, str_2 = ne_data.stringify_en_zh()
        assert str_1 == 'A or B-c and D'
        assert str_2 == '甲或乙-丙与丁'
        
        
        ne_data = NmmsnNeData(
            [['a', '甲'], 'or', ['b c', '乙 丙'], 'and', ['d', '丁']]
        )
        
        # Test 2: reverse_zh_str
        str_1, str_2 = ne_data.stringify_en_zh(reverse_zh_str=True)
        assert str_1 == 'A or B-c and D'
        assert str_2 == '丁与乙-丙或甲'
        
        # Test 3: remove_zh_and
        str_1, str_2 = ne_data.stringify_en_zh(reverse_zh_str=True, remove_zh_and=True)
        assert str_1 == 'A or B-c and D'
        assert str_2 == '丁乙-丙或甲'
    
    
    def test_extract_map_pairs(self):
        # 1
        ne_data = NmmsnNeData(self.special_ne_list[0])
        expected_output = [('a', 'A'), ('b', 'B'), ('c', 'C')]
        assert ne_data.extract_map_pairs() == expected_output
        # 2
        ne_data = NmmsnNeData([])
        assert ne_data.extract_map_pairs() == []
        
        
        # testing the extract_first_logical_operator method
    def test_extract_first_logical_operator(self):
        ne_data = NmmsnNeData(self.valid_ne_list[0])
        assert ne_data.extract_first_logical_operator() == 'or'
        
    
    def test_extract_logical_operators(self):
        # Test empty input data
        nmmsn_ne_list = []
        nmmsn_ne_data = NmmsnNeData(nmmsn_ne_list)
        assert nmmsn_ne_data.extract_logical_operators() == set()

        # Test valid input data
        nmmsn_ne_list = [['a', 'b'], 'and', ['d', 'e  f'], 'or', ['g', 'h i']]
        nmmsn_ne_data = NmmsnNeData(nmmsn_ne_list)
        assert nmmsn_ne_data.extract_logical_operators() == {'and', 'or'}

        # Test input data with only one logical operator
        nmmsn_ne_list = [['a', 'b'], 'or', ['d', 'e  f'], 'or', ['g', 'h i']]
        nmmsn_ne_data = NmmsnNeData(nmmsn_ne_list)
        assert nmmsn_ne_data.extract_logical_operators() == {'or'}

        # Test input data with only one logical operator
        nmmsn_ne_list = [['a', 'b'], 'and', ['d', 'e  f'], 'and', ['g', 'h i']]
        nmmsn_ne_data = NmmsnNeData(nmmsn_ne_list)
        assert nmmsn_ne_data.extract_logical_operators() == {'and'}
            
    
    def test_convert_to_nmmsn_ne_mono(self):
        # Test case 1
        input_list = [['a', '甲'], 'or', ['b c', '乙 丙'], 'and', ['d', '丁'], 'or', ['e', '戊'], 'and', ['f', '己']]
        expected_output = (['a', 'or', 'b c', 'and', 'd', 'or', 'e', 'and', 'f'], ['甲', 'or', '乙 丙', 'and', '丁', 'or', '戊', 'and', '己'])
        assert NmmsnNeData(input_list).convert_to_nmmsn_ne_mono() == expected_output


def test_construct_nmmsn_spe_ori():
    tests = [
        {
            "input": [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra equisetina', '木贼麻黄']],
            "output": (
                'Ephedra equisetina vel intermedia vel sinica', 
                '木贼麻黄或中麻黄或草麻黄', 
                # error message not empty
                'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.',
                [['Ephedra equisetina', '木贼麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra sinica', '草麻黄']]
            ),
        },
        {
            "input": [['Ephedra sinica', '草麻黄'], 'and', ['Ephedra intermedia', '中麻黄'], 'and', ['Ephedra equisetina', '木贼麻黄']],
            "output": (
                'Ephedra equisetina et intermedia et sinica', 
                '木贼麻黄与中麻黄与草麻黄', 
                'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.',
                [['Ephedra equisetina', '木贼麻黄'], 'and', ['Ephedra intermedia', '中麻黄'], 'and', ['Ephedra sinica', '草麻黄']]
            ),
        },
        
        # duplicated or
        {
            "input": [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra sinica', '草麻黄'], 'or', ['Ephedra sinica', '草麻黄']],
            "output":  (
                'Ephedra sinica', 
                '草麻黄', 
                '',
                [['Ephedra sinica', '草麻黄']]
            ),
        },
        
        # duplicated and
        {
            "input": [['Ephedra sinica', '草麻黄'], 'and', ['Ephedra sinica', '草麻黄'], 'and', ['Ephedra sinica', '草麻黄']],
            "output":  (
                'Ephedra sinica', 
                '草麻黄', 
                '',
                [['Ephedra sinica', '草麻黄']]
            ),
        },
        
        # with non-ascii characters
        {
            "input": [['Ephedra sinica × intermedia', '虚拟的草麻黄杂交种'], 'or', ['Ephedra sinica var. intermedia', '虚拟的草麻黄变种']],
            "output":  (
                'Ephedra sinica var intermedia vel sinica intermedia',
                '虚拟的草麻黄变种或虚拟的草麻黄杂交种',
                'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.',
                [['Ephedra sinica var. intermedia', '虚拟的草麻黄变种'], 'or', ['Ephedra sinica × intermedia', '虚拟的草麻黄杂交种']]
            ),
        },
        
        # with special zh punctuations
        {
            "input": [
                ['Strobilanthes cusia', '（ 原 ）板 蓝'], # with special zh punctuations and space
                'or',
                ['Ephedra sinica', '草麻黄']
            ],
            "output":  (
                'Ephedra sinica vel Strobilanthes cusia',
                '草麻黄或原板蓝',
                'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.',
                [['Ephedra sinica', '草麻黄'], 'or', ['Strobilanthes cusia', '（原）板蓝']]
            ),  
        },
        
        # species with inclusion
        {
            "input": [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra', '麻黄属']],
            "output":  (
                'Ephedra',
                '麻黄属',
                'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Species inclusion detected.',
                [['Ephedra', '麻黄属']]
            ),
        },
        {
            "input": [['Ephedra sinica', '草麻黄'], 'and', ['Ephedra', '麻黄属']],
            "output":  (
                'Ephedra',
                '麻黄属',
                'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Species inclusion detected.',
                [['Ephedra', '麻黄属']]
            ),
        },
        {
            "input": [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra sinica var. intermedia', '虚拟的草麻黄变种']],
            "output":  (
                'Ephedra sinica',
                '草麻黄',
                'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Species inclusion detected.',
                [['Ephedra sinica', '草麻黄']]
            ),
        }
    ]
    for test in tests:
        assert construct_nmmsn_spe_ori(test["input"]) == test["output"]

    
    # Testing with an empty list
    with pytest.raises(ValueError):  # Adjust this to match the exception your function should raise
        construct_nmmsn_spe_ori([])

    # Testing with invalid logical operator
    spe_ori_input = [['Ephedra sinica', '草麻黄'], 'not', ['Ephedra intermedia', '中麻黄'], 'not', ['Ephedra equisetina', '木贼麻黄']]
    with pytest.raises(ValueError):
        construct_nmmsn_spe_ori(spe_ori_input)

    # Testing with invalid data type
    with pytest.raises(ValueError):
        construct_nmmsn_spe_ori("invalid input type") # type: ignore

    
    # Testing faid case
    faid_spe_ori_inputs = [
        # empty list
        [],
        # not oo mapping
        [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra sinica', '草草麻黄']],
        [['Ephedra sinica sinica', '草麻黄'], 'and', ['Ephedra sinica', '草麻黄']],
        # multiple different logical operators
        [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'and', ['Ephedra equisetina', '木贼麻黄']],
    ]
    for faid_spe_ori_input in faid_spe_ori_inputs:
        with pytest.raises(ValueError):
            construct_nmmsn_spe_ori(faid_spe_ori_input)
            

def test_construct_nmmsn_med_par():
    # Test case with successful execution
    med_par_inputs = [
        [['rOOt', '根']],
        [['root', '根'], 'and', ['rhizome', '根茎'], 'or', ['leaf', '叶'], 'or', ['stem herbaceous', '草质茎']],
    ]
    expected_outputs = [
        (
            'Root',
            '根',
            '',
            [['root', '根']]
        ),
        (
            'Leaf or Rhizome and Root or Stem-herbaceous', 
            '叶或根茎与根或草质茎', 
            'Pipe: construct_nmmsn_med_par. Status: warning. Reason: Multiple medicinal parts detected.',
            [['leaf', '叶'], 'or', ['rhizome', '根茎'], 'and', ['root', '根'] , 'or', ['stem herbaceous', '草质茎']]
        )
    ]
    for med_par_input, expected_output in zip(med_par_inputs, expected_outputs):
        assert construct_nmmsn_med_par(med_par_input) == expected_output
        
        
    # Test case with invalid input
    invalid_input = ['Invalid', 'Input']
    with pytest.raises(ValueError): 
        construct_nmmsn_med_par(invalid_input) # type: ignore

    # Test case with empty input
    empty_input = []
    with pytest.raises(ValueError):
        construct_nmmsn_med_par(empty_input)


def test_construct_nmmsn_spe_des():
    spe_des_input = [
        [],
        [['fRESh', '鲜']],
        [['fresh', '鲜'], 'or', ['dried', '干'], 'or', ['dried', '干'], 'or', ['fresh', '鲜']]
    ]
    expected_output = [
        (
            '',
            '',
            '',
            []
        ),
        (
            'Fresh',
            '鲜',
            '',
            [['fresh', '鲜']]
        ),
        (
            'Dried or Fresh', 
            '鲜或干', 
            'Pipe: construct_nmmsn_spe_des. Status: warning. Reason: Multiple special descriptions detected.',
            [['dried', '干'], 'or', ['fresh', '鲜']]
        )
    ]
    for spe_des_input, expected_output in zip(spe_des_input, expected_output):
        assert construct_nmmsn_spe_des(spe_des_input) == expected_output


def test_construct_nmmsn_pro_met():
    # Test case with successful execution
    pro_met_inputs = [
        [],
        [['steamed', '蒸制']],
        [['   steAmed', '蒸制'], 'and', ['stirfried', '炒制']],
        [['stirfried', '炒制'], 'and', ['aquafried', '炙制'], 'or', ['steamed', '蒸制'], 'or', ['steamed', '蒸制']], # Test: 1. Whether remove the duplicated processing methods with "or" logic; 2. Whether correctly order the processing methods with "or" logic.
        [['steamed', '蒸']],
    ]
    expected_outputs = [
        (
            '',
            '',
            '',
            []
        ),
        (
            'Steamed',
            '蒸制',
            '',
            [['steamed', '蒸制']]
        ),
        (
            'Steamed and Stirfried', 
            '炒制蒸制', 
            '',
            [['steamed', '蒸制'], 'and', ['stirfried', '炒制']]
        ),
        (
            'Steamed or Stirfried and Aquafried',
            '炙制炒制或蒸制', # The order of the processing methods is reversed and the "与" is removed
            'Pipe: construct_nmmsn_pro_met. Status: warning. Reason: Multiple processing methods with "or" logic detected.',
            [['steamed', '蒸制'], 'or', ['stirfried', '炒制'], 'and', ['aquafried', '炙制']] # The order of the processing methods are ordered by the order of alphabetical order. But the order of the processing methods with "and" logic is not changed.
        ),
        (
            'Steamed',
            '蒸',
            'Pipe: construct_nmmsn_pro_met. Status: warning. Reason: Not all processing methods end with "制".',
            [['steamed', '蒸']]
        ),
    ]
    for pro_met_input, expected_output in zip(pro_met_inputs, expected_outputs):
        assert construct_nmmsn_pro_met(pro_met_input) == expected_output


def test_construct_nmmsn():
    # Test 1
    input = NmmsnNameElement.model_validate(
        {
            'nmm_type': "plant",
            'species_origins': [['Ephedra sinica', '草麻黄']],
            'medicinal_parts': [['herbaceous stem', '草质茎']],
            'special_descriptions': [],
            'processing_methods': []
        }
    )
    
    expected_output = {
        'success': True,
        'error_msg': '',
        'error_msg_en_zh': {
            'en': '',
            'zh': '',
        },
        'nmmsn': {
            'nmmsn': 'Ephedra sinica Herbaceous-stem',
            'nmmsn_zh': {
                'zh': '草麻黄草质茎',
                'pinyin': 'cǎo má huáng cǎo zhì jīng',
            },
            'nmmsn_name_element': {
                'nmm_type': 'plant',
                'species_origins': [['Ephedra sinica', '草麻黄']],
                'medicinal_parts': [['herbaceous stem', '草质茎']],
                'special_descriptions': [],
                'processing_methods': []
            },
            'nmmsn_seq': [['Ephedra sinica', '草麻黄'], ['Herbaceous-stem', '草质茎'], ['', ''], ['', '']]
        }
    }
    assert construct_nmmsn(input).model_dump() == expected_output
    
    # Test 2
    input = NmmsnNameElement.model_validate(
        {
            'nmm_type': "processed",
            'species_origins': [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra equisetina', '木贼麻黄']],
            'medicinal_parts': [['root', '根'], 'and', ['rhizome', '根茎'], 'or', ['herbaceous stem', '草质茎']],
            'special_descriptions': [['fresh', '鲜'], 'or', ['dried', '干']],
            'processing_methods': [['stirfried', '炒制'], 'and', ['steamed', '蒸制']]
        }
    )
    
    expected_output = {
        'success': True,
        'error_msg': 'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.\nPipe: construct_nmmsn_med_par. Status: warning. Reason: Multiple medicinal parts detected.\nPipe: construct_nmmsn_spe_des. Status: warning. Reason: Multiple special descriptions detected.',
        'error_msg_en_zh': {
            'en': 'Multiple species origins detected.\nMultiple medicinal parts detected.\nMultiple special descriptions detected.',
            'zh': '检测到多个物种基源。\n检测到多个药用部位。\n检测到多个特殊描述。',
        },
        'nmmsn': {
            'nmmsn': 'Ephedra equisetina vel intermedia vel sinica Herbaceous-stem or Rhizome and Root Dried or Fresh Stirfried and Steamed',
            'nmmsn_zh': {
                'zh': '蒸制炒制鲜或干木贼麻黄或中麻黄或草麻黄草质茎或根茎与根',
                'pinyin': 'zhēng zhì chǎo zhì xiān huò gàn mù zéi má huáng huò zhōng má huáng huò cǎo má huáng cǎo zhì jīng huò gēn jīng yǔ gēn', # 注意，这里的gàn拼音错了，是pypinyin的问题
            },
            'nmmsn_name_element': {
                'nmm_type': 'processed',
                'species_origins': [['Ephedra equisetina', '木贼麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra sinica', '草麻黄']],
                'medicinal_parts': [['herbaceous stem', '草质茎'], 'or', ['rhizome', '根茎'], 'and', ['root', '根']],
                'special_descriptions': [['dried', '干'], 'or', ['fresh', '鲜']],
                'processing_methods': [['stirfried', '炒制'], 'and', ['steamed', '蒸制']]
            },
            'nmmsn_seq': [['Ephedra equisetina vel intermedia vel sinica', '木贼麻黄或中麻黄或草麻黄'], ['Herbaceous-stem or Rhizome and Root', '草质茎或根茎与根'], ['Dried or Fresh', '鲜或干'], ['Stirfried and Steamed', '蒸制炒制']]
        }
    }
    assert construct_nmmsn(input).model_dump() == expected_output
    
    # Test 3
    input = NmmsnNameElement.model_validate(
        {
            'nmm_type': 'processed',
            'species_origins': [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra equisetina', '木贼麻黄']],
            'medicinal_parts': [['stem herbaceous', '草质茎']],
            'special_descriptions': [],
            'processing_methods': [['segmented', '段制'], 'and', ['aquafried honey', '蜜炙制']]
        }
    )
    
    expected_output = {
        'success': True,
        'error_msg': 'Pipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.',
        'error_msg_en_zh': {
            'en': 'Multiple species origins detected.',
            'zh': '检测到多个物种基源。',
        },
        'nmmsn': {
            'nmmsn': 'Ephedra equisetina vel intermedia vel sinica Stem-herbaceous Segmented and Aquafried-honey',
            'nmmsn_zh': {
                'zh': '蜜炙制段制木贼麻黄或中麻黄或草麻黄草质茎',
                'pinyin': 'mì zhì zhì duàn zhì mù zéi má huáng huò zhōng má huáng huò cǎo má huáng cǎo zhì jīng',
            },
            'nmmsn_name_element': {
                'nmm_type': 'processed',
                'species_origins': [['Ephedra equisetina', '木贼麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra sinica', '草麻黄']],
                'medicinal_parts': [['stem herbaceous', '草质茎']],
                'special_descriptions': [],
                'processing_methods': [['segmented', '段制'], 'and', ['aquafried honey', '蜜炙制']]
            },
            'nmmsn_seq': [['Ephedra equisetina vel intermedia vel sinica', '木贼麻黄或中麻黄或草麻黄'], ['Stem-herbaceous', '草质茎'], ['', ''], ['Segmented and Aquafried-honey', '蜜炙制段制']]
        }
    }
    assert construct_nmmsn(input).model_dump() == expected_output

    
    # Test 4: Test wrong nmm_type
    input = NmmsnNameElement.model_validate(
        {
            'nmm_type': 'plant',
            'species_origins': [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra equisetina', '木贼麻黄']],
            'medicinal_parts': [['stem herbaceous', '草质茎']],
            'special_descriptions': [],
            'processing_methods': [['segmented', '段制'], 'and', ['aquafried honey', '蜜炙制']]
        }
    )
    
    expected_output = {
        'success': False,
        'error_msg': 'Pipe: construct_nmmsn. Status: failed. Reason: Processing methods detected in non-processed NMM.\nPipe: construct_nmmsn_spe_ori. Status: warning. Reason: Multiple species origins detected.',
        'error_msg_en_zh': {
            'en': 'Processing methods detected in non-processed NMM.\nMultiple species origins detected.',
            'zh': '检测到非炮制NMM中的炮制方法。\n检测到多个物种基源。',
        }
    }
    assert construct_nmmsn(input).model_dump() == expected_output
