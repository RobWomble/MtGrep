#!/usr/bin/env python3
""" Author: Rob Womble
    Script to convert human-friendly MagicCompRules
    file into a python-friendly format              """

# import statements here
import json


# define a constant with section names as a list.
# will save lines in handbook_adapt()
SECTIONS = ['title', 'date', 'intro',
            'contents', 'rules',
            'glossary', 'credits']


def rule_dict(rulebook_data_ref, line_str):
    """ Take rule lines from rulebook file and
        convert them into complex dictionary
        keys and values                     """
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

    # variables to increment (should be inside with?)
    # current_section = 0
    # gloss_lines = 0
    # gloss_key = ""

    # fill rulebook_data with information from rules text
    with open(rule_input_file, "r") as rulebook:
    ''' I still have to research the object type and applicable methods
        for rulebook to see if the for line will work as-is, or if I
        need to perform some method on it to make it iterable. It's at
        least hopefully obvious what the plan is.                   '''
        for rule_line in rulebook:

            # if the string matches one of the lines that denotes a
            # new section: add 1 to current_section, providing the
            # determination of which elif works on a line

            # elif title, date, or intro sections:
            # join to appropriate key of rulebook_data

            # elif contents section: ignore
            # contents section can be reproduced by printing keys in
            # rules dictionary

            # elif rules section: call rule_dict() to translate,
            # use returned data to define new values in ['rules']

            # elif glossary section:
            ''' I was considering making seperate function(s) for this
                step, but I ended up with either multiple one-line
                functions that were called by this if statement
                anyway, or a single function that returned different
                types of output depending on the input, which I don't
                know how to handle without an if statement anyway.  '''
            #    if rule_line == "\n":  # start new key if empty
            #        gloss_lines = 0
            #    elif gloss_lines == 0:  #define key
            #        gloss_lines =+ 1
            #        gloss_key = rule_line
            #        rulebook_data['glossary'][gloss_key] = []
            #    else:  #append to value of defined key
            #        rulebook_data['glossary'][gloss_key].append(rule_line)

            # else:
            #    must be credits, join to rulebook_data['credits']

    # create file to put rulebook_data into
    with open("rulebook.json", "r") as rule_output_file:
        json.dump(rulebook_data, target_file)


def test_rule_dict():
    # I have to define a variable here or I get complaints from vim
    rulebook_test_dict = {}
    # I would like to find a prettier way to write this.
    assert rule_dict(rulebook_test_dict,
                     "100.4a In constructed play, a sideboard may contain no\
                     more than fifteen cards. The four-card limit\
                     (see rule 100.2a) applies to the combined deck and\
                     sideboard."
                     ) == (rulebook_test_dict['rules']['100']['4a'],
                           "In constructed play, a sideboard may contain no\
                           more than fifteen cards. The four-card limit\
                           (see rule 100.2a) applies to the combined deck and\
                           sideboard.")


if __name__ == "__main__":
    handbook_adapt("MagicCompRules-20210712.txt")
