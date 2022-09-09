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

import datetime

from schema import Or, Optional, Schema

from .atlas_id import (
    TACTIC_ID_REGEX_EXACT,
    TECHNIQUE_ID_REGEX_EXACT,
    SUBTECHNIQUE_ID_REGEX_EXACT,
    CASE_STUDY_ID_REGEX_EXACT
)

"""Describes ATLAS object schemas.

The Schema objects defined are set to be definitions referenced
by the provided name.
"""

tactic_schema = Schema(
    {
        "id": TACTIC_ID_REGEX_EXACT,
        "object-type": 'tactic',
        "description": str,
        "name": str,
    },
    name="tactic",
    as_reference=True
)

technique_schema = Schema(
    {
        "id": TECHNIQUE_ID_REGEX_EXACT,
        "object-type": "technique",
        "name": str,
        "description": str,
        "tactics": [
            TACTIC_ID_REGEX_EXACT # List of tactic IDs
        ]
    },
    name="technique",
    as_reference=True
)

subtechnique_schema = Schema(
    {
        "id": SUBTECHNIQUE_ID_REGEX_EXACT,
        "object-type": "technique",
        "name": str,
        "description": str,
        "subtechnique-of": TECHNIQUE_ID_REGEX_EXACT # Top-level technique ID
    },
    name="subtechnique",
    as_reference=True
)

case_study_schema = Schema(
    {
        "id": CASE_STUDY_ID_REGEX_EXACT,
        "object-type": "case-study",
        "name": str,
        "summary": str,
        "incident-date": datetime.date,
        "incident-date-granularity": Or('YEAR', 'MONTH', 'DATE'),
        "procedure": [
            {
                "tactic": TACTIC_ID_REGEX_EXACT,
                "technique": Or(
                    TECHNIQUE_ID_REGEX_EXACT,   # top-level techniquye
                    SUBTECHNIQUE_ID_REGEX_EXACT # subtechnique
                ),
                "description": str
            }
        ],
        "reported-by": str,
        Optional("references"): Or(
            [
                {
                    "title": Or(str, None),
                    "url": Or(str, None)
                }
            ]
            , None
        )
    },
    name="case_study",
    as_reference=True
)
