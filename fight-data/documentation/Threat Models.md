
# FiGHT Threat Models

This repository contains all of the CSV and Word documents that comprise the FiGHT Templates for FiGHT Objects, including but not limited to Techniques, Subtechniques, Critical Assets, Data Sources, and Mitigations.

## Structure and Naming Conventions

This repository shall consist of two folders:

1. CSV
2. Word

Data will only be loaded from these two folders.

Note that the contents of the CSV folder will take prescedence (overwrite) the contents of the Word folder in the event of a conflict.

### CSV Folder

The CSV Folder shall contain the following documents, using the names specified. Failure to follow naming convention will result in data not being processed.

* Critical_Assets.csv  // Contains list of critical assets.
* Data_Sources.csv  // Contains list of data sources from which detections are drawn.
* Detections.csv  // List of detections for each FiGHT Technique and Subtechnique, addendum or FiGHT original, with mappings to appropriate Data Source(s).
* Mitigations.csv  // Contains list of mitigations.
* Releases.csv  // List of FiGHT Techniques and Subtechniques, including addendums.

### Word Folder

This consists of Word documents that must follow the format in the FiGHT Technique Template, available at the root of this repository, to successfully load data. This template defines the structure necessary to build a FiGHT Technique or Subtechnique, including addendums, and the metadata and associations (such as references and detections) that define these objects.

There is no naming convention for document in this folder. The software will attempt to load whatever it can find, however incomplete or corrupted results may result in ugly entries on the website side.

## Deploying Data to Test Website

To verify that the data is complete and correctly presented, push the data to the repository and go to the 5G Pages GitLab repository and run the CI/CD pipeline. This will upload the data to the [development website, 5G Pages](https://5g-security.pages.mitre.org/), where the results can be checked. Eventually, the contents of the development website will be pushed to the public facing production website at GitHub, at a schedule determined by the FiGHT Team.
