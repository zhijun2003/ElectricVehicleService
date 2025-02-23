// pages/index/index.js
const app = getApp()

Page({
  data: {
    menuItems: [
      {
        id: 'menu_001',
        icon: 'map',
        title: '充电地图',
        color: 'linear-gradient(135deg, #6B8DD6, #8E37D7)',
        url: '/pages/map/map'
      },
      {
        id: 'menu_002',
        icon: 'records',
        title: '充电记录',
        color: 'linear-gradient(135deg, #00C6FB, #005BEA)',
        url: '/pages/charging_records/charging_records'
      },
      {
        id: 'menu_003',
        icon: 'repair',
        title: '维修申报',
        color: 'linear-gradient(135deg, #FF8008, #FFC837)',
        url: ' /pages/repair/repair'
      },
      {
        id: 'menu_004',
        icon: 'user',
        title: '个人中心',
        color: 'linear-gradient(135deg, #38EF7D, #11998E)',
        url: '/pages/user/user'
      },

    ],
    stats: {
      availableStations: 0,
      avgWaitTime: 0
    },
    userStatus: {
      charging: false,
      reservation: null
    },
    recordsCount: 0,
    defaultColor: '#F5F5F5',
    imageError: {
      status: false,
      menu: false
    }
  },

  onShow() {
    this.getRealTimeStats()
    this.checkChargingStatus()
    this.getRecordsCount()
  },

  getRealTimeStats() {
    wx.request({
      url: app.globalData.apiBase + 'statistics/',
      success: res => {
        this.setData({
          stats: {
            availableStations: res.data?.availableStations || 0,
            avgWaitTime: res.data?.avgWaitTime || 0
          }
        })
      },
      fail: () => {
        this.setData({
          stats: { availableStations: 0, avgWaitTime: 0 }
        })
      }
    })
  },

  checkChargingStatus() {
    wx.request({
      url: app.globalData.apiBase + 'charging/status/',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: res => {
        const data = res.data || {}
        this.setData({
          userStatus: {
            charging: data.charging || false,
            station: data.station || '未知站点',
            remain: data.remain ?? 0,
            ...data
          }
        })
      },
      fail: () => {
        this.setData({
          userStatus: { charging: false, reservation: null }
        })
      }
    })
  },

  getRecordsCount() {
    wx.request({
      url: app.globalData.apiBase + 'charging_records/unread/',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: res => {
        const count = Math.min(Number(res.data?.count || 0), 99)
        this.setData({ recordsCount: count })
      },
      fail: () => {
        this.setData({ recordsCount: 0 })
      }
    })
  },

  navigateTo(e) {
    const url = e.currentTarget.dataset.url
    if (url) {
      wx.navigateTo({ url })
    }
  }
})
