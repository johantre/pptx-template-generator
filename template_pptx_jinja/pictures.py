import hashlib
from PIL import Image
from pptx.util import Inches, Pt, Emu  # Emu = 英制单位，1英寸 = 914400 EMU

def get_hash(filename):
    with open(filename, "rb") as f:
        blob = f.read()
    sha1 = hashlib.sha1(blob)
    return sha1.hexdigest()

# 替换图片并将尺寸调整为新图的原始尺寸
def replace_img_slide(slide, img_shape, img_path):
    # Step 1: 读取新图像的二进制
    with open(img_path, 'rb') as f:
        new_img_blob = f.read()

    # Step 2: 替换图片内容
    img_pic = img_shape._pic
    img_rid = img_pic.xpath('./p:blipFill/a:blip/@r:embed')[0]
    img_part = slide.part.related_part(img_rid)
    img_part._blob = new_img_blob

    # Step 3: 获取新图片的尺寸（以像素为单位）
    with Image.open(img_path) as im:
        px_width, px_height = im.size
        dpi = im.info.get("dpi", (96, 96))  # 有些图片不含 DPI 信息，默认 96
        inch_width = px_width / dpi[0]
        inch_height = px_height / dpi[1]

    # Step 4: 调整图片形状尺寸（单位为 EMU）
    img_shape.width = Inches(inch_width)
    img_shape.height = Inches(inch_height)
