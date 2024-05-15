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
