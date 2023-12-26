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

export function uploadData (params) {
  return request({
    url: '/getdata',
    method: 'post',
    params
  })
}

export function downloadTrace (params) {
  return request({
    url: '/outputtracecsv',
    method: 'get',
    params
  })
}

export function downloadGroundtruth (params) {
  return request({
    url: '/outputrclcsv',
    method: 'get',
    params
  })
}
