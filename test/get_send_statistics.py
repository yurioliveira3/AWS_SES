from botocore.exceptions import ClientError
from psycopg2 import Error
import boto3 
import psycopg2
import datetime 

# CONNECT TO DB
connection = psycopg2.connect(user="postgres", password="", host="127.0.0.1", port="5432", database="")
connection.autocommit = True
cursor = connection.cursor()

# GET LAST COLLECT 
cursor.execute('SELECT max(collect_timestamp) FROM test.send_mail_statistics;')
last_collect_timestamp = cursor.fetchone()[0] or datetime.datetime(20, 12, 20, 11, 11, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=75600)))

# INSTANCE SERVICE "SES"
client = boto3.client('ses')

# GET STATISTICS FROM SES
# Provides sending statistics for the current AWS Region. The result is a list of data points, 
# representing the last two weeks of sending activity. Each data point in 
# the list contains statistics for a 15-minute period of time.
API_response = client.get_send_statistics()

# RESPONSE 
    # Timestamp (datetime)       -- Time of the data point.
    # DeliveryAttempts (integer) -- Number of emails that have been sent.
    # Bounces (integer)          -- Number of emails that have bounced.
    # Complaints (integer)       -- Number of unwanted emails that were rejected by recipients.
    # Rejects (integer)          -- Number of emails rejected by Amazon SES.

# ITERATE IN RESPONSE
for key in API_response:
    if key == 'SendDataPoints':
        values = API_response[key]
        query = 'INSERT INTO test.send_mail_statistics(delivery_attempts, bounces, complaints, rejects, collect_timestamp) VALUES'
        for value in values:
            if value['Timestamp'].replace(tzinfo=datetime.timezone.utc) > last_collect_timestamp:
                insert_values = value['DeliveryAttempts'], value['Bounces'], value['Complaints'], value['Rejects'], str(value['Timestamp'])
                insert_values = query + str(insert_values) +';'
                try:
                    # INSERT ON DB
                    cursor.execute(insert_values)
                except ClientError as e:
                    print(e.response['Error']['Message'])
                except (Exception, Error) as error:
                    print("Error while connecting to PostgreSQL", error)

# CLOSE PG CONNECTION
cursor.close()
connection.close()
