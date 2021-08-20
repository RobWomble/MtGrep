#!/usr/bin/env python3
""" Magic: The Greppening | CompRules Formatter
    Author: Rob Womble
    Script to convert human-friendly MagicCompRules
    txt file into a python-friendly json format     """


import json
import argparse


# defining constants for use later
# section names as a list, saves elif lines later
SECTIONS = ['title', 'date', 'intro',
            'contents', 'rules',
            'glossary', 'credits']

# line names for handbook_adapt()'s if statement to look for.
SECTION_DELIMS = ['Introduction', 'Contents', 'Glossary', 'Credits']

# variables updated and referenced by rule_dict()
current_chapter_data = ''
current_rulenum_data = ''
rule_chap = ''; rule_num = ''
rule_sub = ''; rule_text = ''


def rule_dict(rulebook_data, rule_line):
    """ update the dictionary with
        the given rulebook line    """

    #  these were defined globally so we can reuse them later
    global current_chapter_data
    global current_rulenum_data
    global rule_chap
    global rule_num
    global rule_sub
    global rule_text

    # we only want these to update if NOT an example line
    if rule_line[1] == '.' or rule_line[3] == '.':
        rule_chap = rule_line[0]
        rule_num = rule_line.split(maxsplit=1)[0].split('.')[0]
        rule_sub = rule_line.split(maxsplit=1)[0].split('.')[1]
        rule_text = rule_line.split(maxsplit=1)[1]

    # chapter line: create chapter dict and insert into main dict
    if rule_line[1] == '.':
        current_chapter_data = {'chapter': rule_text}
        rulebook_data['rules'].update({rule_chap: ''})
        rulebook_data['rules'][rule_chap] = current_chapter_data
    # rule number line: create dict and push up to higher dicts
    elif rule_line[3:5] == '. ':
        current_rulenum_data = {'rule': rule_text}
        current_chapter_data.update({rule_num: ''})
        current_chapter_data[rule_num] = current_rulenum_data
        rulebook_data['rules'][rule_chap] = current_chapter_data
    # subrule: create dict and push to higher dicts
    elif rule_line[3] == '.' and rule_line[4] != ' ':
        current_rulenum_data.update({rule_sub: rule_text})
        current_chapter_data[rule_num] = current_rulenum_data
        rulebook_data['rules'][rule_chap] = current_chapter_data
    # example line: join with newline to last entry
    else:
        old_text = rulebook_data['rules'][rule_chap][rule_num][rule_sub]
        rulebook_data['rules'][rule_chap][rule_num][rule_sub] \
            = '\n'.join([old_text, rule_line])
    # give updated file back to handbook_data()
    return rulebook_data


def dump_to_file(rulebook_data):
    """ dumps rulebook_data to file """

    # create file to put rulebook_data into
    with open("rulebook.json", "a") as rule_output_file:
        # save the data in the file as json
        json.dump(rulebook_data, rule_output_file)
    # let the calling function know it's done
    return True


def handbook_adapt(rule_input_file):
    """ defines and fills data structure """

    # define the format of the final file
    rulebook_data = {
            SECTIONS[0]: '',  # title
            SECTIONS[1]: '',  # date
            SECTIONS[2]: '',  # intro, use '\n'.join()
            SECTIONS[4]: {},  # rules (skip contents)
            SECTIONS[5]: {},  # glossary
            SECTIONS[6]: '',  # credits, use '\n'.join()
    }

    # open txt file to use contents
    with open(rule_input_file, "r") as rulebook:

        # variables used by for loop
        current_section = 0
        gloss_lines = 0
        gloss_key = ''

        # generate and manipulate each line in file
        for rule_line in rulebook.readlines():

            # remove whitespace: makes logic easier to write
            rule_line = rule_line.strip('\n ')

            # increment to track document position
            if rule_line in SECTION_DELIMS:
                current_section += 1
            # discard blank lines unless glossary needs them
            elif rule_line == '' and current_section != 7:
                continue
            # title or date sections:
            elif current_section < 2:
                rule_line = rule_line.strip('\\\ufeff')  # title format
                rulebook_data[SECTIONS[current_section]] = rule_line
                current_section += 1
            # Current_section no longer matches SECTIONS;
            # intro section title caused an increment
            # intro section:
            elif current_section == 3:
                if rulebook_data['intro'] == '':
                    rulebook_data['intro'] = rule_line
                else:
                    intro_data = [rulebook_data['intro'], rule_line]
                    rulebook_data['intro'] = '\n\n'.join(intro_data)
            # contents section can be reproduced by printing keys in
            # rules dictionary and SECTION_DELIMS, so we'll ignore it
            elif current_section < 6:
                continue
            # rule_dict() returns code to add to rules section
            elif current_section == 6:
                rulebook_data = rule_dict(rulebook_data, rule_line)
            # glossary section, multiple lines per entry
            elif current_section == 7:
                if rule_line == '':  # start new key if empty
                    gloss_key = ''
                    gloss_lines = 0
                elif gloss_lines == 0:  # define key
                    gloss_lines += 1
                    gloss_key = rule_line
                    rulebook_data['glossary'][gloss_key] = ''
                else:   # join to value of defined key,
                        # remove leading newline if first join
                    rulebook_data['glossary'][gloss_key]\
                            = '\n'.join([rulebook_data['glossary'][gloss_key],
                                        rule_line]).strip('\n')
            else:  # should be credits
                if rulebook_data['credits'] == '':
                    rulebook_data['credits'] = rule_line
                else:
                    credit_data = [rulebook_data['credits'], rule_line]
                    rulebook_data['credits'] = '\n\n'.join(credit_data)
    return rulebook_data


def main(target_file):
    """calls the other functions"""

    # generate dictionary
    rulebook_data = handbook_adapt(target_file)
    # save to file
    if dump_to_file(rulebook_data):
        print("success")


# run with current rules text in working directory
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Convert MTG Comprehensive rules to json file.')
    parser.add_argument('-f', '--file',
                        default="MagicCompRules-20210712.txt",
                        help='input from local file',
                        type=str)
    args = parser.parse_args()

    main(args.file)
