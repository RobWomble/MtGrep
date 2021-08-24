#!/usr/bin/env python3
""" Magic: The Greppening | CompRules Formatter
    Author: Rob Womble    | Revision: 3
    Script to convert human-friendly MagicCompRules
    txt file into a python-friendly json format     """


# standard library imports
import json
import argparse


# line names for handbook_adapt()'s if statement to look for.
SECTION_DELIMS = ['Introduction', 'Contents', 'Glossary', 'Credits']


class RulebookData:
    """ object to store and manipulate
        data from source txt        """
    def __init__(self):
        self.chap_dict = {}
        self.rule_dict = {}
        self.rule_chap = ''
        self.rule_num = ''
        self.rule_sub = ''
        self.rule_text = ''
        self.gloss_blank = 0
        self.gloss_key = ''
        self.final_dict = {
            'title': '',
            'date': '',
            'intro': '',
            'rules': {},
            'glossary': {},
            'credits': '',
        }

    def rule_add(self, rule_line):
        """ update the dictionary with rulebook line """

        # we only want these to update if NOT an example line
        if rule_line[1] == '.' or rule_line[3] == '.':
            self.rule_chap = rule_line[0]
            self.rule_num = rule_line.split(maxsplit=1)[0].split('.')[0]
            self.rule_sub = rule_line.split(maxsplit=1)[0].split('.')[1]
            self.rule_text = rule_line.split(maxsplit=1)[1]

        # chapter line: create chapter dict and insert into main dict
        if rule_line[1] == '.':
            self.chap_dict = {'chapter': self.rule_text}
            self.final_dict['rules'].update({self.rule_chap: ''})
            self.final_dict['rules'][self.rule_chap] = self.chap_dict
        # rule number line: create dict and push up to higher dicts
        elif rule_line[3:5] == '. ':
            self.rule_dict = {'rule': self.rule_text}
            self.chap_dict.update({self.rule_num: ''})
            self.chap_dict[self.rule_num] = self.rule_dict
            self.final_dict['rules'][self.rule_chap] = self.chap_dict
        # subrule: create dict and push to higher dicts
        elif rule_line[3] == '.' and rule_line[4] != ' ':
            self.rule_dict.update({self.rule_sub: self.rule_text})
            self.chap_dict[self.rule_num] = self.rule_dict
            self.final_dict['rules'][self.rule_chap] = self.chap_dict
        # example line: join with newline to last entry
        else:
            # these variables are only for 80 character limit
            chap = self.rule_chap
            num = self.rule_num
            sub = self.rule_sub
            old = self.final_dict['rules'][chap][num][sub]
            self.final_dict['rules'][chap][num][sub]\
                = '\n'.join([old, rule_line])

    def gloss_add(self, rule_line):
        """ update dictionary with glossary line """
        # start new key if the line is empty
        if rule_line == '':
            self.gloss_key = ''
            self.gloss_blank = 0
        # define the current key if the previous line was empty
        elif self.gloss_blank == 0:
            self.gloss_blank += 1
            self.gloss_key = rule_line
            self.final_dict['glossary'][self.gloss_key] = ''
        # join text to the value of the current key
        else:
            self.final_dict['glossary'][self.gloss_key]\
                    = '\n'.join([self.final_dict['glossary'][self.gloss_key],
                                rule_line]).strip('\n')

    def paragraph_add(self, rule_line, section):
        """ update paragraph sections """
        # insert text in blank section
        if self.final_dict[section] == '':
            self.final_dict[section] = rule_line
        # join to existing text
        else:
            sec_data = [self.final_dict[section], rule_line]
            self.final_dict[section] = '\n\n'.join(sec_data)

    def handbook_adapt(self, rule_input_file):
        """ opens source file and
            calls other functions to 
            fill the data structure """
        # open txt file to use contents
        with open(rule_input_file, "r") as rulebook:
            # used to track document progress
            current_section = 0
            # generate and manipulate each line in file
            for line in rulebook.readlines():
                # remove whitespace: makes logic easier to write
                line = line.strip('\n ')
                # increment to track document position
                if line in SECTION_DELIMS:
                    current_section += 1
                # discard blank lines unless glossary needs them
                elif line == '' and current_section != 6:
                    continue
                # title section:
                elif current_section == 0:
                    line = line.strip('\\\ufeff')  # title format
                    self.final_dict['title'] = line
                    current_section += 1
                # date section:
                elif current_section == 1:
                    self.final_dict['date'] = line
                # intro section:
                elif current_section == 2:
                    self.paragraph_add(line, 'intro')
                # contents section can be reproduced by printing keys in
                # rules dictionary and SECTION_DELIMS, so we'll ignore it
                elif current_section < 5:
                    continue
                # rule_dict() returns code to add to rules section
                elif current_section == 5:
                    self.rule_add(line)
                # glossary section, multiple lines per entry
                elif current_section == 6:
                    self.gloss_add(line)
                else:  # should be credits
                    self.paragraph_add(line, 'credits')
        # return completed dictionary
        return self.final_dict


def dump_to_file(rulebook_data):
    """ dumps rulebook_data to file """

    # create file to put rulebook_data into
    with open("rulebook.json", "a") as rule_output_file:
        # save the data in the file as json
        json.dump(rulebook_data, rule_output_file)
    # let the calling function know it's done
    return True


def convert_from_local(target_file):
    """ calls the other functions """

    # generate dictionary object
    rulebook_data = RulebookData()
    # return final dictionary
    rulebook_data = rulebook_data.handbook_adapt(target_file)
    # save to file
    if dump_to_file(rulebook_data):
        print("success")


# run with current rules text in working directory
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Convert MTG Comprehensive rules to json file.')
    parser.add_argument('-f', '--file',
                        default="MagicCompRules 20210712.txt",
                        help='input from local file',
                        type=str)
    args = parser.parse_args()

    convert_from_local(args.file)
