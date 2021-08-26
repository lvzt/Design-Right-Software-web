// const svgoConfig = require('./config/svgo-config.json');

const path = require('path');

function resolve (dir) {
  return path.join(__dirname, '..', dir)
}

let backendDomain = 'http://localhost:6688/';
if (process.env.VUE_APP_BACKEND_DOMAIN) {
  backendDomain = process.env.VUE_APP_BACKEND_DOMAIN;
}

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: backendDomain,
        changeOrigin: true,
      },
    },
    host: '0.0.0.0',
    port: 8090,
    https: false,
    open: false,
  },
//   css: {
//     sourceMap: true,
//     loaderOptions: {
//       scss: {
//         prependData: `@import "~@/styles/global.scss";`
//       },
//     }
//   },
  productionSourceMap: false,
  runtimeCompiler: true,
  transpileDependencies: [
    /\/node_modules\/resize-detector\//,
  ],
  chainWebpack: config => {
//     if (process.env.NODE_ENV === 'production') {
//       config.plugin('gzip-plugin')
//         .use('compression-webpack-plugin', [{
//           filename: '[path].gz[query]',
//           algorithm: 'gzip',
//           test: /\.js$|\.json$|\.css$|\.ttf$/,
//           threshold: 20480, // 只有大小大于该值的资源会被处理
//           minRatio:0.8, // 只有压缩率小于这个值的资源才会被处理
//           deleteOriginalAssets: false, // 不删除原文件
//         }])
//         .end()
//     }

    config.module.rule('md')
      .test(/\.md/)
      .use('raw-loader')
      .loader('raw-loader')
      .end();

    config.module.rule('compile')
      .test(/\.js$/)
      .include
      .add(resolve('src'))
      .end()
      .use('babel')
      .loader('babel-loader')
      .options({
        presets: [
          ['@babel/preset-env', {
            modules: false
          }]
        ]
      });
  },
};