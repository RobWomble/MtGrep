#!/usr/bin/env python3
""" Author: Rob Womble
    Script to convert human-friendly MagicCompRules
    file into a python-readable format              """

# import statements here
import json


# define a constant with section names as a list.
# will save lines in handbook_adapt()
SECTIONS = ['title', 'date', 'intro',
            'contents', 'rules',
            'glossary', 'credits']


def rule_dict():
    """ Take rule lines from rulebook file and
        convert them into complex dictionaries  """
    pass

    ''' Rule dictionary: Rule format is: "(rule #).(subrule #) (text)"
        I want to split the line at the first period and make the
        rule number a key with the value of a dictionary where every
        subrule number is a key and subrule text is the value.
        That sentence may be hard to read, refer to the test function
        to see what I mean. Note that a period separates the rule and
        subrule, and the first subrule has a period instead of a letter.
        Also, the text ends with a period, since it's a sentence. I
        still have to determine a method to break this up properly.
    '''


def handbook_adapt(rule_input_file, rule_output_file):
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
    # section = 0
    # gloss_lines = 0
    # gloss_key = ""

    # fill the dataset with information from rules text
    with open(rule_input_file, "r") as rulebook:
        # I still have to research the object type and applicable
        # methods for rulebook to see if the for loop will work
        # as-is. it's at least hopefully obvious what the plan is
        for line in rulebook:

            # if the string matches one of the lines that denotes a
            # new section: add 1 to section

            # elif title, date, or intro sections:
            # join to appropriate key of rulebook_data

            # elif contents section: ignore
            # contents section can be reproduced by printing keys in
            # rules dictionary

            # elif rules section: call rule_dict()

            # elif glossary section:
            ''' I was considering making seperate function(s) for this
                step, but I ended up with either multiple one-line
                functions that were called by this if statement
                anyway, or a single function that returned different
                types of output depending on the input, which I don't
                know how to handle without an if statement anyway.  '''
            # the following logic should save a key if the previous
            # line was empty, add the line to the value of that key if
            # it wasn't, restart the cycle if the current line is empty
            #   if line == "\n":
            #       gloss_lines = 0
            #   elif gloss_lines == 0:
            #       gloss_key = line
            #       rulebook_data['glossary'][gloss_key] = []
            #   else:
            #       append line to the value of
            #       rulebook_data['glossary'][gloss_key]

            # else:
            #   must be credits, join to rulebook_data['credits']

    # create file to put rule_data into
    with open("rules.json", "r") as rule_output_file:
        json.dump(rulebook_data, rule_output_file)


if __name__ == "__main__":
    handbook_adapt("MagicCompRules-20210712.txt")
