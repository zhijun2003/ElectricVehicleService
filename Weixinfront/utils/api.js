// Weixinfront/utils/api.js
import { BASE_URL, API_CONFIG } from './config'

const request = (method, endpoint, data) => {
    // 添加全局loading
    wx.showLoading({ title: '加载中' })

    return new Promise((resolve, reject) => {
        wx.request({
            url: BASE_URL + API_CONFIG.endpoints[endpoint],
            method: method,
            data: data,
            success: (res) => {
                if (res.statusCode === 200) {
                    resolve(res.data)
                } else {
                    reject(res.data)
                }
            },
            fail: (err) => reject(err)
        })
    })
}

export const get = (endpoint) => request('GET', endpoint)
export const post = (endpoint, data) => request('POST', endpoint, data)