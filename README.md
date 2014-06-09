## gender of GitHub repo owners
-------------

This is the code I used to do a little data-driven analysis of the gender breakdown of owners of public GitHub repositories. [I wrote a blog post](http://alyssafrazee.com/gender-and-github-code.html) about what I found.

The code in here is:
* `get_github_info_byday.py`: uses the GitHub API to scrape repository data
* `merge_files.sh`: puts all scraped data together in a big text file
* `make_database.R`: dumps the scraped data into a SQLite database
* `analyze_data.py`: processes the data
* `bargraph.js`: the JavaScript/D3 code used to make [the graphic showing the results](http://alyssafrazee.com/plgender.html). [Alex Wilson](https://github.com/alexandrinaw) made major contributions to this code.

#### dependencies
**Python libraries**: [PyGithub](http://jacquev6.github.io/PyGithub/v1/index.html), [Unidecode](https://pypi.python.org/pypi/Unidecode/0.04.16), [Pandas](http://pandas.pydata.org/), [SexMachine](https://pypi.python.org/pypi/SexMachine/), [Matplotlib](http://matplotlib.org/)  

**R packages**: [devtools](http://cran.r-project.org/web/packages/devtools/index.html) (to install [my version of read.csv.sql](https://github.com/alyssafrazee/read.csv.sql))
