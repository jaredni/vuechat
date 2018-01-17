define(['zepto'], function(Zepto){
    var conversationDiv = Zepto('.js-conversationDiv');
    var firstMessagePK = conversationDiv.find('p').first().data('pk');
    
    (function poll() {
        var conversation_pk = conversationDiv.data('pk');
        var getMessageURL = conversationDiv.data('getmessageurl');
        var last_message_pk = conversationDiv.find('p').last().data('pk');
        var data = {
            conversation: conversation_pk,
            latestMessage: last_message_pk,
        };

        Zepto.get(getMessageURL, data, function(response){
            for(var i=0; i<response.length; i++) {
                appendMessage(response[i]);
            }
        });
        setTimeout(poll, 5000);
    })();

    Zepto(document).ready(function () {
        Zepto('#chatarea').on('submit', function(e) {
            e.preventDefault();
            Zepto.ajax({
                url : Zepto(this).attr('action'),
                type: "POST",
                data: Zepto(this).serialize(),
                success: function (response) {
                    appendMessage(response);
                },
            });
            Zepto(this)[0].reset();
        });

        if(conversationDiv.data('messagescount') > 5) {
            var href = Zepto('<a href="">Load Previous Messages</a>');
            href.addClass('loadPreviousMessages');
            Zepto('.js-loadPreviousMessagesDiv').append(href);
        }

        Zepto('.loadPreviousMessages').on('click', function(e) {
            e.preventDefault();
            var conversation_pk = conversationDiv.data('pk');
            var loadPreviousMessagesURL = Zepto('.js-loadPreviousMessagesDiv').data('loadpreviousmessages')
            var firstMessagePK = conversationDiv.find('p').first().data('pk');
            
            var data = {
                conversation: conversation_pk,
                firstMessagePK: firstMessagePK,
            };
            Zepto.get(loadPreviousMessagesURL, data, function(response){
                for(var i=0; i<response.length; i++) {
                    var p = Zepto('<p>').text(response[i].text);
                    p.data('pk', response[i].id);
                    p.prepend("<b>" + response[i].sender + "</b>: ");
                    p.append(" (" + response[i].date + ")");
                    conversationDiv.prepend(p);
                }
                if(conversationDiv.find('p').length == conversationDiv.data('messagescount')) {
                    Zepto('.js-loadPreviousMessagesDiv .loadPreviousMessages').remove();
                }
                
            });
        });
    });

    function appendMessage(response) {
        var p = Zepto('<p>').text(response.text);
        p.data('pk', response.id);
        p.prepend("<b>" + response.sender + "</b>: ");
        p.append(" (" + response.date + ")");
        conversationDiv.append(p);
    } 
});
