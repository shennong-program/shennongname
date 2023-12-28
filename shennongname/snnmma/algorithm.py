from collections import defaultdict
import re

from pypinyin import pinyin

from shennongname.lang.lang import get_translation
from shennongname.snnmma.model import NmmsnNeList, NmmsnNameElement, SnnmmaOutputSuccess, SnnmmaOutputFail, EnZh


_ = get_translation('en')
# if you want the program to run in Chinese, uncomment the following line
# _ = get_translation('zh')


# Default parameters
class Default:
    # default time format: no space, no colon
    DATETIME_FORMAT = "%Y%m%d-%H%M%S"
    
    # separator for multiple values in a cell
    SEPARATOR = ";"
    FAILED_MAPPING_TOKEN = "failed_mapping"
    FAILED_CONSTRUCT_TOKEN = "failed_construct"
    FAILED_API_TOKEN = "failed_api"
    
    # default cell value is empty string
    CELL_VALUE = ''


class NmmType:
    # ANMM
    PLANT =  ["plant", "植物药"]
    ANIMAL = ["animal", "动物药"]
    FUNGAL = ["fungal", "真菌药"]
    ALGAL = ["algal", "藻类药"]
    # ANMM can not be automatically named
    MINERAL = ["mineral", "矿物药"]
    OTHER = ["other", "其他药"]
    
    
    # PNMM
    PROCESSED = ["processed", "炮制药"]
    PROCESSED_OTHER = ["processed_other", "其他炮制药"] # ANMM (mineral, other) -> PNMM
    
    
    # Other
    CHEMICAL = ["chemical", "化物药"]
    ARTIFICIAL = ["artificial", "人工药"]
    
    
    # combined
    PAFA = PLANT + ANIMAL + FUNGAL + ALGAL
    
    
    def __init__(self, nmm_type: str):
        self.nmm_type = nmm_type.strip().lower().replace("-", "_")
    
    def is_pafa(self) -> bool:
        return self.nmm_type in self.PAFA
        
    def is_pro(self) -> bool:
        return self.nmm_type in self.PROCESSED
    
    def is_pafa_pro(self) -> bool:
        return self.is_pafa() or self.is_pro()


## Helper ######################################################################

# Helper: String

class AsciiStr:
    ZH_SPECIAL_PUNCTUATION = "（）"
    
    
    def __init__(self, str: str):
        self.str = str
    
    
    # ASCII
    @staticmethod
    def char_is_printable_ascii(c: str) -> bool:
        return ord(c) < 128 and ord(c) >= 32
    
        
    def is_printable_ascii(self) -> bool:
        return all(self.char_is_printable_ascii(c) for c in self.str)


    def get_non_ascii_characters(self) -> set[str]:
        char_list = [c for c in self.str if not self.char_is_printable_ascii(c)]
        char_list = set(char_list)
        return char_list
    

    def replace_non_printable_ascii(self, replacement: str = "") -> 'AsciiStr':
        replaced_str = "".join([c if self.char_is_printable_ascii(c) else replacement for c in self.str])
        # remove multiple spaces
        replaced_str = re.sub(r"\s+", " ", replaced_str)
        replaced_str = replaced_str.strip()
        return AsciiStr(replaced_str)
    
    
    def remove_space(self) -> 'AsciiStr':
        replaced_str = re.sub(r"\s+", "", self.str)
        return AsciiStr(replaced_str)
    
    
    def remove_zh_special_punctuation(self, zh_special_punctuation: str = ZH_SPECIAL_PUNCTUATION) -> 'AsciiStr':
        replaced_str = re.sub(f"[{zh_special_punctuation}]", "", self.str)
        return AsciiStr(replaced_str)
    
    
    # Alphabet and hyphen
    @staticmethod
    def char_is_alphabet_and_hyphen_and_space(c: str) -> bool:
        return c.isalpha() or c == "-" or c == " "
    
    
    def is_alphabet_and_hyphen_and_space(self) -> bool:
        return all(self.char_is_alphabet_and_hyphen_and_space(c) for c in self.str)
    
    
    def get_non_alphabet_and_hyphen_and_space_characters(self) -> set[str]:
        char_list = [c for c in self.str if not self.char_is_alphabet_and_hyphen_and_space(c)]
        char_list = set(char_list)
        return char_list
    
    
    def replace_non_alphabet_and_hyphen_and_space(self, replacement: str = "") -> 'AsciiStr':
        replaced_str = "".join([c if self.char_is_alphabet_and_hyphen_and_space(c) else replacement for c in self.str])
        # remove multiple spaces
        replaced_str = re.sub(r"\s+", " ", replaced_str)
        # remove multiple hyphens
        replaced_str = re.sub(r"-+", "-", replaced_str)
        replaced_str = replaced_str.strip()
        return AsciiStr(replaced_str)


def split_and_strip(string: str, separator: str) -> list[str]:
    split_string = string.split(separator)
    # strip every string in the list    
    split_string = [s.strip() for s in split_string]
    return split_string


def convert_to_capitalize_with_hyphen(word: str) -> str:
    # replace multiple spaces with single space
    word = re.sub(r"\s+", " ", word)
    # strip leading and trailing spaces
    word = word.strip()
    # capitalize first letter
    word = word.capitalize()
    # replace space with hyphen
    word = word.replace(" ", "-")
    return word
    

def convert_to_pinyin(s: str) -> str:
    """
    Convert a Chinese string to Pinyin.

    Parameters
    ----------
    s : str
        The input string.

    Returns
    -------
    str
        The converted Pinyin string.
        
    Examples
    --------
    >>> convert_to_pinyin("青蒿")
    'qīng hāo'
    """
    return ' '.join([i[0] for i in pinyin(s)])


def split_sentence_by_words(sentence: str, split_words: list[str], keep_sep: bool = False) -> list[str]:
    """
    Split a sentence by multiple words.

    Parameters
    ----------
    sentence : str
        The input sentence to be split.
    split_words : list[str]
        A list of words used to split the sentence.
    keep_sep : bool, optional, default=False
        If True, the returned list will include the split words.

    Returns
    -------
    list[str]
        A list of split items, including split words if keep_sep is True.

    Examples
    --------
    >>> split_sentence_by_words("a and b or c", [' and ', ' or '])
    ['a', 'b', 'c']
    >>> split_sentence_by_words("a and b or c", [' and ', ' or '], keep_sep=True)
    ['a', 'and', 'b', 'or', 'c']
    """
    if keep_sep:
        '''
        `(?P<{sep}>{sep})` is a syntax for a named capture group in regular expressions. In this case, we use a named capture group to create a group for each separator word. Let me break down the parts of this expression:

        - `?P<>`: This is the syntax for a named capture group, which allows you to assign a name to the captured group. For example, `(?P<group_name>pattern)`.
        - `{sep}`: This is a Python string formatting placeholder. Here, we replace this placeholder with the value of the `sep` variable.
        - `(?P<{sep}>{sep})`: Ultimately, this expression will create a named capture group whose name and content are both the value of the `sep` variable.

        For example, if `sep` is `'and'`, then `(?P<{sep}>{sep})` would be replaced by `(?P<and>and)`. In the `split_sentence_by_words` function, we use this named capture group syntax to create a group for each word in the `split_words` list. This way, when using the `re.split()` function, we can retain these separators (if `keep_sep=True`) as they have been captured in the named groups.
        '''
        pattern = "|".join(f"(?P<{sep.strip()}>{sep})" for sep in split_words)
        
        split_result = re.split(pattern, sentence)
        result = [part for part in split_result if part]
        result = [part.strip() for part in result]
    else:
        # Combine the split_words with '|' to create a regex pattern
        pattern = '|'.join(split_words)

        # Use re.split to split the sentence
        result = re.split(pattern, sentence)

        # Strip any extra whitespace
        result = [item.strip() for item in result]

    return result


# Helper: Mappping

class Mapping:
    def __init__(self, mapping: list[tuple[str, str]], ignore_case: bool = False):
        self.mapping = []
        if isinstance(mapping, list):
            for item in mapping:
                if isinstance(item, tuple):
                    if len(item) == 2:
                        key = item[0].strip()
                        value = item[1].strip()
                        if ignore_case:
                            key = key.lower()
                            value = value.lower()
                        if key and value:
                            self.mapping.append((key, value))
                        else:
                            raise ValueError(_("Mapping item cannot be empty."))
                    else:
                        raise ValueError(_("Mapping item must have 2 elements."))
                else:
                    raise ValueError(_("Mapping item must be a tuple."))
        else:
            raise ValueError(_("Mapping must be a list."))
        self._remove_duplicate_mapping() # note: this will sort the mapping
        self.mapping_type = self.verify_mapping_type()

    
    def _remove_duplicate_mapping(self):
        """
        Remove duplicate mappings.
        """
        self.mapping = sorted(set(self.mapping))
        return self
    

    def verify_mapping_type(self) -> str:
        """
        The function will return the type of the mapping.

        There are 5 types of mappings:
        1. nn: none-to-none (empty mapping)
        2. oo: one-to-one
        3. mo: multi-to-one
        4. om: one-to-multi
        5. mm: multi-to-multi    
        
        Return
        ------
        str
            The type of the mapping.
        
        Examples
        --------
        >>> mapping = []
        >>> Mapping(mapping).mapping_type
        'nn'
        >>> mapping = [("appla", "apple"), ("carr", "car")]
        >>> Mapping(mapping).mapping_type
        oo
        >>> mapping = [("appla", "apple"), ("carr", "car"), ("appli", "apple")]
        >>> Mapping(mapping).mapping_type
        mo
        >>> mapping = [("appla", "apple"), ("carr", "car"), ("appla", "appli")]
        >>> Mapping(mapping).mapping_type
        om
        >>> mapping = [("appla", "apple"), ("carr", "car"), ("appli", "apple"), ("appla", "appli")]
        >>> Mapping(mapping).mapping_type
        mm
        """
        if len(self.mapping) == 0:
            return 'nn' 
        
        keys_to_values = defaultdict(set)
        values_to_keys = defaultdict(set)
        
        for key, value in self.mapping:
            keys_to_values[key].add(value)
            values_to_keys[value].add(key)
        
        if all(len(values) == 1 for values in keys_to_values.values()) and all(len(keys) == 1 for keys in values_to_keys.values()):
            return 'oo'
        elif any(len(values) > 1 for values in keys_to_values.values()) and all(len(keys) == 1 for keys in values_to_keys.values()):
            return 'om'
        elif all(len(values) == 1 for values in keys_to_values.values()) and any(len(keys) > 1 for keys in values_to_keys.values()):
            return 'mo'
        else:
            return 'mm'


    def get_forward_mapping(self) -> dict[str, str]:
        '''
        If the mapping is in the types of 'oo' or 'mo', the function will convert the mapping to a dictionary.
        '''
        if self.mapping_type in ['oo', 'mo', 'nn']:
            dict_mapping = dict(self.mapping)
        else:
            raise ValueError(_("The mapping is not in the types of one-to-one or multi-to-one."))
        return dict_mapping

    
    def get_backward_mapping(self) -> dict[str, str]:
        if self.mapping_type in ['oo', 'om', 'nn']:
            dict_mapping = dict([(value, key) for key, value in self.mapping])
        else:
            raise ValueError(_("The mapping is not in the types of one-to-one or one-to-multi."))
        return dict_mapping
    

    def get_multi_to_one_mappings(self):
        """
        Return a list of multi-to-one mappings.

        Return
        ------
        list[tuple[str, str]]
            A list of tuples containing the keys and values for multi-to-one mappings.
        
        Example
        -------
        >>> mapping = [("appla", "apple"), ("carr", "car"), ("appli", "apple")]
        >>> get_multi_to_one_mappings(mapping)
        [('appla', 'apple'), ('appli', 'apple')]
        """
        if self.mapping_type == 'mo':
            values_to_keys = defaultdict(set)
            for key, value in self.mapping:
                values_to_keys[value].add(key)
        else:
            raise ValueError(_("The mapping is not in the type of multi-to-one."))
        
        multi_to_one_mappings = []
        for value, keys in values_to_keys.items():
            if len(keys) > 1:
                for key in sorted(keys):
                    multi_to_one_mappings.append((key, value))
        self.multi_to_one_mappings = multi_to_one_mappings
        return self

            
    def report_multi_to_one_mappings(self) -> None:
        """
        Report multi-to-one mappings to the user and ask which one to keep.

        Example
        -------
        >>> multi_to_one_mappings = [('appla', 'apple'), ('appli', 'apple')]
        >>> report_multi_to_one_mappings(multi_to_one_mappings)
        The following multi-to-one mappings were found:
        appla -> apple
        appli -> apple
        Please choose which mappings to keep.
        """
        message = "The following multi-to-one mappings were found:\n"
        for nonstd_str, std_str in self.multi_to_one_mappings:
            message += f"{nonstd_str} -> {std_str}\n"
        message += "Please choose which mappings to keep."
        print(message)


## NMMSN #######################################################################

# Helper: Species origin

def detect_species_inclusion(species_list: list[str]) -> tuple[bool, list[str]]:
    """
    Detect species inclusion in a list of species and return a list without overlap inclusion.

    Parameters
    ----------
    species_list : list[str]
        A list of species.

    Returns
    -------
    tuple[bool, list[str]]
        A tuple containing a boolean value indicating whether any inclusion was detected and
        a list of species with the highest level (no overlap).

    Example
    -------
    >>> species = ["Prinsepia uniflora", "Prinsepia uniflora var. serrata"]
    >>> result = detect_species_inclusion(species)
    >>> print(result)
    (True, ['Prinsepia uniflora'])
    """
    # strip every species in the list
    species_list = [species.strip() for species in species_list]
    # replace consecutive spaces with a single space
    species_list = [re.sub(r'\s+', ' ', species) for species in species_list] # \s+ matches one or more whitespace characters
    species_list = sorted(species_list, key=len) # Sort by length, shortest first
    highest_level_species = []
    inclusion_detected = False

    for species in species_list:
        # ignore upper/lower case
        if not any(species.lower().startswith(higher_species.lower()) for higher_species in highest_level_species):
            highest_level_species.append(species)
        else:
            inclusion_detected = True
    
    # sort the highest_level_species by alphabetical order, a -> z
    highest_level_species = sorted(highest_level_species)

    return inclusion_detected, highest_level_species


# Helper: Error

def formulate_error_msg(pipe_name: str, status: str, reason: str) -> str:
    '''
    Notes
    -----
    Please do not use ending punctuation in the pipe_name and status.
    '''
    
    AVAIL_STATUS = ['failed', 'warning']
    # check if status is valid
    if status not in AVAIL_STATUS:
        raise ValueError(_('Invalid status.'))
    
    return f'Pipe: {pipe_name}. Status: {status}. Reason: {reason}'


def concat_error_msg(prev_error_msg: str, error_msg: str) -> str:
    '''
    Concatenate the previous error message with the current error message.
    '''
    
    # an additional strip() is added to remove the leading space if prev_error_msg is empty
    return f'{prev_error_msg}\n{error_msg}'.strip()


def internationalize_error_msg(error_msg: str) -> EnZh:
    '''
    The format of error_msg is:
    ```
    A error message.
    Pipe: xxx. Status: xxx. Reason: abc.
    B error message.
    Pipe: xxx. Status: xxx. Reason: bcd.
    Pipe: xxx. Status: xxx. Reason: def.
    ```
    Each line is a single error message. 
    If the line starts with `Pipe:`, then we should translate its `Reason:`.
    If its a unstructured error message, then we should translate it directly.
    ```
    A error message.
    abc.
    B error message.
    bcd.
    def.
    ```
    '''
    # Forcing the translation to be zh
    _ = get_translation('zh')
    
    error_list = [i.strip() for i in error_msg.split('\n') if i.strip()]
    new_error_list = []
    for i in error_list:
        if i.startswith('Pipe:'):
            new_error_list.append(re.sub(r'^Pipe:.*Reason: ', '', i))
        else:
            new_error_list.append(i)
        
    # Translate the error messages
    error_msg_en_list = []
    error_msg_zh_list = []
    for i in new_error_list:
        error_msg_en_list.append(i)
        error_msg_zh_list.append(_(i))
        
        
    error_msg_en_zh = EnZh(
        en='\n'.join(error_msg_en_list),
        zh='\n'.join(error_msg_zh_list),
    )
    return error_msg_en_zh


# Helper: NmmsnNeData

class NmmsnNeData:
    '''
    2 conditions:
    1. The input data is empty. E.g., `[]`
    2. The input data is a list of list, str, list, .... E.g., `[['a', 'b'], 'and', ['d', 'e']]`
    '''
    AVAIL_LOGIC_OPERATOR = ['or', 'and']

    def __init__(self, nmmsn_ne_list: NmmsnNeList):
        self.nmmsn_ne_list = nmmsn_ne_list
        self.clean_nmmsn_ne_list() # clean + validate
    
        
    def __str__(self):
        '''
        Returns a string representation of the NmmsnNeData object.

        Examples
        --------
        >>> nmmsn_ne_list = [['a', 'b B'], 'and', ['d', 'e']]
        >>> nmmsn_ne_data = NmmsnNeData(nmmsn_ne_list)
        >>> print(nmmsn_ne_data)
        a | b B and d | e

        Returns
        -------
        str
            A string representation of the NmmsnNeData object.
        '''
        string = ''
        for i in self.nmmsn_ne_list:
            if isinstance(i, list):
                string += ' | '.join(i)
            else:
                string += f' {i} '
        # remove extra spaces
        string = re.sub(r'\s+', ' ', string).strip()
        return string
    
    
    @classmethod
    def init_from_str(cls, nmmsn_ne_str: str):
        '''
        Initialize a NmmsnNeData object from a string.
        
        Examples
        --------
        >>> nmmsn_ne_str = 'a | b B and d | e'
        >>> nmmsn_ne_data = NmmsnNeData.init_from_str(nmmsn_ne_str)
        >>> nmmsn_ne_data.nmmsn_ne_list
        [['a', 'b B'], 'and', ['d', 'e']]
        '''
        # step 1: split the string by 'and' and 'or'
        if nmmsn_ne_str.strip() == '':
            return cls([])
        nmmsn_ne_str = f' {nmmsn_ne_str} '
        logic_operators_with_space = [f' {i} ' for i in cls.AVAIL_LOGIC_OPERATOR]
        nmmsn_ne_list = split_sentence_by_words(nmmsn_ne_str, logic_operators_with_space, keep_sep=True)
        nmmsn_ne_list_2 = []
        # step 2: split the string by '|' and strip
        for i in range(len(nmmsn_ne_list)):
            if '|' in nmmsn_ne_list[i]:
                nmmsn_ne_list_2.append(nmmsn_ne_list[i].split('|'))
            else:
                nmmsn_ne_list_2.append(nmmsn_ne_list[i])
        # step 3: convert to NmmsnNeData object
        return cls(nmmsn_ne_list_2)
    
    
    def clean_nmmsn_ne_list(self):
        '''
        For the input data, the following cleaning operations are performed:
        1. strip and remove empty elements
        2. validate the data type and structure
        '''
        if not isinstance(self.nmmsn_ne_list, list):
            raise ValueError(_("The type of the input data is not list."))

        new_nmmsn_ne_list = []
        for i in self.nmmsn_ne_list:
            if isinstance(i, list):
                temp = []
                if len(i) == 2:
                    for j in i:
                        j = j.strip()
                        temp.append(j)
                    # if any element in the list is empty, remove the whole list
                    if not any(j == '' for j in temp): # if there is no empty element in the list
                        new_nmmsn_ne_list.append(temp)
                else:
                    raise ValueError(_("The length of the inner list is not 2."))
            elif isinstance(i, str):
                temp = i.strip().lower() # convert to lower case
                if temp != '' and temp in self.AVAIL_LOGIC_OPERATOR:
                    new_nmmsn_ne_list.append(temp)
                else:
                    raise ValueError(_("The str in the input data is empty or not in the available logic operator list."))
            else:
                raise ValueError(_("The type of the item in the input data is not list or str."))
        
        self.nmmsn_ne_list = new_nmmsn_ne_list
        
        # Till this step, the input data is assured to be list[list[str] | str]
        self.validate_str_pair_logic_operator_pattern()
        return self
    
    
    # Validations
    '''
    Input validation for NMMSN constructor.
    
    This class allow the user to validate the input data in different ways in pipeline.

    Input data format:
    ```
    [['spe_ori_1', 'spe_ori_1_zh'], 'or', ['spe_ori_2', 'spe_ori_2_zh'], 'and', ...]
    [['med_par_1', 'med_par_1_zh'], 'or', ['med_par_2', 'med_par_2_zh'], 'and', ...]
    [['spe_des_1', 'spe_des_1_zh'], 'or', ['spe_des_2', 'spe_des_2_zh'], 'and', ...]
    [['pro_met_1', 'pro_met_1_zh'], 'or', ['pro_met_2', 'pro_met_2_zh'], 'and', ...]
    ```
    
    There are 2 types in the input data:
    - [str, str]: str_pair.
    - str: logic_operator. It can only be "or" or "and".
    '''    
    def validate_str_pair_logic_operator_pattern(self):
        '''
        For the input list, it item pattern should be:
        1. The first and the last item could not be logic_operator.
        2. The len of the list should be odd.
        3. str_pair, logic_operator, str_pair, logic_operator, ...
        
        Notes
        -----
        Through the `clean_nmmsn_ne_list` of NmmsnNeData (without validation), the input data is already validated to be a list, in which the inner data type is either str or list[str, str]. So, in this validation, we focus on the pattern of the list.
        '''
        if len(self.nmmsn_ne_list) > 0: # Thus, the empty list will always pass this validation.

            # 1. check if the first and the last item is logic_operator
            if isinstance(self.nmmsn_ne_list[0], str) or isinstance(self.nmmsn_ne_list[-1], str):
                raise ValueError(_("The first and the last item could not be logic_operator."))
                
            # 2. check if the len of the list is odd
            if len(self.nmmsn_ne_list) % 2 == 0:
                raise ValueError(_("The length of the list should be odd."))
        
            # 3. check if the input data pattern is str_pair, logic_operator, str_pair, logic_operator, ...
            psudo_input_data = self.nmmsn_ne_list + ['']
            for i in range(0, len(psudo_input_data), 2):
                if not isinstance(psudo_input_data[i], list) or not isinstance(psudo_input_data[i+1], str):
                    raise ValueError(_("The input data pattern is not str_pair, logic_operator, str_pair, logic_operator, str_pair, ..."))
        return self
    
    
    def validate_empty(self):
        '''
        Validate if the input data is empty.
        '''
        if not self.nmmsn_ne_list:
            raise ValueError(_("The nmmsn_ne_list is empty."))
        return self
    
    
    def validate_only_and_or_only_or(self):
        and_detected = False
        or_detected = False
        for i in self.nmmsn_ne_list:
            if i == 'and':
                and_detected = True
            elif i == 'or':
                or_detected = True
            if and_detected and or_detected:
                raise ValueError(_("There are both \"and\" and \"or\" logic operators in the input data, only one of them is allowed."))
        return self
    
    
    def validate_oo_mapping_type(self):
        ne_map_pairs = self.extract_map_pairs()
        # if the ne_map_pairs is not empty, check if the mapping type is one-to-one
        if ne_map_pairs:
            if not Mapping(ne_map_pairs).verify_mapping_type() == 'oo':
                raise ValueError(_("The mapping type is not one-to-one."))
        return self


    # Helper methods
    def convert_inner_list_to_tuple(self) -> list[tuple[str, str] | str]:
        '''
        Convert the inner list to tuple.
        
        Examples
        --------
        >>> lst = [['a', '甲], 'or', ['b', '乙'], 'and', ['c', '丙']]
        >>> print(NmmsnNeData(lst).convert_inner_list_to_tuple())
        [('a', '甲), 'or', ('b', '乙'), 'and', ('c', '丙')]
        '''
        new_nmmsn_ne_list = []
        for i in self.nmmsn_ne_list:
            if isinstance(i, list):
                new_nmmsn_ne_list.append(tuple(i))
            elif isinstance(i, str):
                new_nmmsn_ne_list.append(i)
            else:
                raise ValueError(_("The type of the input data is not list or str."))
        return new_nmmsn_ne_list
    
    
    def convert_inner_tuple_to_list(self, nmmne_list: list[tuple[str, str] | str]) -> NmmsnNeList:
        '''
        Convert the inner tuple to list.
        '''
        new_nmmsn_ne_list = []
        for i in nmmne_list:
            if isinstance(i, tuple):
                new_nmmsn_ne_list.append(list(i))
            elif isinstance(i, str):
                new_nmmsn_ne_list.append(i)
            else:
                raise ValueError(_("The type of the input data is not tuple or str."))
        return new_nmmsn_ne_list    
    
    
    def convert_nmmsn_ne_list_to_lower_case(self) -> 'NmmsnNeData':
        '''
        Convert the input data to lower case.
        '''
        new_nmmsn_ne_list = []
        for i in self.nmmsn_ne_list:
            if isinstance(i, list):
                new_nmmsn_ne_list.append([j.lower() for j in i])
            elif isinstance(i, str):
                new_nmmsn_ne_list.append(i.lower())
            else:
                raise ValueError(_("The type of the input data is not list or str."))
        self.nmmsn_ne_list = new_nmmsn_ne_list
        return self
    
    
    def logic_order(self, based_on_str_pair_index: int = 0, exclude_and: bool = False):
        """
        Sort self.nmmsn_ne_list with string pairs and logical operators.

        The function first splits the list into groups based on the 'or' operator. 
        Then, it sorts each group that is connected by 'and' operator. 
        After that, it sorts the groups and connects them back with 'or'.
        
        This function will also remove duplicate string pairs based on the logic automatically.
        
        Parameters
        ----------
        based_on_str_pair_index : int, optional
            The index of the string pair that the sorting is based on. The default is 0 (the first string pair).
        exclude_and : bool, optional
            If True, the function will ignore the 'and' operator and only sort the string pairs based on the "or" operator. The default is False.
        
        Examples
        --------
        >>> lst = [['str_c', 'str_C'], 'and', ['str_b', 'str_B'], 'or', ['str_f', 'str_F'], 'and', ['str_d', 'str_D'], 'and', ['str_e', 'str_E'], 'or', ['str_a', 'str_A']]
        >>> print(NmmsnNeData(lst).logic_order())
        [['str_a', 'str_A'], 'or', ['str_b', 'str_B'], 'and', ['str_c', 'str_C'], 'or', ['str_d', 'str_D'], 'and', ['str_e', 'str_E'], 'and', ['str_f', 'str_F']]
        >>> lst = [['b', '乙'], 'and', ['a', '甲'], 'or', ['a', '甲']]
        >>> print(NmmsnNeData(lst).logic_order(exclude_and=True)
        [['a', '甲'], 'or', ['b', '乙'], 'and', ['a', '甲']]
        """
        
        # if the input data is empty, return the object itself
        if not self.nmmsn_ne_list:
            return self
        
        tuple_lst = self.convert_inner_list_to_tuple()
        
        # Split the list into groups based on the 'or' operator
        groups: list[list[tuple[str, str]]] = []
        group: list[tuple[str, str]] = []
        for item in tuple_lst:
            if item == 'or':
                groups.append(group)
                group = []
            elif item == 'and':
                pass # Ignore "and" operator. Thus, in groups, there will be no both "and" and "or logic operators.
            elif isinstance(item, tuple):
                group.append(item)
            else:
                raise ValueError(_("The type of the item in the input data is not tuple or str."))
        groups.append(group)
        
        new_groups: list[list[tuple[str, str]]] = []
        if exclude_and:
            new_groups = groups
        else:
            # Sort each group that is connected by 'and' operator
            for group in groups:
                group = list(set(group)) # remove duplicates ("and" level)
                group.sort(key=lambda x: x[based_on_str_pair_index])
                new_groups.append(group)
        
        # remove duplicates in new_groups ("or" level)
        new_groups_tuple = [tuple(i) for i in new_groups]
        new_groups = [list(x) for x in set(new_groups_tuple)]
        
        # sort the groups based on the first string pair
        new_groups.sort(key=lambda x: x[0][based_on_str_pair_index])
        
        # add 'and' operator back
        new_groups_with_and: list[list[tuple[str, str] | str]] = []
        for group in new_groups:
            new_group: list[tuple[str, str] | str] = []
            for sub_group in group:
                new_group.append(sub_group)
                new_group.append('and')
            new_group.pop()
            new_groups_with_and.append(new_group)
        
        # add 'or' operator back
        sorted_lst: list[tuple[str, str] | str] = []
        for group_with_and in new_groups_with_and:
            sorted_lst.extend(group_with_and)
            sorted_lst.append('or')
        
        # Remove the last 'or'
        sorted_lst.pop()
        
        self.nmmsn_ne_list = self.convert_inner_tuple_to_list(sorted_lst)
        
        return self

    
    def stringify(
        self,
        with_capital: bool = False,
        with_hyphen: bool = False,
        reverse_second_str: bool = False,
    ) -> tuple[str, str]:
        '''
        Convert the nmmsn_ne_list to two strings.
        
        Examples
        --------
        >>> lst = [['str_c', 'str_C'], 'and', ['str_b', 'str_B'], 'or', ['str_f', 'str_F'], 'and', ['str_d', 'str_D'], 'and', ['str_e', 'str_E'], 'or', ['str_a', 'str_A']]
        >>> str_1, str_2 = NmmsnNeList(lst).stringify()
        >>> print(str_1)
        str_c and str_b or str_f and str_d and str_e or str_a
        >>> print(str_2)
        str_C and str_B or str_F and str_D and str_E or str_A
        '''
        list_str_1: list[str] = []
        list_str_2: list[str] = []
        
        def process_str(str: str) -> str:
            # remove multiple spaces
            str = re.sub(r'\s+', ' ', str)
            # strip leading and trailing spaces
            str = str.strip()
            if with_capital:
                str = str.capitalize()
            if with_hyphen:
                str = str.replace(' ', '-')
            return str
        
        for x in self.nmmsn_ne_list:
            if isinstance(x, list):
                list_str_1.append(process_str(x[0]))
                list_str_2.append(process_str(x[1]))
            else:
                list_str_1.append(x)
                list_str_2.append(x)
        
        str_1 = ' '.join(list_str_1)
        str_2 = ' '.join(list_str_2)
        
        if reverse_second_str:
            str_2 = ' '.join(list_str_2[::-1])
        
        return str_1, str_2
    
    
    def stringify_en_zh(
        self,
        reverse_zh_str: bool = False,
        remove_zh_and: bool = False,
    ) -> tuple[str, str]:
        '''
        Convert the nmmsn_ne_list to two strings, with English and Chinese.
        
        Examples
        --------
        >>> lst = [['a', '甲], 'or', ['b c', '乙 丙'], 'and', ['d', '丁'], 'or', ['e', '戊'], 'and', ['f', '己']]
        >>> str_en, str_zh = NmmsnNeList(lst).stringify_en_zh()
        >>> print(str_en)
        A or B-c and D or E and F
        >>> print(str_zh)
        甲或乙-丙与丁或戊与己
        '''
        str_en, str_zh = self.stringify(
            with_capital=True, 
            with_hyphen=True,
            reverse_second_str=reverse_zh_str,
        )
        
        str_en = AsciiStr(str_en).replace_non_alphabet_and_hyphen_and_space().str
        
        
        # Process str_en
        # replace 'and' and 'or' with Chinese '与' and '或' in str_zh
        if remove_zh_and:
            str_zh = str_zh.replace(' and ', '')
        else:
            str_zh = str_zh.replace(' and ', '与')
        
        str_zh = str_zh.replace(' or ', '或')
        
        str_zh = AsciiStr(str_zh).replace_non_alphabet_and_hyphen_and_space().remove_space().str
        
        
        return str_en, str_zh
    
    
    def extract_map_pairs(self) -> list[tuple[str, str]]:
        '''
        Extract the mapping pairs from the nmmsn_ne_list.
        
        Examples
        --------
        >>> lst = [['a', '甲], 'or', ['b c', '乙 丙'], 'and', ['d', '丁'], 'or', ['e', '戊'], 'and', ['f', '己']]
        >>> NmmsnNeList(lst).extract_map_pairs()
        [['a', '甲], ['b c', '乙 丙'], ['d', '丁'], ['e', '戊'], ['f', '己']]
        '''
        map_pairs = []
        for i in self.nmmsn_ne_list:
            if isinstance(i, list):
                map_pairs.append(tuple(i))
        # remove duplicates
        if len(map_pairs) > 0:
            map_pairs = Mapping(map_pairs).mapping
        return map_pairs
    
    
    def extract_first_logical_operator(self) -> str:
        '''
        Extract the first logical operator from the nmmsn_ne_list.
        
        Examples
        --------
        >>> lst = [['a', '甲], 'or', ['b c', '乙 丙'], 'and', ['d', '丁'], 'or', ['e', '戊'], 'and', ['f', '己']]
        >>> NmmsnNeList(lst).extract_first_logical_operator()
        'or'
        '''
        first_logical_operator = ''
        for i in self.nmmsn_ne_list:
            if isinstance(i, str):
                first_logical_operator = i
                break
        return first_logical_operator
    
    
    def extract_logical_operators(self) -> set[str]:
        '''
        Extract the logical operators from the nmmsn_ne_list.
        
        Examples
        --------
        >>> lst = [['a', '甲], 'or', ['b c', '乙 丙'], 'and', ['d', '丁'], 'or', ['e', '戊'], 'and', ['f', '己']]
        >>> NmmsnNeList(lst).extract_logical_operators()
        {'and', 'or'}
        '''
        logical_operators = set()
        for i in self.nmmsn_ne_list:
            if isinstance(i, str):
                logical_operators.add(i)
        return logical_operators
    
    
    def convert_to_nmmsn_ne_mono(self) -> tuple[list[str], list[str]]:
        list_1 = []
        list_2 = []
        for i in self.nmmsn_ne_list:
            if isinstance(i, list):
                list_1.append(i[0])
                list_2.append(i[1])
            else:
                list_1.append(i)
                list_2.append(i)
        return list_1, list_2


### NMMSN Constructor ##########################################################

def construct_nmmsn_spe_ori(
    spe_ori_input: NmmsnNeList,
) -> tuple[str, str, str, NmmsnNeList]:
    """
    The function constructs the Latin and Chinese name elements of species origins for the NMMSN system. 

    Parameters
    ----------
    spe_ori_input : NmmsnNeList
        A list containing multiple species names and logical operators.
    failed_construct_token : str, optional
        The token to return if the function fails. Default is `Default.FAILED_CONSTRUCT_TOKEN`.

    Returns
    -------
    tuple[str, str, str, NmmsnNeList]
        The tuple contains 4 elements:
        1. The constructed Latin name element of species origins.
        2. The constructed Chinese name element of species origins.
        3. Error message if the function fails, otherwise an empty string.
        4. Reordered spe_ori_input (remove duplicates, etc.)

    Examples
    --------
    >>> spe_ori_input = [['Ephedra sinica', '草麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra equisetina', '木贼麻黄']]
    >>> construct_nmmsn_spe_ori(spe_ori_input)
    ('Ephedra equisetina vel intermedia vel sinica', '木贼麻黄或中麻黄或草麻黄', '', [['Ephedra equisetina', '木贼麻黄'], 'or', ['Ephedra intermedia', '中麻黄'], 'or', ['Ephedra sinica', '草麻黄']])
    >>> spe_ori_input = [['Ephedra sinica', '草麻黄'], 'and', ['Ephedra intermedia', '中麻黄'], 'and', ['Ephedra equisetina', '木贼麻黄']]
    >>> construct_nmmsn_spe_ori(spe_ori_input)
    ('Ephedra equisetina et intermedia et sinica', '木贼麻黄或中麻黄或草麻黄', '', [['Ephedra equisetina', '木贼麻黄'], 'and', ['Ephedra intermedia', '中麻黄'], 'and', ['Ephedra sinica', '草麻黄']])
    """
    error_msg = ''
    
    spe_ori_ne_data = NmmsnNeData(spe_ori_input)
    spe_ori_ne_data.validate_empty().validate_only_and_or_only_or().validate_oo_mapping_type()
    spe_ori_ne_data.logic_order() # This process will also remove duplicates.
    
    spe_ori_logic = spe_ori_ne_data.extract_first_logical_operator()
    spe_ori_la_zh_map_pairs = spe_ori_ne_data.extract_map_pairs()
    
    spe_ori_la_zh_mapping = dict(spe_ori_la_zh_map_pairs)
    
    species_list = [i[0] for i in spe_ori_la_zh_map_pairs]
    
    # check the species inclusion
    inclusion_detected, highest_level_species = detect_species_inclusion(species_list)
    if inclusion_detected:
        # included_species = set(species_list) - set(highest_level_species)
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_spe_ori',
            'warning', 
            _("Species inclusion detected.")
        ))    
    
    if len(highest_level_species) > 1:
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_spe_ori',
            'warning', 
            _("Multiple species origins detected.")
        ))
    
    
    # latin
    result = []
    match spe_ori_logic:
        case 'and':
            la_logic = 'et'
            zh_logic = '与'
        case 'or':
            la_logic = 'vel'
            zh_logic = '或'
        case _: # when no logical operator is found, use ''
            la_logic = ''
            zh_logic = ''

    prev_genus = None
    for species in highest_level_species:
        genus, *rest = species.split()
        species_name = " ".join(rest)

        if genus == prev_genus:
            result.append(f"{la_logic} " + species_name)
        else:
            if prev_genus:
                result.append(la_logic)
            result.append(species)
        
        prev_genus = genus
    
    spe_ori_la = " ".join(result)
    spe_ori_la = AsciiStr(spe_ori_la).replace_non_alphabet_and_hyphen_and_space().str
    
    # chinese
    result_zh = [spe_ori_la_zh_mapping[species] for species in highest_level_species]
    spe_ori_zh = zh_logic.join(result_zh)
    spe_ori_zh = AsciiStr(spe_ori_zh).replace_non_alphabet_and_hyphen_and_space().remove_space().str
    
    
    # restore spe_ori_ne_list_ordered for further return. Insert the logical operator back to highest_level_species.
    spe_ori_ne_ordered = []
    for x in highest_level_species:
        spe_ori_ne_ordered.append([
            x, 
            AsciiStr(spe_ori_la_zh_mapping[x]).remove_space().str
        ])
        spe_ori_ne_ordered.append(spe_ori_logic)
    # remove the last logical operator
    spe_ori_ne_ordered.pop()
        
    return spe_ori_la, spe_ori_zh, error_msg, spe_ori_ne_ordered


def construct_nmmsn_med_par(
    med_par_input: NmmsnNeList,
) -> tuple[str, str, str, NmmsnNeList]:
    """
    Construct the English and Chinese name elements of medicinal parts for the NMMSN system.

    Parameters
    ----------
    med_par_input : NmmsnNeList
        A list containing the medicinal parts and logical operators.
    failed_construct_token : str, optional
        The token to return if the function fails. Default is `Default.FAILED_CONSTRUCT_TOKEN`.

    Returns
    -------
    tuple[str, str, str, NmmsnNeList]

    Examples
    --------
    >>> med_par_input = [['根', 'Root'], 'and', ['根茎', 'Rhizome'], 'or', ['叶', 'Leaf'], 'or', ['草质茎', 'Herbaceous stem']]
    >>> construct_nmmsn_med_par(med_par_input)
    ('Herbaceous-stem or Leaf or Rhizome and Root', '草质茎或叶或根茎与根', '', [['草质茎', 'Herbaceous stem'], 'or', ['叶', 'Leaf'], 'or', ['根茎', 'Rhizome'], 'and', ['根', 'Root']])
    """
    error_msg = ''
        
    med_par_ne_data = NmmsnNeData(med_par_input)
    med_par_ne_data.validate_empty().validate_oo_mapping_type()
    med_par_ne_data.convert_nmmsn_ne_list_to_lower_case()
    med_par_ne_data.logic_order()

    med_par_en, med_par_zh = med_par_ne_data.stringify_en_zh()
    med_par_ne_ordered = med_par_ne_data.nmmsn_ne_list
    
    if len(med_par_ne_ordered) > 1:
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_med_par',
            'warning', 
            _("Multiple medicinal parts detected.")
        ))
    
    return med_par_en, med_par_zh, error_msg, med_par_ne_ordered


def construct_nmmsn_spe_des(
    spe_des_input: NmmsnNeList,
) -> tuple[str, str, str, NmmsnNeList]:
    
    error_msg = ''
    
    spe_des_ne_data = NmmsnNeData(spe_des_input)
    spe_des_ne_data.validate_oo_mapping_type()
    spe_des_ne_data.convert_nmmsn_ne_list_to_lower_case()
    spe_des_ne_data.logic_order()

    spe_des_en, spe_des_zh = spe_des_ne_data.stringify_en_zh(reverse_zh_str=True)
    spe_des_ne_ordered = spe_des_ne_data.nmmsn_ne_list
    
    if len(spe_des_ne_ordered) > 1:
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_spe_des',
            'warning', 
            _("Multiple special descriptions detected.")
        ))
    
    return spe_des_en, spe_des_zh, error_msg, spe_des_ne_ordered
    

def construct_nmmsn_pro_met(
    pro_met_input: NmmsnNeList,
) -> tuple[str, str, str, NmmsnNeList]:
    error_msg = ''
    
    pro_met_ne_data = NmmsnNeData(pro_met_input)
    pro_met_ne_data.validate_oo_mapping_type()
    pro_met_ne_data.convert_nmmsn_ne_list_to_lower_case()
    pro_met_ne_data.logic_order(exclude_and=True)
    # * No need to order the logical operators in pro_met. Because the order of the logical operators in pro_met is meaningful.
    
    pro_met_en, pro_met_zh = pro_met_ne_data.stringify_en_zh(reverse_zh_str=True, remove_zh_and=True)
    pro_met_ne_ordered = pro_met_ne_data.nmmsn_ne_list
    
    pro_met_en_zh_pairs = pro_met_ne_data.extract_map_pairs()
    pro_met_zh_list = [pair[1] for pair in pro_met_en_zh_pairs]
    
    # if not all zh in pro_met_zh_list end with '制' 
    if not all([zh.endswith('制') for zh in pro_met_zh_list]):
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_pro_met',
            'warning', 
            _("Not all processing methods end with \"制\".")
        ))
    
    pro_met_logic_operators = pro_met_ne_data.extract_logical_operators()
    
    if "or" in pro_met_logic_operators:
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_pro_met',
            'warning', 
            _('Multiple processing methods with "or" logic detected.')
        ))
    
    return pro_met_en, pro_met_zh, error_msg, pro_met_ne_ordered


def construct_nmmsn(nmmsn_ne: NmmsnNameElement) -> SnnmmaOutputSuccess | SnnmmaOutputFail:
    return_fail = SnnmmaOutputFail()
    
    error_msg = ''    
    exception_raised = False
    
    
    # name element: nmm_type
    nmm_type_cls = NmmType(nmmsn_ne.nmm_type)
    if not nmm_type_cls.is_pafa_pro():
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn',
            'warning', 
            _("Invalid NMM type.")
        ))
    if not nmm_type_cls.is_pro():
        try:
            assert len(nmmsn_ne.processing_methods) == 0, _("Processing methods detected in non-processed NMM.")
        except AssertionError as e:
            error_msg = concat_error_msg(error_msg, formulate_error_msg(
                'construct_nmmsn', 'failed', str(e)
            ))
            exception_raised = True
    
    
    # name element: spe_ori
    try:
        spe_ori_la, spe_ori_zh, spe_ori_error_msg, spe_ori_ne_ordered = construct_nmmsn_spe_ori(nmmsn_ne.species_origins)  
        error_msg = concat_error_msg(error_msg, spe_ori_error_msg)
    except Exception as e:
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_spe_ori', 'failed', str(e)
        ))
        exception_raised = True
    
    
    # name element: med_par
    try:
        med_par_en, med_par_zh, med_par_error_msg, med_par_ne_ordered = construct_nmmsn_med_par(nmmsn_ne.medicinal_parts)
        error_msg = concat_error_msg(error_msg, med_par_error_msg)
    except Exception as e:
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_med_par', 'failed', str(e)
        ))
        exception_raised = True
    
    
    # name element: spe_des
    try:
        spe_des_en, spe_des_zh, spe_des_error_msg, spe_des_ne_ordered = construct_nmmsn_spe_des(nmmsn_ne.special_descriptions)
        error_msg = concat_error_msg(error_msg, spe_des_error_msg)
    except Exception as e:
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_spe_des', 'failed', str(e)
        ))
        exception_raised = True
    
    
    # name element: pro_met
    try:
        pro_met_en, pro_met_zh, pro_met_error_msg, pro_met_ne_ordered = construct_nmmsn_pro_met(nmmsn_ne.processing_methods)
        error_msg = concat_error_msg(error_msg, pro_met_error_msg)
    except Exception as e:
        error_msg = concat_error_msg(error_msg, formulate_error_msg(
            'construct_nmmsn_pro_met', 'failed', str(e)
        ))
        exception_raised = True
    
    
    if exception_raised:
        return_fail.error_msg = error_msg
        return_fail.error_msg_en_zh = internationalize_error_msg(error_msg)
        return return_fail
    
                
    nmmsn = f'{spe_ori_la} {med_par_en} {spe_des_en} {pro_met_en}'.strip().replace('  ', ' ') # type: ignore
    nmmsn_zh = f'{pro_met_zh}{spe_des_zh}{spe_ori_zh}{med_par_zh}'.strip() # type: ignore
    
    return_success = SnnmmaOutputSuccess.model_validate(
        {
            "success": True,
            "error_msg": error_msg,
            "error_msg_en_zh": internationalize_error_msg(error_msg),
            "nmmsn": {
                "nmmsn": nmmsn,
                "nmmsn_zh": {
                    "zh": nmmsn_zh,
                    "pinyin": convert_to_pinyin(nmmsn_zh),
                },
                "nmmsn_name_element": {
                    "nmm_type": nmm_type_cls.nmm_type,
                    "species_origins": spe_ori_ne_ordered, # type: ignore
                    "medicinal_parts": med_par_ne_ordered, # type: ignore
                    "special_descriptions": spe_des_ne_ordered, # type: ignore
                    "processing_methods": pro_met_ne_ordered, # type: ignore
                },
                "nmmsn_seq": [[spe_ori_la, spe_ori_zh], [med_par_en, med_par_zh], [spe_des_en, spe_des_zh], [pro_met_en, pro_met_zh]] # type: ignore
            }
        }
    )
    
    return return_success
