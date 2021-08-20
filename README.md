# Magic: The Greppening
#### An interactive version of Magic: The Gathering Comprehensive Rules
#### by Rob Womble
## Overview
This project is an attempt to create a tool with python that can be used to reference an offline copy of the Comprehensive Rulebook for Magic: The Gathering.

### Current features:
* Rule formatting tool: Converts the comprehensive rules txt into python-friendly json.

### Features to be added in the future:
* list rules by chapter
* list paragraphs in a rule, given a rule number
* search by keyword
* update local rules file through web request

## Requirements
* The current script has been tested and known to work with Python 3.8.10
* The only module used is json, which is included in The Python Standard Library.
* YOU MUST PROVIDE YOUR OWN COPY OF THE RULEBOOK TXT FILE. Latest version can be downloaded from https://magic.wizards.com/en/game-info/gameplay/rules-and-formats/rules

## Inspiration
The short story is that I wanted a friendlier way to reference the official rules for Magic without requiring internet access.

	I first started playing Magic as a member of the US Navy on deployment.  Wifi access was inconsistent to say the least; There were many long periods without internet access at all.  Any confusion on how specific game mechanics work or any answer to keywords that I was unfamiliar with would have to wait until the next time I could get online.  One day, I realized I could download the Magic: The Gathering Comprehensive rules, a dry document containing 130,000+ words worth of sweet, sweet certainty.
	Of course, by its nature as the comprehensive document, it's not the easiest to navigate.  Any given interaction in a typical game of magic frequently has multiple rules that apply to it.  When trying to settle a dispute, I would ctrl-f to search for a keyword, find a few results that didn't help me, skip ahead to the glossary entry, search the document for a rule mentioned in the glossary entry, search for a rule referenced in that rule...
	When I started playing Magic again in mid-2021, I of course ran into a card effect that had been added since the last time I had played, and a google search returned links to videos I had no interest in and message board posts filled with arguments about how the new effect was either good or bad.  I decided to pull out "old reliable", the comprehensive txt.  I found what I needed to know after some digging, and in the process, I noticed that the txt version in particular had very little formatting applied to it, with no special characters and every piece of information contained on its own line.  I was taking a linux class at the time, and realized it was quite convenient to use '<grep>' for whatever keyword I was interested in and have all lines mentioning the keyword on screen at once.  This gave me the idea to try to write a shell script that would allow me to either print all the rules with a matching keyword in them or print a specific rule, depending on input.  I didn't get around to it before I started learning python and realized I could do more.

## Skills Used
In order to accomplish this project, I had to use the following pythonic skills:
* for loops
* functions
* if/elif/else logic
* file manipulation (open(r/w))
* string manipulation (slicing, concatenation)
* complex dictionary comprehension
* json/python conversion
