# Fight Matrix

Code to produce the research working version of the matrix for the FIGHT threat model

THIS MODULE REQUIRES THIS VERSION OF `attack-obj-core`

## (Sub)Technique modeling
Developing a (Sub)Technique for FiGHT requires the following artifacts:
- The [FIGHT_releases.xlsx](https://teams.microsoft.com/l/file/7C916103-1F21-4704-BEC2-41BE76AF1FD9?tenantId=c620dc48-1d50-4952-8b39-df4d54d74d82&fileType=xlsx&objectUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel%2FShared%20Documents%2F5G%20Threat%20Model%2F1%20START%20HERE%2FFIGHT_releases.xlsx&baseUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel&serviceName=teams&threadId=19:5630a784d21542ada777b5ecb898b512@thread.tacv2&groupId=be5225e2-901c-41e7-86ac-ea231ba1ac3b) spreadsheet, where one row captures the high level information.
- A Word Document that captures all data for the (Sub)Technique.

### FIGHT_releases.xlsx editing rules
1. Column A, "TempID"
  - Ignored by code
2. Column B, "Domain"
  - Required
  - Usage TBD
3. Column C, "Platform / Architecture"
  - Required
  - Must be one of the following, exact values (TBD)
4. Column D, "Tactics"
  - Required
  - Must be one of these exact values:
    * reconnaissance
    * resource-development
    * initial-access
    * execution
    * persistence
    * privilege-escalation
    * defense-evasion
    * credential-access
    * discovery
    * lateral-movement
    * collection
    * command-and-control
    * exfiltration
    * impact
    * fraud
5. Column E, "New FGTID"
  - Required
  - Must be one of these exact formats:
    * FGT5xxx
    * FGT5xxx.yyy
    * ADDENDUM TO Txxx
    * ADDENDUM TO Txxx.yyy
    * Txxx.5yy
6. Column F, "Technique Name"
  - Required
  - Must contain only valid ASCII characters
  - Subtechniques MUST NOT include their parent Technique name
7. Column G, "BLUF"
  - Required
  - One line of Text only
8. Column H, "Description"
  - Optional
  - This column is presently ignored in favor of the contents of the corresponding DOCX draft.

All subsequent columns are not considered by the code and can be used freely by threat model developers


### FiGHT (Sub)Technique DOCX 

#### IMPORTANT CONSIDERATIONS
* Word comments are ignored by the code.
* Any redlines (proposed deletes, additions, modifications) are ignored by the parsing code.  To see the changes propagate to the website, they must be "Accepted" in Word.

#### Filename Requirements

All Word Documents MUST adhere to the following structure:
`<FGTID> Name.docx`

Where `<FGTID>` Must be one of these exact formats:
  
| Format      | (Sub)Technique Type |
|-------------|---------------------|  
|FGT5xxx      | FiGHT Technique     |
| FGT5xxx.yyy | FiGHT Subtechnique to a FiGHT Technique|
| Txxx        | ATT&CK Technique with one or more FiGHT Addendums |
| Txxx.yyy    | ATT&CK SubTechnique with one or more FiGHT Addendums |
| Txxx.5yy    | FiGHT Subtechnique to an ATT&CK Technique | 

For `Name`, the following rules apply
 * ATT&CK Technique Addendums and ATT&CK Subtechniques Addendums
    - The `Name` value is used by the code to produce section headers for each addendum on the website
    - The `Name` value MUST
        * Contain the 5G descriptive Context Name for the Addendum in question (e.g., `T1557 Non-SBI.docx`).
        * Match the value in Column F (see above) for the corresponding entry in `FIGHT_releases.xlsx`.
    - The `Name` value *MUST NOT* include the word ADDENDUM
    - The `Name` value can *optionally* contain the original ATT&CK name, in addition ot the Addendum Context title.  
        * Separate ATT&CK Technique Names from the Addendum Context Title using `:` (e.g., `T1557 Adversary-in-the-Middle:Non-SBI.docx`)
        * Separate ATT&CK Subtechnique Names from the Addendum Context Title using `;` (e.g., `T1499.002 Endpoint Denial of Service:Service Exhaustion Flood; Base station flood with ficticious requests.docx`)
 * FiGHT Techniques and Subtechniques
    - The `Name` value is NOT used by the code to produce content for the website
    - Should contain the FiGHT name for the (Sub)Technique, but this is only for human consumption
    - Should match the value in Column F (see above) for the corresponding entry in `FIGHT_releases.xlsx`.
    - This includes FiGHT Subtechniques that attach to an ATT&CK Technique
    
#### Document Content Requirements
- The document structure must strictly adhere to the structure specified [in this Guide on Teams](https://teams.microsoft.com/l/file/24CA4CFF-1F15-495E-8227-43264774D88F?tenantId=c620dc48-1d50-4952-8b39-df4d54d74d82&fileType=docx&objectUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel%2FShared%20Documents%2F5G%20Threat%20Model%2F1%20START%20HERE%2FRelease%201%20Templates%2F_FiGHT_Technique_Template_CODE_PARSEABLE.docx&baseUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel&serviceName=teams&threadId=19:5630a784d21542ada777b5ecb898b512@thread.tacv2&groupId=be5225e2-901c-41e7-86ac-ea231ba1ac3b)
  * updates will be made features are added and as corner cases / bugs are identified and remedied.
  * The code WILL NOT parse any proposed edits, only accepted proposals
- Place your DOCX file in the [Release 1 Templates](https://teams.microsoft.com/_#/files/5G%20Threat%20Model?threadId=19%3A5630a784d21542ada777b5ecb898b512%40thread.tacv2&ctx=channel&context=Release%25201%2520Templates&rootfolder=%252Fsites%252F5gthreatmodel-5GThreatModel%252FShared%2520Documents%252F5G%2520Threat%2520Model%252F1%2520START%2520HERE%252FRelease%25201%2520Templates) folder
- Please [open an issue](https://gitlab.mitre.org/5g-security/fight-matrix/-/issues/new?issue%5Bmilestone_id%5D=) for any parsing issues observed.
- Associating Mitigations with the (Sub)Technique
  * Per the template, The Mitigations table must be populated with one row per associated Mitigation.
    - Column A is for the FGMID, which must be present in the [FiGHT_Mitigations_for_human_edits.xlsx](https://teams.microsoft.com/l/file/452EAEEB-A17A-4CDA-ADA0-65E558BEFB8B?tenantId=c620dc48-1d50-4952-8b39-df4d54d74d82&fileType=xlsx&objectUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel%2FShared%20Documents%2F5G%20Threat%20Model%2F1%20START%20HERE%2FFiGHT_Mitigations_for_human_edits.xlsx&baseUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel&serviceName=teams&threadId=19:5630a784d21542ada777b5ecb898b512@thread.tacv2&groupId=be5225e2-901c-41e7-86ac-ea231ba1ac3b) spreadsheet (See Mitigations Modeling below).
    - Column B is for how the Mitigation is used to prevent the adversary behavior described by the (Sub)Technique captured in the Word Document in question.
- Associating Detections with the (Sub)Technique
    * Per the template, The Detections table must be populated with one row per associated Detection.
        - Column A is for the FGDSID, which must be present in the [FIGHT_DataSources_for_human_edits.xlsx](https://teams.microsoft.com/l/file/85E9520F-7C21-4B38-A4DB-E0FAEC50EE5E?tenantId=c620dc48-1d50-4952-8b39-df4d54d74d82&fileType=xlsx&objectUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel%2FShared%20Documents%2F5G%20Threat%20Model%2F1%20START%20HERE%2FFIGHT_DataSources_for_human_edits.xlsx&baseUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel&serviceName=teams&threadId=19:5630a784d21542ada777b5ecb898b512@thread.tacv2&groupId=be5225e2-901c-41e7-86ac-ea231ba1ac3b) spreadsheet.
        - Column B is for how the Data Source can be used to Detect the adversary behavior described by the (Sub)Technique captured in the Word Document in question.
 - Associating Critical Assets with the (Sub)Technique
    * This feature is not yet implemented, but is planned to follow the exact same methodology as is used for both Mitigation and Data Source/Detections
 - If the text in a given cell of a table in the DOCX file doesn't completely transfer to the website, please try the following procedure before opening a ticket:
    1. Copy the text from the entire row and paste it into a plain text editor (like Notepad or gvim)
    2. Delete the entire row in the DOCX file
    3. Click on the last cell in the last row and hit the TAB key to create a new row
    4. Copy each cell's value from the plain text editor and paste same into the corresponding cell in the new row
 - If the references hyperlinks do not appear on the website correctly, it may be due to oddities in how Word formats hyperlinks in the file.  Please try the following in the DOCX file in quesiton:
    1. Copy URL column of the row(s) in question from the Edit Hyperlink dialog box
    2. Delete the contents of that cell
    3. Paste in the URL value copied from step 1
    


#### Optional
 - Threat modelers have the option to use any and all [Markdown](https://www.markdownguide.org/basic-syntax/) to create italics, boldface, etc, within the text they write.
 - Threat modelers have the option to inline HTML in within the text they write.
 - Threat modelers can footnote references in the References table, using the [X] notation
    * Where the value of X is the row number in the References Table within the Word Document (not counting the header row at the top of the table)
    * Do NOT use the Word footnote feature.  The code will not read this means of doing References.  
    * This feature is not implemented yet in the code, but is planned for implementation before release.


## Mitigation Modeling
Developing a Mitigation for FiGHT requires the following artifacts:
- The [FiGHT_Mitigations_for_human_edits.xlsx](https://teams.microsoft.com/l/file/452EAEEB-A17A-4CDA-ADA0-65E558BEFB8B?tenantId=c620dc48-1d50-4952-8b39-df4d54d74d82&fileType=xlsx&objectUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel%2FShared%20Documents%2F5G%20Threat%20Model%2F1%20START%20HERE%2FFiGHT_Mitigations_for_human_edits.xlsx&baseUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel&serviceName=teams&threadId=19:5630a784d21542ada777b5ecb898b512@thread.tacv2&groupId=be5225e2-901c-41e7-86ac-ea231ba1ac3b) spreadsheet

Each row in the spreadsheet describes a FiGHT (or ATT&CK) Mitigation, using the following columns:
- Column A:  The FGMID, which follows format FGMID5xxx
- Column B:  The Mitigation Name
- Column C:  A one sentence BLUF of what the Mitigation is.

For a Mitgiation to be associated with a (Sub)Technique, it must be listed in the Word Document (see (Sub)Technique modeling, above).

## Data Source Modeling
Developing a Data Source for FiGHT requires the following artifacts:
- The [FIGHT_DataSources_for_human_edits.xlsx](https://teams.microsoft.com/l/file/85E9520F-7C21-4B38-A4DB-E0FAEC50EE5E?tenantId=c620dc48-1d50-4952-8b39-df4d54d74d82&fileType=xlsx&objectUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel%2FShared%20Documents%2F5G%20Threat%20Model%2F1%20START%20HERE%2FFIGHT_DataSources_for_human_edits.xlsx&baseUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel&serviceName=teams&threadId=19:5630a784d21542ada777b5ecb898b512@thread.tacv2&groupId=be5225e2-901c-41e7-86ac-ea231ba1ac3b) spreadsheet.

Each row in the spreadsheet describes a FiGHT (or ATT&CK) Data Source, using the following columns:
- Column A:  The FGDSID, which follows format FGDSID5xxx
- Column B:  The Data Source Name
- Column C:  A one sentence BLUF of what the Data Source is.

For a Data Source to be associated with a (Sub)Technique, it must be listed in the Word Document (see (Sub)Technique modeling, above).

## Critical Assets Modeling
This feature is not yet implemented, but is planned to follow the exact same methodology as is used for both Mitigation and Data Source/Detections.

# FAQ

 * What about any CSV files on Teams?
   - The code does not use any file in a CSV format, so they are not needed for this process.
* What is the [Mitigations_for_human_edits.xlsx](https://teams.microsoft.com/l/file/525952DA-CADE-40F5-8C55-02FF09865D5E?tenantId=c620dc48-1d50-4952-8b39-df4d54d74d82&fileType=xlsx&objectUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel%2FShared%20Documents%2F5G%20Threat%20Model%2F1%20START%20HERE%2FMitigations_for_human_edits.xlsx&baseUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel&serviceName=teams&threadId=19:5630a784d21542ada777b5ecb898b512@thread.tacv2&groupId=be5225e2-901c-41e7-86ac-ea231ba1ac3b) spreadsheet?
    - This spreadsheet was generated for the benefit of the threat modelers, it shows the union of the Mitigations with the (Sub)Techniques, based upon the different DOCX files.
    - It is not needed for the generation of the website.
    - Please note that this file is manually updated.  Pay attention to the Last Modified date on Teams.
 * What is the [Detection_for_human_edits.xlsx](https://teams.microsoft.com/l/file/39FEE5E3-849D-4A0C-9E6B-BE84646B5F3D?tenantId=c620dc48-1d50-4952-8b39-df4d54d74d82&fileType=xlsx&objectUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel%2FShared%20Documents%2F5G%20Threat%20Model%2F1%20START%20HERE%2FDetection_for_human_edits.xlsx&baseUrl=https%3A%2F%2Fmitre.sharepoint.com%2Fsites%2F5gthreatmodel-5GThreatModel&serviceName=teams&threadId=19:5630a784d21542ada777b5ecb898b512@thread.tacv2&groupId=be5225e2-901c-41e7-86ac-ea231ba1ac3b) spreadsheet?
   - This spreadsheet was generated for the benefit of the threat modelers, it shows the union of the Data Sources with the (Sub)Techniques, based upon the different DOCX files.. 
   - It is not needed for the generation of the website.
   - Please note that this file is manually updated.  Pay attention to the Last Modified date on Teams.