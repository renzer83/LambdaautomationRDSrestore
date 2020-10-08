import pymysql
import os
import boto3
from base64 import b64decode

kms = boto3.client('kms')


user01 = os.environ['user01']
user01pwddecrypt = kms.decrypt(CiphertextBlob=b64decode(user01),EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']})['Plaintext'].decode('utf-8')

user02 = os.environ['user02']
user02pwddecrypt = kms.decrypt(CiphertextBlob=b64decode(user02),EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']})['Plaintext'].decode('utf-8')

user03 = os.environ['user03']
user03pwddecrypt = kms.decrypt(CiphertextBlob=b64decode(user03),EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']})['Plaintext'].decode('utf-8')

user04 = os.environ['user04']
user04pwddecrypt = kms.decrypt(CiphertextBlob=b64decode(user04),EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']})['Plaintext'].decode('utf-8')




def changepasswordusers(endpoint,password, dbinstance):
    if dbinstance['DBInstances'][0]['DBInstanceStatus'] == 'available':
        username = 'usernamedb'
        database_name = 'databasename'
        connect = pymysql.connect(endpoint, username, password, database_name)
    
        cursor = connect.cursor()
        cursor.execute("ALTER USER 'user01pwddecrypt'@'%' IDENTIFIED BY '{}'".format(user01pwddecrypt))
        cursor.execute("ALTER USER 'user02pwddecrypt'@'%' IDENTIFIED BY '{}'".format(user02pwddecrypt))
        cursor.execute("ALTER USER 'user03pwddecrypt'@'%' IDENTIFIED BY '{}'".format(user03pwddecrypt))
        cursor.execute("ALTER USER 'user04pwddecrypt'@'%' IDENTIFIED BY '{}'".format(user04pwddecrypt))
        connect.commit()
        cursor.close()
        print('Successfully Modify Password Users')
    else:
        print('IF change')
        print(dbinstance['DBInstances'][0]['DBInstanceStatus'])
        changepasswordusers(endpoint, password, dbinstance)
