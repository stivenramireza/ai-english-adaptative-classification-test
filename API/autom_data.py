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
    con_string = MONGO_CONNECTION_URL
    client = MongoClient(con_string)
    db = client[MONGO_DB_NAME]
    cols = db['questions']
    df = pd.DataFrame(list(cols.find({})))
    del df['_id']
    del df['updatedAt']
    del df['createdAt']
    del df['__v']
    df.columns = ['PREGUNTA', 'N_ITEM', 'Parte', 'DIFICULTAD', 'OPCION_CORRECTA', 'TEXTO']
    path = './data/easy_dataset_12.csv'
    if os.path.exists(path):
        os.remove(path)
    df.to_csv(path)

if __name__ == "__main__":
    main()
