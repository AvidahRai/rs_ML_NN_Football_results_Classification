# rs_ML_NN_Football_results_Classification
Football match result prediction using Machine Learning algorithms and Neural Networks

I have tried to replicate the work from this article https://medium.com/@rolandshum.shc/neural-networks-football-result-prediction-d8b0f933118b by "Roland Shum". 
I have followed his methods and implementation to achieve the same accuracy from the models.

However, his method of labelled data extraction is different from mine. I have only used data from footballdata.co.uk Historical football results files (https://www.football-data.co.uk/data.php). I had manually downloaded the Historicals results CSV files for English Premier League EPL and Spanish La Liga SPL (refer to /data/README.txt). My python program <b>[data_generator.py](data_generator.py)</b> parses all the CSV files in the /data folder to generate the labelled dataset containing both features and labels. The features generated are identical to the features used in the author's project. However my program is dynamic and also designed to extract dataset from ongoing season file.   

<b>[utilities.py](utilities.py)</b> file contains all helper functions. One of the function <b>getTrainTestDataset()</b> returns the prepared training and testing set.

<b>[ 1. Classification_Models.ipynb ](1.%20Classification%20Models.ipynb)</b><br/>
The first set of experiments were done using Scikit Learn Classifiers :- Logistic regression, XGBoost, Decision Trees and Support Vector Classifier. The experiments were done on  both EPL and SPL datasets. The accuracy reached was around 42-54%, with Support Vector Classifier performing the best among them.

<b>[ 2. Neural Networks - Original.ipynb ](2.%20Neural%20Networks%20-%20Original.ipynb)</b><br/>
Two main Neural Network models were produced using Keras models with the exact configurations detailed by the author. The architecture consisted of (1) layer size of 41-75-3, learning rate of 1e-05, batch size of 16 and dropout rate of 0.5 for EPL dataset and (2) layer size of 41-10-10-3, learning rate of 1e-05, batch size of 32 and dropout rate of 0 for SPL dataset. He had determined the configurations after doing long experiments of hyperparameter tuning. 
<br/> In my models, I had applied EarlyStopping to check if the validation loss does not increase after 5 tries. The training stops if the loss increases after 5 tries. The epochs was set to 500. <br/>
The validation accuracy achieved by EPL NN and SPL NN were <b>50.34%</b> and <b>49.83%</b> respectively. These NN models had underperfomed compared to author's 62% and 54% accuracy. This could be because my dataset is slightly different from the author's dataset.

<b>[ 3. Neural Networks - Optimisation.ipynb ](3.%20Neural%20Networks%20-%20Optimisation.ipynb)</b><br/>
This is my attempt to improve the models. <br/>
1) First I used ExtraTreeClassifier to visualise the most important features on both datasets. I had spliced both datasets to only contain the 11 most important features. I trained these new datasets using the same configurations/parameter as before. The accuracy improvement was not significant.<br/>
2) Keeping the no. of features same, I have implemented automatic learning rate reduction using Keras "ReduceLROnPlateau" callback. The validation accuracy improved slightly  <b>53.55%</b> and <b>52.23%</b>.

<b>Next experiments</b></br>
1) Different Layer Sizes
2) More Dataset
3) Dropout rate
4) Grid search
