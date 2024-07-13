from collections import OrderedDict

from django.db.models import Count, Max, Q
from rest_framework.response import Response

from apps.news.models import Reaction
from generic.paginations import BasePagination


class ReactionPagination(BasePagination):
    page_size = 10
    max_page_size = None

    def get_paginated_response(self, data):
        reactions = self.page.paginator.object_list.aggregate(
            likes=Count('id', filter=Q(type=Reaction.Type.LIKE)),
            dislikes=Count('id', filter=Q(type=Reaction.Type.DISLIKE)),
            my_reaction_type=Max('type', filter=Q(author=self.request.user)),
        )

        return Response(
            OrderedDict([
                ('count', self.page.paginator.count),
                ('likes', reactions['likes']),
                ('dislikes', reactions['dislikes']),
                ('my_reaction_type', reactions['my_reaction_type']),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data),
            ]),
        )
