from src.object_detection import process_img
from src.utils import load_image_from_url


def test_process_img_returns_int():
    url = "https://raw.githubusercontent.com/KamSaf/adv_programming/refs/heads/person_detection/examples/example.jpg"
    expt_ppl_num = 27
    img = load_image_from_url(url)
    assert img is not None
    ppl_num = process_img(img)
    assert ppl_num == expt_ppl_num
