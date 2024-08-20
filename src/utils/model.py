import pandas as pd
import pickle
import yaml
from statistics import median, mean

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

    def writeCSV(self, data, label="None"):
        """
        Writes a list of data to a csv file at the specified path.
        """
        filePath = self.directory + '/' + self.file
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
    
    def updateAverageData(self):
        """
        Adds a new item to the self.data attribute containing a list of average axial values for X, Y, Z
        """
        self.data['avg'] = {}
        self.data['avg']['x'] = round(mean(self.data['x']), 2)
        self.data['avg']['y'] = round(mean(self.data['y']), 2)
        self.data['avg']['z'] = round(mean(self.data['z']), 2)

    def updateMedianData(self):
        """
        Adds a new item to the self.data attribute containing a list of average axial values for X, Y, Z
        """
        self.data['med'] = {}
        self.data['med']['x'] = round(median(self.data['x']), 2)
        self.data['med']['y'] = round(median(self.data['y']), 2)
        self.data['med']['z'] = round(median(self.data['z']), 2)
    
    def updateAbsoluteData(self):
        """
        Adds a new item to self.data containing the absolute axial values for X, Y, Z
        """
        self.data['abs'] = {}
        self.data['abs']['x'] = [abs(val) for val in self.data['x']]
        self.data['abs']['y'] = [abs(val) for val in self.data['y']]
        self.data['abs']['z'] = [abs(val) for val in self.data['z']]

    def updateAvgMagnitudeData(self):
        """
        Adds a new item to self.data containing the average magnitude of all the axial values X, Y, Z.
        """
        dataLen = len(self.data['x'])
        magnitude = []
        for i in range(dataLen):
            res = (self.data['x'][i]**2 + self.data['y'][i]**2 + self.data['z'][i]**2) ** 0.5
            magnitude.append(res)
        self.data['magnitude'] = round(mean(magnitude), 2)
    
    def processTactileData(self, mode, label):
        """
        Writes collected data to a csv file or classifies the object based on the GUI settings.
        """
        # Append the Statistical Characteristics
        self.updateAverageData()
        self.updateMedianData()
        self.updateAvgMagnitudeData()

        # Concatenate Tactile Values
        raw = self.data['x'] + self.data['y'] + self.data['z']
        avgs = [val for val in self.data['avg'].values()]
        meds = [val for val in self.data['med'].values()]
        mag = [self.data['magnitude']]
        data = [raw + avgs + meds + mag]

        # Collect Data or Classify Object based on mode 
        if mode == "collect": 
            self.writeCSV(data, label=label)

        if mode == "classify":
            prediction = self.classifyObject(data)
            print(prediction) # future change to emit to console