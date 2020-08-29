# 一、Python二值化降噪图片
### 1、使用介绍
- 直接运行该文件即可CaseRunGather.py
- Pretreatment_MainColorRgb.py ：适用于字符颜色与噪点颜色有明显区别的情况
- Pretreatment_TurnGrayField.py ：9领域法去除周围噪点
# 二、Python使用KNN训练模型并识别验证码
- 首先得准备好已标记好的验证码图片，并存在相应的文件夹下（注： 图片验证码最好是去噪二值化后的验证码图片，且每张图片命名已: 真实名称_random123等命名)
- 然后传入相应参数运行该文件即可KnnIdentifyVerification.py
