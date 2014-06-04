#!/usr/bin/python

import pandas as pd
import numpy as np
import sqlite3
import sexmachine.detector as gender
import matplotlib.pyplot as plt

d = gender.Detector(case_sensitive=False, unknown_value='neutral')

# let's start with Python
# read the data out of the database file:
connec = sqlite3.connect('dat.db')
df = pd.read_sql('select owner_name, language from github', connec)
splitnames = [x.split(' ') for x in df['owner_name']]
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


# matplotlib graphics (static)
plotdata_msort = plotdata.sort('male', ascending=False, axis=0)
plotdata_fsort = plotdata.sort('female', ascending=False, axis=0)
colors = ['#FF6600', '#FFA366', '#C9C9C9', '#80CC80', '#009900']

def makebarplot(dat, fname):
    barlocs = range(1, len(languages)+1)
    bars = []
    for i in range(0, len(labels)):
        bars.append(plt.bar(barlocs, dat[labels[i]], color=colors[i], bottom=dat[labels[:i]].sum(1)))
    plt.xlim(0, len(languages)+2)
    plt.ylim(0, 26700)
    plt.title('gender distribution of github repos by programming language')
    plt.xticks([x+0.5 for x in barlocs], dat.index, rotation=90)
    plt.ylabel('percent of repos, by first name classification')
    #plt.legend(reversed(bars), reversed(labels), loc=7) #loc=7 specifies center, and also, I sort of hate the legend
    plt.tight_layout()
    plt.savefig(fname, facecolor='white')

makebarplot(plotdata_msort, 'plot_msort_nonorm.png')
makebarplot(plotdata_fsort, 'plot_fsort.png')

plotdata_neutralsort = plotdata.sort('neutral', ascending=False, axis=0)
makebarplot(plotdata_neutralsort, 'plot_neutralsort.png')


