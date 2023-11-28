import numpy as np
import cv2
import glob
from keras.models import Sequential
from keras.models import load_model
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import folium
import glob
import re
import random
import os
import time


def Module_3():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

    for i in range(20):
        print("\n")
    
    #Loading In Custom Co-Ordinates
    coordinates = []
    fh = open("D:\Code Of Honour\Mod3\Custom_Pothole_Data.txt")
    text = (fh.read()).split('\n')
    for i in text:
        if len(i)==22:
            tmp = i.split(',')
            x = float(tmp[0])
            y = float(tmp[1])
            coordinates.append([x,y])

    #Adding Custom Markings
    def Map():
        map = folium.Map(location=[0, 0], zoom_start=2)
        for coord in new_cods:
            folium.Marker(location=coord).add_to(map)
        map.save("Generated_Map.html")


    #Loading ML Model And Making PredectionsD:\Code Of Honour\Mod3\Generated_Map.html
    model = load_model('D:\\Code Of Honour\\Mod3\\Pothole_Model.h5')
    def predict_pothole(image_location):
        size = 100
        #model = load_model('D:\\Code Of Honour\\Mod3\\Pothole_Model.h5')

        test_image = cv2.imread(image_location, 0)
        if test_image is None:
            print("Error: Unable to load the image.")
            return None
        test_image = cv2.resize(test_image, (size, size))
        test_image = np.asarray(test_image)
        test_image = test_image.reshape(1, size, size, 1)

        prediction = model.predict(test_image)
        class_label = np.argmax(prediction, axis=1)[0]

        return class_label

    print("\n")
    print("\n")
    print("\n")
    print("Running Ml Model ThrughOut...")

    pred = list()
    count = 1
    for i in coordinates:
        img = f"D:\Code Of Honour\Mod3\Test_Images\Test_{count}.png"
        x = predict_pothole(img)
        print("Predicted Class : ", x)
        time.sleep(.5)
        count += 1
        pred.append(x)

    print("\n")
    new_count = 0
    new_cods = list()
    for i in coordinates:
        if pred[new_count]==1:
            print(f"\nPothole Detected At Co-Ordinates : {i} \nCo-Ordintes Marked On Map     |     Location {new_count+1}")
            new_cods.append(i)
        new_count += 1
        x = random.choice([1,2,])
        time.sleep(x)

    Map()

if __name__ == "__main__":
    Module_3()