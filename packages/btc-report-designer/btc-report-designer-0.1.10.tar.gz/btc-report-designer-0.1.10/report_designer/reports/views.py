import abc
import json
from operator import itemgetter

from django.contrib.postgres.aggregates import StringAgg
from django.db import transaction
from django.db.models import (
    Value,
    F,
    BooleanField,
    Case,
    When,
    Q,
    Func,
    CharField,
)
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import DetailView

from report_designer.core.utils import order_by_list
from report_designer.core.views import (
    TitleMixin,
    AjaxContentListView,
    ParentMixin,
    ObjectActionAjaxView,
    DynamicContentTableBaseView,
    CreateAjaxView,
    ActionGroupMixin,
    UpdateAjaxView,
    BreadcrumbsListMixin,
    BackUrlDetailMixin,
    BreadcrumbsDetailMixin,
)
from report_designer.models import (
    Report,
    DBTable,
    TableField,
    ReportField,
    ReportFieldRelation,
    ReportTableRelation,
)
from report_designer.reports.actions import (
    ReportListActionGroup,
    ReportDropdownActionGroup,
    ReportAddFieldActionGroup,
)
from report_designer.reports.filters import ReportFilterSet, ReportFieldsFilterSet, ReportTableRelationFilterSet
from report_designer.reports.forms import ReportCreateForm, ReportUpdateForm
from report_designer.reports.tables import ReportTable, ReportFieldsTable, ReportTableRelationTable


# endregion Базовые миксины


class ReportBreadcrumbsListMixin(BreadcrumbsListMixin):
    """
    Хлебные крошки отчетов
    """

    title_breadcrumb = 'Список отчетов'


class ReportBreadcrumbsDetailBaseMixin(BreadcrumbsDetailMixin, ReportBreadcrumbsListMixin):
    """
    Хлебные крошки отчета
    """

    pass


class ReportsDynamicContentTableBaseView(ParentMixin, DynamicContentTableBaseView):
    """
    Базовое представление для динамических список на странице отчета
    """

    parent_model = Report
    is_paginate = False

    def get_content_url_kwargs(self):
        content_url_kwargs = super().get_content_url_kwargs()
        content_url_kwargs.update(pk=self.parent.pk)
        return content_url_kwargs


# endregion Базовые миксины


# region Список отчетов


class ReportListView(ReportBreadcrumbsListMixin, DynamicContentTableBaseView):
    """
    Представление: Список отчетов
    """

    model = Report
    filterset_class = ReportFilterSet
    table_class = ReportTable
    title = 'Отчеты'
    ajax_content_name = 'reports'
    action_group_classes = (ReportListActionGroup,)


# endregion Список отчетов


# region Создание / редактирование отчета


class ReportCreateUpdateMixin:
    """
    Миксин создания / редактирования отчета
    """

    model = Report

    def get_success_redirect_url(self):
        return self.object.get_detail_url()


class ReportCreateView(ReportCreateUpdateMixin, CreateAjaxView):
    """
    Представление: Создание отчета
    """

    title = 'Создание отчета'
    form_class = ReportCreateForm

    def set_object_additional_values(self, obj):
        super().set_object_additional_values(obj)
        obj.author = self.request.user

    def after_save(self):
        super().after_save()
        self.object.report_tables.create(
            report=self.object,
            db_table=self.object.root,
            is_root=True
        )


class ReportUpdateView(ReportCreateUpdateMixin, UpdateAjaxView):
    """
    Представление: Редактирование отчета
    """

    title = 'Редактирование отчета'
    form_class = ReportUpdateForm


# endregion Создание / редактирование отчета


# region Просмотр отчета


class ReportDetailView(
    BackUrlDetailMixin,
    ReportBreadcrumbsDetailBaseMixin,
    ActionGroupMixin,
    TitleMixin,
    DetailView,
):
    """
    Представление: Просмотр отчета
    """

    model = Report
    template_name = 'report_designer/reports/detail.html'
    context_object_name = 'report'
    action_group_classes = (
        ReportDropdownActionGroup,
        ReportAddFieldActionGroup,
    )

    def get_title(self):
        return f'Отчет "{self.object.name}"'


# endregion Просмотр отчета


# region Редактирование списка таблиц в отчете


class BaseTreeListView(AjaxContentListView):
    """
    Базовое представления для вывода дерева
    """

    is_paginate = False
    is_only_ajax = True
    is_subtree = False
    template_name = 'report_designer/reports/blocks/tree_branch.html'
    context_object_name = 'tree_branches'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                'is_subtree': self.is_subtree,
            }
        )
        return context_data


class DBTablesBaseTreeListView(ParentMixin, BaseTreeListView):
    """
    Базовое представление: Список таблиц БД / в отчете
    """

    queryset = DBTable.objects.available()
    context_object_name = 'tree_branches'
    parent_model = Report
    kwargs_parent_fk = 'report_pk'
    parent_context_name = 'report'
    is_processed = False

    def get_queryset(self):
        # Аннотация параметров для списка таблиц
        # 1). PK для URL загрузки полей
        # 2). Title из alias
        # 3). Существование связи для URL загрузки полей
        return (
            super()
            .get_queryset()
            .annotate(
                related_table_pk=F('pk'),
                title=F('alias'),
                is_relation=Value(True, output_field=BooleanField()),
            )
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({'action_url': self.get_action_tables_url(), 'is_processed': self.is_processed})
        return context_data

    @abc.abstractmethod
    def get_action_tables_url(self):
        """
        URL для действия с таблицами
        """
        raise NotImplementedError


class DBTablesTreeListView(DBTablesBaseTreeListView):
    """
    Представление: Список таблиц БД
    """

    def get_action_tables_url(self):
        return reverse_lazy('report_designer:reports:add-table', kwargs={'pk': self.parent.pk})


class ReportDBTablesTreeListView(DBTablesBaseTreeListView):
    """
    Представление: Список таблиц в отчете
    """

    is_processed = True

    def get_queryset(self):
        # Доступны таблицы, добавленные в отчет
        return super().get_queryset().for_report(self.parent)

    def get_action_tables_url(self):
        return reverse_lazy('report_designer:reports:remove-table', kwargs={'pk': self.parent.pk})


class TableFieldsListView(ParentMixin, BaseTreeListView):
    """
    Представление: Список таблиц БД / в отчете
    """

    queryset = TableField.objects.is_visible()
    parent_model = DBTable
    parent_field = 'db_table'
    is_subtree = True

    def get_queryset(self):
        queryset = super().get_queryset()

        # Цепочка связи
        chain = self.request.GET.get('chain', '')
        if self.is_processed:
            # Аннотация хеша цепочки связей полей отчета
            chain_kwargs = Func(
                StringAgg(
                    Cast(
                        Case(When(report_fields__report__pk=self.report.pk, then=F('report_fields__relations'))),
                        output_field=CharField(),
                    ),
                    delimiter=',',
                ),
                function='md5',
            )
            # Поля таблиц БД в полях очтета
            fields_in_report_fields = self.report.report_fields.values_list('field', flat=True)

            # Условие принадлежности поля к отчету
            condition = (
                chain
                and When(chain=Value(chain), then=Value(True))
                or When(pk__in=fields_in_report_fields, chain__isnull=True, then=Value(True))
            )
            is_exists_in_report_kwargs = Case(condition, default=Value(False), output_field=BooleanField())
            queryset = queryset.annotate(chain=chain_kwargs).annotate(is_exists_in_report=is_exists_in_report_kwargs)
        return queryset.with_related_tables(self.parent).with_title().order_by('is_relation', 'related_table_pk', 'pk')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                'report': self.report,
                'is_processed': self.is_processed,
            }
        )
        return context_data

    @property
    def is_processed(self):
        """
        Переносимые поля
        """
        return 'is_processed' in self.request.GET

    @cached_property
    def report(self):
        """
        Отчет
        """
        return get_object_or_404(Report, pk=self.kwargs.get('report_pk'))


class ReportDBTableChangeBaseView(ObjectActionAjaxView):
    """
    Базовое представление: Добавление / удаление таблицы в отчете
    """

    model = Report
    join_errors = True
    dependents = (('ajax_contents', 'report_tables'),)

    @cached_property
    def table(self):
        """
        Добавляемая таблица
        """
        return get_object_or_404(DBTable.objects.available(), pk=self.request.POST.get('table'))


class ReportDBTableAddView(ReportDBTableChangeBaseView):
    """
    Представление: Добавление таблицы в отчет
    """

    title = 'Добавление таблицы в отчет'

    def valid_action(self):
        is_valid = super().valid_action()
        if self.object.report_tables.filter(db_table=self.table).exists():
            self.add_error(f'Таблица "{self.table.alias}" уже добавлена в отчет')
            is_valid = False
        return is_valid

    def action(self):
        super().action()
        self.object.report_tables.create(db_table=self.table, order=self.object.table_next_order)


class ReportDBTableRemoveView(ReportDBTableChangeBaseView):
    """
    Представление: Удаление таблицы из отчета
    """

    title = 'Удаление таблицы из отчета'

    def valid_action(self):
        is_valid = super().valid_action()
        if not self.object.report_tables.filter(db_table=self.table).exists():
            self.add_error(f'Таблица "{self.table.alias}" не существует в отчете')
            is_valid = False
        if self.table == self.object.root:
            self.add_error(f'Таблица "{self.table.alias}" является основной таблицей отчета')
            is_valid = False
        return is_valid

    def action(self):
        super().action()
        # Удаление таблицы из отчета
        report_table = self.object.report_tables.filter(db_table=self.table)
        order = report_table.first().order
        report_table.delete()

        # Изменение порядка таблиц
        self.object.report_tables.filter(order__gt=order).update(order=F('order') - 1)


# endregion Редактирование списка таблиц в отчете


# region Список связей таблиц отчета


class ReportTableRelationsListView(ReportsDynamicContentTableBaseView):
    """
    Представление: Список связей таблиц отчета
    """

    queryset = ReportTableRelation.objects.all()
    parent_field = 'report_table__report'
    table_class = ReportTableRelationTable
    filterset_class = ReportTableRelationFilterSet
    ajax_content_name = 'report_table_relations'


# endregion Список связей таблиц отчета


# region Список полей в отчете


class ReportFieldsListView(ReportsDynamicContentTableBaseView):
    """
    Представление: Список полей отчета
    """

    queryset = ReportField.objects.order_by('order')
    parent_field = 'report'
    table_class = ReportFieldsTable
    filterset_class = ReportFieldsFilterSet
    ajax_content_name = 'report_fields'


class ReportFieldsAddView(ObjectActionAjaxView):
    """
    Представление: Добавление полей в отчет
    """

    model = Report
    dependents = (
        ('ajax_contents', 'report_tables'),
        ('dynamic_contents', 'report_fields'),
    )

    @transaction.atomic
    def action(self):
        # Создание полей очтета
        table_fields_ids = list(map(itemgetter(-1), self.fields_with_relations))

        # Список полей, отсортированных в полученном порядке
        fields = order_by_list(TableField.objects.filter(pk__in=table_fields_ids), 'pk', table_fields_ids)

        # Последний порядковый номер поля в отчете
        order = self.object.field_next_order

        # Связи полей и поля
        relations_report_fields, report_fields = [], []
        for index, field in enumerate(fields):
            # Добавление поля отчета
            report_field = ReportField(
                name=field.name,
                alias=field.alias,
                representation=field.representation,
                report=self.object,
                field=field,
                order=order + index,
            )
            report_fields.append(report_field)
        objs = ReportField.objects.bulk_create(report_fields)

        # Добавление связей поля
        for report_field, chain in zip(objs, self.fields_with_relations):
            for relation_order, table_field_id in enumerate(chain[:-1]):
                relations_report_fields.append(
                    ReportFieldRelation(
                        order=relation_order, report_field=report_field, table_field_id=table_field_id
                    )
                )
        ReportFieldRelation.objects.bulk_create(relations_report_fields)

    @cached_property
    def fields_with_relations(self):
        """
        Список цепочек полей
        """
        fields_chains = self.request.POST.get('fields_chains[]')
        if not fields_chains:
            return {}
        return json.loads(fields_chains)


class ReportFieldChangeOrderView(ObjectActionAjaxView):
    """
    Представление: Изменение порядка поля
    """

    model = ReportField
    dependents = (('dynamic_contents', 'report_fields'),)

    def action(self):
        # Старое и новое значение
        old, new = self.object.order, int(self.request.POST.get('order'))
        is_downgrade = new < old

        # Обновление порядка у всех полей отчета
        query = Case(
            *[
                When(order=Value(old), then=Value(new)),
                When(
                    Q(
                        **{
                            f'order__{is_downgrade and "l" or "g"}t': Value(old),
                            f'order__{is_downgrade and "g" or "l"}te': Value(new),
                        }
                    ),
                    then=F('order') + (is_downgrade and 1 or -1),
                ),
            ],
            default=F('order'),
        )
        self.object.report.report_fields.update(order=query)


# endregion Список полей в отчете
