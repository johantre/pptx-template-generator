import hashlib
from PIL import Image
from pptx.util import Inches

def get_hash(filename):
    with open(filename, "rb") as f:
        blob = f.read()
    sha1 = hashlib.sha1(blob)
    return sha1.hexdigest()

def replace_img_slide(slide, img_shape, img_path):
    # Step 1: 替换图片内容
    img_pic = img_shape._pic
    img_rid = img_pic.xpath('./p:blipFill/a:blip/@r:embed')[0]
    img_part = slide.part.related_part(img_rid)

    with open(img_path, 'rb') as f:
        new_img_blob = f.read()
    img_part._blob = new_img_blob

    # Step 2: 获取新图尺寸（像素）和 DPI
    with Image.open(img_path) as im:
        px_w, px_h = im.size
        dpi = im.info.get("dpi", (96, 96))  # 默认 96 DPI
        inch_w = px_w / dpi[0]
        inch_h = px_h / dpi[1]

    # Step 3: 获取原图形状尺寸和中心位置（单位：EMU）
    orig_w = img_shape.width
    orig_h = img_shape.height
    center_x = img_shape.left + orig_w // 2
    center_y = img_shape.top + orig_h // 2

    # Step 4: 缩放计算，保持不超出原图区域
    shape_w_inch = orig_w / 914400
    shape_h_inch = orig_h / 914400
    scale_w = shape_w_inch / inch_w
    scale_h = shape_h_inch / inch_h
    scale = min(scale_w, scale_h, 1.0)  # 不放大，只等比缩小

    final_w = Inches(inch_w * scale)
    final_h = Inches(inch_h * scale)

    # Step 5: 应用新尺寸
    img_shape.width = final_w
    img_shape.height = final_h

    # Step 6: 将形状重新居中回原图位置
    img_shape.left = int(center_x - final_w / 2)
    img_shape.top = int(center_y - final_h / 2)
