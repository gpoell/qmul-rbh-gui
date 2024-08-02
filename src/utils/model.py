import pandas as pd
import pickle
import yaml
from statistics import fmean, median
from math import fsum

class DataModel:
    def __init__(self, data):
        self.data = data
        self._setConfig()

    def _setConfig(self):
        """
        Sets the model configuration based on the model properties in settings.yaml
        """
        with open('src/settings.yaml', 'r') as file:
            conf = yaml.safe_load(file)
            self.directory = conf['model']['directory']
            self.file = conf['model']['file']
            self.model = conf['model']['model']
            self.columns = conf['model']['columns']
            self.classifiers = conf['gripper']['classifiers']
            self.filePath = self.directory + '/' + self.file

    def writeCSV(self, label, file, data):
        ### Remove data and file parameter -- temporarily using for data collection ###
        """
        Writes data to a csv file at the specified path.
        Expects a label to 
        """
        # filePath = self.directory + '/' + self.file
        filePath = self.directory + '/' + file
        with open(filePath, 'a+') as f:
            for row in data:
                f.writelines(f"{value}," for value in row)
                f.write(label)
                f.write("\n")
            f.close()

    def classifyObject(self, data):
        """
        Predicts the classification of an object based using the ML model
        """
        filePath = self.directory + '/' + self.model
        with open(filePath, 'rb') as f:
            model = pickle.load(f)

        df = pd.DataFrame(data=data, columns=self.columns)
        prediction = int(model.predict(df))

        return self.decodePrediction(prediction)
    
    def decodePrediction(self, prediction):
        """
        Decodes model predictions to original object classifications.
        Sorts the classifiers to align with the model Encoder (alphabetical)
        and returns the classifier using the prediction as the index.
        """
        classifiers = sorted(self.classifiers)
        print(classifiers)
        return classifiers[prediction]
    
    def averageData(self):
        """
        Returns a new list of average values for feature in a uniform tactile data set
        """
        feature_length = len(self.data[0])
        avg_features = []
        for i in range(feature_length):
            avg_features.append(round(fmean([float(sample[i]) for sample in self.data]), 2))
        return avg_features
    
    def absoluteData(self):
        """
        Appends the absolute values of tactile data to the original list
        """
        for row in self.data:
            self.data.append([abs(val) for val in row])

    def absMagnitudeData(self):
        """
        Returns a new list of data with the additon of absolute and magnitude of the tactile values
        """
        result = self.data
        for index, row in enumerate(result):
            absData = [abs(float(val)) for val in row]
            magnitude = round(fsum(val**2 for val in absData) ** 0.5, 2)
            result[index] = row + absData + [magnitude]
        return result
    
    def restructureData(self):
        x = [float(val[0]) for val in self.data]
        y = [float(val[1]) for val in self.data]
        z = [float(val[2]) for val in self.data]
        return [x, y, z]
    
    def sequentialData(self):
        """
        Returns a new list with data formatted sequentially and the average magnitude
        """
        data = self.restructureData()
        mag = []
        for index, row in enumerate(self.data):
            mag.append(round(fsum(float(val)**2 for val in row) ** 0.5, 2))
        magAvg = round(fmean(mag), 2)
        return [data[0] + data[1] + data[2] + [magAvg]]
    
    def avgMedMagData(self):
        """
        Returns a new list with the average, median, and magnitude of the data
        """
        data = self.restructureData()
        mag = []
        avg = []
        med = []
        # Append average and median values in order of X, Y, Z
        for row in data:
            avg.append(round(fmean(row), 2))
            med.append(round(median(row), 2))
        # Calculate the magnitude of X, Y, Z values
        for row in self.data:
            mag.append(round(fsum(float(val)**2 for val in row) ** 0.5, 2))
        magAvg = round(fmean(mag), 2)
        return [avg + med + [magAvg]]
    
    def processTactileData(self, mode, label):
        """
        Writes collected data to a csv file or classifies the object based on the GUI settings.
        """

        # Write data to a csv file or classify the object using the data model
        if mode == "collect":
            #### Sequential Method Testing ####
            data = self.sequentialData()
            if len(data[0]) != 31: print("error with sequential data")
            file = "sequential_data.csv"
            self.writeCSV(label, file, data)

            #### Avg, Med, Mag ####
            data = self.avgMedMagData()
            if len(data[0]) != 7: print("error with avgMedMag data")
            file = "avg_med_mag_data.csv"
            self.writeCSV(label, file, data)

        if mode == "classify":
            data = self.sequentialData()
            # data = self.avgMedMagData()
            # data = self.averageData()
            prediction = self.classifyObject(data)
            print(prediction) # future change to emit to console

if __name__ == "__main__":
    x = [1, 1]
    y = [2, 2]
    z = [4, 4]
    print(x + y + z)