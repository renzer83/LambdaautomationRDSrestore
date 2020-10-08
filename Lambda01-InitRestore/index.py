import boto3
import os
from botocore.exceptions import ClientError
from helpers import checklastsnapshot, modify_instance, checkdbchangename
from restoresnaprds import restoretosnapshot
import json

client = boto3.client('rds')
clientsqs = boto3.client('sqs')



def lambda_handler(event, context):
    activeexec = os.environ['ACTIVEEXEC']
    fromsnapshotdb = os.environ['FROMSNAPSHOTDB']
    rds_db_name = os.environ['RDS_DB_NAME']
    snsarn = os.environ['SNSTOPICARN']
    identifier_snapshot = checklastsnapshot(fromsnapshotdb)
    print(identifier_snapshot)
    
    if activeexec == 'YES':
        try:
            print("Start script")
            print("################")
            print("Change RDS snapshot old")
            modify_instance(rds_db_name)
            print("Check snapshot name change")
            checkdbchangename(rds_db_name, identifier_snapshot)
        except ClientError as err:
            print('Error Client: {}'.format(err))
            if err.response['Error']['Code'] == "DBInstanceNotFound":
                print('DBInstanceNotFound for: {}'.format(rds_db_name))
                restoretosnapshot(identifier_snapshot)
            else:
                print("Error Boto3: {}".format(err))
        except Exception as xerror:
            print('Error {}'.format(xerror))    

    
