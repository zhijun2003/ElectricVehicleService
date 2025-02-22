// pages/charging_records.js
import { get } from '../../utils/api'

Page({
  data: {
    list: [],
    page: 1,
    loading: false,
    hasMore: true,
    searchKey: ''
  },

  onLoad() {
    this.loadRecords();
  },

  async loadRecords() {
    if (this.data.loading || !this.data.hasMore) return;

    this.setData({ loading: true });
    wx.showLoading({ title: '加载中...' });

    try {
      const params = {
        page: this.data.page,
        page_size: 20, // 与后端分页设置一致
        keyword: this.data.searchKey.trim()
      };

      const res = await wx.$http.get('/charging/records/', { params });

      if (res.statusCode === 200) {
        this.setData({
          list: [...this.data.list, ...res.data.results],
          hasMore: res.data.next !== null,
          page: this.data.page + 1
        });
      }
    } catch (error) {
      console.error('加载失败:', error);
      wx.showToast({ title: '数据加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
      wx.hideLoading();
    }
  },

  onSearch: _.debounce(function(e) {
    this.setData({
      searchKey: e.detail.trim(),
      list: [],
      page: 1,
      hasMore: true
    });
    this.loadRecords();
  }, 500),

  loadMore() {
    if (!this.data.loading && this.data.hasMore) {
      this.loadRecords();
    }
  }
});
