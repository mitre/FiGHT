import csv

def get_gold_csv(filename):
    spreadsheet = {}
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            tempid = row[0]
            domain = row[1]
            platform = row[2]
            tactics = row[3]
            tid = row[4]
            t_name = row[5]
            bluf = row[6]
            source = row[7]
            if tempid:
                spreadsheet[tempid] = {
                    "domain": domain,
                    "platform": platform,
                    "tactics": tactics,
                    "tid": tid,
                    "technique_name": t_name,
                    "bluf": bluf,
                    "source": source,
                    "row": row
                }
    return spreadsheet
