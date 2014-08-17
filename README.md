## gender of GitHub repo owners
-------------

This repository contains the code and data used to analyze the gender breakdown of owners of public GitHub repositories. [I wrote a blog post](http://alyssafrazee.com/gender-and-github-code.html) about what I found.

To reproduce the analysis, run scripts in the following order: 
* `get_github_info_byday.py`: uses the GitHub API to scrape repository data. (nb: This will take something like 60 hours to run).
* `merge_files.sh`: puts all scraped data together in a big text file
* `make_database.R`: dumps the scraped data into a SQLite database
* `analyze_data.py`: processes the data
* `bargraph.js`: JavaScript/D3 code used to make [the graphic showing the results](http://alyssafrazee.com/plgender.html). [Alex Wilson](https://github.com/alexandrinaw) made major contributions to this code.

#### data
The data I scraped in `get_github_info_byday.py` and processed with `merge_files.sh` and `make_database.R` is available in a .db file [here](https://www.dropbox.com/s/z0wh9hdf1mnnpu6/dat_anon.db?dl=0). I removed all repo owner last names.

#### dependencies
**Python libraries**: [PyGithub](http://jacquev6.github.io/PyGithub/v1/index.html), [Unidecode](https://pypi.python.org/pypi/Unidecode/0.04.16), [Pandas](http://pandas.pydata.org/), [SexMachine](https://pypi.python.org/pypi/SexMachine/), [Matplotlib](http://matplotlib.org/). Make sure these are installed before running scripts. See [requirements.txt](https://github.com/alyssafrazee/github_analysis/blob/master/requirements.txt) for a more detailed specification of Python dependencies, including versions. 

**R packages**: [devtools](http://cran.r-project.org/web/packages/devtools/index.html), [proto](http://cran.r-project.org/web/packages/proto/index.html), [DBI](http://cran.r-project.org/web/packages/DBI/index.html), [chron](http://cran.r-project.org/web/packages/chron/index.html), [RSQLite](http://cran.r-project.org/web/packages/RSQLite/index.html), and [RSQLITE.extfuns](http://cran.r-project.org/web/packages/RSQLite.extfuns/index.html). All can be installed from CRAN in R using the `install.packages` function. 
