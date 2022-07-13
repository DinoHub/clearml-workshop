"""
How to register data with ROIs and metadata from a json file.
Create a list of ROI's for each image in the metadata format required by a frame.

Notice: This is a custom parser for a specific dataset. Each dataset requires a different parser.

You can run this example from this dir with:

python registration_with_roi_and_meta.py
--path data/sample_ds --ext jpg --ds_name my_uploaded_dataset --version_name my_version
"""
import glob
import json
import os
from argparse import ArgumentParser

from allegroai import DatasetVersion, SingleFrame
from pathlib2 import Path


def add_rois_to_frame(filename, a_frame):
    """
    Add the ROIs for each frame
    :param filename: Full file path
    :type filename: str
    :param a_frame: Frame to add ROIs
    :type a_frame: SingleFrame
    """
    data = get_json_file(filename)

    # Iterating over rois in the json
    for roi in data['rois']:
        a_frame.add_annotation(
            poly2d_xy=roi["poly"],
            labels=roi['labels'],
            metadata={'alive': roi['meta']['alive']},
            confidence=roi['confidence']
        )


def add_frame_meta(filename, single_frame):
    """
    Add the metadata for each frame
    :param filename: Full file path
    :type filename: str
    :param single_frame: Frame to add metadata
    :type single_frame: SingleFrame
    """
    data = get_json_file(filename)
    single_frame.width = data['size']['x']
    single_frame.height = data['size']['y']
    single_frame.metadata['dangerous'] = data['meta']['dangerous']
    single_frame.preview_source = data['url']


def get_json_file(filename):
    """
    Get the data from the json file
    :param filename: Full file path
    :type filename: str
    :return: json data parse as python dictionary
    """
    json_file_path = filename.replace('.jpg', '.json')

    json_file = open(json_file_path, "r")
    data = json.load(json_file)
    json_file.close()

    return data


def get_frames_with_roi_meta(ext):
    fr = []
    # Go over each jpg file in base path
    for file in glob.glob(os.path.join(base_path, "*.{}".format(ext))):
        full_path = os.path.abspath(file)
        print("Getting files from: " + full_path)

        # Create the SingleFrame object
        frame = SingleFrame(source=full_path)

        add_rois_to_frame(full_path, frame)
        add_frame_meta(full_path, frame)
        fr.append(frame)
    return fr


def create_version_with_frames(new_frames, ds_name, ver_name):
    # Get the dataset (will create a new one if we don't have such) version
    ds = DatasetVersion.create_new_dataset(dataset_name=ds_name)
    dv = ds.create_version(version_name=ver_name) if ver_name else DatasetVersion.get_current(dataset_name=ds_name)
    # Add frames to created version
    dv.add_frames(new_frames)
    dv.commit_version()


if __name__ == '__main__':
    parser = ArgumentParser(description='Register allegro dataset with rois and meta')

    parser.add_argument('--path', type=str, help='Path to the folder you like to register.', required=True)
    parser.add_argument('--ext', type=str, help='Files extension to upload from the dir. Default', default="*")
    parser.add_argument('--ds_name', type=str, help='Dataset name for the data', required=True)
    parser.add_argument('--version_name', type=str, help='Version name for the data (default is current version)')

    args = parser.parse_args()

    # this folder contains the images and json files for the data
    base_path = str(Path(__file__).parent / args.path)
    dataset_name = args.ds_name
    version_name = args.version_name

    frames = get_frames_with_roi_meta(args.ext)

    create_version_with_frames(frames, dataset_name, version_name)
    print("We are done :)")
