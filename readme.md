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
| Preliminary methods           |    done   |
| Exploratory data analysis     |  current  |
| Write summary/abstract        |  current  | 
| Organize files                |           |
| Import into SQL db            |  revisit  |

## Introduction
Basketball is an exciting sport supported by many years of data on its players and teams through the last 20+ years. Throughout history, team managements and statisticians have created various metrics to evaluate player impact on the court. One of these metrics, the Player Efficiency Rating, was developed by John Hollinger to help describe a player's accomplishments and failures on the court for a given season. The Player Efficiency Rating is a single value derived from a variety of offensive and defensive player statistics relative to his peers. For any given season an average player would have a PER value of 15, while a rating of close to 30 represents a player who is exceptional compared to his peers. 

Currently, 30 NBA teams across two conferences play 82 games during the regular season hoping to qualify for one of 16 spots in the NBA playoffs. To earn a spot for the post-season, teams must have a win ratio above 0.5 and be in the top 4 for their respective conferences. Although PER is a good metric to quantify an individual player's ability on the court, it doesn't capture an entire team's ability. This project aims to investigate whether PER ratings of players correlate with their team's win ratio and therefore a predictive of a playoff spot.  


## Questions
1. Does PER significantly differ across basketball positions?
    * Box plot

2. Is there a relationship between Team PER value and win ratio?
    * Correlation

3. Can regular season Team PER values be used to predict post-season teams?
    * Regression Analysis

## Methods
### Data Source
Webscrapers were built to gather data from Basketball Reference's and ESPN's website. Player and team data was scraped from Basketball Reference for seasons spanning from 1998 to 2019. PER data was also scraped from ESPN to help validate PER calculations using Basketball Reference's data.

Note: PER generated from Basketball Reference's player and team data differs from the PER value taken from ESPN. Basketball Reference and ESPN have different PACE values. 

### Data Clean & Prep
PER was calculated for all players from 1998 - 2019, but this project focused on the top 12 individuals of minutes played for each team. By taking only the top 12 minutes played players, this helps account for any roster changes or inactivity throughout the season due trades, injuries, etc.

### Player Efficiency Rating Formula 
```sh
uPER = (1 / MP) *
     [ 3P
     + (2/3) * AST
     + (2 - factor * (team_AST / team_FG)) * FG
     + (FT *0.5 * (1 + (1 - (team_AST / team_FG)) + (2/3) * (team_AST / team_FG)))
     - VOP * TOV
     - VOP * DRB% * (FGA - FG)
     - VOP * 0.44 * (0.44 + (0.56 * DRB%)) * (FTA - FT)
     + VOP * (1 - DRB%) * (TRB - ORB)
     + VOP * DRB% * ORB
     + VOP * STL
     + VOP * DRB% * BLK
     - PF * ((lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP) ]


factor = (2 / 3) - (0.5 * (lg_AST / lg_FG)) / (2 * (lg_FG / lg_FT))
VOP    = lg_PTS / (lg_FGA - lg_ORB + lg_TOV + 0.44 * lg_FTA)
DRB%   = (lg_TRB - lg_ORB) / lg_TRB

Source: BasketBall Reference
```

## Results and Data Analysis
When examining the distribution of PER for players across each season, we see that most distributions are right-skewed. 
![Frequency Histogram](https://github.com/timmy224/NBA_Analysis/blob/master/images/Hist_Season_Player_PER.png?raw=true)

![Q-Q Plot](https://github.com/timmy224/NBA_Analysis/blob/master/images/QQ_Season_Player_PER.png?raw=true)

As a preliminary investigation, PER values for different positions were also examined. 
![Boxplot](https://github.com/timmy224/NBA_Analysis/blob/master/images/Boxplot_Pos_PER.png?raw=true)
All of the PER for different positions seem similar to each other with extreme PER values in the upper range.



3. Is there a relationship between Team PER value and win ratio?
UPDATE - finished calculating Team PER and Team Win Ratio
    * Correlation 
    * Regression
    * Q-Q plot, residuals plot for validation 

4. Can we use 


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