define(['zepto', 'vue', 'requirejs-vue!vue/search/user/user.vue'], function(Zepto, Vue, Test){

	new Vue({
	  el: '#app',
	  template: "<my-component/>",
	  component: { Test }
	})
});