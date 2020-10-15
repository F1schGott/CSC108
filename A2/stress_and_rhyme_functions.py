"""Functions for annotating poetry."""

# Type shorthands
from typing import List, TextIO
PronouncingTable = List[List[str]]

# The main module - need to import so that window code works correctly
import annotate_poetry

NO_STRESS_SYMBOL = 'x'
PRIMARY_STRESS_SYMBOL = '/'
SECONDARY_STRESS_SYMBOL = '\\'  # note: len('\\') == 1 due to special character

"""
A pronouncing table: a nested list, [list of str, list of list of str]
  o a two item list, contains two parallel lists
  o the first item is a list of words (each item in this sublist is a str
    for which str.isupper() is True)
  o the second item is a list of pronunciations, where a pronunciation is a
    list of phonemes (each item in this sublist is a list of str)
  o the pronunciation for the word at index i in the list of words is at index
    i in the list of pronunciations
"""

# A small pronouncing table that can be used in docstring examples.
SMALL_TABLE = [['A', 'BOX', 'CONSISTENT', 'DON\'T', 'FOX', 'IN', 'SOCKS'],
               [['AH0'],
                ['B', 'AA1', 'K', 'S'],
                ['K', 'AH0', 'N', 'S', 'IH1', 'S', 'T', 'AH0', 'N', 'T'],
                ['D', 'OW1', 'N', 'T'],
                ['F', 'AA1', 'K', 'S'],
                ['IH0', 'N'],
                ['S', 'AA1', 'K', 'S']]]

"""
A pronouncing dictionary is a list of pronouncing lines, where a pronouncing
line is a line in the CMU Pronouncing Dictionary format:
  a word followed by the phonemes describing how to pronounce the word.
  o example:
    BOX  B AA1 K S
"""

# A small pronouncing dictionary that can be used in docstring examples.
SMALL_PRONOUNCING_DICT = [
    'A AH0',
    'BOX B AA1 K S',
    'CONSISTENT K AH0 N S IH1 S T AH0 N T',
    'DON\'T D OW1 N T',
    'FOX F AA1 K S',
    'IN IH0 N',
    'SOCKS S AA1 K S']


# ===================== Provided Helper Functions =============================

def prepare_word(s: str) -> str:
    """Return a new string based on s in which all letters have been converted
    to uppercase and punctuation characters have been stripped from both ends.

    Inner punctuation is left unchanged.

    This function prepares a word for looking up in a pronouncing table.

    >>> prepare_word('Birthday!!!')
    'BIRTHDAY'
    >>> prepare_word('"Quoted?"')
    'QUOTED'
    >>> prepare_word("Don't!")
    "DON'T"
    """

    punctuation = """!"`@$%^&_+-={}|\\/,;:'.-?)([]<>*#\n\t\r"""
    result = s.upper().strip(punctuation)
    return result


def get_rhyme_scheme_letter(offset: int) -> str:
    """Return the letter corresponding to the offset from 'A'.  Helpful when
    labelling a poem with its rhyme scheme.

    Precondition: 0 <= offset <= 25

    >>> get_rhyme_scheme_letter(0)
    'A'
    >>> get_rhyme_scheme_letter(25)
    'Z'
    """

    return chr(ord('A') + offset)


# ======== Students: Add Your Code Below This Line ================


def get_word(pronouncing_line: str) -> str:
    """Return the word in the pronouncing line.
    
    >>>get_word('BOX  B AA1 K S')
    'BOX'
    >>>get_word('DON\'T D OW1 N T')
    'DON\'T'    
    """
    
    return pronouncing_line.split()[0]

def get_pronunciation(pronouncing_line: str) -> List[str]:
    """Return a list containing the pronunciation (list of phonemes) from the
    pronouncing line.
    
    >>>get_pronunciation('BOX  B AA1 K S')
    ['B', 'AA1', 'K', 'S']
    >>>get_pronunciation('DON\'T D OW1 N T')
    ['D', 'OW1', 'N', 'T']
    """
    pronunciation = pronouncing_line.split()
    pronunciation.pop(0)

    return pronunciation
    

def make_pronouncing_table(pronouncing_list: List[str]) -> PronouncingTable:
    """

    NOTE: This is not the first function that you should write, but we included
    the function header and one example for illustrative purposes. You should
    fill in the proper docstring and add another example to this function. You
    should also write other functions.
    
    Return the pronouncing table built from those pronouncing_lists

    >>> SMALL_TABLE == make_pronouncing_table(SMALL_PRONOUNCING_DICT)
    True
    >>> make_pronouncing_table(['IN IH0 N', 'SOCKS S AA1 K S'])
    [['IN', 'SOCKS'], [['IH0', 'N'], ['S', 'AA1', 'K', 'S']]]
    """

    table = []
    pro_list = []
    word_list = []
    
    for pro_line in pronouncing_list:
        word_list.append(get_word(pro_line))
        pro_list.append(get_pronunciation(pro_line))
        
    table.append(word_list)
    table.append(pro_list)
    
    return table
    
def look_up_pronunciation(word: str, ProTab: PronouncingTable) -> List[str]:
    """Return a list containing the pronunciation (list of phonemes) for the
    word in the pronouncing table.
    
    >>>look_up_pronunciation('A', SMALL_TABLE)
    ['AH0']
    >>>look_up_pronunciation('consistent', SMALL_TABLE)
    ['K', 'AH0', 'N', 'S', 'IH1', 'S', 'T', 'AH0', 'N', 'T']
    
    """
    
    word = prepare_word(word)
    word_index = ProTab[0].index(word)
    
    return ProTab[-1][word_index]

def is_vowel_phoneme(phoneme: str) -> bool:
    """Return True if the phoneme is a vowel phoneme.Return False if the
    phoneme is not a vowel phoneme.
        
    >>>is_vowel_phoneme('AH0')
    True
    >>>is_vowel_phoneme('Ah0')
    False
    >>>is_vowel_phoneme('AH4')
    False
    """
    
    if len(phoneme) != 3:
        return False
    else:
        ch1 = phoneme[0] in 'AEIOU'
        ch2 = phoneme[1].isupper()
        ch3 = phoneme[2] in '012'
        return ch1 and ch2 and ch3

def last_syllable(pho_list: List[str]) -> List[str]:
    """Return the last vowel phoneme and any subsequent consonant phoneme(s) 
    from the pho_list.
    
    >>>last_syllable(['S', 'T', 'AH0', 'N', 'T'])
    ['AH0', 'N', 'T']
    >>>last_syllable(['K', 'AH0', 'N', 'S', 'IH1', 'S', 'T'])
    ['IH1', 'S', 'T']
    
    """
    
    i = -1
    while  i > -len(pho_list) and not is_vowel_phoneme(pho_list[i]):
        i = i - 1
    
    if i == -len(pho_list) and not is_vowel_phoneme(pho_list[i]):
        return []
    else:
        return pho_list[i:]

def convert_to_lines(poem: TextIO) -> List[str]:
    """Return a list of lines from the poem with whitespace characters stripped 
    from the beginning and end of each line. Lines can be determined by 
    splitting the poem based on the newline character. Blank lines that appear 
    before the first nonblank line in the poem or after the last nonblank line 
    in the poem are not to be included in the list of lines. Blank lines that 
    separate stanzas in the poem are to be represented by a single empty string
    in the list of lines.
    
    examples: lf lines are look like:
    ' '
    ' '
    'A'
    ' '
    ' '
    'B'
    ' '
    ' '
    should return:
    'A'
    ' '
    'B'    
    """
    
    line_list = []
    poem_lines = poem.readlines()
    
    for l in poem_lines:
        line_list.append(l.strip())
        
    i = 0
    while i < len(line_list) - 1 and len(line_list) > 1:
        if line_list[i] == '' and line_list[i + 1] == '':
            line_list.pop(i)
        else:
            i = i + 1  
      
    if len(line_list) != 0 and line_list[0] == '':
        line_list.pop(0)
    if len(line_list) != 0 and line_list[-1] == '':
        line_list.pop(-1)
    return line_list

def make_lasy_syl_list(line_list: List[str], ProTab: PronouncingTable) -> List[str]:
    """Return the list of the last syllable of the line in line_list.
    
    >>>make_lasy_syl_list(['box', 'fox'], SMALL_TABLE)
    [['AA1', 'K', 'S'], ['AA1', 'K', 'S']]
    >>>make_lasy_syl_list(['IN', 'fox', 'socks', 'a'], SMALL_TABLE)
    [['IH0', 'N'], ['AA1', 'K', 'S'], ['AA1', 'K', 'S'], ['AH0']]       
    """
    #I create this function in oder to make the detect_rhyme_scheme shorter.
    #If I put everything in detect_rhyme_scheme, it will be too long.    
    
    syl_list = []
    for l in line_list:
        if l == '':
            syl_list.append('')
        else:
            word_pros = look_up_pronunciation(l.split()[-1], ProTab)
            syl_list.append(last_syllable(word_pros))
    return syl_list  

def detect_rhyme_scheme(line_list: List[str], ProTab: PronouncingTable) -> List[str]:
    """Return the rhyme scheme for the line_list of the poem.
    
    >>>detect_rhyme_scheme(['box', 'fox'], SMALL_TABLE)
    ['A', 'A']
    >>>detect_rhyme_scheme(['box', 'IN', 'fox', 'socks', 'a'], SMALL_TABLE)
    ['A', 'B', 'A', 'A', 'C']
    """
    syl_list = make_lasy_syl_list(line_list, ProTab)
    rhyme_list = []
    rhyme_scheme = []
    
    for syl in syl_list:
        if syl == '':
            rhyme_scheme.append(' ')
        elif syl not in rhyme_list:
            rhyme_list.append(syl)
            rhyme_scheme.append(rhyme_list.index(syl))
        elif syl in rhyme_list:
            rhyme_scheme.append(rhyme_list.index(syl))    
    for i in range(len(rhyme_scheme)):
        if rhyme_scheme[i] != ' ':            
            rhyme_scheme[i] = get_rhyme_scheme_letter(int(rhyme_scheme[i]))
                
    return rhyme_scheme


def get_stress_pattern(word: str, ProTab: PronouncingTable) -> str:
    """Return the stress pattern for word according to the pronouncing table.

    >>>get_stress_pattern('consistent', SMALL_TABLE)
    'x / x     '
    >>>get_stress_pattern('BOX', SMALL_TABLE)
    '/  '
    >>>get_stress_pattern('A', SMALL_TABLE)
    'x'
    """

    stress_pattern = ''
    pros = look_up_pronunciation(word, ProTab)
    for phoneme in pros:
        if is_vowel_phoneme(phoneme):
            if phoneme[2] == '0':
                stress_pattern = stress_pattern + NO_STRESS_SYMBOL + ' '
            elif phoneme[2] == '1':
                stress_pattern = stress_pattern + PRIMARY_STRESS_SYMBOL + ' '
            elif phoneme[2] == '2':
                stress_pattern = stress_pattern + SECONDARY_STRESS_SYMBOL + ' '
    stress_pattern = stress_pattern[:-1]
    while len(stress_pattern) != len(word):
        stress_pattern = stress_pattern + ' '
    return stress_pattern 

# Your code here


if __name__ == '__main__':

    """Optional: uncomment the lines import doctest and doctest.testmod() to
    have your docstring examples run when you run stress_and_rhyme_functions.py
    NOTE: your docstrings MUST be properly formatted for this to work!
    """
    #import doctest
    #doctest.testmod()
