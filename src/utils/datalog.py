import pandas as pd
import pickle

def write_csv(data, object, file="tactile_sensor_data.csv", dir="data"):
    """Writes data to a csv file at the specified path"""

    path = dir + '/' + file
    with open(path, 'a+') as f:
        for row in data:
            f.writelines(f"{value}," for value in row)
            f.write(object)
            f.write("\n")
        f.close()

def classify_object(data, file="model.pkl", dir="data"):
    """Predicts the classification of an object based using the ML model"""
    
    path = dir + '/' + file

    with open(path, 'rb') as f:
        model = pickle.load(f)

    df = pd.DataFrame(data=[data], columns=["tactile_x", "tactile_y", "tactile_z", "abs_x", "abs_y", "abs_z", "magnitude"])
    prediction = model.predict(df)
    
    return decode_prediction(prediction)

def decode_prediction(prediction):
    """Decodes model predictions to original object classifications"""

    prediction = int(prediction)
    # Temporary - future configuration file will determine result
    if prediction == 0: return "Balloon"
    if prediction == 1: return "Tennis Ball"
