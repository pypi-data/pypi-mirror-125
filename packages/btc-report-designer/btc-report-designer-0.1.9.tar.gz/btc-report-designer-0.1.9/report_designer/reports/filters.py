from report_designer.core.filters import StyledFilterSet, SearchBaseFilterSet
from report_designer.models import Report, ReportField


class ReportFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Отчеты
    """

    searching_fields = ('name',)
    searching_select = (
        'root',
        'author',
    )

    class Meta:
        model = Report
        fields = (
            'root',
            'author',
            'groups',
        )


class ReportFieldsFilterSet(StyledFilterSet, SearchBaseFilterSet):
    """
    Фильтр: Поля таблицы отчета
    """

    searching_fields = (
        'alias',
        'name',
    )
    searching_select = ('representation',)

    class Meta:
        model = ReportField
        fields = (
            'is_virtual',
            'is_group',
            'is_sort',
            'reverse_sort',
            'is_aggregate',
        )
