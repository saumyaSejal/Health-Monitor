from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

app = Flask(__name__)

with open('Capstone\models\ensemble_heart.pickle', 'rb') as f:
    # Load the object from the file
    ensem = pickle.load(f)

with open('Capstone\models\standardScaler.pickle', 'rb') as f:
    # Load the object from the file
    std = pickle.load(f)

# Open the file in binary read mode
with open('Capstone\models\Scale_sleep.pickle', 'rb') as f:
    # Load the object from the file
    scl_sleep = pickle.load(f)

# Open the file in binary read mode
with open('Capstone\models\ensemble_sleep.pickle', 'rb') as f:
    # Load the object from the file
    ensem_sleep = pickle.load(f)


# Function to predict heart disease
def predict_disease(input_data, std_scale, model):
    # Reshape input data
    input_data_array = np.asarray(input_data)
    input_data_reshaped = input_data_array.reshape(1, -1)
    scaled_data = std_scale.transform(input_data_reshaped)
    # Make prediction
    prediction = model.predict(scaled_data)
    return prediction

risk = ""
input_data = tuple()

@app.route('/')
def homepage():
   return render_template('homepage.html')

@app.route('/heart')
def heart():
   return render_template('heartattack.html')

@app.route('/sleep')
def sleep():
   return render_template('sleepdisorder.html')

@app.route('/hrisk', methods = ['POST','GET'])
def hrisk():
    if request.method == 'POST':
        try:
            age = request.form['age']
            gender = request.form['gender']
            rbp = request.form['rbp']
            chol = request.form['chol']
            fbs = request.form['fbs']
            ecg = request.form['ecg']
            rate = request.form['rate']
            ang = request.form['ang']
            thal = request.form['thal']

            input_data = (age,gender,rbp,chol,fbs,ecg,rate,ang,thal)
            prediction = predict_disease(input_data, std, ensem)
            if prediction[0] == 0:
                return render_template("heartattack.html", risk="No Risk!")
            else:
                return render_template("heartattack.html", risk="Risk!")

        except:
            print("Error")

# @app.route('/process', methods=['POST']) 
# def process(): 
#     data = request.get_json()
#     result = tuple(data['list'])
#     print(type(result))
#     prediction = predict_disease(result, std, ensem)
#     risk = ""
#     if prediction[0] == 0:
#         risk = "No"
#     else:
#         risk = "Yes"
#     return jsonify(result=risk)

@app.route('/srisk', methods = ['POST','GET'])
def srisk():
    if request.method == 'POST':
        try:
            sys = request.form['sys']
            dia = request.form['dia']
            age = request.form['age']
            slep = request.form['slep']
            phys = request.form['phys']
            rate = request.form['rate']
            step = request.form['step']

            input_data = (sys,dia,age,slep,phys,rate,step)
            prediction = predict_disease(input_data, scl_sleep, ensem_sleep)
            if prediction[0] == 0:
                return render_template("sleepdisorder.html", risk="No Risk!")
            elif prediction[0] == 1:
                return render_template("sleepdisorder.html", risk="Sleep Apnea")
            else:
                return render_template("sleepdisorder.html", risk="Insomnia")

        except:
            print("Error")


if __name__ == '__main__':
   app.run(debug = True)
