define(['zepto', 'mustache'], function(Zepto, Mustache){
	var person = {
	    firstName: "Christophe",
	    lastName: "Coenraets",
	    blogURL: "http://coenraets.org"
	};
	var template = "<h1>{{firstName}} {{lastName}}</h1>Blog: {{blogURL}}";
	var html = Mustache.to_html(template, person);
	Zepto('#sampleArea').html(html);
});