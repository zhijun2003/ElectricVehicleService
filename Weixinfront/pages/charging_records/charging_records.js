Page({
  data: {
    records: []
  },
  onLoad() {
    this.loadChargingRecords();
  },
  loadChargingRecords() {
    wx.request({
      url: 'https://your-backend-url/api/charging_records/',
      method: 'GET',
      success: (res) => {
        this.setData({ records: res.data.data });
      }
    });
  }
});