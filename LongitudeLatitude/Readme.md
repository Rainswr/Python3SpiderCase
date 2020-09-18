## 某房网地图找房市区街道经纬度爬取
#### 一、使用介绍
- 主要是获取这个[链接](https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?cityId=320500&dataSource=ESF&condition=&id=&groupType=bizcircle&maxLatitude=31.32969678645508&minLatitude=31.281503603699104&maxLongitude=120.57172824105535&minLongitude=120.48908413413739)里的数据，而这个链接的难点在于请求参数是js生成的，需逐步调试js
- 调用LJLatLng.py即可，依赖LJLatLng.js文件，即可获取区、街道的经纬度
- LJLatLng.js文件用于生成maxLatitude、minLatitude、maxLongitude、minLongitude四个请求参数；
