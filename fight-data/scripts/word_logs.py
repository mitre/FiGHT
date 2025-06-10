#!/usr/bin/python3

import os
import os
import re
import csv
from tabulate import tabulate
import subprocess

os.environ["GIT_PAGER"] = ""
commit_re = re.compile("([0-9a-f]{40})")
author_re = re.compile("Author: (.*)")
date_re = re.compile("Date: (.*)")
fgtid_re = re.compile("(FGT\d{4}[.00\d]*)")
tid_re = re.compile("(T\d{4}[.00\d]*)")
git_commit_href_base = "https://gitlab.mitre.org/5g-security/atlas-data/-/tree/"
git_commit_docx_href_base = "https://gitlab.mitre.org/5g-security/atlas-data/-/blob/"
git_commit_docx_href_path = "/threat_models/Word/"
fight_href_base = ""
login = os.getenv('GITLAB_USER_LOGIN')
branch = os.getenv('CI_COMMIT_BRANCH')
pages_href_base = "https://atlas-data-5g-security-0808414fbaccfbaacd37b35ef62c693273c0629e.pages.mitre.org/"
pages_href_path = f"sandboxes/{login}/{branch}/techniques/"


def make_a_href(commit):
    url = git_commit_href_base+commit
    tag = f"<a href=\"{url}\">{commit[:6]}</a>"
    return tag

def make_a_docx_href(commit, filename):
    url_filename = filename.replace(" ", "%20")
    url = git_commit_href_base+commit+git_commit_docx_href_path+url_filename
    tag = f"<a href=\"{url}\">{filename}</a>"
    return tag

def make_a_pages_href(filename):
    tid = fgtid_re.search(filename).groups()[0]
    url = pages_href_base+pages_href_path+tid
    tag = f"<a href=\"{url}\">{tid}</a>"
    return tag

class GitLog(object):
    
    def __init__(self, filename, log):
        self.data = {
            "filename": filename,
            "log": log,
            "commit": "",
            "author": "",
            "date": "",
            "comment": ""
        }
        for line in self.data["log"].split("\n"):
            commit_m = commit_re.search(line)
            author_m = author_re.search(line)
            date_m = date_re.search(line)
            if commit_m:
                self.data["commit"] = commit_m.groups()[0]
            elif author_m:
                self.data["author"] = author_m.groups()[0]
            elif date_m:
                self.data["date"] = date_m.groups()[0]
            else:
                self.data["comment"] += line

    def get_data(self):
        return self.data

class WordFile(object):

    def __init__(self, path, filename):
        self.filename = filename
        self.path = path
        self.git_logs = []
        full_filename = os.path.join(self.path, self.filename)
        fgtid_m = fgtid_re.search(full_filename)
        tid_m = tid_re.search(full_filename)
        if fgtid_m:
            self.fgtid = fgtid_m.groups()[0]
        elif tid_m:
            self.fgtid = "FG"+tid_m.groups()[0]
        else:
            raise Exception(f"Invalid filename {full_filename}")
        self.get_git_log(full_filename)

    def get_git_log(self, filename):
        command = f"git log --all --full-history  -- '{filename}'"
        results = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        logs = results.stdout.split("commit ")
        for log in logs:
            self.git_logs.append(GitLog(filename, log))

    def print_latest_header(self):
        if self.git_logs:
            git_log = self.git_logs[-1].get_data()
            author = git_log["author"]
            this_date = git_log["date"]
            commit = make_a_href(git_log["commit"])
            comment = git_log["comment"]
            print(f"|{self.fgtid}|{self.filename}|{author}|{this_date}|{commit}|{comment}|")

    def get_last_header_list(self):
        if self.git_logs:
            index = 0
            for git_log_obj in self.git_logs:
                git_log = git_log_obj.get_data()
                if index == 0:
                    index += 1
                    continue
                elif "Merg" in git_log["comment"]:
                    index += 1
                    continue
                elif git_log["comment"]:
                    author = git_log["author"]
                    this_date = git_log["date"]
                    commit = make_a_href(git_log["commit"])
                    comment = git_log["comment"]
                    url_filename = make_a_docx_href(git_log["commit"], self.filename)
                    a_fgtid = make_a_pages_href(self.fgtid)
                    return [a_fgtid, url_filename, author, this_date, commit, comment]

def walk_directory(directory_path):
    technique_docxs = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            technique_docx = WordFile(root, file_name)
            technique_docxs.append(technique_docx)
    return technique_docxs

def write_csv(technique_docxs):
    outfile = "status.csv"
    header = ["FGTID", "Filename", "Author", "Date", "commit", "comment"]
    csvfile = open(outfile, "w")
    writer = csv.writer(csvfile)
    writer.writerow(header)
    for technique_docx in technique_docxs:
        data = technique_docx.get_last_header_list()
        if data:
            writer.writerow(data)

def write_html_table(technique_docxs):
    outfilename = "status.html"
    header = ["FGTID", "Filename", "Author", "Date", "commit", "comment"]
    table = [header]
    for technique_docx in technique_docxs:
        data = technique_docx.get_last_header_list()
        if data:
            table.append(data)
    outfile = open(outfilename, "w")
    outfile.write(tabulate(table, tablefmt='unsafehtml'))


if __name__ == "__main__":
    directory_path = 'threat_models/Word'
    technique_docxs = walk_directory(directory_path)
    write_csv(technique_docxs)
    write_html_table(technique_docxs)