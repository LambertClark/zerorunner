import request from '/@/utils/request';

/**
 * PC 图片素材接口
 * @method getTreeList       获取素材树列表
 * @method saveOrUpdateTree  新增或更新树节点
 * @method deletedTree       删除树节点
 * @method getPictureList    获取素材列表
 * @method saveOrUpdate      新增或更新素材
 * @method deleted           删除素材
 * @method getPictureInfo    获取素材详情
 * @method searchPicture     搜索素材（步骤编辑器中使用）
 */
export function usePcPictureApi() {
  return {
    // ---- 素材树 ----
    getTreeList: (data) => {
      return request({
        url: '/pc/picture/tree/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdateTree: (data) => {
      return request({
        url: '/pc/picture/tree/saveOrUpdate',
        method: 'POST',
        data,
      });
    },
    deletedTree: (data) => {
      return request({
        url: '/pc/picture/tree/deleted',
        method: 'POST',
        data,
      });
    },

    // ---- 素材 ----
    getPictureList: (data) => {
      return request({
        url: '/pc/picture/list',
        method: 'POST',
        data,
      });
    },
    saveOrUpdate: (data) => {
      return request({
        url: '/pc/picture/saveOrUpdate',
        method: 'POST',
        data,
      });
    },
    deleted: (data) => {
      return request({
        url: '/pc/picture/deleted',
        method: 'POST',
        data,
      });
    },
    getPictureInfo: (data) => {
      return request({
        url: '/pc/picture/getInfo',
        method: 'POST',
        data,
      });
    },
    searchPicture: (data) => {
      return request({
        url: '/pc/picture/search',
        method: 'POST',
        data,
      });
    },
  };
}
