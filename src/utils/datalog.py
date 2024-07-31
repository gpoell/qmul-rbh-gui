import pandas as pd
import pickle
from statistics import fmean
from math import fsum

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

def average_tactile_features(data):
        """Returns the average feature values of a uniform tactile data set"""
        feature_length = len(data[0])
        avg_features = []
        for i in range(feature_length):
            avg_features.append(round(fmean([float(sample[i]) for sample in data]), 2))
        return avg_features
    
def absMagnitudeData(data):
    """Returns a new list appending the absolute and magnitude of the tactile values"""
    result = data
    for index, row in enumerate(result):
        absData = [abs(float(val)) for val in row]
        magnitude = round(fsum(val**2 for val in absData) ** 0.5, 2)
        result[index] = row + absData + [magnitude]
    return result

def processTactileData(settings, data):
    """
    Writes collected data to a csv file or classifies the object based on the GUI settings.
    """
    # Compute and add the magnitude and absolute tactile values
    data = absMagnitudeData(data)

    # Write data to a csv file or classify the object using the data model
    mode = settings['mode']
    label = settings["classifier"]
    if mode == "collect": write_csv(data, label)
    if mode == "classify":
        avg_data = average_tactile_features(data)
        prediction = classify_object(avg_data)
        print(prediction) # future change to emit to console