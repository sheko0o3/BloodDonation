import django_filters

from database import models

class SearchDonatorFilter(django_filters.FilterSet):
    bloodtype = django_filters.CharFilter(field_name="bloodType__bloodtype", lookup_expr="icontains")
    govern = django_filters.CharFilter(field_name="govern__name", lookup_expr="iexact")
    state = django_filters.CharFilter(field_name="state__name", lookup_expr="iexact")
    class Meta:
        model = models.UserInformation
        fields = ['bloodtype', 'govern',"state"]