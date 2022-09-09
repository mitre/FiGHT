"""
NOTICE
This software was produced for the U. S. Government under Basic Contract No. W56KGU-18-D-0004, and
is subject to the Rights in Noncommercial Computer Software and Noncommercial Computer Software 
Documentation Clause 252.227-7014 (FEB 2012). Copyright (c) 2022 The MITRE Corporation.

FiGHT Object Core is a MITRE funded and developed Python library for importing
data from STIX, CSV, and Word to produce FiGHT data, including STIX Bundles and YAML
for website support.

This copyright notice must not be removed from this software, 
absent MITRE's express written permission.
"""

import os
from spellchecker import SpellChecker

"""
Sets up usage of https://pyspellchecker.readthedocs.io/en/latest/.
"""

# Add words to the spellcheck by adding to this file
custom_words_file = os.path.join(os.path.dirname(__file__), "custom_words.txt")

# Read in list of words
with open(custom_words_file) as f:
    CUSTOM_WORDS = [w.strip() for w in f.readlines()]

# Create English spell checker with additional custom words for syntax test use
SPELL_CHECKER = SpellChecker()
SPELL_CHECKER.word_frequency.load_words(CUSTOM_WORDS)
