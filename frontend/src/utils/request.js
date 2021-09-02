import Vue from 'vue';
import axios from 'axios';
import merge from 'lodash/merge';

// Vue.prototype.$http = axios;
const app = Vue.createApp(App);
app.config.globalProperties.$http = axios;

const request = app.config.globalProperties.$http.create({
  // baseURL: '/api', // api base_url
  timeout: 6000, // 请求超时时间
});

const resolve = (response) => {
  const { data } = response;
  if (data instanceof Array) {
    return data;
  }
  if (data instanceof Object) {
    // if (data.errno === undefined && Object.keys(data).length !== 0) {
    if (Object.keys(data).length !== 0) {
      return data;
    }
    // if (data.errno !== 0) {
    //   return Promise.reject(data);
    // }
    return data.data;
  }
  return Promise.reject(data);
};

const err = (error) => {
  if (error.response) {
    const { data } = error.response;
    if (error.response.status === 403) {
      app.config.globalProperties.$message.error(data.message);
    }
  }
  return Promise.reject(error);
};

/* eslint-disable no-param-reassign */
// request.interceptors.request.use((request) => {
//   const token = localStorage.getItem('token');
//   if (token) {
//     request.headers.Authorization = `Token ${token}`;
//   }
//   return request;
// }, err);

// response interceptor
request.interceptors.response.use(resolve, err);


/**
 * 请求地址处理
 * @param {*} actionName action方法名称
 */
request.adornUrl = actionName => actionName;

/**
 * get请求参数处理
 * @param {*} params 参数对象
 * @param {*} openDefaultParams 是否开启默认参数?
 */
request.adornParams = (params = {}, openDefaultParams = true) => {
  const defaults = {
    t: new Date().getTime(),
  };
  return openDefaultParams ? merge(defaults, params) : params;
};

/**
 * post请求数据处理
 * @param {*} data 数据对象
 * @param {*} openDefaultData 是否开启默认数据?
 * @param {*} contentType 数据格式
 *  json: 'application/json; charset=utf-8'
 *  form: 'application/x-www-form-urlencoded; charset=utf-8'
 */
request.adornData = (data = {}) => data;

app.config.globalProperties.$request = request;
/* eslint-disable */
export { request };
