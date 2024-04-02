import boto3
import os
import sys
from os import path as op


def download_tif(access_key, 
                 secret_key, 
                 date_key, 
                 bucket,
                 output_dir='./data/raw/'):
    
    # Convert Date
    ds = date_key

    product_folder = 'alps/{}/'.format(ds)

    product_name = "{}+000_alps_SWE_product.tif".format(ds)

    selection = os.path.join(product_folder,
                        product_name)

    download_to = os.path.join(output_dir,
                          os.path.basename(selection))
    
    print(download_to)

    session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name='eu-central-1'
            )

    s3 = session.client('s3')

    s3.download_file(bucket, selection, download_to)

if __name__ == '__main__':
    date_key = str(sys.argv[1])

    # Convert Date
    ds = date_key

    product_folder = 'alps/{}/'.format(ds)

    product_name = "{}+000_alps_SWE_product.tif".format(ds)

    selection = op.join(product_folder, product_name)

    download_to = op.join('data/raw/', op.basename(selection))
    # Recall access and secret keys need to be exported in shell
    download_tif(access_key, 
                 secret_key, 
                 date_key, 
                 bucket)
            
    print('finished download')

