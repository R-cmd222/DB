module.exports = {
  devServer: {
    port: 9528,
    proxy: {
      '/api': {
        target: 'http://localhost:9527',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  }
} 