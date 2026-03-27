import request from '/@/utils/request';

/**
 * PC 执行机接口
 * @method getList       获取执行机列表
 * @method getOnlineList 获取在线执行机列表（用于执行前选择）
 */
export function usePcDevicesApi() {
  return {
    getList: (data) => {
      return request({
        url: '/pc/devices/list',
        method: 'POST',
        data,
      });
    },
    getOnlineList: (data) => {
      return request({
        url: '/pc/devices/onlineList',
        method: 'POST',
        data,
      });
    },
  };
}
