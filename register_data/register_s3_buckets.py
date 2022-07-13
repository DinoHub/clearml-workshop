"""
This script will register s3 data as a ClearML hyperdataset.
The script will register each image in the bucket as a SingleFrame in ClearML dataset, in a version named on the base
folder in the bucket.

Example:
    For s3 bucket with paths s3://bucket/folder1/.../base_folder/train/<images>,
    s3://bucket/folder1/.../base_folder/test/<images>
    running the script with `s3://bucket/folder1/.../base_folder/` parameter will create 2 new versions, train and test
    each with the images stored in the bucket

You can run this example from this dir with:

python register_s3_buckets.py --ds_name coco_sample --bucket s3://bucket/folder/
"""
import os
from argparse import ArgumentParser

from allegroai import DatasetVersion, SingleFrame
from clearml import StorageManager


def create_frames(bucket):
    """
    Create a dictionary with the version name as a key and list of frames as value
    :param bucket: The bucket root path to folders to write in the dataset
    :return: dictionary with version name and list of frames for the version, e.g.
        {"version_name": [SingleFrame1, SingleFrame2,..., SingleFrameN], ...}
    """
    # Get the bucket's internal folders
    b_folders = StorageManager.list(bucket)
    # Generate single frames
    versions_frames = {}
    print("Going over the follow: {}".format(b_folders))
    for folder in b_folders:
        versions_frames[folder] = []
        # Get the files in the bucket
        files_path = os.path.join(bucket, folder)
        print("Listing file inside {} dir".format(files_path))
        folder_files = StorageManager.list(files_path)
        for file in folder_files:
            # Our source for each frame is the link to this file in the bucket
            f = SingleFrame(source=file)  # The source here should be the S3 path to the file
            versions_frames[folder].append(f)
    return versions_frames


def create_version_with_frames(ds_name, frames_dict):
    """
    Create a version per key in the dictionary and upload the frames to it
    :param ds_name: Dataset name for the versions
    :param frames_dict: dictionary contain the version name as a key and list of frames as value
    """
    ds = DatasetVersion.create_new_dataset(ds_name)
    for version_name, frames in frames_dict.items():
        # get new version in a Dataset (this is our version we will upload to)
        dv = ds.create_version(version_name=version_name)
        print('starting upload')
        dv.add_frames(frames)
        dv.commit_version()
        print('Done uploading {} frames to version {}'.format(len(frames), version_name))


if __name__ == '__main__':
    parser = ArgumentParser(description='Register allegro dataset from S3 bucket')

    parser.add_argument('--ds_name', type=str, help='Dataset name for the data', required=True)
    parser.add_argument('--bucket', type=str, help='Bucket root path to copy the data from')

    args = parser.parse_args()

    ver_frames_dict = create_frames(args.bucket)

    create_version_with_frames(args.ds_name, ver_frames_dict)
