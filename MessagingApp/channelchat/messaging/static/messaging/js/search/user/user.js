define(['zepto', 'search/user/utils/append', 'search/user/utils/exclude', 'mustache'], function(Zepto, Append, Exclude, Mustache){
	var searchUserInput = Zepto('.js-searchUserInput');
	var searchedUserUl = Zepto('.js-searchUserUl');
    var isPressed = false;

    searchUserInput.keyup(function(event) {
        if(isPressed) {
            var url = searchUserInput.data('url');

            var field_names = ['id', 'username'];
            var excludes = Exclude[searchUserInput.data('append')]();

            var filters = {
                username__icontains: searchUserInput.val()
            };
            
            var data = {
                field_names: JSON.stringify(field_names),
                excludes: JSON.stringify(excludes), 
                filters: JSON.stringify(filters)
            };
            searchedUserUl.empty();

            Zepto.get(url, data, function(response){
                for(var i=0; i<response.length; i++) {
                    Append[searchUserInput.data('append')](
                        response[i].id,
                        response[i].username,
                        searchedUserUl
                    );
                }
            });
        }
        isPressed = false;
    }).keydown(function(event) {
        isPressed = true;
    });
});