# -*- coding: utf-8 -*-
"""
GymTrack Pro - version KivyMD (Android/escritorio)

Migracion funcional de la app web (gymtrack_pro_rutina_diario_de_cargas.html)
a una app nativa con Kivy + KivyMD, conservando:
 - Rutina de 5 dias con ejercicios, series/reps objetivo y notas tecnicas.
 - Registro diario de cargas (peso/reps por serie) y marcado de completado.
 - Calculo de volumen por ejercicio y acumulado historico.
 - Temporizador de descanso (con aviso sonoro + vibracion al finalizar).
 - Calculadora de 1RM (formula de Epley) con tabla de porcentajes.
 - Historial por fecha con estadisticas totales.
 - Exportar/Importar respaldo (JSON/CSV) y borrado de datos.
"""
import csv
import json
import os
from datetime import datetime

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import NoTransition

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar

import colors
import data
import storage
import utils
from screens.workout import WorkoutView
from screens.history import HistoryView
from screens.rm import RMView
from screens.settings import SettingsView
from widgets import BottomNavBar

NAV_TABS = [
    ("workout", "calendar-month", "Rutina"),
    ("history", "chart-bar", "Historial"),
    ("rm", "calculator-variant", "Calc 1RM"),
    ("settings", "cog-outline", "Ajustes"),
]

class RootWidget(FloatLayout):
    pass


class GymTrackApp(MDApp):
    timer_display = StringProperty("00:00")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logs = {}
        self._timer_event = None
        self._timer_remaining = 0
        self._timer_dialog = None
        self._confirm_dialog = None
        self._file_manager = None
        self._import_dialog_result = None

        self.workout_view = None
        self.history_view = None
        self.rm_view = None
        self.settings_view = None
        self.bottom_nav = None
        self.root_widget = None

    # ------------------------------------------------------------------
    # Ciclo de vida
    # ------------------------------------------------------------------
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Teal"
        Window.clearcolor = colors.BG_950

        self.logs = storage.load_logs()

        root = RootWidget()
        self.root_widget = root

        self.workout_view = WorkoutView(self)
        self.history_view = HistoryView(self)
        self.rm_view = RMView(self)
        self.settings_view = SettingsView(self)

        root.ids.workout_container.add_widget(self.workout_view)
        root.ids.history_container.add_widget(self.history_view)
        root.ids.rm_container.add_widget(self.rm_view)
        root.ids.settings_container.add_widget(self.settings_view)

        # Transicion instantanea entre pantallas (barra de navegacion propia,
        # ver widgets.BottomNavBar, para evitar un glitch de animacion de
        # KivyMD 1.2.0 al volver a la primera pestana).
        root.ids.screen_manager.transition = NoTransition()

        self.bottom_nav = BottomNavBar(NAV_TABS, on_tab_press=self.switch_tab)
        root.ids.bottom_nav_slot.add_widget(self.bottom_nav)
        self.switch_tab("workout")

        return root

    def on_start(self):
        self._maybe_request_android_permissions()

    def _maybe_request_android_permissions(self):
        try:
            from kivy.utils import platform

            if platform == "android":
                from android.permissions import request_permissions, Permission

                request_permissions(
                    [Permission.VIBRATE, Permission.WAKE_LOCK]
                )
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Navegacion
    # ------------------------------------------------------------------
    def switch_tab(self, name):
        sm = self.root_widget.ids.screen_manager
        sm.current = name
        # Forzamos visibilidad exclusiva de la pantalla activa: evita un
        # "fantasma" de la pantalla anterior quedando dibujado encima,
        # un glitch observado en algunas versiones de Kivy/KivyMD al
        # cambiar de pantalla sin transicion animada.
        for screen in sm.screens:
            is_current = screen.name == name
            screen.opacity = 1 if is_current else 0
            screen.disabled = not is_current
        self.bottom_nav.set_active_tab(name)
        if name == "workout":
            self.workout_view.refresh()
        elif name == "history":
            self.history_view.refresh()

    # ------------------------------------------------------------------
    # Logica de ejercicios / registro diario
    # ------------------------------------------------------------------
    def _today_entry(self, ex_id, n_sets=3):
        today = storage.today_str()
        day_logs = self.logs.setdefault(today, {})
        if ex_id not in day_logs or not day_logs[ex_id]:
            day_logs[ex_id] = storage.default_exercise_entry(n_sets)
        if "sets" not in day_logs[ex_id]:
            day_logs[ex_id]["sets"] = [{} for _ in range(n_sets)]
        return day_logs[ex_id]

    def toggle_exercise_complete(self, ex_id):
        entry = self._today_entry(ex_id)
        entry["completed"] = not entry.get("completed", False)
        storage.save_logs(self.logs)
        self.workout_view.refresh()

    def update_set_data(self, ex_id, set_idx, field, value):
        entry = self._today_entry(ex_id)
        sets = entry.setdefault("sets", [])
        while len(sets) <= set_idx:
            sets.append({})
        sets[set_idx][field] = value
        storage.save_logs(self.logs)
        self.workout_view.refresh()

    def open_exercise_video(self, exercise_name):
        utils.open_url(utils.youtube_search_url(exercise_name))

    def show_snackbar(self, text):
        MDSnackbar(
            MDLabel(
                text=text,
                theme_text_color="Custom",
                text_color=colors.TEXT_WHITE,
            ),
            md_bg_color=colors.BORDER_800,
            duration=2.5,
        ).open()

    # ------------------------------------------------------------------
    # Temporizador de descanso
    # ------------------------------------------------------------------
    def open_timer_modal(self):
        if self._timer_dialog:
            self._timer_dialog.dismiss()

        content = FloatLayout(size_hint_y=None, height="150dp")
        from kivymd.uix.gridlayout import MDGridLayout

        grid = MDGridLayout(cols=2, spacing="8dp", size_hint=(1, 1), pos_hint={"top": 1})
        for secs in (45, 60, 90, 120):
            btn = MDRaisedButton(
                text=f"{secs} seg",
                md_bg_color=colors.BORDER_800,
                size_hint=(1, None),
                height="48dp",
            )
            btn.bind(on_release=lambda inst, s=secs: self._pick_timer(s))
            grid.add_widget(btn)
        content.add_widget(grid)

        self._timer_dialog = MDDialog(
            title="Temporizador de Descanso",
            text="Selecciona los segundos de descanso",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCELAR", on_release=lambda *_: self._timer_dialog.dismiss())
            ],
        )
        self._timer_dialog.open()

    def _pick_timer(self, seconds):
        if self._timer_dialog:
            self._timer_dialog.dismiss()
        self.start_rest_timer(seconds)

    def start_rest_timer(self, seconds):
        if self._timer_event:
            self._timer_event.cancel()
        self._timer_remaining = seconds
        self._update_timer_display()
        floating = self.root_widget.ids.floating_timer
        floating.opacity = 1
        floating.disabled = False
        self._timer_event = Clock.schedule_interval(self._tick_timer, 1)

    def stop_rest_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None
        floating = self.root_widget.ids.floating_timer
        floating.opacity = 0
        floating.disabled = True
        self.timer_display = "00:00"

    def add_timer_time(self, secs):
        self._timer_remaining += secs
        self._update_timer_display()

    def _tick_timer(self, dt):
        self._timer_remaining -= 1
        if self._timer_remaining <= 0:
            self.stop_rest_timer()
            utils.vibrate([300, 150, 300])
            utils.play_beep()
        else:
            self._update_timer_display()

    def _update_timer_display(self):
        self.timer_display = utils.format_mmss(self._timer_remaining)

    # ------------------------------------------------------------------
    # Exportar / Importar / Borrar
    # ------------------------------------------------------------------
    def export_json(self):
        path = os.path.join(
            storage.get_exports_dir(),
            f"GymTrack_Backup_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json",
        )
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)
        self.show_snackbar(f"Guardado en: {path}")

    def export_csv(self):
        path = os.path.join(
            storage.get_exports_dir(),
            f"GymTrack_Export_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv",
        )
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Fecha", "EjercicioID", "Serie", "Peso", "Reps", "Volumen"])
            for date, exercises in self.logs.items():
                for ex_id, ex_log in exercises.items():
                    for idx, s in enumerate(ex_log.get("sets", [])):
                        if s.get("weight") or s.get("reps"):
                            w = utils.safe_float(s.get("weight"))
                            r = utils.safe_float(s.get("reps"))
                            writer.writerow([date, ex_id, idx + 1, w, r, w * r])
        self.show_snackbar(f"Guardado en: {path}")

    def open_import_file_manager(self):
        start_path = storage.get_exports_dir()
        try:
            from kivy.utils import platform

            if platform == "android":
                from android.storage import primary_external_storage_path

                ext_path = primary_external_storage_path()
                if os.path.isdir(ext_path):
                    start_path = ext_path
        except Exception:
            pass

        if not self._file_manager:
            self._file_manager = MDFileManager(
                exit_manager=self._close_file_manager,
                select_path=self._on_file_selected,
                ext=[".json"],
            )
        self._file_manager.show(start_path)

    def _close_file_manager(self, *args):
        if self._file_manager:
            self._file_manager.close()

    def _on_file_selected(self, path):
        self._close_file_manager()
        if not path.lower().endswith(".json"):
            self.show_snackbar("Selecciona un archivo .json valido")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                parsed = json.load(f)
            if not isinstance(parsed, dict):
                raise ValueError("Formato invalido")
            self.logs = parsed
            storage.save_logs(self.logs)
            self.workout_view.refresh()
            self.history_view.refresh()
            self.show_snackbar("Datos importados con exito")
        except Exception as e:
            self.show_snackbar(f"Error al leer el archivo JSON: {e}")

    def confirm_clear_all_data(self):
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()
        self._confirm_dialog = MDDialog(
            title="Borrar todos los datos",
            text="Estas seguro de borrar todo tu historial de entrenamiento? "
            "Esta accion no se puede deshacer.",
            buttons=[
                MDFlatButton(
                    text="CANCELAR", on_release=lambda *_: self._confirm_dialog.dismiss()
                ),
                MDFlatButton(
                    text="BORRAR",
                    theme_text_color="Custom",
                    text_color=colors.ROSE_400,
                    on_release=self._do_clear_all_data,
                ),
            ],
        )
        self._confirm_dialog.open()

    def _do_clear_all_data(self, *args):
        if self._confirm_dialog:
            self._confirm_dialog.dismiss()
        self.logs = {}
        storage.save_logs(self.logs)
        self.workout_view.refresh()
        self.history_view.refresh()
        self.show_snackbar("Historial borrado")


if __name__ == "__main__":
    GymTrackApp().run()
