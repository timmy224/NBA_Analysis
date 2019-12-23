# NBA Analysis - In Progress

## Introduction
Basketball is an exciting sport with many years of recorded data on its players and teams throughout the last 20+ years. In its history, team managements and statisticians have created various metrics to evaluate player impact on the court. One of these metrics, the Player Efficiency Rating, was developed by John Hollinger to help describe a player's accomplishments and failures on the court for a given season. The Player Efficiency Rating is a single value derived from a variety of offensive and defensive player statistics relative to his peers. For any given season, an average player will have a PER value of 15, while a rating of close to 30 represents a player who is exceptional compared to his peers. 

Currently, 30 NBA teams across two conferences play 82 games during the regular season hoping to qualify for one of 16 spots in the NBA playoffs. To earn a spot for the post-season, teams must have a win ratio above 0.5 and be in the top 8 of their respective conferences. Although PER is a good metric to quantify an individual player's ability on the court, it doesn't capture an entire team's ability. This project aims to determine whether PER ratings of players correlate with their team's win ratio and if it can be predictive of a playoff spot.  


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
PER was calculated for all players from 1998 - 2019, but this project focused on the top 12 individuals of minutes played for each team. By taking only the top 12 minutes played (MP) players, this helps account for any roster changes or inactivity throughout the season due trades, injuries, etc.

### Player Efficiency Rating Formula 
```
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
### Regression Analysis
For the simplicity of this personal project, only the last 3 seasons were used to investigate whether team PER correlated with win ratio. 

Team PER was calculated by taking the PERs of the top 12 MP players and multiplying it with their respective minutes played. PER is a per-minute rating so by multiplying it with minutes played, it gives players with more minutes played more weight in the team PER value. If a high PER player doesn't play as many minutes, he may not contribute as much to team PER relative to a teammate who has average PER but has played a higher number of minutes. 

Because preliminary data showed that our data was heteroscedastic, a BoxCox test and transformation was applied to team PER values to make it more homoscedastic. BoxCox test returned a lambda of ~0.546, which corresponds to a log transformation of the data. 

Linear models were created using Ordinary Least Squares and evaluated using adjusted R^2, F-statistic from Wald test, residual, and Q-Q plots. 

## Results and Data Analysis
When examining the distribution of PER for players across each season, we see that most distributions are right-skewed. 
![Frequency Histogram](https://github.com/timmy224/NBA_Analysis/blob/master/images/Hist_Season_Player_PER.png?raw=true)

![Q-Q Plot](https://github.com/timmy224/NBA_Analysis/blob/master/images/QQ_Season_Player_PER.png?raw=true)

As a preliminary investigation, PER values for different positions were also examined. 
![Boxplot](https://github.com/timmy224/NBA_Analysis/blob/master/images/Boxplot_Pos_PER.png?raw=true)
All of the PER for different positions seem similar to each other with extreme PER values in the upper range.

### 2016 - 2017 Regular Season
There is a distinct linear trend when examining the correlation between Team PER and win ratio. When comparing teams belonging to different conferences, the Western Conference comparatively has stronger teams indicated by the cluster representing high team PER and win ratio. 
![Corr_2016-2017](https://github.com/timmy224/NBA_Analysis/blob/master/images/Corr_16-17.png?raw=true) 

The summary of our linear model showed an adjusted R^2 of 0.633 and a significant F-statistic. However, when evaluating our model with residuals, we can see there are extreme residuals (especially Minnesota Timberwolves) with an overestimation for lower team PER. Our probability value for Omnibus is low which supports that residuals are not normally distributed. Extreme deviations at the tails will skew distribution as observed in the Q-Q plot. 

<p float="center">
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/OLS_16-17.png?raw=true" width="290" />
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/Residual_16-17.png?raw=true" width="290" /> 
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/QQ_16-17.png?raw=true" width="290" />
</p>

### 2017 - 2018 Regular Season
In the 2017-2018 regular season, we can see that the Golden State Warriors are no longer the team with the highest PER. The Houston Rockets, Toronto Raptors, and Minnesota Timberwolves appear to have similar team PER, but different win ratios. As observed again, the Western Conference shows a strong correlation for having teams with higher PER and win ratio with a larger cluster in the upright portion of the graph. 
![Corr_2017-2018](https://github.com/timmy224/NBA_Analysis/blob/master/images/Corr_17-18.png?raw=true) 

There is an improvement for this season's linear model with an adjusted R^2 of 0.711 and significant F-statistic explaining the variability in data. Despite an improved probability for Omnibus (0.909)  and random pattern in our residuals plot, there are clear outliers in our data as represented by Phoenix, Memphis, Boston, and Minnesota teams. According to the Q-Q plot, there seems to be fewer deviations from the predicted team PER values relative to the previous season. 

<p float="center">
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/OLS_17-18.png?raw=true" width="290" />
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/Residual_17-18.png?raw=true" width="290" /> 
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/QQ_17-18.png?raw=true" width="290" />
</p>

### 2018 - 2019 Regular Season
Compared to the previous season, the Memphis Grizzlies and Phoenix Suns deviate from this linear model with the Memphis Grizzlies having a higher win ratio with similar Team PER, and the Pheonix Suns having similar win ratio and Team PER.
![Corr_2018-2019](https://github.com/timmy224/NBA_Analysis/blob/master/images/Corr_18-19.png?raw=true)
 
The summary of our linear model indicated that our model had an adjusted R^2 of 0.722 and significant according to F-statistics. The residuals do not appear to be randomly dispersed with a low Omnibus probability value of 0.081 indicating our residuals are not normally distributed. There is also moderate skew as indicated by the skew value of -0.816 and Q-Q plot. 

<p float="center">
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/OLS_18-19.png?raw=true" width="290" />
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/Residual_18-19.png?raw=true" width="290" /> 
  <img src="https://github.com/timmy224/NBA_Analysis/blob/master/images/QQ_18-19.png?raw=true" width="290" />
</p>


### Prediction: OLS (StatsModel)
Despite the different fits of linear models to previous season data, they were used to test against 2018-2019 data to determine if Team PER can be used to predict win ratio in the following season. When looking at the following graph, after the first 10 rankings, the residuals between (both 2016-2017 and 2017-2018) increase dramatically. 

![Pred_18-19](https://github.com/timmy224/NBA_Analysis/blob/master/images/Pred_18-19.png?raw=true)

### Top 16 teams 
Using the linear regression generated from data of 2017 - 2018, 10 out of 16 (62.5%) teams were correctly predicted to qualify for playoffs using the 2017-2018 model (bolded team abbreviations were not predicted).  

<center>
####                        Eastern Conference                     
|      Actual  2018 - 2019      |  Prediction 16-17, 17-18 model  |
|:-----------------------------:|:-------------------------------:|
|              MIL              |                BOS              | 
|              TOR              |                MIL              |
|            **PHI**            |                TOR              |
|              BOS              |                IND              |
|              IND              |                ORL              |
|              BRK              |              **CHO**            |
|              ORL              |              **MIA**            |
|            **DET**            |                BRK              | 

####                         Western Conference                      
|      Actual  2018 - 2019      |  Prediction 16-17, 17-18 model  |
|:-----------------------------:|:-------------------------------:|
|              GSW              |                GSW              |
|              DEN              |                SAS              |
|              POR              |                DEN              |
|              HOU              |                HOU              |
|              UTA              |                POR              |
|              OKC              |                OKC              |
|              SAS              |                UTA              |
|            **LAC**            |              **MIN**            |

</center>

## Discussion
As seen with data from the last 3 seasons, there is a clear linear relationship between Team PER and win ratio. This relationship makes sense given that teams with higher PER should perform better, thus win more games during the season. While our linear models were significant with supporting adjusted R^2 and F-statistic values from Wald test, there were outliers in our data, thus increasing the variability in our model. While team PER from the previous season can predict the majority of teams that will make the playoffs the subsequent season, it isn't reliable with a 62.5% accuracy.

There can be many explanations for the outliers. For high PER teams that underperform, this may be caused by high PER players who play alot of minutes but do not consistently win games. This could be represented by teams that have one or two star players but a weak bench resulting in high effiency from those players, but a low win ratio. For low PER teams that overperform, this can be caused by the exact opposite where high performing players are aren't playing as much during a game but the bench players are. A scenario where this can occur is when a team has a good lead early in the game and star players are benched for injury prevention or rest for future games. 

Overall, PER may not be the best indicator for defensive statistics. As stated by John Hollinger, PER is not a reliable measure of defensive acumen as it only incorporates active stats such as blocks and steals which do not always explain a player's contribution to the team's defense. By incorporating another metric that better describes a player's defensive performance, we may reduce unexplained variability in our model. 

## Future Directions
Because PER is a metric that involves many basketball statistics, I'd like to do a machine learning project that uses player stats, instead of PER, across seasons to determine which stat(s) can give the best prediction for win ratio and playoff appearance. 

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
| Data analysis                 |    done   |
| Projections                   |    done   |
| Write summary/abstract        |    done   | 
| Organize files                |    done   |
| Update requirements           |           |
| Import into SQL db            |           |

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

