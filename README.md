# Logistic_Regression

This is deployment only file for Logistic Regression. These files can be used to deploy the logistic regression model in Heroku could platform. 

Problem Definition: Objective is to classify a person with given pregnancy, glucose, blood pressure, skin thickness, insulin, BMI, diabetic pedigree factor and 
age data into diabetic and non diabetic.

Model details: This binary classification problem was modelled using logistic regression classification. The trained model is saved as logistic_model.sav. 
The standard scaler model (logistic_stdscaler.sav) has also been saved for single person classification prediction. 

Flask App details: The application to host the diabetic classification problem was written using Flask. This app handles both single and bulk data input for the prediction. 
Incase of bulk data points, please use the myfile.xlsx to provide data to the app. 

https://diabetic-prediction.herokuapp.com/


