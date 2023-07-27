#!/usr/bin/env python3

import sys
from tabulate import tabulate
import traceback
import pandas as pd
from argparse import ArgumentParser, Namespace

w = lambda x: (x.replace('\x0d\x0a', '<br>'))
converters_dict = {
    'Description': w,
    'BLUF': w
    }

def dump_dataframe(df):
    for label, content in df.items():
        print(f'label: {label}')
        print(f'content: {content}', sep='\n')
    
def main(args):
    csv_file1_pd = pd.read_csv(args.file1, index_col="NEWID", converters=converters_dict)
    csv_file2_pd = pd.read_csv(args.file2, index_col="NEWID", converters=converters_dict)
    #csv_file1_pd.index = csv_file1_pd.index.map(int)
    #csv_file2_pd.index = csv_file2_pd.index.map(int)
    csv_file1_pd.sort_index(inplace=True)
    csv_file2_pd.sort_index(inplace=True)
    index1_ps = pd.Series(csv_file1_pd.index)
    index2_ps = pd.Series(csv_file2_pd.index)
    num_rows1 = len(index1_ps)
    num_rows2 = len(index2_ps)
    count = 1
    for i in range(num_rows1):
        if i <= num_rows2:
            row1 = csv_file1_pd.loc[index1_ps[i]]
            row2 = csv_file2_pd.loc[index1_ps[i]]
            r1r2_compare = row1.compare(row2, result_names=(args.file1, args.file2))
            if not r1r2_compare.empty:
                print(f"\n\n# Diff {count}")
                print("\n\nFound a content difference between\n")
                print(f"\n* NEWID {index1_ps[i]} from {args.file1}\n\n* NEWID {index1_ps[i]} from {args.file2}\n")
                print("-"*3+"\n\n")
                table = tabulate(r1r2_compare, headers='keys', tablefmt='github')
                table = table.replace('\x0a\x0a', '  ')
                print(table)
                print("\n\n"+"-"*3+"\n\n\n")
                count += 1
    for i in range(num_rows2):
        temp_id = index2_ps[i]
        try:
            row1 = csv_file1_pd.loc[temp_id]
        except Exception:
            print("="*100)
            print(f"TempID {temp_id} not found in {args.file1}")
            print("-"*100)
            print(csv_file2_pd.loc[temp_id]+"\n")
            print("=-"*50+"\n\n\n")
        

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-1", "--file1", help="path to CSV file 1 to diff")
    parser.add_argument("-2", "--file2", help="path to CSV file 2 to diff")
    args = parser.parse_args()
    main(args)
