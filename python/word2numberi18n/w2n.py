# SPDX-FileCopyrightText: 2016 - Akshay Nagpal <akshaynagpal@user.noreplay.github.com>
# SPDX-FileCopyrightText: 2020-2021 - Sebastian Ritter <bastie@users.noreply.github.com>
# SPDX-License-Identifier: MIT

import os
import locale
import codecs
import re

number_system = {}
normalize_data = {}
lang = "en"

#
lang = locale.getlocale()[0]
if "w2n.lang" in os.environ:
    lang = os.environ["w2n.lang"]
if lang is None:
    lang = locale.getdefaultlocale()[0]
if lang is None or lang[0] is None:
    lang = None
    if "LANGUAGE" in os.environ:
        lang = os.environ["LANGUAGE"]
if lang is None:
    lang = "en"  # fallback
lang = lang[:2]

data_file = os.path.dirname(__file__)+os.sep+"data"+os.sep+"number_system_"+lang+".txt"
with codecs.open(data_file, "rU", encoding="utf-8") as number_system_data:
    for line in number_system_data:
        if line.startswith('#'):
            pass
        else:
            (key, val) = line.split("=")
            if key.startswith("replace:"):
                key =key[len("replace:"):]
                normalize_data[key] = val.strip()
            else:
                if "point" != key:
                    val = int(val)
                else:
                    val = val.strip()
                number_system[key] = val

decimal_words = list(number_system.keys())[:10]


def number_formation(number_words):
    """
    function to form numeric multipliers for million, billion, thousand etc.
    
    input: list of strings
    return value: integer
    """
    numbers = []
    for number_word in number_words:
        numbers.append(number_system[number_word])
    if lang == "ru":
        if len(numbers) > 3:
            if numbers[0] < 100:
                numbers[0] = numbers[0] * 100

        if len(numbers) == 4:
            return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
        elif len(numbers) == 3:
            return numbers[0]+numbers[1]+numbers[2]
        elif len(numbers) == 2:
            return numbers[0]+numbers[1]
        else:
            return numbers[0]
    else:
        if len(numbers) == 4:
            return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
        elif len(numbers) == 3:
            return numbers[0] * numbers[1] + numbers[2]
        elif len(numbers) == 2:
            if 100 in numbers:
                return numbers[0] * numbers[1]
            else:
                return numbers[0] + numbers[1]
        else:
            return numbers[0]


def get_decimal_string(decimal_digit_words):
    """
    function to convert post decimal digit words to numerial digits
    it returns a string to prevert from floating point conversation problem
    
    input: list of strings
    output: string
    """
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if(dec_word not in decimal_words):
            return 0
        else:
            decimal_number_str.append(number_system[dec_word])
    final_decimal_string = ''.join(map(str, decimal_number_str))
    return final_decimal_string


def normalize(number_sentence):
    """ function to normalize the whole(!) input text
    note: float or int parameters are allowed 
    
    input: string the fill text
    output: string
    """
    # we need no check for numbers...
    if type(number_sentence) is float:
        return number_sentence
    if type(number_sentence) is int:
        return number_sentence

    # ...but if it is a string we need normalizing
    number_sentence = number_sentence.lower()  # converting input to lowercase
    
    # change in result of externalize localizing information
    #number_sentence = number_sentence.replace('- ', ' ')
    #number_sentence = number_sentence.replace(' -', ' ')
    #number_sentence = number_sentence.removeprefix('-')
    #number_sentence = number_sentence.removesuffix('-')

    # for examples: both is right "vingt et un" and "vingt-et-un"
    # we change this to composed value "vingt-et-un" over the localized data file "replace:" entry
    for non_composed_number_value, composed_number_value in normalize_data.items():
        if non_composed_number_value.count(' ') >1:
            number_sentence = number_sentence.replace(non_composed_number_value, composed_number_value)

    return number_sentence


def check_double_input (new_number, clean_numbers):
    """ internal function to check false redundant input
    note: this method has language configuration dependency
    
    note: call this after lemma text
    
    example: check_double_input (1000, "thousand thousand") with lang="en" throws a ValueError
    example: check_double_input (1000, "thousand thousand") with lang="de" its ok
    example: check_double_input (1000, "tausend tausend") with lang="de" throws a ValueError
    
    input: int new_number, string[] words - looking for count of localized name of new_numerb in words     
    raise: if redundant input error
    """
    # in result of work with numeric values and remove point 
    # we need not longer language specific code
    localized_name = get_name_by_number_value(new_number)
    if clean_numbers.count(localized_name) > 1:
        raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")
        # i18n save für later:
        # de: "Redundantes Nummernwort! Bitte gebe ein zulässiges Nummernwort ein (z.B. zwei Millionen Dreiundzwanzigtausend und Neunundvierzig)"
        # ru: "Избыточное числовое слово! Введите правильное числовое слово (например, два миллиона двадцать три тысячи сорок девять)" 


def get_name_by_number_value (new_number):
    """
    internal function to get the localized name form value
    
    input: numeric value
    output: name from number_system map or None if not found 
    """
    for number_name, number_value in number_system.items():
        if new_number == number_value:
            return number_name
    return None


def get_index_for_number(new_number, clean_numbers):
    """ [internal] function to get the index of name for given number 
        note: call this after lemma text

        input: int number
        output: index or -1 if not found
    
    """
    # in result of get name by numeric value, the localized name came from dictionary
    # and we need no language specific code
    localized_name = get_name_by_number_value(new_number)
    return clean_numbers.index(localized_name) if localized_name in clean_numbers else -1


def get_number_value (clean_numbers):
    """ get the pre-decimal number from clean_number
    
        input: sorted array with number words
        output: int number
        raise: ValueError 
    """
    result = 0

    thousand_index = get_index_for_number(1_000, clean_numbers)
    million_index  = get_index_for_number(1_000_000, clean_numbers)
    billion_index  = get_index_for_number(1_000_000_000, clean_numbers)
    trillion_index = get_index_for_number(1_000_000_000_000, clean_numbers)

    if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or (million_index > -1 and million_index < billion_index):
        raise ValueError("Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    #
    # The simple algorithm based on the idea from NLP to work with tagging (key)words
    # but yes it is handmade implemented today.
    #
    # -- 2021-02-05 --
    # The tagging can be tested on for example https://parts-of-speech.info and tell for
    # nine trillion one billion two million twenty three thousand and forty nine point two three six nine
    # - "and" is a conjunction
    # - "point" is a none
    # - all other are numbers
    # But also contains this line these "measure words" for numbers:
    # - trillion
    # - billion
    # - million
    # - thousand
    # - hundred
    # This new algorithm split the word array from highest value to lowest 
    # (because hundred can be a measure and also a number). Then it work
    # only with number for this measure, simplify so the algorithm and
    # make it free from other measure part in the number.
    # Also it is no different to calculate a trillion or a million or other
    #
    trillion_index = get_index_for_number(1_000_000_000_000, clean_numbers)    
    if trillion_index > -1:
        param = clean_numbers[0:trillion_index]
        param = param if len(param)>0 else {get_name_by_number_value(1)}
        multiplier = number_formation(param)
        result +=  multiplier * 1_000_000_000_000
        clean_numbers = clean_numbers[trillion_index+1:]
        pass
    billion_index  = get_index_for_number(1_000_000_000, clean_numbers)
    if billion_index > -1:
        param = clean_numbers[0:billion_index]
        param = param if len(param)>0 else {get_name_by_number_value(1)}
        multiplier = number_formation(param)
        result +=  multiplier * 1_000_000_000
        clean_numbers = clean_numbers[billion_index+1:]
        pass
    million_index  = get_index_for_number(1_000_000, clean_numbers)
    if million_index > -1:
        param = clean_numbers[0:million_index]
        param = param if len(param)>0 else {get_name_by_number_value(1)}
        multiplier = number_formation(param)
        result +=  multiplier * 1_000_000
        clean_numbers = clean_numbers[million_index+1:]
        pass
    thousand_index = get_index_for_number(1_000, clean_numbers)
    if thousand_index > -1:
        param = clean_numbers[0:thousand_index]
        param = param if len(param)>0 else {get_name_by_number_value(1)}
        multiplier = number_formation(param)
        result +=  multiplier * 1_000
        clean_numbers = clean_numbers[thousand_index+1:]
        pass
    hundred_index  = get_index_for_number(  100, clean_numbers)
    if hundred_index > -1:
        param = clean_numbers[0:hundred_index]
        param = param if len(param)>0 else {get_name_by_number_value(1)}
        multiplier = number_formation(param)
        result +=  multiplier * 100
        clean_numbers = clean_numbers[hundred_index+1:]
        pass
    if len(clean_numbers) > 0:
        multiplier = number_formation(clean_numbers)
        result +=  multiplier * 1
        clean_numbers_new = {}
        pass
    
    return result


def word_to_num(number_sentence):
    """
    public function to return integer for an input `number_sentence` string
    
    input: string
    output: int or double or None
    """
    if type(number_sentence) is float:
        return number_sentence
    if type(number_sentence) is int:
        return number_sentence
    
    if type(number_sentence) is not str:
        raise ValueError("Type of input is not string! Please enter a valid number word (eg. \'two million twenty three thousand and forty nine\')")

    number_sentence = normalize(number_sentence) 

    if(number_sentence.isdigit()):  # return the number if user enters a number string
        return int(number_sentence)

    split_words = re.findall(r'\w+', number_sentence)  # strip extra spaces and comma and than split sentence into words

    clean_numbers = []
    clean_decimal_numbers = []

    # removing and, & etc.
    for word in split_words:
        word = normalize_data.get(word,word) # replacing words and lemma text
        if word in number_system:
            clean_numbers.append(word)
        elif word == number_system['point']:
            clean_numbers.append(word)

    # Error message if the user enters invalid input!
    if len(clean_numbers) == 0:
        raise ValueError("No valid number words found! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    check_double_input(1_000, clean_numbers)
    check_double_input(1_000_000, clean_numbers)
    check_double_input(1_000_000_000, clean_numbers)
    check_double_input(1_000_000_000_000, clean_numbers)

    # something about point
    if clean_numbers.count(number_system['point'])>1:
         raise ValueError("Redundant point word "+number_system['point']+"! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")         
    # separate decimal part of number (if exists)
    point = number_system['point']
    point_count = clean_numbers.count(point)
    if point_count == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index(point)+1:]
        clean_numbers = clean_numbers[:clean_numbers.index(point)]

    total_sum = get_number_value(clean_numbers)
    
    # adding decimal part to result (if exists)
    if len(clean_decimal_numbers) > 0:
        total_sum_as_string = str(total_sum)+"."+str(get_decimal_string(clean_decimal_numbers))
        total_sum = float(total_sum_as_string)

    return total_sum

#EOF

