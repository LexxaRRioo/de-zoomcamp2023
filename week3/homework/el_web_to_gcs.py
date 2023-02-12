from pathlib import Path
from google.cloud import storage

import os
import wget

project_id = 'de-zoomcamp-2023-375411'
bucket_name = 'dez-week3-razvodov'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= '/home/AlexRaz/de-zoomcamp-2023-375411-380c4b80eee9.json'

def download_file(filename: str) -> Path:
    dataset_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{filename}'
    os.system(f'wget {dataset_url} -O data/{filename}')
    path = f'/home/AlexRaz/git/de-zoomcamp2023/week3/homework/data/{filename}'
    return path


def upload_file(bucket_name, source_path, gcs_path, project_id):
  """Uploads a file to the bucket."""
  storage_client = storage.Client(project_id)
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(gcs_path)
  blob.upload_from_filename(source_path)
  print(f'\nFile {source_path} uploaded to {gcs_path}.')


def etl_parent_flow(bucket_name: str, project_id: str, months: list[int] = [1, 2], years: list[int] = [2020]):

    for year in years:
        for month in months:
            filename = f'fhv_tripdata_{year}-{month:02}.csv.gz'
            path = download_file(filename)
            #path = '/home/AlexRaz/git/de-zoomcamp2023/week3/homework/data/fhv_tripdata_2019-01.csv.gz uploaded to data/fhv_tripdata_2019-01.csv.gz'
            gcs_path = f'data/{filename}'
            upload_file(bucket_name=bucket_name, source_path=path, gcs_path=gcs_path, project_id=project_id)
    
    return


if __name__ == "__main__":
    months = [*range(1,13)]
    years = [*range(2019,2022)]
    etl_parent_flow(months=months, years=years, bucket_name=bucket_name, project_id=project_id)



# предусмотреть обработку ошибки если месяц не существует


# wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-02.csv.gz
# wget https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv/fhv_tripdata_2019-02.csv.gz -O data/fhv_tripdata_2019-02.csv