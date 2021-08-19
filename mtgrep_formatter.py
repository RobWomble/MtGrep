#!/usr/bin/env python3
""" Magic: The Greppening | CompRules Formatter
    Author: Rob Womble
    Script to convert human-friendly MagicCompRules
    txt file into a python-friendly json format     """

# import statements here
import json


# defining constants for use later
# section names as a list, saves elif lines later
SECTIONS = ['title', 'date', 'intro',
            'contents', 'rules',
            'glossary', 'credits']

# line names for handbook_adapt()'s if statement to look for.
SECTION_DELIMS = ['Introduction', 'Contents', 'Glossary', 'Credits']


def rule_dict(rule_line, old_line):
    """ returns a string of code designed to update the dictionary """

    # Rule format is: "(rule #).(subrule #) (text)"
    rule_output = ''
    rule_chap = rule_line[0]
    rule_text = rule_line.split(maxsplit=1)[1]
    rule_num = rule_line.split(maxsplit=1)[0].split('.')[0]
    # the following only gives index errors on lines used by else,
    # which doesn't use this variable, so it's safe to ignore.
    try:
        rule_sub = rule_line.split(maxsplit=1)[0].split('.')[1]
    except IndexError:
        pass

    # single digit followed by period denotes chapter
    if rule_line[1] == '.':
        rule_output = str(
            f'rulebook_data["rules"]["{rule_chap}"] = {{}}; '
            f'rulebook_data["rules"]["{rule_chap}"]["chapter"] = "{rule_text}"')

    # 3 digits without a number after the period: rule title
    elif rule_line[3:5] == '. ':
        rule_output = str(
            f'rulebook_data["rules"]["{rule_chap}"]["{rule_num}"] = {{}}; '
            f'rulebook_data["rules"]["{rule_chap}"]["{rule_num}"]["rule"] = "{rule_text}"')

    # 3 digits with number after period: subrule paragraph
    elif rule_line[3] == '.' and rule_line[4] != ' ':
        rule_output = str(
            f'rulebook_data["rules"]["{rule_chap}"]["{rule_num}"]'
            f'["{rule_sub}"] = "{rule_text}"')

    else:  # example text provided after some rules
        rule_line = str('\\n' + rule_line)
        rule_output = str(old_line[:-1] + rule_line + old_line[-1])

    return str(rule_output)


def handbook_adapt(rule_input_file):
    """ Main Function:
        defines data format,
        fills it with data,
        saves to a file     """

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
        # must be defined to run rule_dict()
        old_line = ''

        # generate and manipulate each line in file
        for rule_line in rulebook.readlines():

            # remove line breaks: makes logic easier to write
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

            # Current_section no longer matches SECTIONS,
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
                new_line = rule_dict(rule_line, old_line)
                exec(new_line)
                old_line = new_line

            # glossary section, multiple lines per entry
            elif current_section == 7:
                if rule_line == '':  # start new key if empty
                    gloss_key = ''
                    gloss_lines = 0
                elif gloss_lines == 0:  # define key
                    gloss_lines += 1
                    gloss_key = rule_line
                    rulebook_data['glossary'][gloss_key] = []
                else:  # append to value of defined key
                    rulebook_data['glossary'][gloss_key].append(rule_line)

            else:  # should be credits
                if rulebook_data['credits'] == '':
                    rulebook_data['credits'] = rule_line
                else:
                    credit_data = [rulebook_data['credits'], rule_line]
                    rulebook_data['credits'] = '\n\n'.join(credit_data)

    # create file to put rulebook_data into
    with open("rulebook.json", "a") as rule_output_file:
        json.dump(rulebook_data, rule_output_file)


# run with current rules text in working directory
if __name__ == "__main__":
    handbook_adapt("MagicCompRules-20210712.txt")
