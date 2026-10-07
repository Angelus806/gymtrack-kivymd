# -*- coding: utf-8 -*-
"""Pestana 'Historial': resumen y volumen acumulado por fecha."""
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

import colors
import data


def _stat_card(label, value, value_color):
    card = MDCard(
        orientation="vertical",
        padding=dp(14),
        size_hint_y=None,
        height=dp(72),
        md_bg_color=colors.BG_900,
        line_color=colors.BORDER_800,
        radius=[14, 14, 14, 14],
    )
    card.add_widget(
        MDLabel(
            text=label,
            font_style="Overline",
            theme_text_color="Custom",
            text_color=colors.TEXT_SLATE_500,
            size_hint_y=None,
            height=dp(16),
        )
    )
    card.add_widget(
        MDLabel(
            text=value,
            bold=True,
            font_style="H5",
            theme_text_color="Custom",
            text_color=value_color,
        )
    )
    return card


class HistoryView(ScrollView):
    def __init__(self, app, **kwargs):
        super().__init__(do_scroll_x=False, **kwargs)
        self.app = app
        self.column = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=dp(14),
            spacing=dp(14),
        )
        self.column.bind(minimum_height=self.column.setter("height"))
        self.add_widget(self.column)
        self.refresh()

    def refresh(self):
        self.column.clear_widgets()
        logs = self.app.logs
        dates = sorted(logs.keys(), reverse=True)

        total_vol = 0.0
        total_completed = 0
        for d in dates:
            for ex in logs[d].values():
                if ex.get("completed"):
                    total_completed += 1
                for s in ex.get("sets", []):
                    try:
                        total_vol += float(s.get("weight") or 0) * float(s.get("reps") or 0)
                    except (TypeError, ValueError):
                        pass

        header = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(44))
        header.add_widget(
            MDLabel(
                text="Historial de Cargas",
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
                text="Resumen y volumen acumulado por fecha",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=colors.TEXT_SLATE_400,
                size_hint_y=None,
                height=dp(16),
            )
        )
        self.column.add_widget(header)

        stats_row = MDBoxLayout(size_hint_y=None, height=dp(72), spacing=dp(10))
        stats_row.add_widget(_stat_card("EJERCICIOS HECHOS", str(total_completed), colors.INDIGO_400))
        stats_row.add_widget(
            _stat_card("VOLUMEN TOTAL", f"{(total_vol / 1000):.1f}k Kg", colors.EMERALD_400)
        )
        self.column.add_widget(stats_row)

        if not dates:
            empty = MDCard(
                padding=dp(20),
                size_hint_y=None,
                height=dp(90),
                md_bg_color=colors.BG_900,
                line_color=colors.BORDER_800,
                radius=[14, 14, 14, 14],
            )
            empty.add_widget(
                MDLabel(
                    text="Aun no tienes cargas registradas. Comienza a anotar tu "
                    "entrenamiento en la pestana 'Rutina'.",
                    font_style="Caption",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=colors.TEXT_SLATE_400,
                )
            )
            self.column.add_widget(empty)
            return

        for date in dates:
            day_logs = logs[date]
            logged_ex_keys = [k for k in day_logs.keys() if day_logs[k]]
            if not logged_ex_keys:
                continue

            day_vol = 0.0
            for k in logged_ex_keys:
                for s in day_logs[k].get("sets", []):
                    try:
                        day_vol += float(s.get("weight") or 0) * float(s.get("reps") or 0)
                    except (TypeError, ValueError):
                        pass

            date_card = MDCard(
                orientation="vertical",
                padding=dp(14),
                spacing=dp(8),
                size_hint_y=None,
                md_bg_color=colors.BG_900,
                line_color=colors.BORDER_800,
                radius=[14, 14, 14, 14],
            )
            date_card.bind(minimum_height=date_card.setter("height"))

            top = MDBoxLayout(size_hint_y=None, height=dp(26))
            top.add_widget(
                MDLabel(
                    text=f"[b]{date}[/b]",
                    markup=True,
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=colors.TEXT_SLATE_300,
                )
            )
            top.add_widget(
                MDLabel(
                    text=f"{day_vol:.0f} kg total",
                    bold=True,
                    halign="right",
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=colors.EMERALD_400,
                )
            )
            date_card.add_widget(top)

            for ex_id in logged_ex_keys:
                ex_log = day_logs[ex_id]
                name = data.find_exercise_name(ex_id)
                sets_text_parts = []
                for idx, s in enumerate(ex_log.get("sets", [])):
                    if s.get("weight"):
                        sets_text_parts.append(
                            f"S{idx + 1}: {s.get('weight')}kg x {s.get('reps') or 0}"
                        )
                if not sets_text_parts and not ex_log.get("completed"):
                    continue

                ex_box = MDBoxLayout(
                    orientation="vertical", size_hint_y=None, padding=dp(8), spacing=dp(4)
                )
                ex_box.bind(minimum_height=ex_box.setter("height"))
                name_row = MDBoxLayout(size_hint_y=None, height=dp(20))
                name_row.add_widget(
                    MDLabel(
                        text=name,
                        bold=True,
                        font_style="Caption",
                        theme_text_color="Custom",
                        text_color=colors.TEXT_SLATE_300,
                    )
                )
                if ex_log.get("completed"):
                    name_row.add_widget(
                        MDLabel(
                            text="Completado",
                            halign="right",
                            font_style="Caption",
                            theme_text_color="Custom",
                            text_color=colors.EMERALD_400,
                        )
                    )
                ex_box.add_widget(name_row)
                if sets_text_parts:
                    ex_box.add_widget(
                        MDLabel(
                            text="   |   ".join(sets_text_parts),
                            font_style="Caption",
                            theme_text_color="Custom",
                            text_color=colors.TEXT_SLATE_400,
                            size_hint_y=None,
                            height=dp(18),
                        )
                    )
                date_card.add_widget(ex_box)

            self.column.add_widget(date_card)
