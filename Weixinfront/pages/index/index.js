// pages/index/index.js
const app = getApp()

Page({
  data: {
    menuItems: [
      {icon: 'map', title: '充电地图', color: 'linear-gradient(135deg, #6B8DD6, #8E37D7)', url: '/pages/map/map'},
      {icon: 'clock', title: '充电记录', color: 'linear-gradient(135deg, #00C6FB, #005BEA)', url: '/pages/charging_records/charging_records'},
      {icon: 'repair', title: '维修申报', color: 'linear-gradient(135deg, #FF8008, #FFC837)', url: '/pages/repair_record_detail/repair_record_detail'},
      {icon: 'user', title: '个人中心', color: 'linear-gradient(135deg, #38EF7D, #11998E)', url: '/pages/user/user'}
    ],
    stats: {
      availableStations: 0,
      avgWaitTime: 0
    },
    userStatus: {
      charging: false,
      reservation: null
    },
    recordsCount: 0
  },

  onShow() {
    this.getRealTimeStats()
    this.checkChargingStatus()
    this.getRecordsCount()
  },

  // 获取实时数据
  getRealTimeStats() {
    wx.request({
      url: app.globalData.apiBase + 'statistics/',
      success: res => {
        this.setData({ stats: res.data })
      }
    })
  },

  // 检查充电状态
  checkChargingStatus() {
    wx.request({
      url: app.globalData.apiBase + 'charging/status/',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: res => {
        this.setData({ userStatus: res.data })
      }
    })
  },

  // 获取未读记录数
  getRecordsCount() {
    wx.request({
      url: app.globalData.apiBase + 'charging_records/unread/',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: res => {
        this.setData({ recordsCount: res.data.count })
      }
    })
  },

  // 统一导航方法
  navigateTo(e) {
    const url = e.currentTarget.dataset.url
    wx.navigateTo({ url })
  }
})