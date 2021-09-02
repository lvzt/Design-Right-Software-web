import Vue from 'vue';
import Router from 'vue-router';
import { constantRouterMap } from '@/config/router.config';


Vue.use(Router);

/**
 * TIPS:
 * meta: {
 *   hidden: false,    // If `hidden:true` will not appear in the navigation bar or sidebar(default is false)
 *   auth: [],         // It will control the page roles (you can set multiple roles)
 *   icon: 'home',     // Icon will appear in the navigation bar or sidebar
 *   hasMulSub: false, // It has multiple children
 * }
 */

const scrollBehavior = (to) => {
  if (to.hash) {
    return {
      selector: to.hash,
    };
  }
  return { y: 0 };
};

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  scrollBehavior,
  routes: constantRouterMap,
});