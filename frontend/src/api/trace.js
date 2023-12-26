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

export function gettracelist (params) {
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
