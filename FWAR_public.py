# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:42:29 2024

"""
import pandas as pd
import random

def yearly_df(df, year):
    df = df[df['Year']==year]
    players = df.Name.unique()
    players_list = []
    for player in players:
        player_df = df[df['Name']==player]
        totalscore = pd.to_numeric(player_df['PTS']).sum()
        scorelist = pd.to_numeric(player_df['PTS']).tolist()
        players_list.append([player,scorelist,totalscore,totalscore/len(scorelist)])
    final_df = pd.DataFrame(players_list,columns=['Name','Games','Score','Score Per Game'])
    return final_df

qbs_df = pd.read_csv('qb_logs.csv')
rbs_df = pd.read_csv('rb_logs.csv')
wrs_df = pd.read_csv('wr_logs.csv')
tes_df = pd.read_csv('te_logs.csv')

teams = 12
qbs = 2
rbs = 2
wrs = 2
flex = 2
tes = 1

##Determine Player Pool

rb_pool_count = int((rbs + (flex*.5) + 1) * teams)
wr_pool_count = int((wrs + (flex*.5) + 1) * teams)
qb_pool_count = int((qbs + 1) * teams)
te_pool_count = int((tes + 1) * teams)
results = []

year_list = list(range(2001,2024))
for Year in year_list:
    
    
    #Establish Years DF
    
    ##QB
    QB_Year = yearly_df(qbs_df, Year)
    QB_pool = QB_Year.sort_values('Score Per Game',ascending = False).head(qb_pool_count+teams)[0:qb_pool_count]
    QB_pool_scores = sum(QB_pool['Games'].tolist(),[])
    QB_replacement_pool = QB_Year.sort_values('Score Per Game',ascending = False).head(qb_pool_count+teams)[qb_pool_count:qb_pool_count+teams]
    QB_replacement_pool_scores = sum(QB_replacement_pool['Games'].tolist(),[])
    
    ##RB
    RB_Year = yearly_df(rbs_df, Year)
    RB_pool = RB_Year.sort_values('Score Per Game',ascending = False).head(rb_pool_count+teams)[0:rb_pool_count]
    RB_pool_scores = sum(RB_pool['Games'].tolist(),[])
    RB_replacement_pool = RB_Year.sort_values('Score Per Game',ascending = False).head(rb_pool_count+teams)[rb_pool_count:rb_pool_count+teams]
    RB_replacement_pool_scores = sum(RB_replacement_pool['Games'].tolist(),[])
    
    ##WR
    WR_Year = yearly_df(wrs_df, Year)
    WR_pool = WR_Year.sort_values('Score Per Game',ascending = False).head(wr_pool_count+teams)[0:wr_pool_count]
    WR_pool_scores = sum(WR_pool['Games'].tolist(),[])
    WR_replacement_pool = WR_Year.sort_values('Score Per Game',ascending = False).head(wr_pool_count+teams)[wr_pool_count:wr_pool_count+teams]
    WR_replacement_pool_scores = sum(WR_replacement_pool['Games'].tolist(),[])
    
    ##TE
    TE_Year = yearly_df(tes_df, Year)
    TE_pool = TE_Year.sort_values('Score Per Game',ascending = False).head(te_pool_count+teams)[0:te_pool_count]
    TE_pool_scores = sum(TE_pool['Games'].tolist(),[])
    TE_replacement_pool = TE_Year.sort_values('Score Per Game',ascending = False).head(te_pool_count+teams)[te_pool_count:te_pool_count+teams]
    TE_replacement_pool_scores = sum(TE_replacement_pool['Games'].tolist(),[])
    
    ##FLEX
    Flex_pool = pd.concat([RB_pool,WR_pool])
    Flex_pool_scores = sum(Flex_pool['Games'].tolist(),[])

    for POS in ['QB','RB','WR','TE']:
        if POS == 'QB':
            names = QB_Year.Name.unique()
        if POS == 'RB':
            names = RB_Year.Name.unique()
        if POS == 'WR':
            names = WR_Year.Name.unique()
        if POS == 'TE':
            names = TE_Year.Name.unique()
        WOE = 0
        for i in range(1,1000):
            for k in range(0,17):
                players_team = 0
                opp_team = 0
                ##QB
                for j in range(0,qbs):
                    opp_team += random.choice(QB_pool_scores)
                if POS == 'QB':
                    for j in range(0,qbs-1):
                        players_team += random.choice(QB_pool_scores)
                else:
                    for j in range(0,qbs):
                        players_team += random.choice(QB_pool_scores)        
                ##RB
                for j in range(0,rbs):
                    opp_team += random.choice(RB_pool_scores)
                if POS == 'RB':
                    for j in range(0,rbs-1):
                        players_team += random.choice(RB_pool_scores)
                else:
                    for j in range(0,rbs):
                        players_team += random.choice(RB_pool_scores)          
                ##WR
                for j in range(0,wrs):
                    opp_team += random.choice(WR_pool_scores)
                if POS == 'WR':
                    for j in range(0,wrs-1):
                        players_team += random.choice(WR_pool_scores)
                else:
                    for j in range(0,wrs):
                        players_team += random.choice(WR_pool_scores)      
                ##TE
                for j in range(0,tes):
                    opp_team += random.choice(TE_pool_scores)
                if POS == 'TE':
                    for j in range(0,tes-1):
                        players_team += random.choice(TE_pool_scores)
                else:
                    for j in range(0,tes):
                        players_team += random.choice(TE_pool_scores) 
                ##FLEX
                for j in range(0,flex):
                    opp_team += random.choice(Flex_pool_scores)
                    players_team += random.choice(Flex_pool_scores)
                ##Player
                if POS == 'QB':
                    players_team += random.choice(QB_replacement_pool_scores)
                if POS == 'RB':
                    players_team += random.choice(RB_replacement_pool_scores)
                if POS == 'WR':
                    players_team += random.choice(WR_replacement_pool_scores)
                if POS == 'TE':
                    players_team += random.choice(TE_replacement_pool_scores)
                if players_team > opp_team:
                    WOE += .5
                else:
                    WOE -= .5
            replacement_level_woe = WOE/i
        RLWOE_Per_Game = replacement_level_woe/17
        print('pos: '+POS+' RLWOE '+str(replacement_level_woe))
        
        for Player in names:
            WOE = 0
            for i in range(1,1000):
                if POS == 'QB':
                    games_played = len(QB_Year[QB_Year['Name']==Player]['Games'].iloc[0])
                if POS == 'RB':
                    games_played = len(RB_Year[RB_Year['Name']==Player]['Games'].iloc[0])
                if POS == 'WR':
                    games_played = len(WR_Year[WR_Year['Name']==Player]['Games'].iloc[0])
                if POS == 'TE':
                    games_played = len(TE_Year[TE_Year['Name']==Player]['Games'].iloc[0])
                for k in range(0,games_played):
                    players_team = 0
                    opp_team = 0
                    ##QB
                    for j in range(0,qbs):
                        opp_team += random.choice(QB_pool_scores)
                    if POS == 'QB':
                        for j in range(0,qbs-1):
                            players_team += random.choice(QB_pool_scores)
                    else:
                        for j in range(0,qbs):
                            players_team += random.choice(QB_pool_scores)        
                    ##RB
                    for j in range(0,rbs):
                        opp_team += random.choice(RB_pool_scores)
                    if POS == 'RB':
                        for j in range(0,rbs-1):
                            players_team += random.choice(RB_pool_scores)
                    else:
                        for j in range(0,rbs):
                            players_team += random.choice(RB_pool_scores)          
                    ##WR
                    for j in range(0,wrs):
                        opp_team += random.choice(WR_pool_scores)
                    if POS == 'WR':
                        for j in range(0,wrs-1):
                            players_team += random.choice(WR_pool_scores)
                    else:
                        for j in range(0,wrs):
                            players_team += random.choice(WR_pool_scores)      
                    ##TE
                    for j in range(0,tes):
                        opp_team += random.choice(TE_pool_scores)
                    if POS == 'TE':
                        for j in range(0,tes-1):
                            players_team += random.choice(TE_pool_scores)
                    else:
                        for j in range(0,tes):
                            players_team += random.choice(TE_pool_scores) 
                    ##FLEX
                    for j in range(0,flex):
                        opp_team += random.choice(Flex_pool_scores)
                        players_team += random.choice(Flex_pool_scores)
                    ##Player
                    if POS == 'QB':
                        players_team += random.choice(QB_Year[QB_Year['Name']==Player]['Games'].iloc[0])
                    if POS == 'RB':
                        players_team += random.choice(RB_Year[RB_Year['Name']==Player]['Games'].iloc[0])
                    if POS == 'WR':
                        players_team += random.choice(WR_Year[WR_Year['Name']==Player]['Games'].iloc[0])
                    if POS == 'TE':
                        players_team += random.choice(TE_Year[TE_Year['Name']==Player]['Games'].iloc[0])
                    if players_team > opp_team:
                        WOE += .5
                    else:
                        WOE -= .5
                AVG_WOE = WOE/i
            print([Year,POS,Player,AVG_WOE,AVG_WOE - (games_played*RLWOE_Per_Game)])
            results.append([Year,POS,Player,AVG_WOE,AVG_WOE - (games_played*RLWOE_Per_Game)])
            
            
results_df = pd.DataFrame(results,columns=['Year','pos','player','WOE','WAR'])


non_neg_results = results_df
non_neg_results.loc[non_neg_results['WAR'] <0, 'WAR'] = 0

alltime_war = non_neg_results.groupby('player').sum()

player = non_neg_results[non_neg_results['player']==' CeeDee Lamb'][['Year','WAR']]
ax = player.plot.area(x='Year',y='WAR')

