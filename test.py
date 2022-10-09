import json
import time
import requests
import shutil

from alive_progress import alive_bar

start_url = "https://postimg.cc/json"
start_page = 1
content = f"action=list&album=XCFBXjj&page={start_page}"
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

total_images = []
while True:
    response = requests.post(start_url, data=content, headers=headers)
    images = json.loads(response.text)
    has_page_next = json.loads(response.text).get("has_page_next")
    if has_page_next:
        total_images.extend(images["images"])
        start_page += 1
        content = f"action=list&album=XCFBXjj&page={start_page}"
    else:
        break

clear_list_images = {
    f"{item[2]}.{item[3]}":
    f"https://i.postimg.cc/{item[1]}/{item[2]}.{item[3]}"
    for item in total_images
}
# print(clear_list_images)

zipped_list = zip(clear_list_images.keys(), clear_list_images.values())


def download_images(images: tuple[str, str]) -> None:
    with alive_bar(len(clear_list_images)) as bar:
        current_image = images[0][0]
        last_image = images[-1][0]
        break_count = 0
        while current_image != last_image:
            try:
                for count, name_and_url in enumerate(images):
                    if current_image == last_image:
                        break
                    if count != break_count:
                        continue
                    break_count += 1
                    current_image = name_and_url[0]
                    response = requests.get(name_and_url[1], stream=True)
                    with open(f"./memes/{name_and_url[0]}", 'wb') as outfile:
                        shutil.copyfileobj(response.raw, outfile)
                        bar()
            except Exception as e:
                print(e)
                time.sleep(30)


download_images(tuple(zipped_list))