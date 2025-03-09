// pages/repair_record/repair_record.js
import { get } from '../../utils/api'
import { formatTime } from '../../utils/util'

Page({
  data: {
    list: [],
    page: 1,
    pageSize: 15,
    loading: false,
    hasMore: true,
    searchKey: '',
    filterStatus: 'all',
    statusOptions: [
      { text: '全部', value: 'all' },
      { text: '待处理', value: 'pending' },
      { text: '处理中', value: 'processing' },
      { text: '已完成', value: 'completed' }
    ],
    refreshing: false
  },

  onLoad() {
    this.loadRecords(true)
  },

  // 加载记录
  async loadRecords(init = false) {
    if (this.data.loading || !this.data.hasMore) return

    this.setData({ loading: true })

    try {
      const params = {
        page: init ? 1 : this.data.page,
        page_size: this.data.pageSize,
        search: this.data.searchKey,
        status: this.data.filterStatus === 'all' ? undefined : this.data.filterStatus
      }

      const res = await get('REPAIRS', params)

      this.setData({
        list: init ? res.data.results : [...this.data.list, ...res.data.results],
        hasMore: res.data.next !== null,
        page: init ? 2 : this.data.page + 1,
        refreshing: false
      })
    } catch (error) {
      wx.showToast({ title: '加载失败', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },

  // 状态筛选
  onStatusChange(e) {
    this.setData({
      filterStatus: e.detail.value,
      list: [],
      page: 1,
      hasMore: true
    }, () => this.loadRecords(true))
  },

  // 搜索
  onSearch(e) {
    this.setData({
      searchKey: e.detail,
      list: [],
      page: 1,
      hasMore: true
    }, () => this.loadRecords(true))
  },

  // 下拉刷新
  onRefresh() {
    if (this.data.refreshing) return
    this.setData({ refreshing: true })
    this.loadRecords(true)
  },

  // 加载更多
  loadMore() {
    this.loadRecords()
  },

  // 状态颜色映射
  getStatusColor(status) {
    const map = {
      pending: 'danger',
      processing: 'warning',
      completed: 'success'
    }
    return map[status] || ''
  },

  // 取消申报
  async cancelRecord(e) {
    const id = e.currentTarget.dataset.id
    try {
      await wx.$http.put(`/repairs/${id}/`, { status: 'canceled' })
      wx.showToast({ title: '已取消申报' })
      this.loadRecords(true)
    } catch (error) {
      wx.showToast({ title: '操作失败', icon: 'none' })
    }
  },

  // 预览图片
  previewImage(e) {
    wx.previewImage({
      current: e.currentTarget.dataset.src,
      urls: [e.currentTarget.dataset.src]
    })
  },

  // 跳转新建页
  navigateToCreate() {
    wx.navigateTo({ url: '/pages/repair_record_create/repair_record_create' })
  },

  // 时间格式化
  formatTime
})

// 增加防抖处理
let searchTimer = null

onSearch(e) {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    this.setData({
      searchKey: e.detail,
      list: [],
      page: 1,
      hasMore: true
    }, () => this.loadRecords(true))
  }, 500)
}

// 滚动加载优化
loadMore() {
  if (!this.data.hasMore || this.data.loading) return
  this.setData({
    page: this.data.page + 1
  }, () => this.loadRecords())
}