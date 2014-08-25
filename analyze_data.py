#!/usr/bin/python

import pandas as pd
import sqlite3
import sexmachine.detector as gender
import matplotlib.pyplot as plt

d = gender.Detector(case_sensitive=False, unknown_value='neutral')

# let's start with Python
# read the data out of the database file:
#connec = sqlite3.connect('dat.db')
connec = sqlite3.connect('dat_anon.db') #last names removed for public database
df = pd.read_sql('select owner_name, language from github', connec)
splitnames = [x.split(' ') for x in df['owner_name']] #redundant if using dat_anon
df['gender'] = [d.get_gender(x[0]) for x in splitnames]
labels = ['male', 'mostly_male', 'neutral', 'mostly_female', 'female']
languages = ['JavaScript', 'Python', 'Ruby', 'PHP', 'Java', 'Objective-C', 'C', 'C++', 'Shell', 'C#', 'Go' ,'Perl', 'Clojure', 'Scala', 'Haskell', 'Erlang', 'R']
plotdata = pd.DataFrame(index=languages, columns=labels)
for language in languages:
    langdf = df[df['language']==language]
    vc = langdf['gender'].value_counts()
    norm = sum(vc)
    for aggcount in vc.iteritems():
        gclass, count = aggcount
        plotdata[gclass][language] = "{:.1f}".format(100*float(count)/norm)

# save file to use in D3 graphic:
plotdata.to_csv('plotdata.csv')

# for raw count graph:
plotdata_nonorm = pd.DataFrame(index=languages, columns=labels)
for language in languages:
    langdf = df[df['language']==language]
    vc = langdf['gender'].value_counts()
    norm = sum(vc)
    for aggcount in vc.iteritems():
        gclass, count = aggcount
        plotdata_nonorm[gclass][language] = count

plotdata_nonorm.to_csv('plotdata_nonorm.csv')


