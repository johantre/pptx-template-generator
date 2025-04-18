import hashlib
from PIL import Image
from pptx.util import Inches, Pt, Emu  # Emu = English Metric Unit, 1 inch = 914400 EMU

def get_hash(filename):
    with open(filename, "rb") as f:
        blob = f.read()
    sha1 = hashlib.sha1(blob)
    return sha1.hexdigest()

# Replace image and resize to the new image's original dimensions
def replace_img_slide(slide, img_shape, img_path):
    # Step 1: Read new image binary data
    with open(img_path, 'rb') as f:
        new_img_blob = f.read()

    # Step 2: Replace image content
    img_pic = img_shape._pic
    img_rid = img_pic.xpath('./p:blipFill/a:blip/@r:embed')[0]
    img_part = slide.part.related_part(img_rid)
    img_part._blob = new_img_blob

    # Step 3: Get new image dimensions (in pixels)
    with Image.open(img_path) as im:
        px_width, px_height = im.size
        dpi = im.info.get("dpi", (96, 96))  # Some images don't contain DPI info, default to 96
        inch_width = px_width / dpi[0]
        inch_height = px_height / dpi[1]

    # Step 4: Adjust image shape size (in EMU units)
    img_shape.width = Inches(inch_width)
    img_shape.height = Inches(inch_height)
