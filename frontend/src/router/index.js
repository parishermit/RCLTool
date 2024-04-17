import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Locate from '../components/Locate.vue'
import Microservice from '../components/Microservice.vue'
import Task from '@/views/task'
import LabelRootCause from '@/views/labelrootcause'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/microservice',
      name: 'microservice',
      component: Microservice
    },
    {
      path: '/task',
      name: 'task',
      component: Task
    },
    {
      path:'/labelrootcause',
      name:'LabelRootCause',
      component:LabelRootCause
    }
  ]
})
