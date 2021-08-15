#!/usr/bin/env python3
""" Author: Rob Womble
    Script to convert human-friendly MagicCompRules
    file into a python-readable format              """

# import statements here


def rule_dict():
    """ Take rule lines from rulebook file and
        convert them into complex dictionaries  """
    pass

    ''' Rule dictionary: Rule format is: "(rule #).(subrule #) (text)"
        I want to split the line at the first period and make the
        rule number a key with the value of a dictionary where every
        subrule number is a key and subrule text is the value.
        That sentence may be hard to parse, refer to the test function
        to see what I mean. Note that a period separates the rule and
        subrule, and the first subrule has a period instead of a letter.
        Also, the text just has to end with a period, being a
        sentence and all. I'll have to do some research to see if
        using a .split() method will even work for me.  Maybe I'll have
        to define another incrementable value to count how many periods
        are in the current working line...
    '''


def handbook_adapt(rule_input_file):
    """ Main Function:
        defines data format,
        fills it with data,
        saves to a file     """

    # define the format of the final file
    # # at this time, I'm thinking something along the lines of:
    # rule_data = {{}, {}}
    # #             |  | |
    # #             |  | Overarching dictionary: for items outside of
    # #             |  | rules and glossary that I may or may not want
    # #             |  | to access in the other script, one key for
    # #             |  | each section of the document
    # #             |  |
    # #             |  Glossary dictionary: The glossary format is
    # #             |  "(term)\n(definition)" with empty lines above and
    # #             |  below, so the plan for now is to use an
    # #             |  increment in the glossary section to properly
    # #             |  assign keys and values when there's two lines
    # #             |  of text in a row
    # #             |
    # #             Rule dictionary: see rule_dict()

    # variables to increment
    # section = 0
    # line_not_empty = 0
    # glossary_key = ""

    # fill the dataset with information from rules text
    # I'm struggling with the idea of breaking this into separate
    # functions without ruining the variables
    with open(rule_input_file, "r") as rulebook:
        # I still have to research the object type and applicable
        # methods for rulebook to see if the for loop will work
        # as-is. it's at least hopefully obvious what the plan is
        for line in rulebook:

            # if the string matches one of the lines that denotes a
            # new section: add 1 to section

            # elif title, date, or intro sections:
            # add to appropriate key of rule_data

            # elif contents section: ignore
            # contents section can be reproduced by printing keys in
            # rules dictionary

            # elif rules section: call rule_dict()

            # elif glossary section:
            # the following logic should save a key if the previous
            # line was empty, add the line to the value of that key if
            # it wasn't, restart the cycle if the current line is empty

                # if line_not_empty == 0:
                    # glossary_key = line
                    # line_not_empty += 1

                # elif line == "\n":
                    # line_not_empty = 0

                # else:
                    # add line to values of glossary_key

            # else:
                # must be credits, add to rule_data['credits']

    # create file to put rule_data into
    with open("rules.json", "r") as rule_output_file:
        json.dump(rule_data, rule_output_file)

if __name__ == __main__:
    handbook_adapt("MagicCompRules-20210712.txt")
