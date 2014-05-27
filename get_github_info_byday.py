#!/usr/bin/python

# download data (per day) about public github repos

# need PyGithub and unidecode
# pip install PyGithub
# pip install unidecode

from github import Github
from unidecode import unidecode
from datetime import datetime, timedelta
import time

# github credentials
g = Github("alyssafrazee", "totallynotmypassword")

# range function for dates (thanks stackoverflow: http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

today = datetime.today()
grad_day = datetime(2010, 5, 30)

# check ratelimits before you start:
for day in daterange(grad_day, today+timedelta(1)):
    filetag = str(day.year) + '-' + str(day.month).zfill(2) + '-' + str(day.day).zfill(2)
    query = 'created:' + filetag + ' stars:>4'

    repos = g.search_repositories(query=query)

    with open(filetag + '.txt', 'w') as f:
        f.write('repo_name' +'\t'+ 'owner_name' +'\t'+ 'language' +'\t'+ 'stars' +'\t'+ 'date_created'+ '\n')
        for repo in repos:
            if repo.owner.type == 'User':
                f.write(repo.name)
                f.write('\t')
                if repo.owner.name:
                    f.write(unidecode(repo.owner.name))
                else:
                    f.write("None")
                f.write('\t')
                f.write(str(repo.language))
                f.write('\t')
                f.write(str(repo.stargazers_count))
                f.write('\t')
                f.write(str(repo.created_at))
                f.write('\n')
