import { get } from '../../utils/api'

Page({
  data: {
    markers: [],
    latitude: 0,
    longitude: 0,
    stations: [] // 添加缺失的stations数据定义
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

  async loadChargingStations() {
    try {
      const res = await wx.$http.get('/charging/stations/', {
        params: {
          status: 'available' // 可选过滤条件
        }
      });

      this.setData({
        stations: res.data.results
      });

    } catch (error) {
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },  // 这里添加缺失的逗号

  navigateToStation(e) {
    const station = e.currentTarget.dataset.station;
    wx.openLocation({
      latitude: station.latitude,
      longitude: station.longitude,
      name: station.name,
      address: station.location // 根据模型字段修正为location
    });
  }
});