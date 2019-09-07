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

## Introduction
Player Efficiency Rating is a metric developed by John Hollinger one type of metric used describe a player's accomplishments and failures on the court for a given season. A PER value of 15 is the average rating of a player, while a rating of approaching 30 represents a player who is exceptional compared to his peers. 

## Questions
1. Does PER significantly differ across basketball positions?
    * Box plot

2. Is there a relationship between Team PER value and win ratio?
    * Regression Analysis

3. How has basketball playstyle changed over the last 21 years? (i.e. seasons v. 3 points, 3pts v. win/loss ratio
    * Time Series 

## Methods
### Data Source
Webscrapers were built to gather data from Basketball Reference and ESPN's website. I initially scraped player and team data from Basketball Reference for seasons spanning from 1998 to 2019. I also decided to scrape ESPN's NBA data primarily for their PER values as a validation for my PER calculations using Basketball Reference's data.

Note: PER generated from Basketball Reference's player and team data differs from the PER value taken from ESPN. Basketball Reference and ESPN have different PACE values. 

### Data Clean/Prep
I calculated PER for all players from 1998 - 2019, but only chose to work with the top 12 individuals of games minutes played because these players serve as the roster for the majority of the season (accounting for trades, injuries, etc. as none to minimal minutes played relative to other players on team).

1. What is the distribution of player PER values for each season?
    * Frequency Histogram - most distributions are right skewed
    * Q-Q Plot - some distributions are right-skewed or some just have heavy right tails 

2. What is the distribution of PER values for basketball positions? 
    * Mean PER values were relatively the same across all positions

3. Is there a relationship between Team PER value and win ratio?
UPDATE - finished calculating Team PER and Team Win Ratio
    * Regression
    * Q-Q plot, residuals plot for validation 

4. How has 3-pt shooting changed over the years? 


## Future

| Task List                     |   Status  | 
|:------------------------------|:---------:|
| Rewrite project in R          |           |
| Tableau Visuals               |           |

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