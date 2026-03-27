import request from '/@/utils/request';

/**
 * PC 文件管理接口（素材文件上传/下载）
 * @method upload    上传素材文件
 * @method getUrl    获取素材访问 URL
 */
export function usePcFileManagerApi() {
  return {
    upload: (data) => {
      return request({
        url: '/pc/fm/upload',
        method: 'POST',
        headers: { 'Content-Type': 'multipart/form-data' },
        data,
      });
    },
    getUrl: (data) => {
      return request({
        url: '/pc/fm/getUrl',
        method: 'POST',
        data,
      });
    },
  };
}
