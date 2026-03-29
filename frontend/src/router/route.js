/**
 * 建议：路由 path 路径与文件夹名称相同，找文件可浏览器地址找，方便定位文件位置
 *
 * 路由meta对象参数说明
 * meta: {
 *      title:          菜单栏及 tagsView 栏、菜单搜索名称（国际化）
 *      isLink：        是否超链接菜单，开启外链条件，`1、isLink: 链接地址不为空 2、isIframe:false`
 *      isHide：        是否隐藏此路由
 *      isKeepAlive：   是否缓存组件状态
 *      isAffix：       是否固定在 tagsView 栏上
 *      isIframe：      是否内嵌窗口，开启条件，`1、isIframe:true 2、isLink：链接地址不为空`
 *      roles：         当前路由权限标识，取角色管理。控制路由显示、隐藏。超级管理员：admin 普通角色：common
 *      icon：          菜单、tagsView 图标，阿里：加 `iconfont xxx`，fontawesome：加 `fa xxx`
 * }
 */


/**
 * 定义动态路由
 * 前端添加路由，请在顶级节点的 `children 数组` 里添加
 * @description 未开启 isRequestRoutes 为 true 时使用（前端控制路由），开启时第一个顶级 children 的路由将被替换成接口请求回来的路由数据
 * @description 各字段请查看 `/@/views/system/menu/component/addMenu.vue 下的 ruleForm`
 * @returns 返回路由菜单数据
 */
export const dynamicRoutes = [
	{
		path: '/',
		name: '/',
		component: () => import('/@/layout/index.vue'),
		redirect: '/home',
		meta: {
			isKeepAlive: true,
		},
		children: [
			{
				path: '/home',
				name: 'home',
				component: () => import('/@/views/home/index.vue'),
				meta: {
					title: '首页',
					isLink: '',
					isHide: false,
					isKeepAlive: true,
					isAffix: true,
					isIframe: false,
					roles: ['admin', 'common'],
					icon: 'iconfont icon-shouye',
				},
			},
			// ===== PC 自动化模块 =====
			{
				path: '/pcAutoTest',
				name: 'pcAutoTest',
				component: () => import('/@/layout/routerView/parent.vue'),
				redirect: '/pcAutoTest/pcCase',
				meta: {
					title: 'PC 自动化',
					isLink: '',
					isHide: false,
					isKeepAlive: true,
					isAffix: false,
					isIframe: false,
					roles: ['admin', 'common'],
					icon: 'iconfont icon-pc',
				},
				children: [
					{
						path: '/pcAutoTest/pcCase',
						name: 'pcAutoCaseList',
						component: () => import('/@/views/pcAutoTest/pcCase/pcAutoCaseList.vue'),
						meta: {
							title: 'PC 用例',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: 'iconfont icon-a-case-o1',
						},
					},
					{
						path: '/pcAutoTest/pcCase/edit',
						name: 'editPcAutoCase',
						component: () => import('/@/views/pcAutoTest/pcCase/editPcAutoCase.vue'),
						meta: {
							title: '编辑 PC 用例',
							isLink: '',
							isHide: true,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: '',
						},
					},
					{
						path: '/pcAutoTest/pcCaseTemplate',
						name: 'pcAutoCaseListTemplate',
						component: () => import('/@/views/pcAutoTest/pcCaseTemplate/pcAutoCaseListTemplate.vue'),
						meta: {
							title: 'PC 模板用例',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: 'iconfont icon-step',
						},
					},
					{
						path: '/pcAutoTest/pcCaseTemplate/edit',
						name: 'editPcAutoCaseTemplate',
						component: () => import('/@/views/pcAutoTest/pcCaseTemplate/editPcAutoCaseTemplate.vue'),
						meta: {
							title: '编辑 PC 模板用例',
							isLink: '',
							isHide: true,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: '',
						},
					},
					{
						path: '/pcAutoTest/pcReport',
						name: 'pcReportList',
						component: () => import('/@/views/pcAutoTest/pcReport/pcReportList.vue'),
						meta: {
							title: 'PC 报告',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: 'iconfont icon-baogao',
						},
					},
					{
						path: '/pcAutoTest/pcReport/detail',
						name: 'pcAutoCaseReportDetail',
						component: () => import('/@/views/pcAutoTest/pcReport/pcReportDetail.vue'),
						meta: {
							title: 'PC用例报告详情',
							isLink: '',
							isHide: true,
							isKeepAlive: false,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: '',
						},
					},
					{
						path: '/pcAutoTest/pcPlan',
						name: 'pcAutoPlanList',
						component: () => import('/@/views/pcAutoTest/pcPlan/pcAutoPlanList.vue'),
						meta: {
							title: 'PC 计划',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: 'iconfont icon-renwu',
						},
					},
					{
						path: '/pcAutoTest/pcPlan/edit',
						name: 'editPcPlan',
						component: () => import('/@/views/pcAutoTest/pcPlan/editPcPlan.vue'),
						meta: {
							title: '编辑 PC 计划',
							isLink: '',
							isHide: true,
							isKeepAlive: false,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: '',
						},
					},
					{
						path: '/pcAutoTest/pcPlan/report',
						name: 'pcPlanReportList',
						component: () => import('/@/views/pcAutoTest/pcPlan/pcPlanReportList.vue'),
						meta: {
							title: 'PC 计划报告',
							isLink: '',
							isHide: true,
							isKeepAlive: false,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: '',
						},
					},
					{
						path: '/pcAutoTest/pictureMaterialLibrary',
						name: 'pictureMaterialLibrary',
						component: () => import('/@/views/pcAutoTest/pictureMaterialLibrary/index.vue'),
						meta: {
							title: '素材库',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: 'iconfont icon-tupian',
						},
					},
					{
						path: '/pcAutoTest/pictureList',
						name: 'pcAutoPictureList',
						component: () => import('/@/views/pcAutoTest/pictureList/pcAutoPictureList.vue'),
						meta: {
							title: '素材列表',
							isLink: '',
							isHide: true, 
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: 'iconfont icon-list',
						},
					},
					{
						path: '/pcAutoTest/pcDevice',
						name: 'pcDeviceList',
						component: () => import('/@/views/pcAutoTest/pcDevice/deviceList.vue'),
						meta: {
							title: 'PC 执行机',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin', 'common'],
							icon: 'iconfont icon-jisuanji',
						},
					},
				],
			},
			// ===== 系统设置 =====
			{
				path: '/system',
				name: 'system',
				component: () => import('/@/layout/routerView/parent.vue'),
				redirect: '/system/menu',
				meta: {
					title: '系统设置',
					isLink: '',
					isHide: false,
					isKeepAlive: true,
					isAffix: false,
					isIframe: false,
					roles: ['admin'],
					icon: 'iconfont icon-xitongshezhi',
				},
				children: [
					{
						path: '/system/menu',
						name: 'systemMenu',
						component: () => import('/@/views/system/menu/index.vue'),
						meta: {
							title: '菜单管理',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin'],
							icon: 'iconfont icon-caidan',
						},
					},
					{
						path: '/system/role',
						name: 'systemRole',
						component: () => import('/@/views/system/role/index.vue'),
						meta: {
							title: '角色管理',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin'],
							icon: 'ele-ColdDrink',
						},
					},
					{
						path: '/system/user',
						name: 'systemUser',
						component: () => import('/@/views/system/user/index.vue'),
						meta: {
							title: '用户管理',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin'],
							icon: 'iconfont icon-icon-',
						},
					},
					{
						path: '/system/dept',
						name: 'systemDept',
						component: () => import('/@/views/system/dept/index.vue'),
						meta: {
							title: '部门管理',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin'],
							icon: 'ele-OfficeBuilding',
						},
					},
					{
						path: '/system/dic',
						name: 'systemDic',
						component: () => import('/@/views/system/dic/index.vue'),
						meta: {
							title: '字典管理',
							isLink: '',
							isHide: false,
							isKeepAlive: true,
							isAffix: false,
							isIframe: false,
							roles: ['admin'],
							icon: 'ele-SetUp',
						},
					},
				],
			},
		],
	},
];

/**
 * 定义404、401界面
 * @link 参考：https://next.router.vuejs.org/zh/guide/essentials/history-mode.html#netlify
 */
export const notFoundAndNoPower = [
	{
		path: '/:path(.*)*',
		name: 'notFound',
		component: () => import('/@/views/error/404.vue'),
		meta: {
			title: '找不到此页面',
			isHide: true,
		},
	},
	{
		path: '/401',
		name: 'noPower',
		component: () => import('/@/views/error/401.vue'),
		meta: {
			title: '没有权限',
			isHide: true,
		},
	},
];

/**
 * 定义静态路由（默认路由）
 * 此路由不要动，前端添加路由的话，请在 `dynamicRoutes 数组` 中添加
 * @description 前端控制直接改 dynamicRoutes 中的路由，后端控制不需要修改，请求接口路由数据时，会覆盖 dynamicRoutes 第一个顶级 children 的内容（全屏，不包含 layout 中的路由出口）
 * @returns 返回路由菜单数据
 */
export const staticRoutes = [
	{
		path: '/login',
		name: 'login',
		component: () => import('/@/views/login/index.vue'),
		meta: {
			title: '登录',
		},
	},
];
