from hdfs import InsecureClient
import pandas as pd

InsecureClient('http://127.0.0.1:50070', user='maria_dev')

filepath = '/user/datasets/titanic.csv'

with client.read(filepath) as reader
    pd.read_csv(reader)


df.head()
