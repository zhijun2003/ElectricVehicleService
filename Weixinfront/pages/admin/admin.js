// pages/admin/admin.js
const ADMIN_MENU = [
  {
    id: 'user_mgr',
    name: '用户管理',
    icon: 'user',
    permissions: ['view_user', 'edit_user']
  },
  {
    id: 'station_mgr',
    name: '充电桩管理',
    icon: 'charging',
    permissions: ['view_station', 'edit_station']
  }
]

Page({
  data: {
    adminMenu: [],
    hasPermission: false
  },

  onLoad() {
    this.checkAdminRole()
  },

  checkAdminRole() {
    wx.request({
      url: app.globalData.apiBase + 'auth/check_admin/',
      header: { 'Authorization': 'Bearer ' + app.globalData.token },
      success: res => {
        this.setData({
          hasPermission: res.data.is_admin,
          adminMenu: this.filterMenu(ADMIN_MENU, res.data.permissions)
        })
      }
    })
  },

  filterMenu(menu, permissions) {
    return menu.filter(item =>
      item.permissions.every(p => permissions.includes(p))
    )
  }
})
