## 某房网地图找房市区街道经纬度爬取
#### 一、使用介绍
- 主要是获取这个链接里的数据：https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist ，而这个链接的难点在于请求参数是js生成的，需逐步调试js
- 调用LJLatLng.py即可，依赖LJLatLng.js文件，即可获取区、街道的经纬度
- LJLatLng.js文件用于生成maxLatitude、minLatitude、maxLongitude、minLongitude四个请求参数；
