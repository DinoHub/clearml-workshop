"""
This script will register local data and upload it to cloud.
It will replace the source in your SingleFrame object to the one uploaded to the cloud which make this dataset version
accessible to everyone using this allegro dataset.

Data is hash based on the data content, so for 2 or more different files paths but the same content, only one copy will
be uploaded.
For each dataset, a new file will be uploaded (for example, ~/toy_img/Aaron_Guiel/Aaron_Guiel_0001.jpg will be uploaded
once for dataset_A and another copy for dataset_B, but will be the same for every version in each dataset).

You can run this example from this dir with:

python register_dataset_with_upload.py
--path ./toy_img/ --ext jpg --ds_name my_uploaded_dataset --version_name my_version
--bucket s3://bucket/folder/
"""
from argparse import ArgumentParser

from allegroai import DatasetVersion, SingleFrame
from pathlib2 import Path


def get_frames(base_folder, ext):
    # Generate single frames
    ret_frames = []
    base_folder = Path(base_folder)
    for file in base_folder.rglob('*.{}'.format(ext)):
        f = SingleFrame(source=file.absolute().as_posix(), metadata={"meta": "data"})  # ~/toy_img/Aaron_Guiel/Aaron_Guiel_0001.jpg
        ret_frames.append(f)
    return ret_frames


def create_version_with_frames(ds_name, version_name, version_frames, bucket=None, path=None):
    ds = DatasetVersion.create_new_dataset(ds_name)
    # get new version in a Dataset (this is our version we will upload to)
    dv = ds.create_version(version_name=version_name) if version_name \
        else DatasetVersion.get_current(dataset_name=ds_name)
    print('starting upload')
    dv.add_frames(
        version_frames,
        auto_upload_destination=bucket,
        local_dataset_root_path=path if bucket else None,
    )
    dv.commit_version()
    print('Done uploading {} frames'.format(len(version_frames)))


if __name__ == '__main__':
    parser = ArgumentParser(description='Register allegro dataset and upload data')

    parser.add_argument('--path', type=str, help='Path to the folder you like to register.', required=True)
    parser.add_argument('--ext', type=str, help='Files extension to upload from the dir. Default', default="*")
    parser.add_argument('--ds_name', type=str, help='Dataset name for the data', required=True)
    parser.add_argument('--version_name', type=str, help='Version name for the data (default is current version)')
    parser.add_argument('--bucket', type=str, help='Bucket path to upload the data to (s3://bucket/folder/)')

    args = parser.parse_args()

    frames = get_frames(args.path, args.ext)

    create_version_with_frames(args.ds_name, args.version_name, frames, args.bucket, args.path)
