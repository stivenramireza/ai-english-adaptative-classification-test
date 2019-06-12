from pymongo import MongoClient
import pymongo
import pandas as pd
import argparse, getpass
import os

def main():
    """
        Starts the autommation script to extract the data of the database and creates a data file for the model.
    """
    # DB USER
    user = os.environ.get('DBUSER')
    # DB PASSWORD
    password = os.environ.get('DBPASSWORD')
    # DB HOST
    host = os.environ.get('DBHOST')
    # DB NAME
    dbname = os.environ.get('DBNAME')
    # DB PORT
    port = os.environ.get('DBPORT')
    # QUESTIONS COLLECTION NAME
    col_name = os.environ.get('DBCOLNAME')
    user = 'user2'
    password = 'user123'
    host = 'ds025232.mlab.com'
    dbname='eacidb'
    port = '25232'
    col_name='questions'
    # FULL CONNECTION STRING TO THE DATABASE
    con_string = "mongodb://{:s}:{:s}@{:s}:{:s}/{:s}".format(user, password, host, port, dbname)
    # MONGO CLIENT
    client = MongoClient(con_string)
    # DB NAME
    db = client.eacidb
    # QUESTIONS
    colls = db[col_name]
    # CONVERTS TO DATAFRAME
    df = pd.DataFrame(list(colls.find({})))
    # REMOVES DB ID
    if '_id' in df:
        del df['_id']
    if 'updatedAt' in df:
        del df['updatedAt']
    # CHANGE COLUMNS NAMES FOR THE MODEL
    print(df.columns)
    df.columns = ['DIFICULTAD', 'N_ITEM', 'TEXTO', 'Parte', 'PREGUNTA', 'OPCION_CORRECTA']
    # PATH TO SAVE THE QUESTIONS
    path = './data/easy_dataset_12.csv'
    if os.path.exists(path):
        os.remove(path)
    # SAVES QUESTIONS TO A CSV FILE
    df.to_csv(path)
if __name__ == "__main__":
    main()