import { get } from '../../utils/api'

Page({
  data: {
    markers: [],
    latitude: 0,
    longitude: 0
  },
  onLoad() {
    wx.getLocation({
      type: 'wgs84',
      success: (res) => {
        this.setData({
          latitude: res.latitude,
          longitude: res.longitude
        });
        this.loadChargingStations();
      }
    });
  },
  loadChargingStations() {
    get('STATIONS').then(res => {
      const markers = res.data.map(/* 转换逻辑 */)
      this.setData({ markers })
    }).catch(console.error)
  },
  navigateToStation(e) {
    const station = e.currentTarget.dataset.station;
    wx.openLocation({
      latitude: station.latitude,
      longitude: station.longitude,
      name: station.name,
      address: station.address
    });
  }
});