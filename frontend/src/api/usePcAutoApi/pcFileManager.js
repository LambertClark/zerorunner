import { post, get } from '/@/utils/request';

const API = '/pc/fm/';

export function usePcFileManagerApi() {
  return {
    uploadPhoto: data => post(API + 'upload-photo', data, { 'Content-Type': 'multipart/form-data' }),
    downloadPhoto: data => get(API + 'download', data),
  };
}
