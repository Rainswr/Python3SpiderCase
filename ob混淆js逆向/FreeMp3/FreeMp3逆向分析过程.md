[Toc]

#### 一、obsfuscator混淆特点

- 1、通过[混淆工具Obfuscator](https://obfuscator.io/)混淆过的代码即obsfuscator混淆（简称ob混淆），点击`Obsfucate`即可混淆如下代码
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200927082128390.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)

- 2、特点：代码变量形式大篇幅的已`_0x`为前缀进行命名，通过`死代码`和`花指令`增加代码可读难度；通常死代码在程序中完全不会调用，而花指令可能将一个变量经过一系列操作又变回原形的值，其过程毫无意义

```javascript
var _0x2f9b = ['Hello\x20World!']; (function(_0x3af67b, _0x2f9b76) {
    var _0x471fa6 = function(_0x578853) {
        while (--_0x578853) {
            _0x3af67b['push'](_0x3af67b['shift']());
        }
    };
    _0x471fa6(++_0x2f9b76);
} (_0x2f9b, 0xb2));
var _0x471f = function(_0x3af67b, _0x2f9b76) {
    _0x3af67b = _0x3af67b - 0x0;
    var _0x471fa6 = _0x2f9b[_0x3af67b];
    return _0x471fa6;
};
function hi() {
    var _0x2b0421 = _0x471f;
    console['log'](_0x2b0421('0x0'));
}
hi();
```

#### 二、如何分析逆向obsfuscator混淆

- 1、第一种（不推荐）：正向找传参入口，通过首次传入的参数正向分析它被改变或者被赋值给哪些变量，一步步看函数逻辑，还原代码，耗时间，最终结果可能还是错误的；
- 2、第二种（推荐）：逆向分析，留头留尾，找到传入的参数的入口，找到返回的参数，然后通过返回的参数一步步倒推分析这个返回的参数是如何生成的，然后缺啥补啥；
- 3、第三种（推荐）：如果第二种无法解决的话，终极武器，通过分析AST抽象语法树的结构，还原整个代码处理逻辑

#### 三、逆向ob混淆实战

##### 1、目标结果

- [获取音乐列表数据](http://tool.liumingye.cn/music/?page=audioPage&type=migu&name=%E5%91%A8%E6%9D%B0%E4%BC%A6)
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928072054947.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)

##### 2、查找哪个请求有目标数据

- 观察请求响应，发现search这个请求结果里正好是我们的目标结果数据，而它的请求参数data是加密的，所以接下来是研究data是如何生成的
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/2020092807264466.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)

##### 3、查找加密参数生成位置

- 首先`全局搜与data`，通过全局搜索(ctr + F)data、var data、data:、data=这一系列，可以发现都不是我们所要的data参数
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928073334960.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 然后，`尝试调用栈寻找`，打开该请求调用栈，发现有个ajax请求，我们点击f、ajax、send这三个蓝色的VM，发现在f这个VM里面有我们要的data字段
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928073850938.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- `打断点、刷新页面`：f的VM点进去后，左下角{}格式化后如下图，成功找到data参数的生成位置，在这里打个断点，刷新页面，会发现成功的断在了data参数的位置，接下来是分析data生成的具体流程，点击右上角第三个向下箭头进入函数内部查看生成逻辑
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/2020092807440846.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)

##### 4、分析data参数生成逻辑

- 调试发现，encode这个方法就是生成data的关键方法，传入参数是这么一个格式`"text=周杰伦&page=1&type=migu"` 
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928074814637.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 我们将function encode这个方法全部复制下来，存到一个==ZJL.js文件==（先将该`VM所有js代码`复制下来保存为==音乐2.js==文件，搜索该函数encode并折叠复制）
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928075427911.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 在ZJL.js里面最后一行添加`console.log(encode("text=周杰伦&page=1&type=migu"))`，并运行该ZJL.js文件，发现缺少参数`_0x5e84`
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928075705109.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 查找参数_0x5e84生成位置，在音乐2.js文件里搜索`var _0x5e84 `即为该参数生成位置，折叠发现83行到175行为_0x5e84为参数生成的所有
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928080242857.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 看_0x5e84内部生成逻辑，回到谷歌调试界面，逐步调试，_0x5e84这个我进行了代码简化处理，简单的还原的该参数生成代码如下(ps：这一部分_0x5e84参数生成可以好好研究一下，细节不做介绍，省略~)
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928080757637.png#pic_center)
- 在ZJL.js文件里补上这个_0x5e84参数的生成代码，继续运行，发现少location参数，回到谷歌页面调试
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928080922630.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 在谷歌VM页面搜索`location[_0x5e84(`，打上断点，调试跳到该断点处，在console界面输出location，嗯~有结果，然后copy(location)，复制到ZJL.js文件
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928081438516.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928081815903.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 保存再运行，发现少MD5参数(ReferenceError: md5 is not defined)，`npm install crypto-js` ,从crypto-js文件里导入md5
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928082149675.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 保存再运行，发现有可能会报如下错误`_0x514ed7[_0x5e84(...)] is not a function`，这个原因是 _0x5e84['EIMrEA'] 这个对象里面参数不全的原因，到谷歌里面调试
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/2020092808230348.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 在encode方法return这里打个断点，调试跳到这里，console界面输出_0x5e84['EIMrEA']这个结果，并复制到ZJL.js文件里替换_0x5e84['EIMrEA']，`这个_0x5e84['EIMrEA']的key很多，尽可能的运行到函数返回结果的时候，在复制这个参数，否则还会报错_0x514ed7[_0x5e84(...)] is not a function`![在这里插入图片描述](https://img-blog.csdnimg.cn/202009280826232.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)
- 如果保存文件后运行还有类似_0x514ed7[_0x5e84(...)] is not a function报错，在console界面输出_0x514ed7[_0x5e84(...)]这个结果，然后将js文件里对应的替换掉就行
  ![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928083302873.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)

- 运行，结果输出，加密完成。将md5这里在稍微改下，添加个.toString()，这样data参数前4位就会随时间戳md5值改变了，但是不加也没啥影响，data的前4个字符随意生成4个字符都没啥问题

```javascript
 var _0x271eea = _0x514ed7[_0x5e84('139', '!rZ)')](md5, new Date()[_0x5e84('13a', '*OHJ')]().toString())
```


![在这里插入图片描述](https://img-blog.csdnimg.cn/20200928204130857.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzQxMTU4NQ==,size_16,color_FFFFFF,t_70#pic_center)

##### 5、python请求验证结果

- 用上面的data参数python请求看下结果，运行正常没问题

```python
import requests
url = "https://app.onenine.cc/m/api/search"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "http://tool.liumingye.cn"
}
data = {
    "data": "7c02QNBLytVZbtF9mFfgD1dlXCFcC_oAP4r3MDsbkvy-zP-yky9cO3wePMzVl9KMZpX9IrZwPNfDFXzu",
    "v": 2
}
resp = requests.post(url, data=data, headers=headers)
print(resp.text)
```
