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
        path: 'define-view',
        name: 'DefineView',
        component: () => import('@/views/Chapter1/DefineView.vue'),
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