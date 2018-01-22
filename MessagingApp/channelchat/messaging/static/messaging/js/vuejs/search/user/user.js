define(['vue', 'vuerouter', 'requirevue!vue/search/user/user.vue'], function(Vue, VueRouter, Test){
	Vue.use(VueRouter)

	const User = {
	  template: `<div>User {{ $route.params.userId }}</div>`,
	  beforeRouteUpdate: function(to, from, next) {
	  	console.log('beforeRouteUpdate', to.params.userId);
	    next();
	  }
	}

	const Sample = {
		template: `<div> REDIRECTED </div>`
	}

	const NotFoundComponent = {
		template: `<div> Not found! </div>`
	}

	const router = new VueRouter({
	  mode: 'history',
	  routes: [
	    {
	      path: '/user/:userId',
	      name: 'user',
	      component: User
	    },
	    {path: '/sample/mehn', redirect: '/testing'},
	    {path: '/testing', component: Sample},
	    {path: '*', component: NotFoundComponent }
	  ]
	})

	const app = new Vue({ router,
		el: '#app',
		template: `
	  	<div>
	      <router-link :to="{ name: 'user', params:{ userId: 'foo' }}"">/user/foo</router-link>
	      <router-link to="/user/bar">/user/bar</router-link>
	      <router-link to="/sample/mehn">/sample/mehn</router-link>
	      <router-link to="/testing">/testing</router-link>
	      <router-view></router-view>
	      {{ message }}
	    </div>
	    `,
	    data: {
	    	message: 'Hello Vue'
	    }
	})
});