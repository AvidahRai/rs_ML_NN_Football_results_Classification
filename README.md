# rs_ML_NN_Football_results_Classification
Football match result prediction using ML algorithms and Neural Networks

I have tried to replicate the work from this article https://medium.com/@rolandshum.shc/neural-networks-football-result-prediction-d8b0f933118b by "Roland Shum". 
I have followed his methods and implementation to achieve the same accuracy from the models.

However, his method of labelled data extraction is different from mine. I have only used data from footballdata.co.uk Historical football results files (https://www.football-data.co.uk/data.php). I had manually downloaded the Historicals results CSV files for English Premier League and Spanish La Liga (refer to /data/README.txt). My python program <b>data_generator.py</b> parses all the CSV files in the /data folder to generate the labelled dataset containing features and labels. The features generated are identical to the features used in the author's project. However my program is dynamic and also designed to extract dataset from ongoing season.   
