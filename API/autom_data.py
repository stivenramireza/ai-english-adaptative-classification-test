from credentials import (
    MONGO_CONNECTION_URL,
    MONGO_DB_NAME
)

from pymongo import MongoClient
import pymongo
import pandas as pd
import argparse, getpass
import os

def main():
    """
        Starts the autommation script to extract the data of the database and creates a data file for the model.
    """
    # FULL CONNECTION STRING TO THE DATABASE
    con_string = MONGO_CONNECTION_URL
    # MONGO CLIENT
    client = MongoClient(con_string)
    # DB NAME
    db = client[MONGO_DB_NAME]
    # QUESTIONS
    cols = db['questions']
    # CONVERTS TO DATAFRAME
    df = pd.DataFrame(list(cols.find({})))
    # REMOVES DB ID
    if '_id' in df:
        del df['_id']
    if 'updatedAt' in df:
        del df['updatedAt']
    # CHANGE COLUMNS NAMES FOR THE MODEL
    df.columns = ['DIFICULTAD', 'N_ITEM', 'TEXTO', 'Parte', 'PREGUNTA', 'OPCION_CORRECTA']
    # PATH TO SAVE THE QUESTIONS
    path = './data/easy_dataset_12.csv'
    if os.path.exists(path):
        os.remove(path)
    # SAVES QUESTIONS TO A CSV FILE
    df.to_csv(path)

if __name__ == "__main__":
    main()