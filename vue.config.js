// All configuration item explanations can be find in https://cli.vuejs.org/config/
module.exports = {
  /**
     * You will need to set publicPath if you plan to deploy your site under a sub path,
     * for example GitHub Pages. If you plan to deploy your site to https://foo.github.io/bar/,
     * then publicPath should be set to "/bar/".
     * In most cases please use '/' !!!
     * Detail: https://cli.vuejs.org/config/#publicpath
     */
  // publicPath: '/',
  // outputDir: 'dist',
  // assetsDir: 'static',
  // lintOnSave: process.env.NODE_ENV === 'development',
  // productionSourceMap: false,
  devServer: {
    port: 8080,
    proxy: {
      '/register_dev': {
        target: 'http://127.0.0.1:3000',
        // ws:true,
        changeOrigin: true
      },
      '/login_dev': {
        target: 'http://127.0.0.1:3000',
        // ws:true,
        changeOrigin: true
      },
      '/users': {
        target: 'http://127.0.0.1:3000',
        // ws:true,
        changeOrigin: true
      },
      '/index_1/posts': {
        target: 'http://127.0.0.1:3000',
        // ws:true,
        changeOrigin: true
      },
      '/robotapi/': {
        target: 'http://127.0.0.1:3000',
        // ws:true,
        changeOrigin: true
      }
      // '/upload/':{
      //   target: 'http://127.0.0.1:3000',
      //   changeOrigin: true
      // }
      // '/foo':{
      //   target:'<other_url'
      // }
    }
  }
}
