Page({
  data: {
    isLogin: false,
    userInfo: {},
    loading: true
  },

  onShow() {
    this.checkLoginStatus();
    this.loadUserStats();
  },

  // 新增用户数据统计
  async loadUserStats() {
    if (!this.data.isLogin) return;

    try {
      const [basicRes, statsRes] = await Promise.all([
        wx.$http.get('/user/info'),
        wx.$http.get('/user/stats')
      ]);

      this.setData({
        userInfo: {
          ...basicRes.data,
          ...statsRes.data
        },
        loading: false
      });
    } catch (err) {
      wx.showToast({ title: '数据加载失败', icon: 'none' });
    }
  },

  // 优化登录逻辑
  async handleWechatLogin() {
    wx.showLoading({ title: '登录中', mask: true });

    try {
      const { code } = await wx.login();
      const res = await wx.$http.post('/auth/wechat-login', { code });

      wx.setStorageSync('token', res.data.token);
      await this.checkLoginStatus();
      wx.showToast({ title: '登录成功' });
    } catch (err) {
      wx.showToast({ title: '登录失败', icon: 'none' });
    } finally {
      wx.hideLoading();
    }
  },

  // 新增跳转处理
  navigateTo(e) {
    const url = e.currentTarget.dataset.url;
    wx.vibrateShort();
    wx.navigateTo({ url });
  }
});
