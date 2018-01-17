define(['zepto'], function(Zepto){
	return {
		normal: function() {
			return {
				pk__in: [currentUserPK],
			}
		},
		createGroupMessage: function() {
			// participantsPK => templates/messaging/group/create.html
			return {
				pk__in: participantsPK,
			}
		},
		existingGroupMessage: function() {
			var participantsPK = [currentUserPK];
			Zepto('.participants li').each(function(i) {
				participantsPK.push(Zepto(this).data('pk'));
			});

			return {
				pk__in: participantsPK,
			}
		},
	}
});