import { post } from '/@/utils/request';

const API = '/pc/picture/';

export function usePcPictureApi() {
  return {
    getTree: data => post(API + 'getTree', data),
    saveOrUpdateTree: data => post(API + 'saveOrUpdateTree', data),
    deletedTree: data => post(API + 'deletedTree', data),
    saveOrUpdatePicture: data => post(API + 'saveOrUpdatePicture', data),
    pictureByTreeId: data => post(API + 'pictureByTreeId', data),
    getList: data => post(API + 'list', data),
    deletePicture: data => post(API + 'deletePicture', data),
    pictureByName: data => post(API + 'pictureByName', data),
  };
}
