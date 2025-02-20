Page({
  data: {
    record: {}
  },
  onLoad(options) {
    this.loadRepairRecord(options.id);
  },
  loadRepairRecord(record_id) {
    wx.request({
      url: `https://your-backend-url/api/repair_records/${record_id}/`,
      method: 'GET',
      success: (res) => {
        this.setData({ record: res.data.data });
      }
    });
  },
  updateRecordStatus() {
    wx.request({
      url: `https://your-backend-url/api/repair_records/${this.data.record.id}/`,
      method: 'PUT',
      data: {
        status: 'completed'
      },
      success: (res) => {
        wx.showToast({
          title: 'Record updated successfully',
          icon: 'success'
        });
        this.loadRepairRecord(this.data.record.id);
      }
    });
  }
});