import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import generic


class SearchUser(generic.View):
    model = User

    def get(self, request, *args, **kwargs):
        data = []

        # e.g. 'Username'
        # search_input = self.request.GET.get('searched_user', '')
        # e.g. '[1, 2, 3]'
        # excluded_pks = json.loads(
        #     self.request.GET.get('excluded_pks', '[]'))
        # e.g. '['id', 'username']'
        field_names = json.loads(self.request.GET.get('field_names', '[]'))
        # e.g. {'username__icontains': 'text here'}
        filters = json.loads(self.request.GET.get('filters', '{}'))
        # e.g. {'pk': 0}
        excludes = json.loads(self.request.GET.get('excludes', '{}'))

        searched_users = self.model.objects.filter(**filters).\
            exclude(**excludes)

        for user in searched_users:
            # data.append({
            #     'id': user.id,
            #     'username': user.username
            # })
            user_data = {}
            for field_name in field_names:
                user_data[field_name] = getattr(user, field_name)
            data.append(user_data)

        return HttpResponse(json.dumps(data), content_type='application/json')
