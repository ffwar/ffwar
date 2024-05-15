In this repository, you will find all related data, code, and results to the WAR caculations and associated analyses. 

**How WAR is Calculated**

The method used for calculating WAR is simulation. For each player, and each season they played in from 2001 through 2023, we simulated 1000 seasons with that player locked into the starting lineup (For the number of games played), observed the average number of wins achieved by the team with that player. And then we simulated 1000 seasons with a "replacement level player" locked in to that same positional slot and compared the wins generated by each instance. For example if the average wins for a team with Keenan Allen locked into a WR slot was 8 and the average wins with a replacement level WR was 6, Keenan Allen's WAR for the season would be 2. 

**How Games were Simulated**

For these calculations the following league settings were used:

12 Teams

2 QB

2 RB

2 WR

2 Flex

1 TE

Then based on these numbers, a player pool count was determined for each position which was equal to (Number_Started + 1) * (Number of teams). Flex postions are counted as .5 for both WR and RB. This was an attempt to approximate the number of players which are used by a league in a given year. This is likely not perfect and a potential weakness of this method of calculation. Then, for a given year, and position, players are sorted by their points per game, and the top X (X = postions pool count) are selected into the player pool. A flex pool is created which is simply the RB and WR pools combined. Each pool is then distilled futher into a list of game results from every player in the pool called the pool_scores.

For each simulated game, an opponent score is generated based on random draws from each positions pool_scores. While in a single simulation, this may produce a very low or very high score, over a large number of simulations this attempts to mimic the scores and variation of a random teams score for a random week. Next a player score is generated using the same process, except that for the position of the player who is being simulated, one of the pool_scores is replaced by a random draw of the players score from that year. 

This simulation is then done for the number of games a player played and the results are noted against expectation. So if Joe Mixon only played 12 games in a year, for each iteration, 12 games would be simulated, and wins would be tallied for those 12 games and compared to the wins a replacement level player would have in 12 simulated games. The result of this is that if 2 players have the same game to game impact on winning in a year, but player A played twice the games as player B, player A's WAR would be twice that of player B's. 
