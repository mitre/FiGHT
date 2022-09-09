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

import pytest
from schema import SchemaError, SchemaWrongKeyError

"""
Validates ATLAS data objects against schemas defined in conftest.py.
"""

def test_validate_matrix(matrix_schema, matrix):
    """Validates the ATLAS matrix dictionary.
    Explicitly fails with message to capture more in pytest short test info.
    """
    try:
        matrix_schema.validate(matrix)
    except SchemaError as e:
        pytest.fail(e.code)

def test_validate_tactics(tactic_schema, tactics):
    """Validates each tactic dictionary.
    Explicitly fails with message to capture more in pytest short test info.
    """
    try:
        tactic_schema.validate(tactics)
    except SchemaError as e:
        pytest.fail(e.code)

def test_validate_techniques(technique_schema, subtechnique_schema, techniques):
    """Validates each technique dictionary, both top-level and subtechniques.
    Explicitly fails with message to capture more in pytest short test info.
    """
    try:
        # Check if dictionary is a top-level technique
        technique_schema.validate(techniques)
    except (SchemaWrongKeyError, SchemaError) as e:
        # Could be a subtechnique
        #   SchemaWrongKeyError: flagging on presence of 'subtechnique-of'
        #   SchemaError: flagging on ID having extra numbers at end
        if e.code.startswith("Wrong key 'subtechnique-of'") or "does not match" in e.code:
            try:
                # Validate the subtechnique
                subtechnique_schema.validate(techniques)
            except SchemaError as se:
                # Fail with any errors
                pytest.fail(se.code)
        else:
            # Otherwise is another key error
            pytest.fail(e.code)

def test_validate_case_studies(case_study_schema, case_studies):
    """Validates each case study dictionary.
    Explicitly fails with message to capture more in pytest short test info.
    """
    try:
        case_study_schema.validate(case_studies)
    except SchemaError as e:
        pytest.fail(e.code)
