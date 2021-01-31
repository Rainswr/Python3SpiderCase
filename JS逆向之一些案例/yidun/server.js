//文件
var fpJs = require('./get_fp.js')
var acTokenJs = require('./actoken_d_param.js')
var dataJs = require('./cb_data.js')
// express应用
var express = require('D:\\Software\\node\\node_modules\\express');
var app = express();
var bodyParser = require('D:\\Software\\node\\node_modules\\body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

// cb参数请求： http://127.0.0.1:8082/get_cb
app.get("/get_cb",function(req,res){
   res.send(dataJs.Get_cb());
});

// data参数请求： http://127.0.0.1:8082/get_data?xyt=&token=&offset=
// http://127.0.0.1:8082/get_data?xyt=[[7, 2, 109], [8, 2, 122], [9, 2, 142], [11, 2, 159], [15, 2, 176], [17, 2, 193], [20, 2, 210], [22, 2, 225], [25, 2, 241], [26, 2, 257], [27, 2, 276], [28, 2, 292], [30, 2, 304], [31, 2, 323], [32, 2, 343], [34, 2, 361], [36, 1, 374], [38, -1, 391], [40, -1, 409], [44, -1, 424]]&token=f8b0ab29f37742dc82a5c949a03e8cb3&offset=203.px
app.get("/get_data",function(req,res){
    res.send(dataJs.Get_data(eval(req.query.xyt), req.query.token, req.query.offset));
});

// acToken参数请求： http://127.0.0.1:8082/get_actoken?d=KVIKmNbjLGpAUUFVERdqOD3OfTKIHrD+
app.get("/get_actoken",function(req,res){
   res.send(acTokenJs.Get_acToken(req.query.d));
});

// fp参数请求： http://127.0.0.1:8082/get_fp
 app.get("/get_fp",function(req,res){
   res.send(fpJs.Get_fp());
});

// 获取d参数请求： http://127.0.0.1:8082/get_dd
app.get("/get_dd",function(req,res){
   res.send(acTokenJs.Get_dd());
});

// 获取d参数请求： http://127.0.0.1:8082/get_bd?e=Ghi97IPeOoRERFUAVBc/PbdrZp0F01bd&g=AUx5Ub/I7x1AUEBFVEYvPKN/N41ExgbM
app.get("/get_bd",function(req,res){
   res.send(acTokenJs.Get_bd(req.query.e, req.query.g));
});

//监听8082端口
const server = app.listen(8082);
