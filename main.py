import csv
import re
import os
import sys
from dotenv import load_dotenv
from io import StringIO
from services.SPOJCrawler import SPOJCrawler
from services.Codeforces import CodeforcesInteractor

BASE_URL = 'https://vn.spoj.com/'


def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path)
    load_dotenv()

    # get codeforces link
    data = open('database/codeforces_link.txt').read().strip()
    pattern = r'(\w+) https.+/contest/(\d+)/problem/(\w+)'
    data = re.findall(pattern, data)
    links = {}
    for name, contest, id in data:
        links[name] = '/'.join([contest, id])

    voj_username = os.getenv('VOJ_USERNAME')
    voj_password = os.getenv('VOJ_PASSWORD')
    cf_username = os.getenv('CF_USERNAME')
    cf_password = os.getenv('CF_PASSWORD')
    if None in [voj_username, voj_password, cf_username, cf_password]:
        print('Please create .env file and fill it with your voj, codeforces account.\n'
              'See .env-example for more information')
        return
    # login to voj, CF
    crawler = SPOJCrawler(BASE_URL,
                          BASE_URL + 'files/src/save/{id}')
    crawler._login(voj_username, voj_password)
    submiter = CodeforcesInteractor(cf_username, cf_password)
    if submiter.login() == False:
        return
    # user must be in VNOI group
    if submiter.check_in_group() == False:
        return

    output_dir = voj_username
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    solved_list = crawler.get_solved_list(voj_username)
    submission_count = solved_list.count('\n')
    print("You have", submission_count, "accepted submissions")
    # |   ID    |        DATE         |  PROBLEM  |  RESULT   | TIME  |  MEM   | LNG |
    csv_reader = csv.reader(StringIO(solved_list), delimiter='|')
    cnt_submitted = 0
    # start crawling
    for row in csv_reader:
        row = list(map(str.strip, row))[1:-1]

        result = row[3]
        is_AC = (re.match('(AC|100)', result) != None)
        if not is_AC:
            continue
        file_name = row[2]
        if file_name not in links:
            print(f"Problem {file_name} is not found")
            continue
        try:
            code, lang = crawler.download_solution(os.path.join(
                output_dir, file_name), voj_username, row[0], row[6])
            if lang not in ['java', 'cpp', 'pas']:
                print('Cannot submit solution with extention:', lang)
                continue
            # submit to codeforces
            contest, id = links[file_name].split('/')
            submiter.submit(file_name, code, lang, contest, id)
        except Exception as e:
            print('Error', str(e))
            continue
        cnt_submitted += 1

    print("Submitted solution:", cnt_submitted)


if __name__ == '__main__':
    main()
