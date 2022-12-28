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
cursor.execute('SELECT max(collect_timestamp) FROM test.get_metric_statistics;')
last_collect_timestamp = cursor.fetchone()[0] or datetime.datetime(20, 12, 20, 11, 11, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=75600)))

# INSTANCE SERVICE "CLOUDWATCH"
client = boto3.client('cloudwatch')

#JSON TO SET
namespace='AWS/SES'
metric='Delivery'
start_collect=datetime.datetime(2022, 12, 23, 00, 00, 00).strftime("%Y-%m-%dT%H:%M:%SZ")
end_collect=datetime.datetime(2022, 12, 23, 23, 59, 59).strftime("%Y-%m-%dT%H:%M:%SZ") 
period = 360 
statistic = 'Sum'

# GET METRICAS FROM CLOUDWATCH
API_response = client.get_metric_statistics(
    Namespace=namespace,
    MetricName=metric,
    StartTime=start_collect,
    EndTime=end_collect,
    Period=period,
    Statistics=[statistic]
    # Dimensions=[
    #     {
    #         'Name': 'string',
    #         'Value': 'string'
    #     },
    # ],
    # ExtendedStatistics=[
    #     'string',
    # ],
    #Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
    #Unit='Seconds'
)

# RESPONSE
#    'Label': 'string',
#    'Datapoints': [{
#       'Timestamp': datetime(2015, 1, 1),
#       'SampleCount': 123.0,
#       'Average': 123.0,
#       'Sum': 123.0,
#       'Minimum': 123.0,
#       'Maximum': 123.0,
#       'Unit': 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None',
#       'ExtendedStatistics': {'string': 123.0}
#        },]}

#print(f"Getting data for metric AWS/SES - Click during timespan "f"of {start_collect} to {end_collect} (times are UTC).")
#stats = cw_wrapper.get_metric_statistics(metric_namespace, metric_name, start, datetime.utcnow(), 60, ['Average', 'Minimum', 'Maximum'])

print(f"Got {len(API_response['Datapoints'])} data points for metric {namespace} - {metric}")

#print(sorted(API_response['Datapoints'], key=lambda x: x['Timestamp']))

# ITERATE IN RESPONSE
for key in API_response:
    if key == 'Datapoints':
        values = API_response[key]
        query = 'INSERT INTO test.get_metric_statistics(metric, statistic, totalizator, unit, collect_timestamp) VALUES'
        for value in values:
            #if value['Timestamp'].replace(tzinfo=datetime.timezone.utc):
                insert_values = metric, statistic, value[statistic], value['Unit'], str(value['Timestamp'])
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

# print(f"Getting data for metric {metric_namespace}.{metric_name} during timespan "
#         f"of {start} to {datetime.utcnow()} (times are UTC).")
# stats = cw_wrapper.get_metric_statistics(
#     metric_namespace, metric_name, start, datetime.utcnow(), 60,
#     ['Average', 'Minimum', 'Maximum'])
# print(f"Got {len(stats['Datapoints'])} data points for metric "
#         f"{metric_namespace}.{metric_name}.")
# pprint(sorted(stats['Datapoints'], key=lambda x: x['Timestamp']))