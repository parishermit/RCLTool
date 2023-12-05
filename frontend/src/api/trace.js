import request from '@/utils/request'

export function getTrace (params) {
  return request({
    url: '/getspanlist',
    method: 'get',
    params
  })
}
