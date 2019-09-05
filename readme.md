# NBA Analysis - In Progress

## Priority
| Task List                     |   Status  | 
|:------------------------------|:---------:|
| Scrape data - BR              |    done   |
| Clean data - BR               |    done   |
| Scrape data - ESPN            |    done   |
| Clean data - ESPN             |    done   |
| Calculate PER - initial check |    done   |
| Add readme, requirements      |    done   |
| Calculate PER - all seasons   |    done   |
| Import into SQL db            |    done   |
| Work on Readme.md             |  current  |        
| Exploratory data analysis     |  current  |
| Reassess questions            |           |
| Preliminary methods           |           |
| Organize files                |           |
| Write summary/abstract        |           |

## Future

| Task List                     |   Status  | 
|:------------------------------|:---------:|
| Rewrite project in R          |           |
| Tableau Visuals               |           |

## Questions
1. Does PER significantly differ across basketball positions?
    * Box plot

2. Is there a relationship between Team PER value and win ratio?
    * Regression Analysis

3. How has basketball playstyle changed over the last 21 years? (i.e. seasons v. 3 points, 3pts v. win/loss ratio
    * Time Series 

## Methods
### Data Source
Webscrapers were built to gather data from Basketball Reference and ESPN's website. I initially scraped player and team data from Basketball Reference for seasons spanning from 1998 to 2019. I also decided to scrape ESPN's NBA data primarily for their player efficiency rating (PER) values as a validation for my PER calculations using Basketball Reference's data.

Note: PER generated from Basketball Reference's player and team data differs from the PER value taken from ESPN. Basketball Reference and ESPN have different PACE values. 

### Data Clean/Prep
I calculated PER for all players from 1998 - 2019, but only chose to work with the top 12 individuals of games minutes played because these players serve as the backbone for the majority of the season (accounting for trades, injuries, etc. as no to minimal minutes played relative to other players on team).


### Exploratory Data Analysis
1. What is the distribution of player PER values for each season? Is there a difference in distribution for any year?
    * Frequency Histogram - most distributions are right skewed
    * Q-Q Plot

2. What is the distribution of PER values for basketball positions? 
    
2. Do we need to transform data?
    * Boxcox plot

3. Correlation matrix 



## Notes

| Team Name                         | Season    | Team Abbrev |
|:----------------------------------|:---------:|:-----------:|
| New Jersey Nets                   | 1998-2012 |             |
| Brooklyn Nets                     | 2012-2019 |             |
| Vancouver Grizzlies               | 1998-2001 |             |
| Memphis Grizzlies                 | 2001-2019 |             |
| Seattle Supersonics               | 1998-2008 |             |
| Oklahoma City Thunder             | 2008-2019 |             |
| Charlotte Hornets                 | 1998-2002 | CHH         |
| Charlotte Bobcats                 | 2004-2014 | CHA         |
| Charlotte Hornets                 | 2014-2019 | CHO         |
| New Orleans Hornets               | 2002-2005 | NOH         |
| New Orleans/Oklahoma City Hornets | 2005-2007 | NOK         |
| New Orleans Hornets               | 2007-2013 | NOH         |
| New Orleans Pelicans              | 2013-2019 | NOP         |