'''
    @file Utilies
    @description Contains utility (helper) functions
    @author Avinash Rai
    @datemodified 09/03/2021
'''
import csv
import itertools
import os
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

'''
    Get teams name from footballdata.co.uk historical data csv file
    @filename | string | Name of the file
    @return List
'''
def getTeams( filename ):
    teams = []
    with open( filename ) as file:
        reader = csv.DictReader(file)
        for row in reader:

            homeTeam = row['HomeTeam'].strip()
            awayTeam = row['AwayTeam'].strip()

            if not( homeTeam in teams) or not( awayTeam in teams ):
                if not  homeTeam == '' and not  awayTeam == '':
                    if not( homeTeam in teams):
                        teams.append( homeTeam )
                    elif not( awayTeam in teams):
                        teams.append( awayTeam )
    return teams

'''
    Get dictionary of team and all the matches played from footballdata.co.uk historical data csv file
    @teams | List | List of team names
    @filename | string | Name of the file
    @return Dict
'''
def getTeamMatches( teams, filename ):
    teamMatches = {}
    for team in teams:
        if not team in teamMatches:
            teamMatches[team] = []

        with open( filename ) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if  row['HomeTeam'] == team or row['AwayTeam'] == team:
                    
                    sliceRow = dict(itertools.islice(row.items(), 23 ))
                    teamMatches[ team ].append(sliceRow)
    
    return teamMatches

'''
    Encode Full time result string to numerical value
    @result_string | string | Result string between H, D, A
    @return int
'''
def encode_ftr( result_string ):
    result = 0
    if result_string == 'H':
        result = 0
    elif result_string == 'D':
        result = 1
    elif result_string == 'A':
        result = 2
    return result

'''
    Decode Full time result from numerical value to string value
    @result_string | string | Result string between 0, 1, 2
    @return int
'''
def decode_ftr( numerical ):
    string = ""
    if numerical == 0:
        string = 'H'
    elif numerical == 1:
        string = 'D'
    elif numerical == 2:
        string = 'A'
    return string    
    
'''
    Data Preparation
        1) Extract labels 
        2) Selectively normalise the features of the dataset 
        3) Convert the whole dataset to Pandas dataframe
        4) Split the dataset into Training set and Testing set 
    @filename | string | Name of the Pickle file that contains the labelled datasets
    @return dataframe, dataframe, dataframe, dataframe
'''
def getTrainTestDataset(filename):

    with open( filename, 'rb') as file:
        datasets = pickle.load(file)
        df = pd.DataFrame(datasets)
        df = df.dropna()
        # df = df.sample(frac=1) # Shuffle

    labels = df[["FTR"]]
    unscalables = df[["HM1","HM2","HM3","HM4","HM5","AM1","AM2","AM3","AM4","AM5",
                    "HTWinStreak3", "HTWinStreak5", "HTLossStreak3", "HTLossStreak5",
                    "ATWinStreak3", "ATWinStreak5","ATLossStreak3","ATLossStreak5","DiffLP" ]]

    df = df.drop(columns=[ "HM1","HM2","HM3","HM4","HM5","AM1","AM2","AM3","AM4","AM5",
        "HTWinStreak3", "HTWinStreak5", "HTLossStreak3", "HTLossStreak5",
        "ATWinStreak3", "ATWinStreak5","ATLossStreak3","ATLossStreak5", "DiffLP", "FTR" ])

    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    main_input = pd.concat([ df_scaled, unscalables], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(main_input, labels, test_size=0.33, random_state=1)

    return X_train, X_test, y_train, y_test

'''
    Plot pretty confusion matrix (Works only for Scikit Learn Models)
    @fitted_model | obj | Trained Scikit Learn model object
    @X | dataframe | Testing features
    @y | dataframe | Testing labels
    @return None
'''    
def cat_3_confusion_matrix( fitted_model, X, y):

    matrix = metrics.plot_confusion_matrix( fitted_model, X, y, 
                                           display_labels=['H','D','A'], values_format = '.0f')
    matrix.ax_.set_title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Truth')
    plt.show()