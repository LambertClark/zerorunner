import { post } from '/@/utils/request';

const API = '/pc/plan/';
const REPORT_API = '/pc/planReport/';

export function usePcPlanApi() {
  return {
    getPcPlanList: data => post(API + 'list', data),
    copyPcPlan: data => post(API + 'copyPcPlan', data),
    saveOrUpdate: data => post(API + 'saveOrUpdate', data),
    deletePcPlan: data => post(API + 'deletePcPlan', data),
    getPcPlanInfo: data => post(API + 'getPcPlanInfo', data),
    getPcPlanDetail: data => post(API + 'getPcPlanDetail', data),
    runPlanCases: data => post(API + 'runPlanCases', data),
  };
}

export function usePcPlanReportApi() {
  return {
    getPcPlanReportList: data => post(REPORT_API + 'list', data),
    saveOrUpdateReport: data => post(REPORT_API + 'saveOrUpdate', data),
    deletePcPlanReport: data => post(REPORT_API + 'deletePcPlanReport', data),
    getPcPlanReportDetail: data => post(REPORT_API + 'getPcPlanReportDetail', data),
    getPcPlanReportStatistics: data => post(REPORT_API + 'getPcPlanReportStatistics', data),
    savePcPlanReportStepDetail: data => post(REPORT_API + 'savePcPlanReportStepDetail', data),
    getPcPlanReportInfo: data => post(REPORT_API + 'getPcPlanReportInfo', data),
  };
}
