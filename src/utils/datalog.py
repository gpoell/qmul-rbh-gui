import pandas as pd
import pickle

def write_csv(data, object="", file="tactile_sensor_data.csv", dir="data"):
    """Writes data to a csv file at the specified path"""

    path = data + '/' + file
    with open(path, 'a+') as f:
        for value in data:
            f.write(f"{value[0]},{value[1]},{value[2]},{object}")
            f.write("\n")
        f.close()

def classify_object(data, file="model.pkl", dir="data"):
    """Predicts the classification of an object based using the ML model"""
    
    path = data + '/' + file
    with open(path, 'rb') as f:
        model = pickle.load(f)

    # Create Data Frame
    df = pd.DataFrame(data=[data], columns=["tactile_x", "tactile_y", "tactile_z"])

    return model.predict(df)