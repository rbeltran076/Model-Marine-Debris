from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import pandas as pd
import urllib.request, urllib.parse, urllib.error
import json
import ssl
import xml.etree.ElementTree as ET
import os
import sqlite3
import codecs
import webbrowser
import winsound

print(
"""
==========================================================================
Hi, this is a program that shows you predictions about marine debris!!!

This model has been trained with data extracted from USA marine debris findings
all the data that this model has used has been obtained from kaggle.com

Before we can make predictions, insert the coordinates (latitude and longitude)
of the place where you think there could be marine debris.
===================================
"""
)

latitudeInserted = input('Latitude: ')
longitudeInserted = input('Longitude: ')

debris_filepath = 'C:/Users/USER/Desktop/Prog/PROGRAMAS/proyecto_NASA_workspace/proyecto_NASA_csv/debris_data_1.csv'
not_filtered_debris_dataset = pd.read_csv(debris_filepath)

def newline(numberOfLines):
    print('____________________________________________\n' * numberOfLines)
def searchMap(latitude, longitude):
    fhand = codecs.open('C:/Users/USER/Desktop/Prog/PROGRAMAS/proyecto_NASA_workspace/proyecto_NASA_pythons/Spot That Fire v.3.0 App/where.js', 'w', "utf-8")
    fhand.write("myData = [\n")
    output = "["+ str(latitude)+ "," + str(longitude) + "]"
    fhand.write(output)
    fhand.write("\n];\n")
    webbrowser.open("C:/Users/USER/Desktop/Prog/PROGRAMAS/proyecto_NASA_workspace/proyecto_NASA_pythons/Spot That Fire v.3.0 App/where.html")
    fhand.close()

# Filter the table and leave it with no empty spaces, so that everything is used
debris_dataset = not_filtered_debris_dataset.dropna(axis = 1, how = 'any', subset = None, inplace = False).drop(columns = ['MaterialDescription', 'ListID', 'Timestamp', 'ListName', 'ItemName', 'LogID'])

# Append a last row with the new lat and lng
new_row = {'ItemID':182, 'Latitude':latitudeInserted, 'Longitude':longitudeInserted, 'Altitude':1, 'Quantity':1, 'ErrorRadius':5.00, 'MaterialID':1}
debris_dataset = debris_dataset.append(new_row, ignore_index=True)

# Material Model
Y_material = debris_dataset.MaterialID
X_features_material = ['Latitude', 'Longitude', 'Altitude', 'Quantity', 'ItemID']
X_material = debris_dataset[X_features_material]
material_model = RandomForestRegressor()

# Quantity Model
Y_quantity = debris_dataset.Quantity
X_features_quantity = ['Latitude', 'Longitude', 'Altitude', 'MaterialID', 'ItemID']
X_quantity = debris_dataset[X_features_quantity]
quantity_model = RandomForestRegressor()

# Item model
Y_item = debris_dataset.ItemID
X_features_item = ['Latitude', 'Longitude', 'Altitude', 'Quantity', 'MaterialID']
X_item = debris_dataset[X_features_item]
item_model = RandomForestRegressor()
    
menuAnswer = input(
"""
Choose an option to predict:

1. Material of debris
2. Quantity of debris
3. Elements potentially involved
4. Yeah, all of them please
===========================================================================
Option: """
)

if (int(menuAnswer) == 1):
    print('Predicting, please wait...')
    material_model.fit(X_material, Y_material)
    lotsof_predicted_material_id = material_model.predict(X_material)
    print('Predicted!!!')
    predicted_material_id = int(round(lotsof_predicted_material_id[-1], 0))
    tabla_filtrada = not_filtered_debris_dataset[not_filtered_debris_dataset['MaterialID'] == predicted_material_id]
    print(f"""If there is marine debris at this location, it may be made of this material: {tabla_filtrada.iloc[1].MaterialDescription}

Notice that: If the prediction is unclear, or the material is rare or unidentified, the prediction will be 'Other'""")
    answer = input('Would you like to see the location of the marine debris? (Y/N)')
    if (answer == 'Y'):
        searchMap(latitudeInserted, longitudeInserted)
    else:
        print('Ok, the program has finished')

elif (int(menuAnswer) == 2):
    print('Predicting, please wait...')
    quantity_model.fit(X_quantity, Y_quantity)
    predicted_quantity_id = quantity_model.predict(X_quantity)
    print('Predicted!!!')
    print(f'If marine debris is found here, it is likely that there is around {int(round(predicted_quantity_id[-1], 0))} elements of it')
    answer = input('Would you like to see the location of the marine debris? (Y/N)')
    if (answer == 'Y'):
        searchMap(latitudeInserted, longitudeInserted)
    else:
        print('Ok, the program has finished')

elif (int(menuAnswer) == 3):
    print('Predicting, please wait...')
    item_model.fit(X_item, Y_item)
    lotsof_predicted_item_id = item_model.predict(X_item)
    print('Predicted!!!')
    predicted_item_id  = int(round(lotsof_predicted_item_id[-1], 0))
    tabla_filtrada = not_filtered_debris_dataset[not_filtered_debris_dataset['ItemID'] == predicted_item_id]
    print(f"""If marine debris is found here, it is likely that it is {tabla_filtrada.iloc[1].ItemName}

Notice that: If the prediction is unclear, or the item is rare or unidentified, the prediction will be 'Other'""")
    answer = input('Would you like to see the location of the marine debris? (Y/N)')
    if (answer == 'Y'):
        searchMap(latitudeInserted, longitudeInserted)
    else:
        print('Ok, the program has finished')

elif (int(menuAnswer) == 4):
    print('Predicting, please wait... You just selected the most demanding option!')
    material_model.fit(X_material, Y_material)
    lotsof_predicted_material_id = material_model.predict(X_material)
    predicted_material_id = material_model.predict(X_material)
    predicted_material_id = int(round(lotsof_predicted_material_id[-1], 0))
    extract_material = not_filtered_debris_dataset[not_filtered_debris_dataset['MaterialID'] == predicted_material_id]

    quantity_model.fit(X_quantity, Y_quantity)
    predicted_quantity_id = quantity_model.predict(X_quantity)

    item_model.fit(X_item, Y_item)
    predicted_item_id = item_model.predict(X_item)
    lotsof_predicted_item_id = item_model.predict(X_item)
    predicted_item_id  = int(round(lotsof_predicted_item_id[-1], 0))
    extract_item = not_filtered_debris_dataset[not_filtered_debris_dataset['ItemID'] == predicted_item_id]
    print('Predicted!!!')
    
    print(
    f"""___________________________________________________________________________________________________________________
    If the location contains any marine debris, then it's likely that it has the following characteristics:
    Material    {extract_material.iloc[1].MaterialDescription}
    Quantity    {int(round(predicted_quantity_id[-1], 0))}
    Item        {extract_item.iloc[1].ItemName}

Notice that: If the prediction is unclear, or the item is rare or unidentified, the prediction will be 'Other'
    """
    )
    answer = input('Would you like to see the location of the marine debris? (Y/N)')
    if (answer == 'Y'):
        searchMap(latitudeInserted, longitudeInserted)
    else:
        print('Ok, the program has finished')