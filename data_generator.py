'''
    @file Data Generator
    @description Create labelled dataset by parsing data from footballdata.co.uk Historical csv files
    @author Avinash Rai
    @datemodified 09/03/2021
'''
import os, sys
import csv, pickle, random
from utilities import *

def generateData(leagueCode, destination_file, goal_averages=False):

	datasets = []

	all_files = []
	for path, subdirs, files in os.walk("data"):
	    for name in files:
	    	if leagueCode in name:
	        	all_files.append( os.path.join(path, name) )

	# Single league
	for file in all_files:

		# print(file)
		
		# Get teams
		teams = getTeams(file)
		
		# Get all teams matches
		teamMatches = getTeamMatches(teams, file)
		
		teamMatchesCountList = []
		for k,v in teamMatches.items():
			teamMatchesCountList.append( len(v) )
		count = len(set(teamMatchesCountList))

		# 5 match interval
		pointer  = 5
		endPointer = max(teamMatchesCountList) - 1

		if count != 1:
			print("Trimmed: ", file )
			print( teamMatchesCountList )
			endPointer = min(teamMatchesCountList) - 1
			print( min(teamMatchesCountList), "matches used." )
            
		duplicateMatchFinder = []

		while pointer < endPointer:
            
			'''
				Phase 1 Collect Sample Data
			'''
			sampleEnd = pointer
			sampleStart = sampleEnd - 5
			sampleCurrent = sampleEnd

			sampleTeamFacts = {}
			leagueRankings = []

			for key,value in teamMatches.items():
				
				sampleTeamFacts[key] = {}

				total_matches_played  = 0
				total_wins            = 0
				total_draws           = 0
				total_losses          = 0
				total_goals_for       = 0
				total_goals_against   = 0
				points                = 0
				last_five_results     = []

				for i in range( 0, sampleEnd ):

					match = value[i]

					if match['HomeTeam'] == key or match['AwayTeam'] == key:
						total_matches_played += 1

						if match['FTR'] == 'D':
							total_draws += 1
							points += 1
							last_five_results.append(1)

						# Team is Home team
						if match['HomeTeam'] == key:

							if match['FTR'] == 'H':
								total_wins += 1
								points += 3
								last_five_results.append(3)
							elif match['FTR'] == 'A':
								total_losses += 1
								last_five_results.append(0)

							total_goals_for     = int(match['FTHG']) + total_goals_for
							total_goals_against = int(match['FTAG']) + total_goals_against  
																	
						elif match['AwayTeam'] == key:

							if match['FTR'] == 'A':
								total_wins += 1
								points += 3
								last_five_results.append(3)
							elif match['FTR'] == 'H':
								total_losses += 1
								last_five_results.append(0)
							
							total_goals_against = int(match['FTHG']) + total_goals_against  
							total_goals_for = int(match['FTAG']) + total_goals_for
						
				leagueRankings.append({
					"team" : key.strip(),
					"total_matches_played" : total_matches_played,
					"total_wins" : total_wins,
					"total_draws" : total_draws,
					"total_losses" : total_losses,            
					"total_goals_for" : total_goals_for,
					"total_goals_against" : total_goals_against,
					"goal_difference" : total_goals_for - total_goals_against ,
					"points" : points,
					"last_five_results": last_five_results[-5:]
				})
				
			leagueRankings = sorted(leagueRankings, key = lambda i: ( i['points'], i['goal_difference'], i['total_goals_for'] ), reverse=True )
			
            # Use averages of goals instead of total goals
			if goal_averages:
				import statistics
				league_goal_scored = []
				league_goal_conceded = []

				for item in leagueRankings:
					league_goal_scored.append(item["total_goals_for"])
					league_goal_conceded.append(item["total_goals_against"])

				avg_league_goal_scored = statistics.mean(league_goal_scored) 
				avg_league_goal_conceded = statistics.mean(league_goal_conceded)
            
			for index, value in enumerate(leagueRankings):
				key = value["team"]
				sampleTeamFacts[key]["position"] = int(index) + 1  
				last_five_results = value["last_five_results"]
				sampleTeamFacts[key].update( value )

                # Use averages of goals instead of total goals
				if goal_averages:
					goal_scoring_rating = value["total_goals_for"] / avg_league_goal_scored
					goal_conceded_rating = value["total_goals_against"] / avg_league_goal_conceded
					sampleTeamFacts[key]["total_goals_for"] = round(goal_scoring_rating, 4)
					sampleTeamFacts[key]["total_goals_against"] = round(goal_conceded_rating, 4)
                
				win_streak_3  = False
				win_streak_5  = False
				loss_streak_3 = False
				loss_streak_5 = False
                
				win_streak = 1 
				loss_streak = 1

				if last_five_results[2:].count(3) == 3:
					win_streak_3 = True

				if last_five_results.count(3) == 5:
					win_streak_5 = True

				if last_five_results[2:].count(0) == 3:
					loss_streak_3 = True

				if last_five_results.count(0) == 5:
					loss_streak_5 = True

				sampleTeamFacts[key]["win_streak_3"] = win_streak_3
				sampleTeamFacts[key]["win_streak_5"] = win_streak_5
				sampleTeamFacts[key]["loss_streak_3"] = loss_streak_3
				sampleTeamFacts[key]["loss_streak_5"] = loss_streak_5
            
            
			'''
				Phase 2 - Get Fixture data
			'''
			currentMatches = [] # Main
			
			for key,value in teamMatches.items():

				duplicate_key = str(value[sampleCurrent]["Date"] + value[sampleCurrent]["HomeTeam"] + value[sampleCurrent]["AwayTeam"]).strip()

				if not duplicate_key in duplicateMatchFinder:

					currentMatches.append({
						'DATE': value[sampleCurrent]['Date'].strip(),
						'HOME': value[sampleCurrent]['HomeTeam'].strip(),
						'AWAY': value[sampleCurrent]['AwayTeam'].strip(),
						'FTHG': int(value[sampleCurrent]['FTHG']),
						'FTAG': int(value[sampleCurrent]['FTAG']),
						'FTR': value[sampleCurrent]['FTR'].strip(),
					})

					duplicateMatchFinder.append( duplicate_key )
                      
			'''
				Phase 3 - Build Dataset
			'''
			for match in currentMatches:
				
				homeTeam = match["HOME"]
				awayTeam = match["AWAY"]

				datasets.append({
					# "key": match["DATE"] + " " + homeTeam + " "+ awayTeam,
	               	"HTGS": sampleTeamFacts[homeTeam]["total_goals_for"],
	               	"ATGS": sampleTeamFacts[awayTeam]["total_goals_for"],				
	               	"HTGC": sampleTeamFacts[homeTeam]["total_goals_against"],
	               	"ATGC": sampleTeamFacts[awayTeam]["total_goals_against"],
	               	"HTP": sampleTeamFacts[homeTeam]["points"],
	               	"ATP": sampleTeamFacts[awayTeam]["points"],

	               	"HM1": sampleTeamFacts[homeTeam]["last_five_results"][0],
	               	"HM2": sampleTeamFacts[homeTeam]["last_five_results"][1],
	               	"HM3": sampleTeamFacts[homeTeam]["last_five_results"][2],
	               	"HM4": sampleTeamFacts[homeTeam]["last_five_results"][3],
	               	"HM5": sampleTeamFacts[homeTeam]["last_five_results"][4],
	               	"AM1": sampleTeamFacts[awayTeam]["last_five_results"][0],
	               	"AM2": sampleTeamFacts[awayTeam]["last_five_results"][1],
	               	"AM3": sampleTeamFacts[awayTeam]["last_five_results"][2],
	               	"AM4": sampleTeamFacts[awayTeam]["last_five_results"][3],
	               	"AM5": sampleTeamFacts[awayTeam]["last_five_results"][4],

	               	"HTWinStreak3": (0,1) [ sampleTeamFacts[homeTeam]["win_streak_3"] ],
	               	"HTWinStreak5": (0,1) [ sampleTeamFacts[homeTeam]["win_streak_5"] ],
	               	"HTLossStreak3": (0,1) [ sampleTeamFacts[homeTeam]["loss_streak_3"] ],
	               	"HTLossStreak5": (0,1) [ sampleTeamFacts[homeTeam]["loss_streak_5"] ],

	               	"ATWinStreak3": (0,1) [ sampleTeamFacts[awayTeam]["win_streak_3"] ],
	               	"ATWinStreak5": (0,1) [ sampleTeamFacts[awayTeam]["win_streak_5"] ],
	               	"ATLossStreak3": (0,1) [ sampleTeamFacts[awayTeam]["loss_streak_3"] ],
	               	"ATLossStreak5": (0,1) [ sampleTeamFacts[awayTeam]["loss_streak_5"] ],

	               	"HTGD": sampleTeamFacts[homeTeam]["goal_difference"],
	               	"ATGD": sampleTeamFacts[awayTeam]["goal_difference"],
	               	"DiffPts": sampleTeamFacts[homeTeam]["points"] - sampleTeamFacts[awayTeam]["points"],
	               	"DiffFormPts": sum(sampleTeamFacts[homeTeam]["last_five_results"]) - sum(sampleTeamFacts[awayTeam]["last_five_results"]),
	               	"DiffLP": sampleTeamFacts[homeTeam]["position"] - sampleTeamFacts[awayTeam]["position"],
					
                    # Label
                    "FTR" : encode_ftr( match['FTR'])
				})
            
			pointer += 1
		
	print(len(datasets), "datasets available.")
	random.shuffle(datasets)

	dest_filename = destination_file
	if goal_averages:
		dest_filename = dest_filename + "-average-goals"
	dest_filename = dest_filename + ".pickle"

	with open( dest_filename, 'wb') as f:
		pickle.dump(datasets, f)
	
	print("File saved:", dest_filename, "\n" )

# MAIN
generateData("E0", "pickles\\dataset-epl", False)
generateData("SP1", "pickles\\dataset-spl", False)