import os
import os.path
import time
import json

# Constants
IMAGE_PATH = "static/img"
FILE_TYPES = (".jpg", ".jpeg")
OUTPUT_JSON = "public/image_list.json"

image_list = []

for dirpath, dirnames, filenames in os.walk(IMAGE_PATH):
    for filename in [f for f in filenames if f.endswith(FILE_TYPES)]:
        image_record = {"name": os.path.join(dirpath, filename)}
        image_list.append(image_record)

##############################################################################
# Output format is as follows. It is left like this to be extendable in the 
# future, for example adding lat/long together with the image name.
#
# {
#     "last_update": "Sat Oct 31 12:22:16 2020",
#     "number_of_images": 223
#     "image_list": [ { "name": "image_123.jpg" },
#                     { "name": "image_456.jpg" },
#                     { "name": "image_789.jpg" },
#                      ...
#                   ]
# }

with open(OUTPUT_JSON, "w") as f:
    image_db = {
        "last_modified": time.ctime(os.path.getmtime(OUTPUT_JSON)),
        "number_of_images": len(image_list),
        "image_list": image_list
    }
    json.dump(image_db, f)
