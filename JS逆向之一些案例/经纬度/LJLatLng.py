import requests
import execjs
from urllib.parse import urlencode
import copy
import re


class LianJiaLatLng:
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            "Host": "map.ke.com",
            "Origin": "https://map.lianjia.com",
            "plat": "LJ",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        }
        self.item = None
        self.param = {
            "cityId": "",
            "dataSource": "ESF",
            "condition": "",
            "id": "",
            "groupType": "district",
            "maxLatitude": "",
            "minLatitude": "",
            "maxLongitude": "",
            "minLongitude": ""
        }

    @staticmethod
    def get_js_params(longitude, latitude, num):
        c = {"lng": longitude, "lat": latitude, "Se": "inner"}
        path = "./LJLatLng.js"
        with open(path, 'r', encoding='utf8') as f:
            js_text = f.read()
            obj = execjs.compile(js_text).call('req', c, num)
            return obj

    def get_street_lng_lat(self, districtid, cityid):
        """街道请求参数get"""
        url = f"https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/center?" \
            f"cityId={cityid}&dataSource=ESF&condition=&groupId={districtid}" \
            f"&groupType=district&lngWidth=0.16528821383594305&" \
            f"latHeight=0.11564716295402366"
        resp = requests.get(url, headers=self.headers, timeout=25)
        print(resp.text)
        return resp.json()["data"]["lng"], resp.json()["data"]["lat"]

    def get_city_lng_lat(self, cityid):
        """
        获取city的中心经纬度
        :param cityid: city的邮政码
        :return: city的经纬度
        """
        url = f"https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/initdata?cityId={cityid}&dataSource=ESF"
        resp = requests.get(url, headers=self.headers, timeout=25)
        # 获取city的经纬度
        lat, lng = resp.json()['data']['latitude'], resp.json()['data']['longitude']
        lat_lng = {"city_longitude": lng, "city_latitude": lat}
        return lat_lng

    def get_longitude_latitude(self, record, param, name="district"):
        """获取经纬度"""
        url = f"https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?{urlencode(param)}"
        resp = requests.get(url, headers=self.headers, timeout=25)
        if not resp.json()['data'].get('bubbleList', []):
            record.update({
                name: "",
                f"{name}_code": "",
                f"{name}_longitude": "",
                f"{name}_latitude": "",
                f"{name}_border": "",
            })
            yield record
        else:
            for row in resp.json()['data']['bubbleList']:
                record.update({
                    name: row['name'],
                    f"{name}_code": row['id'],
                    f"{name}_longitude": row['longitude'],
                    f"{name}_latitude": row['latitude'],
                    f"{name}_border": row['border'],
                    "fullSpell": row['fullSpell']
                })
                yield record

    def main(self):
        city_code = 320500
        city_lat_lng = self.get_city_lng_lat(city_code)
        city_lat_lng['city_code'] = 320500
        city_lat_lng['city'] = "江苏省——苏州"
        obj = self.get_js_params(city_lat_lng['city_longitude'], city_lat_lng['city_latitude'], 12)
        self.param.update(obj)
        self.param.update({"groupType": "district", "cityId": city_code})
        for yield_record in self.get_longitude_latitude(city_lat_lng, self.param):
            if 'fullSpell' in yield_record:
                del yield_record['fullSpell']
            print(">>>> district_longitude_latitude:", yield_record)
            # 获取街道经纬度
            param = copy.deepcopy(self.param)
            lng, lat = self.get_street_lng_lat(yield_record['district_code'], yield_record['city_code'])
            obj = self.get_js_params(lng, lat, 14)
            param.update(obj)
            param.update({"groupType": "bizcircle"})
            for yield_ds in self.get_longitude_latitude(yield_record, param, "street"):
                if 'fullSpell' in yield_ds:
                    district_code = re.search(r"d(\d+)b", yield_ds['fullSpell']).group(1)
                    if district_code != str(yield_ds['district_code']):
                        continue
                    del yield_ds['fullSpell']
                print("street_longitude_latitude:", yield_ds)


if __name__ == '__main__':
    _object = LianJiaLatLng()
    _object.main()

