import { post } from '/@/utils/request';

const API = '/pc/testcase/';

export function usePcTestCaseApi() {
  return {
    getPcCaseList: data => post(API + 'getPcCaseList', data),
    getPcCaseTemplateList: data => post(API + 'getPcCaseTemplateList', data),
    copyPcCase: data => post(API + 'copyPcCase', data),
    deleteCase: data => post(API + 'deletePcCase', data),
    getCasesModules: data => post(API + 'getPcCasesModuleTree', data),
    runPcCases: data => post(API + 'runCases', data),
    saveOrUpdate: data => post(API + 'saveOrUpdate', data),
    getCaseInfo: data => post(API + 'getCaseInfo', data),
  };
}
