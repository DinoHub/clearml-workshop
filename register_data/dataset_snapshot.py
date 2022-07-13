"""
Create a snapshot for a version.

This script will create a snapshot version for the latest version in "cats" dataset.
First, it will create and upload a frame to "cata" dataset, and after it will create a snapshot for this version.
"""

from allegroai import DatasetVersion, SingleFrame


new_ds_name = "cats"
save_version = True

# notice if we do not provide ID for the frame,
# The ID will be created based on the URL of the image
frame = SingleFrame(
    source='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/1280px-Cat_poster_1.jpg',
)


# Add annotation
# example bounding box at x=10,y=10 with width of 30px and height of 20px
# label of the bounding box is test
# See SingleFrame.add_annotation for full features and documentation
frame.add_annotation(box2d_xywh=(10, 10, 30, 20), labels=['test'])

# Create a dataset if it doesn't exists already
DatasetVersion.create_new_dataset(dataset_name=new_ds_name)

# Gets latest editable version
dataset = DatasetVersion.get_current(dataset_name=new_ds_name)

# Add or Update frames in the dataset
# after this function is executed, we will be able to see the new frame in the web-app
dataset.add_frames([frame])
dataset.commit_version()

# Creating a snapshot thus locking version for changes and creating a new one for editing
if save_version:
    DatasetVersion.create_snapshot(dataset_name=new_ds_name)

print('We are done, see you next time')
