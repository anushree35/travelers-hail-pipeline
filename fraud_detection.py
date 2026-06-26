from PIL import Image, ExifTags

IMAGE_PATH = "sample_roof.jpg"

# create a blank placeholder image to test with
image = Image.new("RGB", (224, 224), color=(100, 100, 100))
image.save(IMAGE_PATH)

# open the image and read its hidden metadata
img = Image.open(IMAGE_PATH)
exif_data = img._getexif()

if exif_data is None:
    print("No metadata found — this is suspicious")
else:
    for tag, value in exif_data.items():
        name = ExifTags.TAGS.get(tag, tag)
        print(f"{name}: {value}")
