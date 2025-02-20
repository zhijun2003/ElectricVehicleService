// pages/user/user.js
Page({
  data: {
    username: '',
    password: '',
    email: '',
    message: '',
    isLoggedIn: false
  },

  onLoad() {
    this.checkLoginStatus();
  },

  checkLoginStatus() {
    const app = getApp();
    wx.request({
      url: app.globalData.apiBase + 'user/check_login',
      method: 'GET',
      header: {
        'Authorization': 'Bearer ' + wx.getStorageSync('token')
      },
      success: (res) => {
        if (res.data.status === 'success') {
          this.setData({
            isLoggedIn: true,
            username: res.data.username
          });
        }
      }
    });
  },

  handleRegister() {
    const { username, password, email } = this.data;
    const app = getApp();
    wx.request({
      url: app.globalData.apiBase + 'user/register',
      method: 'POST',
      data: { username, password, email },
      success: (res) => {
        this.setData({ message: res.data.message });
        if (res.data.status === 'success') {
          this.setData({ username: '', password: '', email: '' });
        }
      }
    });
  },

  handleLogin() {
    const { username, password } = this.data;
    const app = getApp();
    wx.request({
      url: app.globalData.apiBase + 'user/login',
      method: 'POST',
      data: { username, password },
      success: (res) => {
        if (res.data.status === 'success') {
          wx.setStorageSync('token', res.data.token);
          this.setData({ 
            isLoggedIn: true,
            username: username,
            password: '',
            message: '登录成功'
          });
        } else {
          this.setData({ message: res.data.message });
        }
      }
    });
  },

  handleLogout() {
    const app = getApp();
    wx.request({
      url: app.globalData.apiBase + 'user/logout',
      method: 'POST',
      header: {
        'Authorization': 'Bearer ' + wx.getStorageSync('token')
      },
      success: () => {
        wx.removeStorageSync('token');
        this.setData({ 
          isLoggedIn: false,
          username: '',
          message: '已退出登录'
        });
      }
    });
  }
});