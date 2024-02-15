import boto3
from os import path as op
from datetime import datetime

#   AWS Credentials
access_key = ''
secret = ''
bucket = 'exolabs-swiss-project'

#   Configuration
date_of_interest = '11. November 2023'

# Convert Date
ds = datetime.strptime(date_of_interest, '%d. %B %Y').strftime('%Y-%m-%d')

product_folder = 'alps/{}/'.format(ds)

product_name = "{}+000_alps_SWE_product.tif".format(ds)

selection = op.join(product_folder, product_name)

download_to = op.join('D:\Dashboards\Wetter\exolabs', op.basename(selection))

session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret,
            region_name='eu-central-1'
        )

s3 = session.client('s3')

s3.download_file(bucket, selection, download_to)
print(download_to)
