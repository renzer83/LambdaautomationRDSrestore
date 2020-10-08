import boto3
client = boto3.client('rds')

def checklastsnapshot(fromsnapshotdb):
    response = client.describe_db_snapshots(DBInstanceIdentifier=fromsnapshotdb)['DBSnapshots']
    snapshotfilterstatus = filter(lambda x: x['Status'] == 'available', response)
    last = sorted(snapshotfilterstatus, key=lambda x: x['SnapshotCreateTime'], reverse=True)[0]
    identifier_snapshot = last['DBSnapshotIdentifier']
    # print(identifier_snapshot)
    return identifier_snapshot
    
def modify_instance(db_name):
    try:
        dbinstance = client.describe_db_instances(DBInstanceIdentifier=db_name)
        if dbinstance['DBInstances'][0]['DBInstanceIdentifier'] == db_name:
            print('Modify DB_NAME')
            modify = client.modify_db_instance(
                DBInstanceIdentifier=db_name,
                ApplyImmediately=True,
                NewDBInstanceIdentifier=db_name+'old'
            )  
    except Exception as xerror:
        print('modify exceptions {}'.format(xerror))
        raise        
   
    return modify
    
def checkdbchangename(db_name, identifier_snapshot):
    x=1
    while(x==1):

        if client.describe_db_instances(DBInstanceIdentifier=db_name):
            dbinstance = client.describe_db_instances(DBInstanceIdentifier=db_name)
            if dbinstance['DBInstances'][0]['DBInstanceStatus'] == 'available':
                print(dbinstance['DBInstances'][0]['DBInstanceStatus'])
                print(dbinstance['DBInstances'][0]['DBInstanceIdentifier'])
                x=1
            else:
                print(dbinstance['DBInstances'][0]['DBInstanceStatus'])
                x=1  