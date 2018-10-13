import io
import os
import sys
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from loc_summary import locational_summary


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    # print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        # print('\n{} (confidence: {})'.format(object_.name, object_.score))
        # print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
    locational_summary(objects)

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
# Change the filename when using here
file_name = os.path.join(
    os.path.dirname(__file__),
    'test6b.png')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
localize_objects(file_name)
