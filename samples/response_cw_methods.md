
# METHODS

""" 
    get_dashboard() # Displays the details of the dashboard that you specify.
    
    REQUEST
        response = client.get_dashboard(DashboardName='string')
    RESPONSE SYNTAX
        {
            'DashboardArn': 'string',
            'DashboardBody': 'string',
            'DashboardName': 'string'
        }
""" 

""" 
    get_metric_data() # GetMetricData API retrieve CloudWatch metric values.
                      # Can include a CloudWatch Metrics Insights query, and one or more metric math functions.

    REQUEST
        response = client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'string',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'string',
                            'MetricName': 'string',
                            'Dimensions': [
                                {
                                    'Name': 'string',
                                    'Value': 'string'
                                },
                            ]
                        },
                        'Period': 123,
                        'Stat': 'string',
                        'Unit': 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
                    },
                    'Expression': 'string',
                    'Label': 'string',
                    'ReturnData': True|False,
                    'Period': 123,
                    'AccountId': 'string'
                },
            ],
            StartTime=datetime(2015, 1, 1),
            EndTime=datetime(2015, 1, 1),
            NextToken='string',
            ScanBy='TimestampDescending'|'TimestampAscending',
            MaxDatapoints=123,
            LabelOptions={
                'Timezone': 'string'
            }
        )

    RESPONSE SYNTAX 
    {
        'MetricDataResults': [
            {
                'Id': 'string',
                'Label': 'string',
                'Timestamps': [
                    datetime(2015, 1, 1),
                ],
                'Values': [
                    123.0,
                ],
                'StatusCode': 'Complete'|'InternalError'|'PartialData'|'Forbidden',
                'Messages': [
                    {
                        'Code': 'string',
                        'Value': 'string'
                    },
                ]
            },
        ],
        'NextToken': 'string',
        'Messages': [
            {
                'Code': 'string',
                'Value': 'string'
            },
        ]
    }
""" 

""" 
    get_metric_statistics() # Gets statistics for the specified metric.
    
    REQUEST
        response = client.get_metric_statistics(
            Namespace='string',
            MetricName='string',
            Dimensions=[
                {
                    'Name': 'string',
                    'Value': 'string'
                },
            ],
            StartTime=datetime(2015, 1, 1),
            EndTime=datetime(2015, 1, 1),
            Period=123,
            Statistics=[
                'SampleCount'|'Average'|'Sum'|'Minimum'|'Maximum',
            ],
            ExtendedStatistics=[
                'string',
            ],
            Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
        )

    RESPONSE SYNTAX

        {
            'Label': 'string',
            'Datapoints': [
                {
                    'Timestamp': datetime(2015, 1, 1),
                    'SampleCount': 123.0,
                    'Average': 123.0,
                    'Sum': 123.0,
                    'Minimum': 123.0,
                    'Maximum': 123.0,
                    'Unit': 'Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None',
                    'ExtendedStatistics': {
                        'string': 123.0
                    }
                },
            ]
        }

""" 

""" 
    get_metric_stream() # Returns information about the metric stream that you specify.

    REQUEST 
        response = client.get_metric_stream(
            Name='string'
        )

    RESPONSE SYNTAX 
    
        {
            'Arn': 'string',
            'Name': 'string',
            'IncludeFilters': [
                {
                    'Namespace': 'string'
                },
            ],
            'ExcludeFilters': [
                {
                    'Namespace': 'string'
                },
            ],
            'FirehoseArn': 'string',
            'RoleArn': 'string',
            'State': 'string',
            'CreationDate': datetime(2015, 1, 1),
            'LastUpdateDate': datetime(2015, 1, 1),
            'OutputFormat': 'json'|'opentelemetry0.7',
            'StatisticsConfigurations': [
                {
                    'IncludeMetrics': [
                        {
                            'Namespace': 'string',
                            'MetricName': 'string'
                        },
                    ],
                    'AdditionalStatistics': [
                        'string',
                    ]
                },
            ]
        }
""" 


TODO: 

""" 
    list_dashboards()
""" 

""" 
    list_metric_streams()
""" 

""" 
    list_metrics()
""" 