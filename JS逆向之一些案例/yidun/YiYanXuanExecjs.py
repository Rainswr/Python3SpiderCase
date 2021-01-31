# encoding: utf-8
import requests
import cv2
import numpy as np
import re
import json
import random
from urllib.parse import urlencode
import execjs
from PIL import Image


class YiDunecard:

    def __init__(self):
        self.user_agent = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"}
        self.headers = {
            'Accept': "*/*",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            'Host': "webzjcaptcha.reg.163.com",
            "Referer": "https://dl.reg.163.com/",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
        self.img_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Host': "necaptcha.nosdn.127.net",
            "Referer": "https://dl.reg.163.com/",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        }
        self.proxy = {}
        self.fp = ""
        self.get_id_params = {
            "id": "7ef4da58447919badeea0a8b20ac7e54",
            "fp": "",
            "https": "true",
            "type": "2",
            "version": "2.14.1",
            "dpr": 1,
            "dev": 1,
            "cb": "",
            "ipv6": "false",
            "runEnv": 10,
            "group": "",
            "scene": "",
            "width": 300,
            "token": "",
            "referer": "https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html",
            "callback": "__JSONP_ujwusz1_0"
        }
        self.check_id_params = {
            "id": "7ef4da58447919badeea0a8b20ac7e54",
            "token": "",
            "acToken": "",
            "width": 300,
            "data": "",
            "type": 2,
            "version": "2.14.1",
            "cb": "",
            "extraData": "",
            "runEnv": 10,
            "referer": "https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html",
            "callback": "__JSONP_8nuy17n_1"
        }
        self.ac_token = ""

    @staticmethod
    def load_js(file_name):
        with open(file_name, 'r', encoding='utf-8')as f:
            content = f.read().replace('\u1f60', '').replace('\U0001f603', '')
        ctx = execjs.compile(content)
        return ctx

    def get_js_cb(self):
        ctx = self.load_js("cb_data.js")
        return ctx.call("get_cb")

    def get_js_fp(self):
        ctx = self.load_js("get_fp.js")
        return ctx.call("_fp")

    def get_js_data(self, offset, token, xyt):
        ctx = self.load_js("cb_data.js")
        return ctx.call("get_data", xyt, token, offset)

    def get_js_param_bd(self, resp_tid, resp_dt):
        ctx = self.load_js("actoken_d_param.js")
        return ctx.call("get_bd_parm", resp_tid, resp_dt)

    def get_js_param_dd(self):
        ctx = self.load_js("actoken_d_param.js")
        return ctx.call("get_dd_parm")

    def get_js_actoken(self, resp_dt):
        ctx = self.load_js("actoken_d_param.js")
        return ctx.call("get_actoken", resp_dt)

    @staticmethod
    def get_offset(target, template):
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        # 使用二分法查找阈值的精确值
        lef = 0
        rig = 1
        for run_times in range(20):
            threshold = (rig + lef) / 2
            if threshold < 0:
                print('Error threshold')
                return 0
            loc = np.where(res >= threshold)
            if len(loc[1]) > 1:
                lef += (rig - lef) / 2
            elif len(loc[1]) == 1:
                # print(f'目标区域起点x坐标为：{loc[1][0]}')
                return int(loc[1][0])
            elif len(loc[1]) < 1:
                rig -= (rig - lef) / 2

    @staticmethod
    def get_x_list(distance):
        # 本案例识别的距离与end_x即distance = offset + 8等
        # distance = offset + 8
        t_list = [random.randint(50, 160)]
        x_list = [random.randint(5, 11)]
        y_list = list()
        # 生成x坐标轨迹, 生成t坐标轨迹
        for j in range(1, distance):
            x_list.append(x_list[j-1] + random.randint(2, 4))
            if x_list[j] > distance:
                break
        diff = x_list[-1] - distance
        for j in range(diff):
            x_list.append(x_list[-1] + random.randint(-2, -1))
            if x_list[-1] <= distance:
                x_list[-1] = distance
                break
        length = len(x_list)
        # 生成y坐标轨迹
        for i in range(1, length+1):
            if i < int(length * 0.4):
                y_list.append(0)
            elif i < int(length * 0.65):
                y_list.append(-1)
            elif i < int(length * 0.77):
                y_list.append(-2)
            elif i < int(length * 0.95):
                y_list.append(-3)
            else:
                y_list.append(-4)
            t_list.append(t_list[i-1] + random.randint(20, 80))
        # 生成t的坐标
        xyt = list(zip(x_list, y_list, t_list))
        for j in range(length):
            xyt[j] = list(xyt[j])
        return xyt

    def download_img(self, target_url, template_url):
        """下载图片"""
        path_list = []
        for path, url in [("target", target_url), ("template", template_url)]:
            res = requests.get(url, headers=self.img_headers, timeout=25)
            save_img_path = f"{path}.png"
            with open(save_img_path, 'wb') as f:
                f.write(res.content)
            _img = Image.open(save_img_path)
            print(f"{path} 的图片长宽", _img.size, url)
            path_list.append(save_img_path)
        return path_list

    def get_img(self):
        """获取滑动验证码的图片, return target_url, template_url, img_token"""
        for retry_times in range(3):
            self.get_id_params.update({
                "fp": self.fp,
                "cb": self.get_js_cb(),
                "callback": self.load_js("get_fp.js").call("_callback")
            })
            url = f"https://webzjcaptcha.reg.163.com/api/v2/get?{urlencode(self.get_id_params)}"
            resp = requests.get(url, headers=self.headers, timeout=25)
            get_id_data = re.search(r'\((.*)\);', resp.text).group(1)
            resp_json = json.loads(get_id_data)
            if resp_json['error'] == 0:
                target_url = resp_json['data']['bg'][0]
                template_url = resp_json['data']['front'][0]
                img_token = resp_json['data']['token']
                img_path = self.download_img(target_url, template_url)
                return img_path, img_token
            else:
                print("Need to change param_cb")

    def _request_db(self):
        headers = {
            'Accept': "*/*",
            "Host": "webzjac.reg.163.com",
            "Origin": "https://dl.reg.163.com",
            "Referer": "https://dl.reg.163.com/",
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
        # d请求
        url = f"https://webzjac.reg.163.com/v2/d"
        param = {
            "d": self.get_js_param_dd(),
            "v": "c0bda046",
            "cb": "_WM_"
        }
        resp = requests.post(url, headers=headers, timeout=5, data=param)
        print(resp.text)
        d_resp = json.loads(re.search(r'\((.*)\)', resp.text).group(1).replace("null", '{}')).get('result', {})
        resp_tid, resp_dt = d_resp['tid'], d_resp['dt']
        # b请求
        url = "https://webzjac.reg.163.com/v2/b"
        param.update({"d": self.get_js_param_bd(resp_tid, resp_dt)})
        resp = requests.post(url, headers=headers, timeout=5, data=param)
        print(resp.text)
        return resp_dt

    def check_img(self, img_token, data):
        """检验滑动验证码， return validate"""
        self.check_id_params.update({
            "acToken": self.ac_token,
            "token": img_token,
            "data": data,
            "cb": self.get_js_cb(),
        })
        url = f"https://webzjcaptcha.reg.163.com/api/v2/check?{urlencode(self.check_id_params)}"
        resp = requests.get(url, headers=self.headers, timeout=25)
        print(resp.text)
        resp_check = json.loads(re.search(r'\((.*)\);', resp.text).group(1))
        validate = resp_check['data']['validate']
        return validate

    def process(self):
        # 1、获取指纹fp参数
        self.fp = self.get_js_fp()
        print(f">>> fp is {self.fp}")
        # 2、bd请求
        resp_dt = self._request_db()
        # 3、获取actoken参数
        self.ac_token = self.get_js_actoken(resp_dt)
        print(f">>> ac_token is {self.ac_token}")
        # 4、获取滑动验证码的url和token(fp)
        img_path, img_token = self.get_img()
        print(f">>> img token is {img_token}")
        # 5、获取滑动验证码的offset 原网页图片缩放 300 * 150   57 *150
        im = Image.open("target.png")
        im.resize((300, 150), Image.ANTIALIAS).save("target.png")
        im = Image.open("template.png")
        im.resize((57, 150), Image.ANTIALIAS).save("template.png")
        offset = int(self.get_offset(img_path[0], img_path[1]))
        print(f"offset is {offset}")
        # self.ac_token = "9ca17ae2e6ffcda170e2e6ee87e76f918e98aabc74b5a88bb2c15a968e9fbbf441ba87abd2d660a6edfe86b22af0feaec3b92aed9daadaf56e87f19aaeee4f839a9fb7d14b9be9a09ad97f96eeb9a4f07fbc89ee9e"
        # 6、运动轨迹xyt_list
        xyt = self.get_x_list(offset + 8)
        # xyt = eval(input("请输入xyt"))
        print(f"xyt is {xyt}")
        # 7、获取data参数
        data = self.get_js_data(offset, img_token, xyt)
        print(f">>> data param is {data}")
        # 8、 (actoken, token, data, cb )
        validate = self.check_img(img_token, data)
        print(f"validate is {validate}")


if __name__ == '__main__':
    _object = YiDunecard()
    _object.process()
