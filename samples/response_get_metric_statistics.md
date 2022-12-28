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