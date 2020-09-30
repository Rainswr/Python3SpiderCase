from io import BytesIO
from PIL import Image
import requests
import base64
from Pretreatment_MainColorRgb import MainColorRgb
from Pretreatment_TurnGrayField import TurnGrayField
import tesserocr


class ActualCase:
    Headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36"
    }

    def case3(self):
        """字母数字去噪"""
        url = "aHR0cDovL2NyZWRpdC5jdXN0b21zLmdvdi5jbi9jY3Bwc2VydmVyL3ZlcmlmeUNvZGUvY3JlYXRvcg=="
        url = base64.b64decode(url).decode("utf-8")
        resp = requests.get(url, headers=self.Headers)
        im = Image.open(BytesIO(resp.content))
        for num in [6, 7, 8, 9]:
            im.seek(num)
            byte_io = BytesIO()
            im.save(byte_io, format="PNG")
            im = Image.open(BytesIO(resp.content))
            im.show()
            # 去噪、二值化后的图片
            jpg_im = MainColorRgb.clean_image(byte_io.getvalue(), (10, 0, 90, 34), 2, 500, 200)
            jpg_im.show()
            print(num, ">>>>", tesserocr.image_to_text(jpg_im))

    def case2(self):
        """四字成语去噪"""
        url = "aHR0cDovL3h4Z2suc2h6ei5temouc2guZ292LmNuL0NvZGVTZXJ2bGV0"
        url = base64.b64decode(url).decode("utf-8")
        resp = requests.get(url, headers=self.Headers)
        im = Image.open(BytesIO(resp.content))
        im.show()
        # 去噪、二值化后的图片
        im = MainColorRgb.clean_image(resp.content, (35, 11, 162, 37), 5, 0, 27)
        im.show()
        print(tesserocr.image_to_text(im, lang='chi_sim'))

    def case1(self):
        """数字去噪点"""
        url = "aHR0cDovL3dlaXhpbi5jY29weXJpZ2h0LmNvbS9tZW1iZXJhcGkvbG9naW4vdmFsaWRhdGVJbWc="
        url = base64.b64decode(url).decode("utf-8")
        resp = requests.get(url, headers=self.Headers)
        im = Image.open(BytesIO(resp.content))
        im.show()
        # 去噪、二值化后的图片
        im = TurnGrayField.clean_image(resp.content, (7, 5, 60, 32), 130, 5)
        im.show()
        # print(tesserocr.image_to_text(im))


if __name__ == '__main__':
    _object = ActualCase()
    _object.case3()
