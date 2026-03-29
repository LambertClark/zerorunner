import { post } from '/@/utils/request';

const API = '/pc/report/';

export function usePcReportApi() {
  return {
    getList: data => post(API + 'list', data),
    deleted: data => post(API + 'deleted', data),
    saveOrUpdate: data => post(API + 'saveOrUpdate', data),
    getReportDetail: data => post(API + 'getPcReportDetail', data),
    getReportStatistics: data => post(API + 'getPcReportStatistics', data),
  };
}
