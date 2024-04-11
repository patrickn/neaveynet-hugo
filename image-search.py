#!/usr/bin/python
#
# Creates a JSON file containing a list of all the images used on this site.
# This is provided to allow 3rd party access to the images.

import os
import os.path
import json
import datetime
from PIL import Image


# Constants
IMAGE_PATH = "static/img"
SITE_URL = "https://www.adventuremiles.net/"
FILE_TYPES = (".jpg", ".jpeg")
OUTPUT_JSON = "public/image_list.json"

##############################################################################
# Get the telemetry data from an image file
def get_timeAndData(file):
    image = Image.open(file)
    timestamp = image.getexif().get(36867)
    return timestamp

##############################################################################
if __name__ == "__main__":

    image_list = []

    for dirpath, dirnames, filenames in os.walk(IMAGE_PATH):
        for filename in [f for f in filenames if f.endswith(FILE_TYPES)]:

            timestamp = get_timeAndData(os.path.join(dirpath, filename))

            image_record = {"name": SITE_URL + os.path.join(dirpath.replace("static/", ""), filename),
                            "timestamp": timestamp }
            image_list.append(image_record)

    ##############################################################################
    # Output format is as follows:
    #
    # {
    #     "last_update": "Sat Oct 31 12:22:16 2020",
    #     "number_of_images": 223
    #     "image_list": [ { "name": "image_123.jpg",
    #                       "timestamp": "2015:07:20 12:34:46" },
    #                     { "name": "image_456.jpg",
    #                       "timestamp": "2015:07:20 12:23:15" },
    #                     { "name": "image_789.jpg",
    #                       "timestamp": "2015:07:19 14:50:13" },
    #                        ...
    #                   ]
    # }

    with open(OUTPUT_JSON, "w") as f:
        image_db = {
            "last_modified": datetime.datetime.fromtimestamp(os.path.getmtime(OUTPUT_JSON)).isoformat(),
            "number_of_images": len(image_list),
            "image_list": image_list
        }
        json.dump(image_db, f)
