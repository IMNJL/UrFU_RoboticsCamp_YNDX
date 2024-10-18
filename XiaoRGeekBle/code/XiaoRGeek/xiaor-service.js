var util = require('util');

var bleno = require('../..');

var BlenoPrimaryService = bleno.PrimaryService;

var XiaoRCharacteristic = require('./xiaor-characteristic');

function XiaoRService() {
  XiaoRService.super_.call(this, {
      uuid: '0000ffe0-0000-1000-8000-00805f9b34fb',
      characteristics: [
          new XiaoRCharacteristic()
      ]
  });
}

util.inherits(XiaoRService, BlenoPrimaryService);

module.exports = XiaoRService;
