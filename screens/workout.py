# -*- coding: utf-8 -*-
"""Pestana 'Rutina': seleccion de dia + registro de series por ejercicio."""
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField

import colors
import data
from storage import today_str


class ChipButton(MDRaisedButton):
    pass


def _day_pill(day, active, on_press):
    btn = MDRaisedButton(
        text=day["badge"],
        font_size="12sp",
        size_hint=(None, None),
        size=(dp(14) * len(day["badge"]) + dp(36), dp(36)),
        md_bg_color=colors.INDIGO_600 if active else colors.BG_900,
        line_color=colors.BORDER_800,
        theme_text_color="Custom",
        text_color=colors.TEXT_WHITE if active else colors.TEXT_SLATE_400,
    )
    btn.bind(on_release=lambda *_: on_press(day["id"]))
    return btn


def _info_pill(text, color):
    return MDLabel(
        text=text,
        font_style="Caption",
        bold=True,
        theme_text_color="Custom",
        text_color=color,
        size_hint_y=None,
        height=dp(18),
    )


class ExerciseCard(MDCard):
    def __init__(self, ex, idx, ex_data, app, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(8),
            size_hint_y=None,
            md_bg_color=colors.BG_900,
            line_color=colors.EMERALD_500_SOFT if ex_data.get("completed") else colors.BORDER_800,
            radius=[16, 16, 16, 16],
            **kwargs,
        )
        self.ex = ex
        self.idx = idx
        self.ex_data = ex_data
        self.app = app
        self._build()
        self.bind(minimum_height=self.setter("height"))

    def _build(self):
        ex = self.ex
        completed = self.ex_data.get("completed", False)

        # --- Fila superior: check + titulo + boton video ---
        top_row = MDBoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))

        check_btn = MDIconButton(
            icon="check-bold" if completed else "checkbox-blank-outline",
            theme_text_color="Custom",
            text_color=(0.02, 0.09, 0.02, 1) if completed else colors.TEXT_SLATE_400,
            md_bg_color=colors.EMERALD_500 if completed else colors.BG_950,
            pos_hint={"center_y": 0.5},
        )
        check_btn.bind(on_release=lambda *_: self.app.toggle_exercise_complete(ex["id"]))
        top_row.add_widget(check_btn)

        title_box = MDBoxLayout(orientation="vertical")
        title_box.add_widget(_info_pill(f"#{self.idx + 1}  {ex['target']}", colors.INDIGO_400))
        title_box.add_widget(
            MDLabel(
                text=ex["name"],
                bold=True,
                font_style="Subtitle2",
                theme_text_color="Custom",
                text_color=colors.TEXT_WHITE,
            )
        )
        top_row.add_widget(title_box)

        video_btn = MDFlatButton(
            text="Video",
            icon="youtube",
            font_size="11sp",
            size_hint_x=None,
            width=dp(90),
            theme_text_color="Custom",
            text_color=colors.ROSE_400,
            md_bg_color=colors.ROSE_500_SOFT,
        )
        video_btn.bind(on_release=lambda *_: self.app.open_exercise_video(ex["name"]))
        top_row.add_widget(video_btn)

        self.add_widget(top_row)

        # --- Nota ---
        note = MDLabel(
            text=f"[i]{ex['note']}[/i]",
            markup=True,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=colors.TEXT_SLATE_400,
            size_hint_y=None,
        )
        note.bind(texture_size=lambda w, s: setattr(w, "height", s[1]))
        note.text_size = (None, None)
        self.add_widget(note)
        self.bind(width=lambda *_: self._update_note_wrap(note))

        # --- Meta: objetivo + descanso ---
        meta_row = MDBoxLayout(size_hint_y=None, height=dp(28))
        meta_row.add_widget(
            MDLabel(
                text=f"Objetivo: [b][color=818cf8]{ex['sets']} series x {ex['reps']}[/color][/b]",
                markup=True,
                font_style="Caption",
                theme_text_color="Custom",
                text_color=colors.TEXT_SLATE_400,
            )
        )
        if ex["rest"] > 0:
            rest_btn = MDFlatButton(
                text=f"{ex['rest']}s descanso",
                icon="timer-outline",
                font_size="11sp",
                theme_text_color="Custom",
                text_color=colors.EMERALD_400,
                md_bg_color=colors.EMERALD_500_SOFT,
                size_hint_x=None,
                width=dp(130),
            )
            rest_btn.bind(on_release=lambda *_: self.app.start_rest_timer(ex["rest"]))
            meta_row.add_widget(rest_btn)
        self.add_widget(meta_row)

        if data.is_cardio(ex):
            self._build_cardio_row(completed)
        else:
            self._build_sets_table()
            self._build_volume_row()

    def _update_note_wrap(self, note_label):
        note_label.text_size = (self.width - dp(28), None)

    def _build_cardio_row(self, completed):
        row = MDBoxLayout(
            size_hint_y=None,
            height=dp(48),
            padding=dp(10),
            spacing=dp(8),
        )
        with row.canvas.before:
            pass
        row.add_widget(
            MDLabel(
                text="Marcar sesion finalizada",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=colors.TEXT_SLATE_300,
            )
        )
        btn = MDRaisedButton(
            text="Completado" if completed else "Marcar Hecho",
            font_size="12sp",
            md_bg_color=colors.EMERALD_500 if completed else colors.INDIGO_600,
            size_hint_x=None,
            width=dp(130),
        )
        btn.bind(on_release=lambda *_: self.app.toggle_exercise_complete(self.ex["id"]))
        row.add_widget(btn)
        self.add_widget(row)

    def _build_sets_table(self):
        ex = self.ex
        header = MDBoxLayout(size_hint_y=None, height=dp(18), spacing=dp(6))
        for label in ("Serie", "Peso (Kg)", "Reps"):
            header.add_widget(
                MDLabel(
                    text=label,
                    font_style="Overline",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=colors.TEXT_SLATE_500,
                )
            )
        self.add_widget(header)

        sets = self.ex_data.get("sets", [])
        n_sets = min(ex["sets"], 3) if ex["sets"] <= 3 else ex["sets"]
        n_sets = ex["sets"]
        for s_idx in range(min(n_sets, max(len(sets), 3)) if False else n_sets):
            set_val = sets[s_idx] if s_idx < len(sets) else {}
            row = MDBoxLayout(size_hint_y=None, height=dp(40), spacing=dp(6))
            row.add_widget(
                MDLabel(
                    text=f"S{s_idx + 1}",
                    bold=True,
                    halign="center",
                    font_style="Caption",
                    theme_text_color="Custom",
                    text_color=colors.TEXT_SLATE_300,
                    size_hint_x=0.5,
                )
            )
            weight_field = MDTextField(
                text=str(set_val.get("weight", "") or ""),
                hint_text="0",
                input_filter="float",
                mode="rectangle",
                halign="center",
                font_size="14sp",
            )
            weight_field.bind(
                focus=lambda inst, has_focus, si=s_idx: self._on_field_unfocus(
                    inst, has_focus, si, "weight"
                )
            )
            reps_field = MDTextField(
                text=str(set_val.get("reps", "") or ""),
                hint_text="0",
                input_filter="float",
                mode="rectangle",
                halign="center",
                font_size="14sp",
            )
            reps_field.bind(
                focus=lambda inst, has_focus, si=s_idx: self._on_field_unfocus(
                    inst, has_focus, si, "reps"
                )
            )
            row.add_widget(weight_field)
            row.add_widget(reps_field)
            self.add_widget(row)

    def _on_field_unfocus(self, instance, has_focus, set_idx, field):
        if not has_focus:
            self.app.update_set_data(self.ex["id"], set_idx, field, instance.text)

    def _build_volume_row(self):
        total_vol = 0.0
        for s in self.ex_data.get("sets", []):
            w = s.get("weight") or 0
            r = s.get("reps") or 0
            try:
                total_vol += float(w) * float(r)
            except (TypeError, ValueError):
                pass
        row = MDBoxLayout(size_hint_y=None, height=dp(26), padding=[0, dp(4), 0, 0])
        row.add_widget(
            MDLabel(
                text="Volumen Total Ejercicio:",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=colors.TEXT_SLATE_400,
            )
        )
        row.add_widget(
            MDLabel(
                text=f"{total_vol:.1f} Kg",
                bold=True,
                halign="right",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=colors.EMERALD_400,
            )
        )
        self.add_widget(row)


class WorkoutView(MDBoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.app = app
        self.selected_day_id = "day1"

        # --- Pills de dias (scroll horizontal, fuera del scroll vertical
        # para evitar anidar dos ScrollView, lo que puede causar artefactos
        # de render en algunos backends graficos) ---
        self.pills_scroll = ScrollView(
            do_scroll_y=False,
            size_hint_y=None,
            height=dp(52),
            bar_width=0,
        )
        self.pills_row = BoxLayout(
            orientation="horizontal",
            size_hint_x=None,
            spacing=dp(8),
            padding=[dp(14), dp(6)],
        )
        self.pills_row.bind(minimum_width=self.pills_row.setter("width"))
        self.pills_scroll.add_widget(self.pills_row)
        self.add_widget(self.pills_scroll)

        # --- Contenido scrolleable (banner + ejercicios) ---
        self.scroll = ScrollView(do_scroll_x=False)
        self.column = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            padding=[dp(14), 0, dp(14), dp(14)],
            spacing=dp(14),
        )
        self.column.bind(minimum_height=self.column.setter("height"))
        self.scroll.add_widget(self.column)
        self.add_widget(self.scroll)

        self.refresh()

    def select_day(self, day_id):
        self.selected_day_id = day_id
        self.refresh()

    def refresh(self):
        self.pills_row.clear_widgets()
        self.column.clear_widgets()
        logs = self.app.logs
        today = today_str()
        # Solo lectura: no mutar app.logs durante el render (evita que
        # 'Borrar Todos los Datos' deje un registro vacio residual).
        today_logs = logs.get(today, {})

        for day in data.WORKOUT_PROGRAM:
            self.pills_row.add_widget(
                _day_pill(day, day["id"] == self.selected_day_id, self.select_day)
            )

        # --- Banner del dia activo ---
        current_day = data.get_day(self.selected_day_id)
        banner = MDCard(
            orientation="vertical",
            padding=dp(16),
            size_hint_y=None,
            height=dp(92),
            md_bg_color=colors.DAY_COLORS.get(current_day["id"], colors.INDIGO_600),
            radius=[18, 18, 18, 18],
        )
        banner.add_widget(
            MDLabel(
                text="RUTINA ACTIVA",
                font_style="Overline",
                bold=True,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.85),
                size_hint_y=None,
                height=dp(16),
            )
        )
        banner.add_widget(
            MDLabel(
                text=current_day["title"],
                bold=True,
                font_style="H6",
                theme_text_color="Custom",
                text_color=colors.TEXT_WHITE,
                size_hint_y=None,
                height=dp(28),
            )
        )
        banner.add_widget(
            MDLabel(
                text=current_day["subtitle"],
                font_style="Caption",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 0.85),
                size_hint_y=None,
                height=dp(16),
            )
        )
        self.column.add_widget(banner)

        # --- Lista de ejercicios ---
        for idx, ex in enumerate(current_day["exercises"]):
            ex_data = today_logs.get(ex["id"]) or {"sets": [{}] * ex["sets"], "completed": False}
            card = ExerciseCard(ex, idx, ex_data, self.app)
            self.column.add_widget(card)
