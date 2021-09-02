import chapter1 from "@/router/modules/chapter1";

export const constantRouterMap = [
  // {
  //   path: '/login',
  //   name: 'Login',
  //   component: Login,
  //   meta: {
  //     hidden: true,
  //   },
  // },
  {
    path: '/403',
    meta: {
      hidden: true,
    },
    // redirect: { name: 'Index' },
    // component: Login,
  },
  {
    path: '/404',
    meta: {
      hidden: true,
    },
    component: () => import('@/views/error-pages/App404.vue'),
  },
  {
    path: '/401',
    meta: {
      hidden: true,
    },
    component: () => import('@/views/error-pages/App401.vue'),
  },
  special,
];

export const asyncRouterMap = [
  {
    path: '/',
    name: 'Home',
    component: ElLayout,
    redirect: '/home',
    meta: {
      hidden: false,
      hasMulSub: false,
    },
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        // meta: { icon: 'icon-dashboard' },
      },
      chapter1,
    ],
  },
  {
    path: '*',
    redirect: '/404',
    meta: {
      hidden: true,
    },
  },
];
