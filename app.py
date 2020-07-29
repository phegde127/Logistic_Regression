from flask import Flask, request, redirect, app, render_template
#from flask import Response
import numpy as np
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
import dataProcessing
import os

app = Flask(__name__)
CORS(app)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create route to display the home page
@app.route('/', methods=['GET'])
@cross_origin()

def homePage():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predictRoute():
    if request.method == 'POST':
        filename1 = 'logistic_model.sav'
        model = pickle.load(open(filename1, 'rb'))
        opt = request.form['entry']
        if opt == 'file':
            file = request.files['myfile']
            file.save(os.path.join(os.getcwd(), file.filename))

            try:
                file = request.files['myfile']
                file.stream.seek(0)  # seek to the beginning of file
                myfile = file.filename  # will point to tempfile itself
                data = pd.read_excel(myfile)
                if data[data['Insulin'] == 0].shape != 0:
                    processor = dataProcessing.Processing(data, 'Insulin')
                    processor.impute_random()
                if data[data['SkinTickness'] == 0].shape != 0:
                    processor = dataProcessing.Processing(data, 'SkinTickness')
                    processor.impute_random()
                data['Insulin_log'] = np.log(data['Insulin'])
                data['Age_log'] = np.log(data['Age'])
                data = data.drop(columns=['Age', 'Insulin'])
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(data)
                pred = model.predict(X_scaled)
                return render_template('results.html', prediction=pred)
            except Exception as e:
                print("The exception message is : ", e)
                return "Something is wrong"

        if opt == 'single':
            try:
                pregnancy = float(request.form['Pregnancies'])
                glucose = float(request.form['Glucose'])
                bp = float(request.form['Blood_Pressure'])
                st = float(request.form['Skin_Thickness'])
                bmi = float(request.form['BMI'])
                dpf = float(request.form['DPF'])
                insulin = float(request.form['Insulin'])
                insulin = np.log(insulin)
                age = float(request.form['Age'])
                age = np.log(age)
                filename2 = 'logistic_stdscaler.sav'
                scaler = pickle.load(open(filename2, 'rb'))
                prediction = model.predict(scaler.transform([[pregnancy, glucose, bp, st, bmi, dpf, insulin, age]]))
                if prediction == 0:
                    return render_template('results.html', prediction="{}, you are not diabetic.".format(prediction))
                else:
                    return render_template('results.html', prediction="{}, you are diabetic.".format(prediction))
            except Exception as e:
                print("The exception message is : ", e)
                return "Something is wrong"
        else:
            return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    #httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    #httpd.serve_forever()