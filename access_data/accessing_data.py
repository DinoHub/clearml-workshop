"""
How to access and go over data
The general flow:
 - Create new dataview.
 - Query your dataview.
 - Two ways to go over the frames:
   - dataview.get_iterator()
   - dataview.to_list()
"""

from allegroai import DataView, IterationOrder, Task

import cv2

task = Task.init(project_name="examples", task_name="dv accessing")


# Create a DataView object for a simple query
dataview = DataView(name="train")

# Please change the label "person" to a one you have in the version
# A simple query example: filter for images with the annotation label "person"
dataview.add_query(
    dataset_id='Your dataset ID',
    version_id='Your version ID',
    roi_query='person'
)

# You can also connect a dataview with `task.connect` - in this case, it will connect to the task automatically
# task.connect(dataview)

# Start pre-fetching the actual images
# The call returns immediately and the pre-fetching id done in the backgrounds
dataview.prefetch_files()


# Iterate over the SingleFrames returned by the DataView
for idx, frame in enumerate(dataview.get_iterator()):
    # Download the file locally
    local_file = frame.get_local_source()

    print(local_file, frame.annotations)
    im = cv2.imread(local_file)
    cv2.imshow('image', im)
    cv2.waitKey()
    if idx == 10:  # stop after 10 files
        break

# First, set the DataView to iterate randomly over our images
dataview = DataView(iteration_order=IterationOrder.random)

# A frame metadata query example: key "dangerous" and value "no"
dataview.add_multi_query(
    dataset_name='YOUR DATASET NAME',
    version_name='YOUR VERSION NAME',
    frame_query='meta.dangerous:"no"',
)


# Start pre-fetching the actual images
# The call returns immediately and the pre-fetching id done in the backgrounds
dataview.prefetch_files()

# Iterate over the SingleFrames returned by the DataView
for idx, frame in enumerate(dataview.get_iterator()):
    # Download the file locally
    local_file = frame.get_local_source()

    print(local_file, frame.annotations)
    im = cv2.imread(local_file)
    cv2.imshow('image', im)
    cv2.waitKey()
    if idx == 10:  # stop after 10 files
        break


# A complex query example with more sophisticated filter
# First, set the DataView to iterate randomly over our images
dataview = DataView(iteration_order=IterationOrder.random)

# Second, set a seed number for random order
dataview.set_iteration_parameters(random_seed=1337)

# A complex query example: filter for ROI labels "aeroplane" and "person and
#   frame metadata key "dangerous" and value "no"
dataview.add_multi_query(
    dataset_name='YOUR DATASET NAME',
    version_name='YOUR VERSION NAME',
    frame_query='meta.dangerous:"no"',
    roi_queries=[{'label': 'aeroplane'}, {'label': 'person'}]
)

# Get a list of SingleFrames
frames = dataview.to_list()


for idx, frame in enumerate(frames):
    # Download the file locally
    local_file = frame.get_local_source()

    print(local_file, frame.annotations)
    im = cv2.imread(local_file)
    cv2.imshow('image', im)
    cv2.waitKey()
    if idx == 10:  # stop after 10 files
        break
