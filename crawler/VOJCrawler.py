import csv
import re
import os
import sys
from dotenv import load_dotenv
from io import StringIO
from tqdm import tqdm
from crawler.SPOJCrawler import SPOJCrawler

BASE_URL = 'https://vn.spoj.com/'
def main(crawler, output_dir):
    username = input('Your username: ')
    password = input('Your password: ')

    crawler._login(username, password)
    
    output_dir = os.path.join(output_dir, username)
    output_dir = os.path.join(output_dir, 'accepted_code')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    solved_list = crawler.get_solved_list(username)
    submission_count = solved_list.count('\n') 
    print("You have", submission_count, "accepted submissions")
    accepted_submission_count = 0
    #|   ID    |        DATE         |  PROBLEM  |  RESULT   | TIME  |  MEM   | LNG |
    csv_reader = csv.reader(StringIO(solved_list), delimiter = '|')
    tBar = tqdm(range(submission_count))
    for i in tBar:
        row = next(csv_reader)[1 : -1]
        if (row == None):
            continue
        row = list(map(str.strip, row))
        
        result = row[3]
        is_AC = (re.match('(AC|100)', result) != None)
        if is_AC:
            accepted_submission_count += 1
        if not is_AC:
            continue
        file_name = row[2]

        crawler.download_solution(os.path.join(output_dir, file_name), username, row[0], row[6])
        tBar.set_description("Accepted submissions found: " + str(accepted_submission_count))
    print("You have", accepted_submission_count, "accepted submissions")