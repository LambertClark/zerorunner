// 直接从 request.js 引入 post
import { post } from '/@/utils/request';

const API = '/pc/devices/';

export function usePcDevicesApi() {
  return {
    getPcDevices: (data) => post(API + 'getPcDevices', data),
  };
}
