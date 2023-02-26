import json
import time
import requests
import shutil
from alive_progress import alive_bar

# URL to access the album
start_url = "https://postimg.cc/json"
import os

def create_img_set():
    # Create a set to store images
    img_set = set()

    # Iterate over the files in the directory
    for file in os.listdir('./memes/'):
        # Check if the file is an image
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
            # Add the file to the set
            img_set.add(file)

    # Return the set
    return img_set
# Start page of the album
start_page = 1

# Content of the request
content = f"action=list&album=XCFBXjj&page={start_page}"

# Headers of the request
headers = {
    "Host": "postimg.cc",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "32",
    "Origin": "https://postimg.cc",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://postimg.cc/gallery/XCFBXjj",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "TE": "trailers"
}

# List of images in album
total_images = []

# Loop until all the images in the album are collected
while True:
    # Make request
    response = requests.post(start_url, data=content, headers=headers)
    # Get images from response
    images = json.loads(response.text)
    has_page_next = json.loads(response.text).get("has_page_next")
    # Add images to list
    if has_page_next:
        total_images.extend(images["images"])
        start_page += 1
        content = f"action=list&album=XCFBXjj&page={start_page}"
    else:
        break

# Create dictionary of image names and URLs
clear_list_images = {
    f"{item[2]}.{item[3]}":
    f"https://i.postimg.cc/{item[1]}/{item[2]}.{item[3]}"
    for item in total_images
}

# Zip together the image names and URLs
zipped_list = zip(clear_list_images.keys(), clear_list_images.values())


def download_images(images: tuple[str, str]) -> None:
    """Download images from album.

    Parameters:
        images (tuple[str, str]): Tuple of image names and URLs.
    """
    with alive_bar(len(clear_list_images)) as bar:
        # Initialize variables
        current_image = images[0][0]
        last_image = images[-1][0]
        break_count = 0
        while current_image != last_image:
            try:
                # Loop through images
                for count, name_and_url in enumerate(images):
                    if current_image == last_image:
                        break
                    if count != break_count:
                        continue
                    break_count += 1
                    current_image = name_and_url[0]
                    # Make request
                    response = requests.get(name_and_url[1], stream=True)
                    # Write image to file
                    with open(f"./memes/{name_and_url[0]}", 'wb') as outfile:
                        shutil.copyfileobj(response.raw, outfile)
                        bar()
            except Exception as e:
                print(e)
                time.sleep(30)


download_images(tuple(zipped_list))