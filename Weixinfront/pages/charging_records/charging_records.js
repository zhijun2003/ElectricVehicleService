// pages/charging_records.js
import { get } from '../../utils/api'

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
    get('RECORDS').then(res => {
      this.setData({ records: res.data })
    }).catch(console.error)
  },
  onShowRecordDetail(e) {
    const recordId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/repair_record_detail/repair_record_detail?id=${recordId}`
    })
  }
});