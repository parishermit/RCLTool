import request from '@/utils/request'

export function getTrace (params) {
  return request({
    url: '/getspanlist',
    method: 'get',
    params
  })
}

export function getNodesAndEdges (params) {
  return request({
    url: '/getNodesAndEdges',
    method: 'get',
    params
  })
}

export function getTraceList (params) {
  return request({
    url: '/gettracelist',
    method: 'get',
    params
  })
}

export function abnormalLabelRequest (params) {
  return request({
    url: '/getRootCause',
    method: 'get',
    params
  })
}

export function uploadData (formData) {
  return request({
    url: '/getdata',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data' // 设置 Content-Type
    }
  })
}

export function downloadTrace (params) {
  return request({
    url: '/outputtracecsv',
    method: 'get',
    responseType: 'blob',
    params
  })
}

export function downloadGroundtruth (params) {
  return request({
    url: '/outputrclcsv',
    method: 'get',
    responseType: 'blob',
    params
  })
}

export function testGetRes (params) {
  return request({
    url: '/get_res',
    method: 'get',
    params
  })
}

export function saveTask (params) {
  return request({
    url: '/save_task',
    method: 'get',
    params
  })
}

export function getTask (params) {
  return request({
    url: '/get_task',
    method: 'get',
    params
  })
}

export function getTree (params) {
  return request({
    url: '/get_tree',
    method: 'get',
    params
  })
}