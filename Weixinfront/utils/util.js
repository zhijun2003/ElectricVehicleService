const formatTime = date => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return `${[year, month, day].map(formatNumber).join('/')} ${[hour, minute, second].map(formatNumber).join(':')}`
}

const formatNumber = n => {
  n = n.toString()
  return n[1] ? n : `0${n}`
}

module.exports = {
  formatTime
}

const request = (url, method, data) => {
  const app = getApp()
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.apiBase + url,
      method,
      data,
      header: {
        'Authorization': `Bearer ${wx.getStorageSync('token')}`
      },
      success: res => res.statusCode === 200 ? resolve(res.data) : reject(res),
      fail: reject
    })
  })
}

module.exports = {
  formatTime,
  request // 暴露请求方法
}