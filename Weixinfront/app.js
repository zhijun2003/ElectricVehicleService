// app.js
App({
  globalData: {
    appid: 'wx650d15724076f822',
    baseUrl: 'http://localhost:8000',  // 开发时使用本地后端
    userInfo: null,
    apiBase: 'https://localhost:8000/api/',//后端接口地址
    location: null
  },
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
  },
  
  
  // 获取全局位置信息
  updateLocation() {
    wx.getLocation({
      type: 'wgs84',
      success: res => {
        this.globalData.location = {
          latitude: res.latitude,
          longitude: res.longitude
        }
      }
    })
  }
})
