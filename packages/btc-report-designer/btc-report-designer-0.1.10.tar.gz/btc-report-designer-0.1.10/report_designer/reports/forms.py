from django.forms import ModelForm

from report_designer.core.forms import StyledFormMixin
from report_designer.models import Report


class ReportBaseForm(StyledFormMixin, ModelForm):
    """
    Базовая форма отчета
    """

    searching_select = (
        'root',
        'groups',
    )

    class Meta:
        model = Report
        fields = (
            'name',
            'groups',
            'is_visible_in_reports',
        )


class ReportCreateForm(ReportBaseForm):
    """
    Форма: создание отчета
    """

    class Meta(ReportBaseForm.Meta):
        fields = (
            'name',
            'root',
            'groups',
            'is_visible_in_reports',
        )


class ReportUpdateForm(ReportBaseForm):
    """
    Форма: редактирование отчета
    """

    pass
