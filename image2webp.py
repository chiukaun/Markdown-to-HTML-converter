from PIL import Image
import os

def image2webp(path):
    im = Image.open(path)
    image_name = input("Yo File name be like: ")
    rename = image_name + ".webp"
    source_file = os.path.join(os.path.split(path)[0], rename)
    im.save(source_file, "webp")

image_path = input("Sup, Image path be like: (drag it here bro) ").strip("'")
image2webp(image_path)