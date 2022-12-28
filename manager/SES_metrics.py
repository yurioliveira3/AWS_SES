# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# Author:
# Yuri Oliveira Alves

# References
# - https://github.com/awsdocs/aws-doc-sdk-examples/blob/5458e2b9fd71abb916bca4ed53d8c1a894e4fe87/python/example_code/cloudwatch/cloudwatch_basics.py#L119
# - https://docs.aws.amazon.com/cli/latest/reference/cloudwatch/get-metric-statistics.html#get-metric-statistics
# - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_statistics
# - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html

from botocore.exceptions import ClientError
from psycopg2 import Error
import boto3 
import psycopg2
import datetime 

class DataBaseConnection: 
    def __init__(self, host, database, user, password, port):
        self.connection = psycopg2.connect('host= {0} dbname= {1} user= {2} password= {3} port = {4}'.format(host, database, user, password, port))

        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def get_last_ses_collect(self):
        try:
            self.cursor.execute("SELECT max(collect_timestamp) FROM aws_ses.send_mail_statistics;")
            return self.cursor.fetchone()[0] or datetime.datetime(20, 12, 20, 11, 11, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=75600)))
        except (Exception, Error) as error:
            print("Error while get last collect", error)

    def get_last_cw_collect(self, metric, statistic):
        try:
            self.cursor.execute(f"SELECT max(collect_timestamp) FROM aws_ses.get_metric_statistics_informations WHERE metric = '{metric}' AND statistic = '{statistic}';")
            return self.cursor.fetchone()[0] or datetime.datetime(20, 12, 20, 11, 11, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=75600)))
        except (Exception, Error) as error:
            print("Error while get last collect", error)

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def insert_into_db(self, values):
        try:
            self.cursor.execute(values)
        except ClientError as e:
            print(e.response['Error']['Message'])
        except (Exception, Error) as error:
            print("Error while connecting to DB", error)

    def insert_ses_data(self, stats):
        lst_col = self.get_last_ses_collect()
        insert_rows = 0
        for key in stats:
            if key == 'SendDataPoints':
                values = stats[key]
                query = 'INSERT INTO aws_ses.send_mail_statistics(delivery_attempts, bounces, complaints, rejects, collect_timestamp) VALUES'
                for value in values:
                    if value['Timestamp'].replace(tzinfo=datetime.timezone.utc) > lst_col:
                        insert_values = value['DeliveryAttempts'], value['Bounces'], value['Complaints'], value['Rejects'], str(value['Timestamp'])
                        insert_values = query + str(insert_values) +';'
                        self.insert_into_db(insert_values)
                        insert_rows +=1

                #print(f"  - Insert {len(values)} in send_mail_statistics table!")
                print(f"  - Inserted {insert_rows} new rows in send_mail_statistics table!")

    def insert_cw_data(self, stats, metric, statistic):
        lst_col = self.get_last_cw_collect(metric, statistic)
        insert_rows = 0
        for key in stats:
            if key == 'Datapoints':
                values = stats[key]
                query = 'INSERT INTO aws_ses.get_metric_statistics(metric, statistic, totalizator, unit, collect_timestamp) VALUES'
                for value in values:
                    if value['Timestamp'].replace(tzinfo=datetime.timezone.utc) > lst_col:
                        insert_values = metric, statistic, value[statistic], value['Unit'], str(value['Timestamp'])
                        insert_values = query + str(insert_values) +';'
                        self.insert_into_db(insert_values)
                        insert_rows+=1

                #print(f"  - Insert {len(values)} in get_metric_statistics table!")
                print(f"  - Inserted {insert_rows} new rows in send_mail_statistics table!")

class SESWrapper: 
    def __init__(self, emailservice_client):
        self.emailservice_client = emailservice_client
    
    def get_send_stats(self):
        try:
            stats = self.emailservice_client.get_send_statistics()
        except ClientError as e:
            # print("Couldn't get statistics for %s.%s.", namespace, name)
            print(e.response['Error']['Message'])                   
            raise
        else:
            return stats

class CloudWatchWrapper: 
    def __init__(self, cloudwatch_resource):
        self.cloudwatch_resource = cloudwatch_resource
    
    def get_metric_statistics(self, namespace, name, start, end, period, stat_types):
        try:
            metric = self.cloudwatch_resource.Metric(namespace, name)

            stats = metric.get_statistics(
                        StartTime=start, 
                        EndTime=end, 
                        Period=period, 
                        Statistics=stat_types
                    )
        except ClientError as e:
            print(e.response['Error']['Message'])                   
            raise
        else:
            return stats
    
def main():

    db_connection = DataBaseConnection("127.0.0.1", "test", "postgres", "", "5432")

    print('-'*88)
    print("SESWrapper")
    print('-'*88)

    ses_wrapper = SESWrapper(boto3.client('ses'))

    ses_stats = ses_wrapper.get_send_stats()

    print(f" - Got {len(ses_stats['SendDataPoints'])} statistics for AWS/SES")

    # print(sorted(stats['SendDataPoints'], key=lambda x: x['Timestamp']))
    
    db_connection.insert_ses_data(ses_stats)

    print('-'*88)
    print("CloudWatchWrapper")
    print('-'*88)
    
    cw_wrapper = CloudWatchWrapper(boto3.resource('cloudwatch'))

    metric_namespace = 'AWS/SES'
    # start = datetime.utcnow() - datetime.timedelta(minutes=minutes)
    # minutes = 20
    start_collect=datetime.datetime(2022, 12, 23, 00, 00, 00).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_collect=datetime.datetime(2022, 12, 23, 23, 59, 59).strftime("%Y-%m-%dT%H:%M:%SZ") 
    period = 360 
    statistics = 'Sum' #statistics = ['SampleCount', 'Sum', 'Average', 'Minimum', 'Maximum']
    metric_name = ['Delivery','Open','Click']
      
    for metric in metric_name:
        cw_stats = cw_wrapper.get_metric_statistics(
            metric_namespace, metric, start_collect, end_collect, period, [statistics]
        )

        print(f" - Got {len(cw_stats['Datapoints'])} data points for metric {metric_namespace}.{metric}.")

        #print(sorted(cw_stats['Datapoints'], key=lambda x: x['Timestamp']))

        db_connection.insert_cw_data(cw_stats, metric, statistics)

    print('-'*88)
  
    db_connection.close_connection()

if __name__ == '__main__':
    main()
