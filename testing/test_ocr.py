from ez_tess_ocr import create_ocr,release_ocr,ocr_image,ocr_conf
import cv2

def test_ocr():
    image = cv2.imread('./testing/ocr_test.png')
    api = create_ocr()
    text = ocr_image(api,image)
    conf = ocr_conf(api)
    release_ocr(api)
    assert text =='apt install tesseract-ocr' and conf >90


if __name__ =='__main__':
    test_ocr()