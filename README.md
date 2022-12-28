# AWS_SES
Script do perform a collect in Amazon Simple Email Service and insert the consolidated data in Postgres DB.

First things first:

1. Install AWS client 
    - https://docs.aws.amazon.com/pt_br/cli/latest/userguide/getting-started-install.html
    - Execute this commands to check te installed aws client version 
        - aws --version
        
2. Execute "aws configure":
    1. AWS Access Key ID 
    2. AWS Secret Access Key
    3. Default region name
    4. Default output format
    
3. Execute the script "manager/SES_metrics.py"
