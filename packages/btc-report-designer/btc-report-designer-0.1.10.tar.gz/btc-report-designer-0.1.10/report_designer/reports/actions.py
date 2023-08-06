from django.urls import reverse_lazy

from report_designer.core.actions import (
    ActionGroup,
    SimpleModalAction,
    DropdownActionGroup,
    UpdateDropdownModalAction,
    SimpleAction,
)


class ReportListActionGroup(ActionGroup):
    """
    Группа действий в списке отчетов
    """

    create = SimpleModalAction(title='Добавить', url=reverse_lazy('report_designer:reports:create'))


class ReportDropdownActionGroup(DropdownActionGroup):
    """
    Выпадающий список действий с отчетом
    """

    edit = UpdateDropdownModalAction(title='Редактировать основную информацию')


class ReportAddFieldActionGroup(ActionGroup):
    """
    Группа действий в списке отчетов
    """

    name = 'add_fields_action_group'
    css_classes = 'tree-block-action-btn'
    add = SimpleAction(title='Перенести в отчет', css_classes='hidden js-rd-add-fields-to-report')

    def __init__(self, user, obj=None, **kwargs):
        super().__init__(user, obj, **kwargs)
        self.actions['add'].url = reverse_lazy('report_designer:reports:add-fields', kwargs={'pk': obj.pk})
