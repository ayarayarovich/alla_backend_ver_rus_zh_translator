# A parser for the CC-Cedict. Convert the Chinese-English dictionary into a list of python dictionaries with
# "traditional","simplified", "pinyin", and "english" keys.

# Make sure that the cedict_ts.u8 file is in the same folder as this file, and that the name matches the file name on
# line 13.

# Before starting, open the CEDICT text file and delete the copyright information at the top. Otherwise the program
# will try to parse it and you will get an error message.

# Characters that are commonly used as surnames have two entries in CC-CEDICT. This program will remove the surname
# entry if there is another entry for the character. If you want to include the surnames, simply delete lines 59 and 60.

# This code was written by Franki Allegra in February 2020.

# open CEDICT file
# !/usr/bin/env python3
import shutil
import sys
import sqlite3
import app.model as _model

list_of_dicts = []
with open('C:/c_work/py_backend/resources/cedict_t.u8', encoding='utf-8') as file:
    shutil.copyfileobj(file, sys.stdout)
    text = file.read()
    lines = text.split('\n')
    dict_lines = list(lines)

    # define functions

    def parse_line(line):
        parsed = {}
        if line == '':
            dict_lines.remove(line)
            return 0
        line = line.rstrip('/')
        line = line.split('/')
        if len(line) <= 1:
            return 0
        english = line[1]
        char_and_pinyin = line[0].split('[')
        characters = char_and_pinyin[0]
        characters = characters.split()
        traditional = characters[0]
        simplified = characters[1]
        pinyin = char_and_pinyin[1]
        pinyin = pinyin.rstrip()
        pinyin = pinyin.rstrip("]")
        parsed['traditional'] = traditional
        parsed['simplified'] = simplified
        parsed['pinyin'] = pinyin
        parsed['english'] = english
        list_of_dicts.append(parsed)


    def remove_surnames():
        for x in range(len(list_of_dicts) - 1, -1, -1):
            if "surname " in list_of_dicts[x]['english']:
                if list_of_dicts[x]['traditional'] == list_of_dicts[x + 1]['traditional']:
                    list_of_dicts.pop(x)


    def main():

        # make each line into a dictionary
        print("Parsing dictionary . . .")
        for line in dict_lines:
            print('Done!')
            parse_line(line)
        # remove entries for surnames from the data (optional):

        # print("Removing Surnames . . .")
        remove_surnames()
        print('Done!')

        return list_of_dicts

        # If you want to save to a database as JSON objects, create a class Word in the Models file of your Django
        # project:

        # print("Saving to database (this may take a few minutes) . . .")
        # for one_dict in list_of_dicts:
        #     new_word = _model.Word(traditional=one_dict["traditional"], simplified=one_dict["simplified"],
        #                            english=one_dict["english"], pinyin=one_dict["pinyin"], hsk=one_dict["hsk"])
        #     new_word.save()

parsed_dict = main()
try:
    sqlite_connection = sqlite3.connect('C:/c_work/py_backend/resources/database.db')
    cursor = sqlite_connection.cursor()
    print("Connected to SQLite")
    sqlite_insert_with_param = """INSERT INTO words
                          (id,traditional, simplified, pinyin, english, hsk)
                           VALUES(?, ?, ?, ?, ?, ?);"""
    data_tuple = (4, '好', '好', 'hǎo', 'good, excellent, fine; well', 1)
    cursor.execute(sqlite_insert_with_param, data_tuple)
    sqlite_connection.commit()
    print("success ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Error while working with SQLite", error)
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Connection to SQLite is closed")