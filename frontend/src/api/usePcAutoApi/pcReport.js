import request from '/@/utils/request';

/**
 * PC 自动化报告接口
 * @method getList       获取报告列表
 * @method deleted       删除报告
 * @method getReportInfo 获取报告详情
 */
export function usePcReportApi() {
  return {
    getList: (data) => {
      return request({
        url: '/pc/report/list',
        method: 'POST',
        data,
      });
    },
    deleted: (data) => {
      return request({
        url: '/pc/report/deleted',
        method: 'POST',
        data,
      });
    },
    getReportInfo: (data) => {
      return request({
        url: '/pc/report/getInfo',
        method: 'POST',
        data,
      });
    },
  };
}
