// pages/charging_records.js
Page({
  data: {
    records: []
  },
  onLoad(options) {
    if (options.id) {
      this.loadRepairRecord(options.id)
    }
  },
  loadChargingRecords() {
    wx.request({
      url: 'https://your-backend-url/api/charging_records/',
      method: 'GET',
      success: (res) => {
        this.setData({ records: res.data.data });
      }
    });
  },
  onShowRecordDetail(e) {
    const recordId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/repair_record_detail/repair_record_detail?id=${recordId}`
    })
  }
});