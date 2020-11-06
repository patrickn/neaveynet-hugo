#!/usr/bin/python
#
# Creates a JSON file containing a list of all the images used on this site.
# This is provided to allow 3rd party access to the images. 

import os
import os.path
import json
import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


# Constants
IMAGE_PATH = "static/img"
SITE_URL = "https://www.neavey.net/"
FILE_TYPES = (".jpg", ".jpeg")
OUTPUT_JSON = "public/image_list.json"

##############################################################################
# Returns a dictionary from the exif data of an PIL Image item. 
# Also converts the GPS Tags
#
def get_exif_data(image):
    exif_data = {}
    info = image.getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

##############################################################################
# Helper function to convert the GPS coordinates stored in the EXIF to 
# degress in float format
def _convert_to_degress(value):
    deg_num, deg_denom = value[0]
    d = float(deg_num) / float(deg_denom)

    min_num, min_denom = value[1]
    m = float(min_num) / float(min_denom)

    sec_num, sec_denom = value[2]
    s = float(sec_num) / float(sec_denom)
    
    return d + (m / 60.0) + (s / 3600.0)

##############################################################################
# Returns the latitude, longitude and altitude, if available, from the 
# provided exif_data (obtained through get_exif_data above)
def get_lat_lon_alt(exif_data):
    lat = None
    lon = None
    alt = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = gps_info.get("GPSLatitude")
        gps_latitude_ref = gps_info.get("GPSLatitudeRef")
        gps_longitude = gps_info.get("GPSLongitude")
        gps_longitude_ref = gps_info.get("GPSLongitudeRef")
        gps_altitude = gps_info.get("GPSAltitude")

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat *= -1

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon *= -1

        alt = gps_altitude

    return lat, lon, alt

##############################################################################
# Get the telemetry data from an image file
def get_location(file):
    image = Image.open(file)
    timestamp = image.getexif().get(36867)
    exif = get_exif_data(image)
    lat, lon, alt = get_lat_lon_alt(exif)
    return [lat, lon, alt, timestamp]

##############################################################################
if __name__ == "__main__":

    image_list = []

    for dirpath, dirnames, filenames in os.walk(IMAGE_PATH):
        for filename in [f for f in filenames if f.endswith(FILE_TYPES)]:

            lat, lon, alt, timestamp = get_location(os.path.join(dirpath, filename))      

            image_record = {"name": SITE_URL + os.path.join(dirpath.replace("static/", ""), filename),
                            "timestamp": timestamp,
                            "lat": lat,
                            "lon": lon,
                            "alt": alt }
            image_list.append(image_record)

    ##############################################################################
    # Output format is as follows:
    #
    # {
    #     "last_update": "Sat Oct 31 12:22:16 2020",
    #     "number_of_images": 223
    #     "image_list": [ { "name": "image_123.jpg",
    #                       "lat": "51.03",
    #                       "lon": "4.48",
    #                       "alt": "1.23" },
    #                     { "name": "image_456.jpg",
    #                       "lat": "51.03",
    #                       "lon": "4.48",
    #                       "alt": "1.23" },
    #                     { "name": "image_789.jpg",
    #                       "lat": "51.03",
    #                       "lon": "4.48",
    #                       "alt": "1.23" },
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
