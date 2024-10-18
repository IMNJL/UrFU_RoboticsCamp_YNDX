/*
小R科技 XiaoRGEEK 蓝牙模式控制机器人驱动代码
请注意：本代码受中华人民共和国著作权法保护，如未经允许用于商业目的，小R科技（深圳市小二极客科技有限公司）将发起侵权诉讼！
官网Home:www.xiao-r.com
*/

var bleno = require('../..');
var XiaoRService = require('./xiaor-service');

var primaryService = new XiaoRService();

bleno.on('stateChange', function(state) {
  console.log('on -> stateChange: ' + state);

  if (state === 'poweredOn') {
    bleno.startAdvertising('XiaoRGEEK', [primaryService.uuid]);
  } else {
    bleno.stopAdvertising();
  }
});

bleno.on('advertisingStart', function(error) {
  console.log('on -> advertisingStart: ' + (error ? 'error ' + error : 'success'));

  if (!error) {
    bleno.setServices([primaryService], function(error){
      console.log('setServices: '  + (error ? 'error ' + error : 'success'));
    });
  }
});
