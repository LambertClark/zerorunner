import request from '/@/utils/request';

/**
 * PC 自动化测试计划接口
 * @method getList          获取计划列表
 * @method saveOrUpdate     新增或更新计划
 * @method deleted          删除计划
 * @method getPlanInfo      获取计划详情
 * @method runPlan          执行计划
 * @method getPlanReportList 获取计划报告列表
 * @method deletedPlanReport 删除计划报告
 */
export function usePcPlanApi() {
  return {
    getList: (data) => {
      return request({
        url: '/pc/plan/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate: (data) => {
      return request({
        url: '/pc/plan/saveOrUpdate',
        method: 'POST',
        data,
      });
    },
    deleted: (data) => {
      return request({
        url: '/pc/plan/deleted',
        method: 'POST',
        data,
      });
    },
    getPlanInfo: (data) => {
      return request({
        url: '/pc/plan/getInfo',
        method: 'POST',
        data,
      });
    },
    runPlan: (data) => {
      return request({
        url: '/pc/plan/runPlan',
        method: 'POST',
        data,
      });
    },
    // ---- 计划报告 ----
    getPlanReportList: (data) => {
      return request({
        url: '/pc/planReport/list',
        method: 'POST',
        data,
      });
    },
    deletedPlanReport: (data) => {
      return request({
        url: '/pc/planReport/deleted',
        method: 'POST',
        data,
      });
    },
    getPlanReportInfo: (data) => {
      return request({
        url: '/pc/planReport/getInfo',
        method: 'POST',
        data,
      });
    },
  };
}
