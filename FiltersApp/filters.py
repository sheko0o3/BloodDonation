import django_filters

from database import models

class SearchDonatorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="user__username", lookup_expr="iexact")
    class Meta:
        model = models.UserInformation
        fields = ['bloodType', 'govern', "name"]