import hashlib as hasher
import datetime as date
import sys
# import sqlite3
import pickle



def save_chain(blockchain):
    with open('blockchain.pkl', 'wb') as f:
        pickle.dump(blockchain, f)

def load_chain():
    try:
        with open('blockchain.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None



