// pages/user/user.js
// user-center.js
Page({
  data: {
    isLogin: false,
    userInfo: {}
  },

  onShow() {
    this.checkLoginStatus();
  },

  // 检查登录状态
  async checkLoginStatus() {
    const token = wx.getStorageSync('token');
    if (token) {
      try {
        const res = await wx.$http.get('/user/info');
        this.setData({
          isLogin: true,
          userInfo: res.data
        });
      } catch (err) {
        wx.removeStorageSync('token');
      }
    }
  },

  // 微信登录
  async handleWechatLogin() {
    const { code } = await wx.login();
    const res = await wx.$http.post('/auth/wechat-login', { code });

    wx.setStorageSync('token', res.data.token);
    this.checkLoginStatus();
  },

  // 退出登录
  handleLogout() {
    wx.removeStorageSync('token');
    this.setData({ isLogin: false });
  }
});
