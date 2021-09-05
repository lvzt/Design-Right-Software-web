const routes = {
    path: '/chapter1',
    name: 'Chater1',
    component: {
      template: '<router-view></router-view>',
    },
    meta: {
      hasMulSub: true,
      hidden: false,
    //   icon: 'icon-ch1',
    },
    children: [
      {
        path: 'define',
        name: 'Define',
        component: () => import('@/views/Chapter1/Define.vue'),
        // meta: {
        //   auth: [1],
        // },
      },
      {
        path: 'define-owner',
        name: 'DefineOwner',
        component: () => import('@/views/Chapter1/DefineOwner.vue'),
        // meta: {
        //   auth: [1],
        // },
      },
    ],
  };
  
  export default routes;