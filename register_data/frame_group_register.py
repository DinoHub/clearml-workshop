"""
This script will register a new FrameGroup with 2 frames ('ship' and 'crew') for 'frameGroup example' dataset.
The FrameGroup will have ROIs and metadata for FrameGroup level.

"""
from allegroai import DatasetVersion, FrameGroup, SingleFrame
from allegroai.dataframe import ImageAnnotation

# See FrameGroup() for full set of arguments for the constructor
# Notice: if we do not provide ID for the frame, a consistent ID will be generated based
# on the frames and 'source's links
frame_group = FrameGroup(id=None)

# Creating and Adding the first "ship" to the FrameGroup
frame_group['ship'] = SingleFrame(
                    # this is where the frame is actually stored
                    source='https://upload.wikimedia.org/wikipedia/en/8/8d'
                           '/A_screenshot_from_Star_Wars_Episode_IV_A_New_Hope_depicting_the_Millennium_Falcon.jpg',
                    # some additional information on the specific frame
                    metadata={'episode': 4, 'name': 'Millennium_Falcon'}
)

# Creating and Adding the "crew" SingleFrame to the FrameGroup
frame_group['crew'] = SingleFrame(
                    # this is where the frame is actually stored
                    source='https://upload.wikimedia.org/wikipedia/en/8/82/Leiadeathstar.jpg'
)

# Adding metadata to the FrameGroup
frame_group.metadata = {
    'location': 'somewhere in a galaxy',
    'distance': 'far far away',
    'year': 1977
}

# Add annotations

# See SingleFrame.add_annotation for full features and documentation
frame_group['crew'].add_annotation(box2d_xywh=(31, 42, 78.5456, 75.56), labels=['Luke'])
frame_group['crew'].add_annotation(box2d_xywh=(248.46, 12.44, 80.7, 85.356), labels=['Han'])
frame_group['crew'].add_annotation(box2d_xywh=(129.7, 70, 65, 70), labels=['Leia'])


# Add a global annotation
# example for frame annotation, will add a label with 'the_force' to all the images in the FrameGroup
frame_group.add_global_annotation(ImageAnnotation(labels=["the_force"]))

# Create a dataset if it doesn't exists already
DatasetVersion.create_new_dataset(dataset_name='Star_Wars')

# Create a dataset version. Dataset version is a collection of frames and annotations,
# we could later freeze this version, and avoid accidental data overwriting or loss.
dataset = DatasetVersion.create_version(dataset_name='Star_Wars', version_name="Jedi_Team")

# Add or Update frames in the dataset
# after this function is executed, we will be able to see the new frame in the web-app
dataset.add_frames([frame_group, ])

print('We are done, see you next time & may the force be with you.')
