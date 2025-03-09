import { get } from '../../utils/api'

// 添加腾讯地图SDK
const QQMapWX = require('../../libs/qqmap-wx-jssdk.min.js');
const qqmapsdk = new QQMapWX({
  key: 'AHIBZ-HCALI-SQQGK-UVZUH-QFLP6-6BFUO' // 腾讯位置服务
});

Page({
  data: {
    mapCtx: null,
    markers: [],
    latitude: 23.1291,
    longitude: 113.2644,
    scale: 16,
    showDetail: false,
    selectedStation: null
  },

  onLoad() {
    this.initMap();
    this.loadChargingStations();
  },

  // 初始化地图上下文
// 修改初始化逻辑
initMap() {
  // 添加权限检查
  wx.authorize({
    scope: 'scope.userLocation',
    success: () => {
      wx.getLocation({
        type: 'wgs84',
        success: res => {
          this.setData({
            latitude: res.latitude,
            longitude: res.longitude
          });
          this.loadChargingStations();
        }
      });
    },
    fail: () => {
      wx.showModal({
        title: '位置权限提示',
        content: '需要您授权位置信息以展示周边充电桩',
        confirmText: '去设置',
        success: res => {
          if (res.confirm) wx.openSetting()
        }
      })
    }
  })

  this.setData({
    mapCtx: wx.createMapContext('stationMap')
  })
}

  // 加载充电桩数据
  async loadChargingStations() {
    try {
      const res = await wx.$http.get('/charging/stations/');
      const markers = res.data.results.map(station => ({
        id: station.id,
        latitude: station.gps_lat,
        longitude: station.gps_lng,
        iconPath: '/images/marker.png',
        width: 32,
        height: 40,
        callout: {
          content: `${station.name}\n状态：${station.status}`,
          color: '#333',
          borderRadius: 8,
          padding: 8,
          display: 'ALWAYS'
        }
      }));

      this.setData({ markers });
    } catch (error) {
      wx.showToast({ title: '加载失败', icon: 'none' });
    }
  },

  // 标记点点击事件
  handleMarkerTap(e) {
    const stationId = e.markerId;
    const selected = this.data.markers.find(s => s.id === stationId);
    this.setData({ selectedStation: selected, showDetail: true });
  },

  // 路线规划
  navigateToStation() {
    const { latitude, longitude, name } = this.data.selectedStation;
    qqmapsdk.direction({
      mode: 'walking',
      from: '',
      to: `${latitude},${longitude}`,
      success: res => {
        wx.openLocation({
          latitude,
          longitude,
          name,
          scale: 18
        });
      }
    });
  }
});