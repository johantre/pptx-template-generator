from copy import deepcopy

def duplicate_slide(pres, slide):
    slide_id = slide.slide_id
    slide_layout = slide.slide_layout
    new_slide = pres.slides.add_slide(slide_layout)
    # Verwijder standaard shapes
    for shape in list(new_slide.shapes):
        new_slide.shapes._spTree.remove(shape._element)
    # Kopieer shapes
    for shape in slide.shapes:
        new_element = deepcopy(shape._element)
        new_slide.shapes._spTree.insert_element_before(new_element, 'p:extLst')
    return new_slide

def copy_shapes(src_slide, dest_slide):
    # Verwijder bestaande shapes (uit layout)
    for shape in list(dest_slide.shapes):
        dest_slide.shapes._spTree.remove(shape._element)

    # Kopieer shapes van src_slide
    for shape in src_slide.shapes:
        new_element = deepcopy(shape._element)
        dest_slide.shapes._spTree.insert_element_before(new_element, 'p:extLst')


def get_shape_text(shape):
    """Geeft de volledige tekstinhoud van een shape terug, of een lege string."""
    if not shape.has_text_frame:
        return ""
    return "\n".join([p.text for p in shape.text_frame.paragraphs])


def is_placeholder(shape):
    """Geeft True als de shape een placeholder is (bv. titel, inhoud)."""
    return hasattr(shape, "placeholder_format")
