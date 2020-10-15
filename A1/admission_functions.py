"""Starter code for Assignment 1 CSC108 Summer 2018"""

SPECIAL_CASE_SCHOOL_1 = 'Fort McMurray Composite High'
SPECIAL_CASE_SCHOOL_2 = 'Father Mercredi High School'
SPECIAL_CASE_YEAR = '2017'

# Add other constants here

DEGREE_LEN = 6
COURSE_LEN = 9

def is_special_case(record: str) -> bool:
    """Return True iff the student should be handled using the special case rules.

    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    True
    >>> is_special_case('Jacqueline Smith,Father Something High School,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    """

    # Complete the body of the function here
    
    case_one = SPECIAL_CASE_SCHOOL_1
    case_two = SPECIAL_CASE_SCHOOL_2
    year = SPECIAL_CASE_YEAR
    #I renamed them to make the code shorter
          
    return ((case_one in record) or (case_two in record)) and (year in record)

# Complete the rest of the functions here

def get_final_mark(record: str, course_mark: str, exam_mark: str) -> float:
    """Return the student's final mark of the course, by calculating the average
    of course_mark and exam_mark in the record. A missing exam mark counts as
    a zero, unless the student is a special case.
    
    >>> get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts', '90', '94')
    92.0
    >>> get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts', '92', 'NE')
    92.0
    >>> get_final_mark('Jacqueline Smith,Fort McDonald Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts', '80', 'NE')
    40.0
    """
    
    if exam_mark == 'NE' and is_special_case(record):
        return float(course_mark)
    elif exam_mark == 'NE' and not is_special_case(record):
        return int(course_mark)/ 2
    else:          
        return (int(course_mark) + int(exam_mark))/ 2

def get_both_marks(course_record: str, course_code: str) -> str:
    """Return a string containing the coursework mark in the course_record if 
    the course_code matches the course_record and the exam mark separated by a
    single space. Otherwise, return the empty string.
    
    >>> get_both_marks('MAT,90,94', 'MAT')
    '90 94'
    >>> get_both_marks('MAT,90,94', 'ACT')
    ''
    >>> get_both_marks('ENG,92,88', 'ENG')
    '92 88'
    """
    
    if course_code in course_record:
        return course_record[4:6] + ' ' + course_record[7:9]
    else:
        return ''
    
    
def extract_course(transcript: str, course_num: int) -> str:
    """Return the coursework mark from the transcript. The course_num represents
    which course to extract. The first course in the transcript being course 1, 
    the second being course 2, etc.
    
    >>> extract_course('MAT,90,94,ENG,92,88,CHM,80,85', 1)
    'MAT,90,94'
    >>> extract_course('MAT,90,94,ENG,92,88,CHM,80,85', 2)
    'ENG,92,88'
    >>> extract_course('MAT,90,94,ENG,92,88,CHM,80,85', 3)
    'CHM,80,85'
    """
    
    return transcript[(course_num - 1)* 10 : (course_num - 1)* 10 + COURSE_LEN]

def applied_to_degree(record: str, degree: str) -> bool:
    """Return True if and only if the student represented by the record
    applied to the degree.
    
    >>> applied_to_degree('Jacqueline Smith,Fort McMurray Composite High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts', 'BArts')
    True
    >>> applied_to_degree('Jacqueline Smith,Fort McMurray BComuter High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BArts', 'BCom')
    False
    >>> applied_to_degree('Jacqueline Smith,Fort McMurray BComuter High,2017,MAT,90,94,ENG,92,88,CHM,80,85,BCom', 'BCom')
    True
    """
    
    return degree in record[-DEGREE_LEN:]

def decide_admission(course_average: float, degree_cutoff: float) -> str:
    """Return 'accept' if the course_average is at least the degree_cutoff but
    below the threshold for a scholarship, 'accept with scholarship' if the 
    course_average is at or above the threshold for a scholarship, and 'reject'
    if the course_average is below the degree_cutoff.
       
    >>> decide_admission(70,80)
    'reject'
    >>> decide_admission(80,80)
    'accept'
    >>> decide_admission(85,80)
    'accept with scholarship'
    """
    
    if course_average < degree_cutoff:
        return 'reject'
    elif course_average >= degree_cutoff + 5:
        return 'accept with scholarship'
    else:
        return 'accept'
    
    
# Programer: SongQi Wang
# Student number: 1003439442
    
        