//copyright文件
var fpJs = require('./get_fp.js')
// express应用
var express = require('D:\\Software\\node\\node_modules\\express');
var app = express();
var bodyParser = require('D:\\Software\\node\\node_modules\\body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

 // fp参数请求： http://127.0.0.1:8082/get_fp
 app.get("/get_fp",function(req,res){
   res.send(fpJs.Get_fp());
});


//监听8082端口
const server = app.listen(8082);
