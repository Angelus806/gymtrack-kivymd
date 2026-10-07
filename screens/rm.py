# -*- coding: utf-8 -*-
"""Pestana 'Calc 1RM': calculadora de repeticion maxima (formula Epley)."""
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

import colors
from utils import epley_1rm, percentages_table

PERCENTS = [95, 90, 85, 80, 75, 70]
REPS_FOR_PERCENT = {95: 2, 90: 4, 85: 6, 80: 8, 75: 10, 70: 12}


class RMView(ScrollView):
    def __init__(self, app, **kwargs):
        super().__init__(do_scroll_x=False, **kwargs)
        self.app = app
        self.percent_labels = {}

        self.column = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(14),
            spacing=dp(14),
        )
        self.column.bind(minimum_height=self.column.setter("height"))
        self.add_widget(self.column)
        self._build()

    def _build(self):
        header = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(44))
        header.add_widget(
            MDLabel(
                text="Calculadora 1RM",
                bold=True,
                font_style="H6",
                theme_text_color="Custom",
                text_color=colors.TEXT_WHITE,
                size_hint_y=None,
                height=dp(26),
            )
        )
        header.add_widget(
            MDLabel(
                text="Estima tu Repeticion Maxima (Formula Epley)",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=colors.TEXT_SLATE_400,
                size_hint_y=None,
                height=dp(16),
            )
        )
        self.column.add_widget(header)

        form_card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(240),
            md_bg_color=colors.BG_900,
            line_color=colors.BORDER_800,
            radius=[16, 16, 16, 16],
        )

        self.weight_field = MDTextField(
            hint_text="Peso Levantado (Kg) - Ej: 80",
            input_filter="float",
            mode="rectangle",
        )
        self.weight_field.bind(text=lambda *_: self._calculate())
        form_card.add_widget(self.weight_field)

        self.reps_field = MDTextField(
            hint_text="Repeticiones Logradas - Ej: 8",
            input_filter="float",
            mode="rectangle",
        )
        self.reps_field.bind(text=lambda *_: self._calculate())
        form_card.add_widget(self.reps_field)

        result_card = MDCard(
            orientation="vertical",
            padding=dp(12),
            size_hint_y=None,
            height=dp(80),
            md_bg_color=colors.INDIGO_600_SOFT,
            line_color=(0.30, 0.27, 0.90, 0.3),
            radius=[12, 12, 12, 12],
        )
        result_card.add_widget(
            MDLabel(
                text="1RM ESTIMADO",
                halign="center",
                font_style="Overline",
                bold=True,
                theme_text_color="Custom",
                text_color=colors.INDIGO_400,
                size_hint_y=None,
                height=dp(18),
            )
        )
        self.result_label = MDLabel(
            text="0.0 Kg",
            halign="center",
            bold=True,
            font_style="H4",
            theme_text_color="Custom",
            text_color=colors.EMERALD_400,
        )
        result_card.add_widget(self.result_label)
        form_card.add_widget(result_card)
        self.column.add_widget(form_card)

        pct_card = MDCard(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(230),
            md_bg_color=colors.BG_900,
            line_color=colors.BORDER_800,
            radius=[16, 16, 16, 16],
        )
        pct_card.add_widget(
            MDLabel(
                text="Porcentajes de Carga",
                bold=True,
                font_style="Subtitle2",
                theme_text_color="Custom",
                text_color=colors.TEXT_SLATE_300,
                size_hint_y=None,
                height=dp(22),
            )
        )

        grid = MDBoxLayout(orientation="vertical", spacing=dp(6))
        rows = [PERCENTS[i : i + 2] for i in range(0, len(PERCENTS), 2)]
        for row_percents in rows:
            row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(42))
            for p in row_percents:
                cell = MDCard(
                    orientation="horizontal",
                    padding=dp(8),
                    md_bg_color=colors.BG_950,
                    line_color=colors.BORDER_800_SOFT,
                    radius=[10, 10, 10, 10],
                )
                cell.add_widget(
                    MDLabel(
                        text=f"{p}% ({REPS_FOR_PERCENT[p]} Reps)",
                        font_style="Caption",
                        theme_text_color="Custom",
                        text_color=colors.TEXT_SLATE_400,
                    )
                )
                value_label = MDLabel(
                    text="-",
                    halign="right",
                    bold=True,
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=colors.TEXT_WHITE,
                )
                self.percent_labels[p] = value_label
                cell.add_widget(value_label)
                row.add_widget(cell)
            grid.add_widget(row)
        pct_card.add_widget(grid)
        self.column.add_widget(pct_card)

    def _calculate(self):
        rm1 = epley_1rm(self.weight_field.text, self.reps_field.text)
        if rm1 <= 0:
            self.result_label.text = "0.0 Kg"
            for p in PERCENTS:
                self.percent_labels[p].text = "-"
            return
        self.result_label.text = f"{rm1:.1f} Kg"
        table = percentages_table(rm1, PERCENTS)
        for p, val in table.items():
            self.percent_labels[p].text = f"{val:.1f} kg"
