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
    wx.request({
      url: 'https://your-backend-url/api/charging_stations/',
      method: 'GET',
      success: (res) => {
        const markers = res.data.data.map(station => ({
          id: station.id,
          latitude: station.location.latitude,
          longitude: station.location.longitude,
          name: station.name,
          status: station.status
        }));
        this.setData({ markers });
      }
    });
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