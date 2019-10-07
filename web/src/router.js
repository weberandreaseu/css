import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/tracker',
      name: 'tracker',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "tracker" */ './views/Tracker.vue')
    },
    {
      path: '/radio',
      name: 'radio',
      component: () => import(/* webpackChunkName: "radio" */'./views/Radio.vue')
    }
  ]
})
