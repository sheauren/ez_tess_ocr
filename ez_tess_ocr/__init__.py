import ctypes
import ctypes.util
import cv2
import os
import sys

# find tessdata
base_dir = os.path.dirname(__file__)
__relative_tesslib_path = "../"
for _ in range(5):
    if os.path.exists(os.path.join(base_dir, __relative_tesslib_path, "tesslib")):
        break
    __relative_tesslib_path+='../'

os.environ["TESSDATA_PREFIX"] = os.path.normpath(
    os.path.join(os.path.join(base_dir, __relative_tesslib_path, "tesslib", "tessdata"))
)
if os.name == "nt":
    os.putenv("PATH", os.path.join(base_dir, __relative_tesslib_path, "tesslib"))
    lib_path = os.path.join(base_dir, __relative_tesslib_path, "libtessacert-5.dll")
else:
    lib_path = "libtesseract.so"
try:
    lib = ctypes.CDLL(lib_path)
except Exception as ex:
    if os.name == "nt":
        pass
    else:
        print(
            """
need install tesseract by:
sudo add-apt-repository -y ppa:alex-p/tesseract5-ocr
sudo apt -y install tesseract-ocr
"""
        )
    raise ex

__api_dict = dict()


class EzTessOrc:
    def __init__(self, char_whitelist=None, lang="eng"):
        self.char_whitelist = char_whitelist
        self.lang = lang
        self.api = create_ocr(char_whitelist, lang)

    def ocr(self, image):
        return ocr_image(self.api, image)

    def conf(self):
        return ocr_conf(self.api)

    def release(self):
        release_ocr(self.api)
        self.api = None


def create_ocr(char_whitelist=None, lang="eng"):
    global __api_dict
    name = char_whitelist or "default"
    if name in __api_dict:
        return __api_dict[name]

    class TessBaseAPI(ctypes._Pointer):
        _type_ = type("_TessBaseAPI", (ctypes.Structure,), {})

    # check tessdata contains lang file
    tessdata_path = os.path.join(os.environ["TESSDATA_PREFIX"], f"{lang}.traineddata")
    if not os.path.exists(tessdata_path):
        msg = f"need add lang data [{lang}.traineddata] to tessdata folder:[{os.environ['TESSDATA_PREFIX']}]"
        print(msg)
        sys.exit(-1)

    lib.TessBaseAPICreate.restype = TessBaseAPI
    api = lib.TessBaseAPICreate()
    lib.TessBaseAPIInit3.argtypes = (TessBaseAPI, ctypes.c_char_p, ctypes.c_char_p)
    lib.TessBaseAPIInit3(
        api, os.environ["TESSDATA_PREFIX"].encode("utf-8"), lang.encode("utf-8")
    )
    lib.TessBaseAPISetImage.argtypes = (
        TessBaseAPI,
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    )

    lib.TessBaseAPIGetUTF8Text.restype = ctypes.c_char_p
    lib.TessBaseAPIGetUTF8Text.argtypes = (TessBaseAPI,)
    lib.TessBaseAPIAllWordConfidences.restype = ctypes.POINTER(ctypes.c_int)

    char_whitelist = (
        char_whitelist
        or r"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.'-_:$=\/*"
    )

    lib.TessBaseAPISetVariable(
        api, "tesseract_char_whitelist".encode("UTF-8"), char_whitelist.encode("UTF-8")
    )
    lib.TessBaseAPISetVariable(
        api, "tessedit_pageseg_mode".encode("UTF-8"), "6".encode("UTF-8")
    )
    lib.TessBaseAPISetVariable(
        api, "user_defined_dpi".encode("UTF-8"), "300".encode("UTF-8")
    )
    __api_dict[name] = api
    return api


def ocr_image(api, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = image.shape
    lib.TessBaseAPISetImage(api, image.ctypes, w, h, 1, w * 1)
    txt = lib.TessBaseAPIGetUTF8Text(api)
    return ctypes.string_at(txt).decode("utf-8").strip()


def ocr_conf(api):
    return lib.TessBaseAPIMeanTextConf(api)


def release_ocr(api):
    lib.TessBaseAPIEnd(api)
    lib.TessBaseAPIDelete(api)


def release_all():
    global __api_dict
    for api in __api_dict.values():
        release_ocr(api)
    __api_dict.clear()


if __name__ == "__main__":
    api = create_ocr()
    image = cv2.imread("./testing/ocr_test.png")
    text = ocr_image(api, image)
    conf = ocr_conf(api)
    #release_ocr(api)
    release_all()
    print("text", text, "conf", conf)
