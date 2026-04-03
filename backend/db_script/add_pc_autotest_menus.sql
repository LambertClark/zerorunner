-- PC 自动化菜单数据初始化
-- 执行前请确认 menu 表当前最大 id，若已有冲突请调整 id 值
-- 列顺序: id, parent_id, path, name, component, title, isLink, linkUrl, isHide, icon, isKeepAlive, isAffix, isIframe, roles, sort, active_menu, menu_type, redirect, creation_date, updation_date, enabled_flag, views, created_by, updated_by, lookup_id, trace_id

-- 幂等保护：先删除可能已存在的同 path 记录，避免重复插入
DELETE FROM `menu` WHERE `path` IN (
    '/pcAutoTest',
    '/pcAutoTest/pcCase',
    '/pcAutoTest/pcCase/edit',
    '/pcAutoTest/pcCaseTemplate',
    '/pcAutoTest/pcCaseTemplate/edit',
    '/pcAutoTest/pcReport',
    '/pcAutoTest/pcReport/detail',
    '/pcAutoTest/pcPlan',
    '/pcAutoTest/pcPlan/edit',
    '/pcAutoTest/pcPlan/report',
    '/pcAutoTest/pictureMaterialLibrary',
    '/pcAutoTest/pictureList',
    '/pcAutoTest/pcDevice'
);

-- 78: PC 自动化（父菜单，显示在侧边栏）
INSERT INTO `menu` VALUES (78, 0, '/pcAutoTest', 'pcAutoTest', 'layout/routerView/parent', 'PC 自动化', 0, NULL, 0, 'iconfont icon-pc', 1, 0, 0, '', 7, NULL, 10, '/pcAutoTest/pcCase', NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 79: PC 用例列表（显示）
INSERT INTO `menu` VALUES (79, 78, '/pcAutoTest/pcCase', 'pcAutoCaseList', 'pcAutoTest/pcCase/pcAutoCaseList.vue', 'PC 用例', 0, NULL, 0, 'iconfont icon-a-case-o1', 1, 0, 0, '', 1, NULL, 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 80: 编辑 PC 用例（隐藏）
INSERT INTO `menu` VALUES (80, 79, '/pcAutoTest/pcCase/edit', 'editPcAutoCase', 'pcAutoTest/pcCase/editPcAutoCase.vue', '编辑 PC 用例', 0, NULL, 1, '', 1, 0, 0, '', 0, '/pcAutoTest/pcCase', 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 81: PC 模板用例（显示）
INSERT INTO `menu` VALUES (81, 78, '/pcAutoTest/pcCaseTemplate', 'pcAutoCaseListTemplate', 'pcAutoTest/pcCaseTemplate/pcAutoCaseListTemplate.vue', 'PC 模板用例', 0, NULL, 0, 'iconfont icon-step', 1, 0, 0, '', 2, NULL, 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 82: 编辑 PC 模板用例（隐藏）
INSERT INTO `menu` VALUES (82, 81, '/pcAutoTest/pcCaseTemplate/edit', 'editPcAutoCaseTemplate', 'pcAutoTest/pcCaseTemplate/editPcAutoCaseTemplate.vue', '编辑 PC 模板用例', 0, NULL, 1, '', 1, 0, 0, '', 0, '/pcAutoTest/pcCaseTemplate', 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 83: PC 报告列表（显示）
INSERT INTO `menu` VALUES (83, 78, '/pcAutoTest/pcReport', 'pcReportList', 'pcAutoTest/pcReport/pcReportList.vue', 'PC 报告', 0, NULL, 0, 'iconfont icon-baogao', 1, 0, 0, '', 3, NULL, 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 84: PC 用例报告详情（隐藏）
INSERT INTO `menu` VALUES (84, 83, '/pcAutoTest/pcReport/detail', 'pcAutoCaseReportDetail', 'pcAutoTest/pcReport/pcReportDetail.vue', 'PC 报告详情', 0, NULL, 1, '', 0, 0, 0, '', 0, '/pcAutoTest/pcReport', 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 85: PC 计划列表（显示）
INSERT INTO `menu` VALUES (85, 78, '/pcAutoTest/pcPlan', 'pcAutoPlanList', 'pcAutoTest/pcPlan/pcAutoPlanList.vue', 'PC 计划', 0, NULL, 0, 'iconfont icon-renwu', 1, 0, 0, '', 4, NULL, 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 86: 编辑 PC 计划（隐藏）
INSERT INTO `menu` VALUES (86, 85, '/pcAutoTest/pcPlan/edit', 'editPcPlan', 'pcAutoTest/pcPlan/editPcPlan.vue', '编辑 PC 计划', 0, NULL, 1, '', 0, 0, 0, '', 0, '/pcAutoTest/pcPlan', 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 87: PC 计划报告（隐藏）
INSERT INTO `menu` VALUES (87, 85, '/pcAutoTest/pcPlan/report', 'pcPlanReportList', 'pcAutoTest/pcPlan/pcPlanReportList.vue', 'PC 计划报告', 0, NULL, 1, '', 0, 0, 0, '', 0, '/pcAutoTest/pcPlan', 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 88: 素材库（显示）
INSERT INTO `menu` VALUES (88, 78, '/pcAutoTest/pictureMaterialLibrary', 'pictureMaterialLibrary', 'pcAutoTest/pictureMaterialLibrary/index.vue', '素材库', 0, NULL, 0, 'iconfont icon-tupian', 1, 0, 0, '', 5, NULL, 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 89: 素材列表（隐藏，从素材库跳转）
INSERT INTO `menu` VALUES (89, 88, '/pcAutoTest/pictureList', 'pcAutoPictureList', 'pcAutoTest/pictureList/pcAutoPictureList.vue', '素材列表', 0, NULL, 1, '', 1, 0, 0, '', 0, '/pcAutoTest/pictureMaterialLibrary', 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);

-- 90: PC 执行机（显示）
INSERT INTO `menu` VALUES (90, 78, '/pcAutoTest/pcDevice', 'pcDeviceList', 'pcAutoTest/pcDevice/deviceList.vue', 'PC 执行机', 0, NULL, 0, 'iconfont icon-jisuanji', 1, 0, 0, '', 6, NULL, 10, NULL, NOW(), NOW(), 1, 0, 7, 7, NULL, NULL);
