from report_designer.core.tables import (
    AbstractTable,
    CellTypeCenter,
    CellTypeDateTime,
    CellTypeBooleanIcon,
    CellTypeDeleteIcon,
)


class ReportTable(AbstractTable):
    """
    Таблица списка отчетов
    """

    def create_header(self, header):
        level_0 = [
            header('Наименование'),
            header('Основная таблица'),
            header('Группы'),
            header('Автор'),
            header('Дата и время обновления'),
        ]
        return [level_0]

    def create_cells(self, obj):
        cell = self.cell_class
        url = obj.get_detail_url()
        return [
            cell(obj.name, cell_type=CellTypeCenter, url=url),
            cell(obj.root, cell_type=CellTypeCenter, url=url),
            cell(obj.get_groups_names, cell_type=CellTypeCenter, url=url),
            cell(obj.author, cell_type=CellTypeCenter, url=url),
            cell(obj.updated, cell_type=CellTypeDateTime, url=url),
        ]


class ReportFieldsTable(AbstractTable):
    """
    Таблица списка полей отчетов
    """

    js_sortable_class = 'js-report-fields-table'

    def create_header(self, header):
        level_0 = [
            header('Наименование'),
            header('Псевдоним'),
            header('Представление'),
            header('Виртуальное'),
            header('Групповое'),
            header('Сортировочное'),
            header('Агрегированное'),
            header(''),
        ]
        return [level_0]

    def create_cells(self, obj):
        cell = self.cell_class
        base_attrs = {
            'link_class': 'js-rd-ajax-load-modal-btn',
            'url': obj.get_edit_url(),
        }
        return [
            cell(obj.name, cell_type=CellTypeCenter, **base_attrs),
            cell(obj.alias, cell_type=CellTypeCenter, **base_attrs),
            cell(obj.representation and obj.representation.name or None, cell_type=CellTypeCenter, **base_attrs),
            cell(obj.is_group, cell_type=CellTypeBooleanIcon, **base_attrs),
            cell(obj.is_sort, cell_type=CellTypeBooleanIcon, **base_attrs),
            cell(obj.reverse_sort, cell_type=CellTypeBooleanIcon, **base_attrs),
            cell(obj.is_aggregate, cell_type=CellTypeBooleanIcon, **base_attrs),
            cell('', cell_type=CellTypeDeleteIcon, html_width=self.sortable_column_width),
        ]

    def get_row_data_attrs(self, obj):
        data_attrs = super().get_row_data_attrs(obj)
        data_attrs.update({
            'pk': obj.pk,
            'order': obj.order,
            'change-order-url': obj.get_change_order_url(),
        })
        return data_attrs
