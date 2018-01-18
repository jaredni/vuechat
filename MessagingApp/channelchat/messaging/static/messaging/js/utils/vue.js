define(['zepto', 'vue', 'requirejs-vue!vue/test.vue'], function(Zepto, Vue, Test){

	new Vue({
	  el: '#app',
	  template: "<my-component/>",
	  component: { Test }
	})
});