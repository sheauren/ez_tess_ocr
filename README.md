# ez_tess_ocr install
```python
pip install ez_tess_ocr
```
# linux need install tesseract-ocr
```cmd
sudo add-apt-repository -y ppa:alex-p/tesseract5-ocr
sudo apt -y install tesseract-ocr
```

# example
```python
from ez_tess_ocr import create_ocr,release_ocr,ocr_image,ocr_conf
import cv2

def test_ocr():
    image = cv2.imread('./testing/ocr_test.png')
    api = create_ocr()
    text = ocr_image(api,image)
    conf = ocr_conf(api)
    release_ocr(api)
    print('text',text,'conf',conf)


if __name__ =='__main__':
    test_ocr()
```

# change language (default='eng')
```cmd
copy 
```