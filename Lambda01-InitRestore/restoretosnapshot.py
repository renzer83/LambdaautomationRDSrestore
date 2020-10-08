import boto3
import os
client = boto3.client('rds')

rds_db_name = os.environ['RDS_DB_NAME']
regionaz = os.environ['Region_AZ']
snsarn = os.environ['SNSTOPICARN']

def restoretosnapshot(identifier_snapshot):
        restoredb = client.restore_db_instance_from_db_snapshot(
                AvailabilityZone=regionaz,
                VpcSecurityGroupIds=['sg'],
                DBSubnetGroupName='rds-subnet',
                DBSnapshotIdentifier=identifier_snapshot,
                DBInstanceClass='db.t2.medium',
                MultiAZ=False,
                DBInstanceIdentifier=rds_db_name,
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': 'serverdb-new' + rds_db_name
                    }
                ]
        )
        print('Restore Started')
        return postrestore(restoredb)
        
def postrestore(restoredb):
    mydb = restoredb['DBInstance']['DBInstanceIdentifier']
    event = client.create_event_subscription(
            Enabled=True,
            EventCategories=[
                'backup',
            ],
            SnsTopicArn=snsarn,
            SourceIds=[
                rds_db_name,
            ],
            SourceType='db-instance',
            SubscriptionName='EventRDSrestore',
        )
    print(mydb)
    return event