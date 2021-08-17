#!/usr/bin/env python3
""" Author: Rob Womble
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


def rule_dict(rulebook_dict_str, rule_line_str):
    """ accepts the input of string that matches
        the name of rulebook_data and a string pulled
        from rules text, outputs a stingle string that
        contains code to update the rulebook_data dict"""
    pass

    ''' Rule dictionary: Rule format is: "(rule #).(subrule #) (text)"
        I want to split the line at the first period and make the
        rule number a key with the value of a dictionary where every
        subrule number is a key and subrule text is the value.
        That sentence may be hard to read, refer to the test function
        to see what I mean. Note that a period separates the rule and
        subrule, and the first subrule has a period instead of a letter.
        Also, the text ends with a period, since it's a sentence. I
        still have to determine a method to break this up properly. '''


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

    # fill rulebook_data with information from rules text
    with open(rule_input_file, "r") as rulebook:

        # variables used by for loop
        current_section = 0
        gloss_lines = 0
        gloss_key = ''

        for rule_line in rulebook.readlines():

            # remove line breaks: makes logic easier to write
            rule_line = rule_line.strip('\n')

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

            # (current_section no longer matches SECTIONS)
            # intro section:
            elif current_section == 3:
                if rulebook_data['intro'] == '':
                    rulebook_data['intro'] = rule_line
                else:
                    intro_data = [rulebook_data['intro'], rule_line]
                    rulebook_data['intro'] = '\n\n'.join(intro_data)

            # contents section can be reproduced by printing keys in
            # rules dictionary, so we'll ignore it
            elif current_section < 6:
                continue

            # rule_dict() returns code to add to rules section
            elif current_section == 6:
                continue  # write rule_dict() first
                rule_code = rule_dict(rulebook_data, rule_line)
                exec(rule_code)

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
    with open("rulebook.json", "r") as rule_output_file:
        pass  # write rule_dict(), then remove print line
        json.dump(rulebook_data, rule_output_file)
    print(rulebook_data)


def test_rule_dict():
    errorlist = []
    if rule_dict("rulebook_test_dict", str("6. Spells, Abilities, and Effects")
                 ) != str("rulebook_test_dict['rules']['6'] = {}; "
                          "rulebook_test_dict['rules']['6']['chapter'] "
                          "= 'Spells, Abilities, and Effects'"):
        errorlist.append("chapter function failed")

    if rule_dict("rulebook_test_dict", str("205. Type Line")
                 ) != str("rulebook_test_dict['rules']['2']['205'] = {}"
                          "rulebook_test_dict['rules']['2']['205']"
                          "['rule name'] = 'Type Line'"):
        errorlist.append("rule function failed")

    if rule_dict("rulebook_test_dict", str(
                     "100.4a In constructed play, a sideboard may"
                     "contain no more than fifteen cards. The four-card"
                     "limit (see rule 100.2a) applies to the combined"
                     "deck and sideboard.")
                 ) != str("rulebook_test_dict['rules']['1']['100']['4a']"
                          " = 'In constructed play, a sideboard may"
                          " contain no more than fifteen cards. The "
                          "four-card limit (see rule 100.2a) applies "
                          "to the combined deck and sideboard.'"):
        errorlist.append("subrule function failed")

    assert not errorlist, "failures:\n{}".format("\n".join(errorlist))


if __name__ == "__main__":
    handbook_adapt("MagicCompRules-20210712.txt")
