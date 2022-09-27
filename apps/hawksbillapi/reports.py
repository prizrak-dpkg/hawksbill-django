from datetime import datetime, timedelta
from typing import Any, Dict
from django.conf import settings
from django.db.models.query import QuerySet
from django.utils.timezone import make_aware
import xlsxwriter
import apps.hawksbillapi.format as report_format
from apps.users.models import User
from apps.clientrequests.models import ClientRequest


class HawksbillReport:
    def __init__(self, user: User, start_date: str, end_date: str) -> None:
        self.__start_date = start_date
        self.__end_date = end_date
        self.__title = (
            "Reporte de eventos del {} de {} del {} al {} de {} del {}".format(
                self.get_start_date.day,
                report_format.months.get(self.get_start_date.month, "..."),
                self.get_start_date.year,
                self.get_end_date.day,
                report_format.months.get(self.get_end_date.month, "..."),
                self.get_end_date.year,
            )
        )
        self.report_path = f"reports/hawksbill_{user.username}.xlsx"

    def stats_worksheet_titles(
        self, workbook: xlsxwriter.Workbook, **kwargs
    ) -> xlsxwriter.Workbook.worksheet_class:
        worksheet: xlsxwriter.Workbook.worksheet_class = workbook.add_worksheet(
            "Estadísticas"
        )
        worksheet.set_column("A:H", width=15)
        worksheet.merge_range(
            "A1:H1",
            "Hawksbill",
            kwargs["title_format"],
        )
        worksheet.merge_range(
            "A2:H2",
            self.__title,
            kwargs["title_format"],
        )
        worksheet.merge_range("A14:H14", "Calificaciones", kwargs["title_format"])
        worksheet.merge_range(
            "A15:B15", "Redes y Telecomunicaciones", kwargs["title_format"]
        )
        worksheet.merge_range("C15:D15", "Software", kwargs["title_format"])
        worksheet.merge_range("E15:F15", "Operaciones", kwargs["title_format"])
        worksheet.merge_range("G15:H15", "Hardware", kwargs["title_format"])
        worksheet.merge_range("A17:D17", "Total de eventos", kwargs["title_format"])
        return worksheet

    def request_worksheet_titles(
        self, workbook: xlsxwriter.Workbook, **kwargs
    ) -> xlsxwriter.Workbook.worksheet_class:
        worksheet = workbook.add_worksheet("Eventos")
        worksheet.set_column("A:I", width=30)
        worksheet.merge_range(
            "A1:I1",
            self.__title,
            kwargs["title_format"],
        )
        worksheet.write(
            "A2",
            "Fecha de apertura",
            kwargs["title_format"],
        )
        worksheet.write(
            "B2",
            "Fecha de cierre",
            kwargs["title_format"],
        )
        worksheet.write(
            "C2",
            "Cliente",
            kwargs["title_format"],
        )
        worksheet.write(
            "D2",
            "Categoría",
            kwargs["title_format"],
        )
        worksheet.merge_range(
            "E2:F2",
            "Descripción",
            kwargs["title_format"],
        )
        worksheet.write(
            "G2",
            "Creador",
            kwargs["title_format"],
        )
        worksheet.write(
            "H2",
            "Responsable",
            kwargs["title_format"],
        )
        worksheet.write(
            "I2",
            "Estado",
            kwargs["title_format"],
        )
        return worksheet

    def stats_worksheet_content(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        data: Dict[str, int],
        **kwargs,
    ) -> None:
        worksheet.merge_range(
            "A16:B16",
            data.get("telecommunications", 0),
            kwargs["integer_content_format"],
        )
        worksheet.merge_range(
            "C16:D16",
            data.get("software", 0),
            kwargs["integer_content_format"],
        )
        worksheet.merge_range(
            "E16:F16",
            data.get("operations", 0),
            kwargs["integer_content_format"],
        )
        worksheet.merge_range(
            "G16:H16",
            data.get("hardware", 0),
            kwargs["integer_content_format"],
        )
        worksheet.merge_range(
            "E17:H17",
            data.get("total", 0),
            kwargs["integer_subtitle_format"],
        )

    def request_worksheet_content(
        self,
        worksheet: xlsxwriter.Workbook.worksheet_class,
        data: QuerySet[ClientRequest],
        **kwargs,
    ):
        start_row = 2
        for index in range(len(data)):
            worksheet.write(
                start_row + index,
                0,
                data[index].registration_date - timedelta(hours=5),
                kwargs["date_content_format"],
            )
            worksheet.write(
                start_row + index,
                1,
                data[index].modification_date - timedelta(hours=5)
                if data[index].is_closed
                else "-",
                kwargs["date_content_format"],
            )
            worksheet.write(
                start_row + index,
                2,
                data[index].client.name,
                kwargs["content_format"],
            )
            worksheet.write(
                start_row + index,
                3,
                data[index].type.name,
                kwargs["content_format"],
            )
            worksheet.merge_range(
                start_row + index,
                4,
                start_row + index,
                5,
                data[index].description,
                kwargs["content_format"],
            )
            worksheet.write(
                start_row + index,
                6,
                f"{data[index].applicant.first_name} {data[index].applicant.last_name}",
                kwargs["content_format"],
            )
            worksheet.write(
                start_row + index,
                7,
                f"{data[index].technician.first_name} {data[index].technician.last_name}",
                kwargs["content_format"],
            )
            worksheet.write(
                start_row + index,
                8,
                "Cerrada" if data[index].is_closed else "Abierta",
                kwargs["content_format"],
            )

    def stats_worksheet_charts(
        self,
        workbook: xlsxwriter.Workbook,
        worksheet: xlsxwriter.Workbook.worksheet_class,
    ) -> None:
        column_chart = workbook.add_chart(
            {
                "type": "column",
            }
        )
        column_chart.set_size({"width": 440, "height": 220})
        column_chart.set_style(18)
        column_chart.set_title(
            {
                "name": "Cantidad de Eventos",
                "name_font": {
                    "name": "Arial Narrow",
                    "size": 12,
                },
            }
        )
        column_chart.add_series(
            {
                "values": f"=Estadísticas!$A$16:$G$16",
                "categories": f"=Estadísticas!$A$15:$G$15",
            }
        )
        column_chart.set_legend({"none": True})
        column_chart.set_x_axis(
            {
                "name": "Eventos",
                "name_font": {
                    "name": "Arial Narrow",
                    "size": 8,
                },
            }
        )
        column_chart.set_y_axis(
            {
                "name": "Cantidad",
                "name_font": {
                    "name": "Arial Narrow",
                    "size": 8,
                },
                "num_format": "#,##0",
            }
        )
        doughnut_chart = workbook.add_chart(
            {
                "type": "doughnut",
            }
        )
        doughnut_chart.set_size({"width": 440, "height": 220})
        doughnut_chart.set_style(18)
        doughnut_chart.set_title(
            {
                "name": "Porcentaje de Eventos",
                "name_font": {
                    "name": "Arial Narrow",
                    "size": 12,
                },
            }
        )
        doughnut_chart.add_series(
            {
                "values": f"=Estadísticas!$A$16:$G$16",
                "categories": f"=Estadísticas!$A$15:$G$15",
                "data_labels": {
                    "percentage": True,
                    "font": {"name": "Arial Narrow", "size": 8, "color": "#FFFFFF"},
                },
            }
        )
        worksheet.insert_chart("A3", chart=column_chart)
        worksheet.insert_chart("E3", chart=doughnut_chart)

    def stats_worksheet(self, workbook: xlsxwriter.Workbook, **kwargs):
        formats: Dict[str, Any] = kwargs["formats"]
        data = self.stats_worksheet_data
        worksheet = self.stats_worksheet_titles(
            workbook=workbook, title_format=formats.get("title_format", None)
        )
        self.stats_worksheet_content(
            worksheet=worksheet,
            data=data,
            integer_subtitle_format=formats.get("integer_subtitle_format", None),
            integer_content_format=formats.get("integer_content_format", None),
        )
        self.stats_worksheet_charts(workbook=workbook, worksheet=worksheet)

    def request_worksheet(self, workbook, **kwargs):
        formats: Dict[str, Any] = kwargs["formats"]
        data: QuerySet[ClientRequest] = ClientRequest.objects.filter(
            status=True,
            registration_date__gte=self.get_start_date,
            registration_date__lte=self.get_end_date,
        )
        worksheet = self.request_worksheet_titles(
            workbook=workbook,
            title_format=formats.get("title_format", None),
        )
        self.request_worksheet_content(
            worksheet=worksheet,
            data=data,
            date_content_format=formats.get("date_content_format", None),
            content_format=formats.get("content_format", None),
        )

    @property
    def stats_worksheet_data(self):
        data: QuerySet[ClientRequest] = ClientRequest.objects.filter(
            status=True,
            registration_date__gte=self.get_start_date,
            registration_date__lte=self.get_end_date,
        )
        return {
            "telecommunications": data.filter(
                type__name="Redes y Telecomunicaciones"
            ).count(),
            "software": data.filter(type__name="Software").count(),
            "operations": data.filter(type__name="Operaciones").count(),
            "hardware": data.filter(type__name="Hardware").count(),
            "total": data.count(),
        }

    @property
    def get_start_date(self):
        return make_aware(datetime.strptime(self.__start_date, "%Y-%m-%d"))

    @property
    def get_end_date(self):
        return make_aware(
            datetime.strptime(
                "{} 23:59:59".format(self.__end_date), "%Y-%m-%d %H:%M:%S"
            )
        )

    @property
    def create_report(self):
        return xlsxwriter.Workbook(
            f"{settings.MEDIA_ROOT}/{self.report_path}", {"remove_timezone": True}
        )

    @property
    def get_report(self):
        workbook = self.create_report
        formats = {
            "title_format": workbook.add_format(report_format.title_format),
            "subtitle_format": workbook.add_format(report_format.subtitle_format),
            "integer_subtitle_format": workbook.add_format(
                report_format.integer_subtitle_format
            ),
            "decimal_subtitle_format": workbook.add_format(
                report_format.decimal_subtitle_format
            ),
            "integer_content_format": workbook.add_format(
                report_format.integer_content_format
            ),
            "decimal_content_format": workbook.add_format(
                report_format.decimal_content_format
            ),
            "date_content_format": workbook.add_format(
                report_format.date_content_format
            ),
            "content_format": workbook.add_format(report_format.content_format),
        }
        self.stats_worksheet(workbook=workbook, formats=formats)
        self.request_worksheet(workbook=workbook, formats=formats)
        workbook.close()
        return self.report_path
