import boto3
import os
from base64 import b64decode
from runquerymysql import changepasswordusers

client = boto3.client('rds')
kms = boto3.client('kms')

rdsdb_old = os.environ['RDS_DBOLD_NAME']
rdsdb_active = os.environ['RDS_DBACTIVE_NAME']
eventsubscription = os.environ['Event_Subscription_NAME']
passencry = os.environ['MasterUserPassword']
passdecrypt = kms.decrypt(CiphertextBlob=b64decode(passencry),EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']})['Plaintext'].decode('utf-8')
endpointdbactive = client.describe_db_instances(DBInstanceIdentifier=rdsdb_active)['DBInstances'][0]['Endpoint']['Address']

def deletedbold(rdsdb_old):
    if client.describe_db_instances(DBInstanceIdentifier=rdsdb_old):
        delete = client.delete_db_instance(
            DBInstanceIdentifier=rdsdb_old,
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True
        )
        print('Successfully Deleted DB_OLD: {}'.format(rdsdb_old))
    else:
        print('DB_OLD Does not exist: {}'.format(rdsdb_old))
        return False
    return delete

def deleteeventrds(eventsubscription):
    event_sub = client.delete_event_subscription(
    SubscriptionName=eventsubscription
    )
    print('Successfully Deleted EventRDS: {}'.format(eventsubscription))
    return event_sub

def modify_password():
    x=1
    while(x==1):
        if client.describe_db_instances(DBInstanceIdentifier=rdsdb_active):
            dbinstance = client.describe_db_instances(DBInstanceIdentifier=rdsdb_active)
            if dbinstance['DBInstances'][0]['DBInstanceStatus'] == 'available':
                modify = client.modify_db_instance(
                    DBInstanceIdentifier=rdsdb_active,
                    ApplyImmediately=True,
                    MasterUserPassword=passdecrypt,
                )
                print('Successfully Modify Password DBisactive: {}'.format(rdsdb_active))
                x=0
                changepasswordusers(endpointdbactive, passdecrypt, dbinstance)
            else:
                print(dbinstance['DBInstances'][0]['DBInstanceStatus'])
                x=1
    return modify
    



def lambda_handler(event, context):
    modify_password()
    print(event)
    message = event['Records'][0]['Sns']['Message']
    message = eval(message)
    dbactive = message['Source ID']
    eventmsg = message['Event Message']
    print(dbactive)
    print(eventmsg)
    
    
    try:
        if "Finished DB Instance backup" in eventmsg:
            if dbactive == rdsdb_active:
                print(event)
                deleteeventrds(eventsubscription)
                deletedbold(rdsdb_old)
                modify_password()
                
        else:
            print('else')
    except Exception as xerror:
        print('Exceptions {}'.format(xerror))
        raise