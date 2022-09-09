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

from datetime import datetime
import json

from schema import Literal, Or, Schema

from .atlas_obj import (
    tactic_schema,
    technique_schema,
    subtechnique_schema,
    case_study_schema
)

"""Describes the ATLAS.yaml schema, which corresponds to data/matrix.yaml."""

atlas_matrix_schema = Schema(
    {
        "id": str,
        "name": str,
        "version": Or(str, int, float),
        "tactics": [
            tactic_schema
        ],
        "techniques": [
            Or(technique_schema, subtechnique_schema)
        ],
        "case-studies": [
            case_study_schema
        ]
    },
    name='ATLAS Matrix Schema',
    description=f'Generated on {datetime.now().strftime("%Y-%m-%d")}'
)
