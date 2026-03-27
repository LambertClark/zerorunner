import request from '/@/utils/request';

/**
 * PC 自动化测试用例接口
 * @method getList 获取 PC 用例列表
 * @method saveOrUpdate 新增或更新 PC 用例
 * @method deleted 删除 PC 用例
 * @method getPcCaseInfo 获取 PC 用例详情
 * @method runCases 执行 PC 用例
 * @method getPcTemplateList 获取 PC 模板用例列表
 * @method saveOrUpdateTemplate 新增或更新 PC 模板用例
 * @method deletedTemplate 删除 PC 模板用例
 * @method getPcTemplateInfo 获取 PC 模板用例详情
 */
export function usePcTestCaseApi() {
  return {
    // ---- 普通用例 ----
    getList: (data) => {
      return request({
        url: '/pc/testcase/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate: (data) => {
      return request({
        url: '/pc/testcase/saveOrUpdate',
        method: 'POST',
        data,
      });
    },
    deleted: (data) => {
      return request({
        url: '/pc/testcase/deleted',
        method: 'POST',
        data,
      });
    },
    getPcCaseInfo: (data) => {
      return request({
        url: '/pc/testcase/getInfo',
        method: 'POST',
        data,
      });
    },
    runCases: (data) => {
      return request({
        url: '/pc/testcase/runCases',
        method: 'POST',
        data,
      });
    },

    // ---- 模板用例 ----
    getPcTemplateList: (data) => {
      return request({
        url: '/pc/testcase/template/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdateTemplate: (data) => {
      return request({
        url: '/pc/testcase/template/saveOrUpdate',
        method: 'POST',
        data,
      });
    },
    deletedTemplate: (data) => {
      return request({
        url: '/pc/testcase/template/deleted',
        method: 'POST',
        data,
      });
    },
    getPcTemplateInfo: (data) => {
      return request({
        url: '/pc/testcase/template/getInfo',
        method: 'POST',
        data,
      });
    },
  };
}
