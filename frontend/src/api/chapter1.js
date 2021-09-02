import { request as axios } from '@/utils/request';

const urlPrefix = '/api/chapter1';

const Chapter1Urls = {
  // label
  define: '/define',
};

Object.keys(Chapter1Urls).map((url) => {
    Chapter1Urls[url] = urlPrefix + Chapter1Urls[url];
  return url;
});

// === define ===
export function Define() {
  const url = `${Chapter1Urls.define}`;
  return axios({
    url,
    method: 'get',
  });
}

export function addOrEditDefine(data) {
  const url = `${Chapter1Urls}${0}`;
  return axios({
    url,
    method: 'put',
    data,
  });
}

// === define owner ===