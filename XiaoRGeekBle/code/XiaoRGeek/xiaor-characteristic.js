var util = require('util');
var os = require('os');
var exec = require('child_process').exec;

var bleno = require('../..');

var Descriptor = bleno.Descriptor;
var Characteristic = bleno.Characteristic;

var net = require('net');

var _updateValueCallback;
//创建TCP客户端
var client = new net.Socket();
//client.setEncoding('utf8');
client.connect(2002,'localhost',function () {
    console.log('已连接到服务器');
});


const Bytes2HexString = (b)=> {
  let hexs = "";
  for (let i = 0; i < b.length; i++) {
    let hex = (b[i]).toString(16);
    if (hex.length === 1) {
      hex = '0' + hex;
    }
    hexs += hex.toUpperCase();
  }
  return hexs;
}

client.on('data', function(data) {
   let str = "";
   str = Bytes2HexString(data)
   //console.log(str)
   if (_updateValueCallback) {
      console.log('EchoCharacteristic read request: ' + str);
      _updateValueCallback(data);
   }
});

client.on('end', function() { 
   console.log('断开与服务器的连接');
});

client.on('error',(e)=>{
   console.log(e.message);
})

var XiaoRCharacteristic = function() {
  XiaoRCharacteristic.super_.call(this, {
     uuid: '0000ffe1-0000-1000-8000-00805f9b34fb',
    properties: ['write', 'writeWithoutResponse', 'read', 'notify']
  });
};

util.inherits(XiaoRCharacteristic, Characteristic);

XiaoRCharacteristic.prototype.onWriteRequest = function(data, offset, withoutResponse, callback) {
  console.log('WriteOnlyCharacteristic write request: ' + data.toString('hex') + ' ' + offset + ' ' + withoutResponse);
  client.write(data);
  callback(this.RESULT_SUCCESS);
};

XiaoRCharacteristic.prototype.onSubscribe = function(maxValueSize, updateValueCallback) {
  console.log('EchoCharacteristic - onSubscribe');
  _updateValueCallback = updateValueCallback;
};

XiaoRCharacteristic.prototype.onUnsubscribe = function() {
  console.log('EchoCharacteristic - onUnsubscribe');
  _updateValueCallback = null;
};

module.exports = XiaoRCharacteristic;
