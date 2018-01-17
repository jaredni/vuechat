define(['zepto'], function(Zepto){
	return {
		normal: function(id, username, resultContainer) {
			var li = Zepto('<li>').text(" " + username);
            var href = Zepto('<a>').attr("href", "private/message/" + id);

            href.text("Send Message");
            li.prepend(href);
            // print result
        	resultContainer.append(li);
		},
		createGroupMessage: function(id, username, resultContainer) {
			// participantsPK => templates/messaging/group/create.html

			var li = Zepto('<li>').text(" " + username);
            var input= Zepto('<input type="button" value="Add User" data-username="'+username+'" data-pk="'+id+'">');

            li.addClass(username);

            Zepto(input).on('click', function(e) {
            	var addUser = Zepto(this);

            	participantsPK.push(addUser.data('pk'));
            	Zepto('.participant_pks').val(JSON.stringify(participantsPK));
        
            	var li = Zepto('<li>').text(addUser.data('username'));
                var removeInput= Zepto('<input type="button" value="Remove User" data-username="'+addUser.data('username')+'" data-pk="'+addUser.data('pk')+'">');

                li.addClass(addUser.data('username'));
                li.prepend(removeInput);

                Zepto(removeInput).on('click', function(e) {
                	var removeUser = Zepto(this);
                	var i = participantsPK.indexOf(removeUser.data('pk'));

                	if(i != -1) {
						participantsPK.splice(i, 1);
					}
					Zepto('.participant_pks').val(JSON.stringify(participantsPK));

					Zepto('.js-participantsUl .' + addUser.data('username')).remove();
                });

                Zepto('.js-participantsUl').append(li);
            	Zepto('.js-searchUserUl .' + addUser.data('username')).remove();
            });
            li.prepend(input);
            // print result
        	resultContainer.append(li);
		},
		existingGroupMessage: function(id, username, resultContainer) {
			// csrftoken => templates/messaging/group/send.html

			var li = Zepto('<li>').text(" " + username);
            li.addClass(username);
            var addUserUrl = resultContainer.data('addurl').replace('/0/', '/'+id+'/');

            var input= Zepto('<input type="button" value="Add User" data-url="'+addUserUrl+'"/>');

            Zepto(input).on('click', function(e) {
                Zepto.ajax({
                    url : Zepto(this).data('url'),
                    type: "POST",
                    data: {'csrfmiddlewaretoken': csrftoken},
                    success: function (response) {
                        var li = Zepto('<li>').text(response.username);
                        li.addClass(response.username);
                        li.data('pk', response.id);
                        var removeUrl = Zepto('.participants').data('removeurl');

                        var removeUserUrl = removeUrl.replace('/0/', '/'+response.id+'/');
                        var removeInput=Zepto('<input class="js-removeUserButton" data-getconversationurl="'+removeUserUrl+'" value="Remove" type="submit"/>');

                        Zepto(removeInput).on('click', function(e) {
                            e.preventDefault();
                            conversationUrl = Zepto(this).data('getconversationurl');
                            Zepto.ajax({
                                url : conversationUrl,
                                type: "POST",
                                data: {'csrfmiddlewaretoken': csrftoken},
                                success: function (response) {
                                    Zepto('.participants .' + response).remove();
                                },
                            });
                        });

                        li.prepend(removeInput);
                        Zepto('.participants').append(li);
                        Zepto('.js-searchUserUl .' + response.username).remove();
                    },
                });
            });

            li.prepend(input);
            // print result
            resultContainer.append(li);
		},
	}
});
