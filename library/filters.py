import django_filters
from library.models import Book, Category
from django.db.models import Q
from django import forms

class BookFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_author_title')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    start = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    end = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Categories"
    )

    class Meta:
        model = Book
        fields = ['search', 'start', 'end', 'min_price', 'max_price', 'category']

    def filter_by_author_title(self, queryset, name, value):
        queryset = (
            queryset
            .filter(Q(authors__first_name__icontains=value) | 
                    Q(authors__last_name__icontains=value) |
                    Q(title__icontains=value)
                   )
        )
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filters['category'].field.label_from_instance = (
            lambda obj: obj.name
        )    