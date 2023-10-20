from django.core import paginator
from django.core.paginator import InvalidPage, Page, Paginator
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'size'
    def get_next_link(self):
        try:
            if not self.page.has_next():
                return ""
            url = self.request.build_absolute_uri()
            page_number = self.page.next_page_number()
            return replace_query_param(url, self.page_query_param, page_number)
        except:
            return ""

    def get_previous_link(self):
        try:
            if not self.page.has_previous():
                return ""
            url = self.request.build_absolute_uri()
            page_number = self.page.previous_page_number()
            if page_number == 1:
                return remove_query_param(url, self.page_query_param)
            return replace_query_param(url, self.page_query_param, page_number)
        except:
            return ""

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            # raise NotFound(msg)
            self.page = Page(list(),page_number, paginator)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)
    def get_paginated_response(self, data):

        try:
            return Response({
                
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                ,
                'total_count': self.page.paginator.count,
                'results': data
            })
        except:
            return Response({
                
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                ,
                'total_count':self.page.paginator.count,
                'results': data
            })