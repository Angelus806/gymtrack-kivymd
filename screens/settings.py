# -*- coding: utf-8 -*-
"""Pestana 'Ajustes': exportar/importar respaldo y borrar datos."""
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton

import colors


def _section_card(title, subtitle=None, height=None):
    card = MDCard(
        orientation="vertical",
        padding=dp(16),
        spacing=dp(10),
        size_hint_y=None,
        md_bg_color=colors.BG_900,
        line_color=colors.BORDER_800,
        radius=[16, 16, 16, 16],
    )
    card.bind(minimum_height=card.setter("height"))
    card.add_widget(
        MDLabel(
            text=title,
            bold=True,
            font_style="Subtitle1",
            theme_text_color="Custom",
            text_color=colors.TEXT_WHITE,
            size_hint_y=None,
            height=dp(24),
        )
    )
    if subtitle:
        lbl = MDLabel(
            text=subtitle,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=colors.TEXT_SLATE_400,
            size_hint_y=None,
        )
        lbl.bind(texture_size=lambda w, s: setattr(w, "height", s[1]))
        card.add_widget(lbl)
    return card


class SettingsView(ScrollView):
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
        self._build()

    def _build(self):
        header = MDBoxLayout(orientation="vertical", size_hint_y=None, height=dp(44))
        header.add_widget(
            MDLabel(
                text="Configuracion y Datos",
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
                text="Exporta, importa o borra tu historial de cargas",
                font_style="Caption",
                theme_text_color="Custom",
                text_color=colors.TEXT_SLATE_400,
                size_hint_y=None,
                height=dp(16),
            )
        )
        self.column.add_widget(header)

        # --- Respaldo de datos ---
        backup_card = _section_card(
            "Respaldo de Datos",
            "Exporta tus cargas registradas para no perderlas al cambiar de celular.",
        )
        btn_row = MDBoxLayout(size_hint_y=None, height=dp(44), spacing=dp(10))
        export_json_btn = MDRaisedButton(
            text="Exportar JSON",
            icon="download",
            font_size="12sp",
            md_bg_color=colors.BORDER_800,
            theme_text_color="Custom",
            text_color=colors.TEXT_SLATE_300,
        )
        export_json_btn.bind(on_release=lambda *_: self.app.export_json())
        export_csv_btn = MDRaisedButton(
            text="Exportar CSV",
            icon="file-table-outline",
            font_size="12sp",
            md_bg_color=colors.BORDER_800,
            theme_text_color="Custom",
            text_color=colors.TEXT_SLATE_300,
        )
        export_csv_btn.bind(on_release=lambda *_: self.app.export_csv())
        btn_row.add_widget(export_json_btn)
        btn_row.add_widget(export_csv_btn)
        backup_card.add_widget(btn_row)

        import_btn = MDFlatButton(
            text="Importar copia de seguridad (JSON)",
            icon="file-upload-outline",
            font_size="12sp",
            theme_text_color="Custom",
            text_color=colors.INDIGO_400,
        )
        import_btn.bind(on_release=lambda *_: self.app.open_import_file_manager())
        backup_card.add_widget(import_btn)
        self.column.add_widget(backup_card)

        # --- Info de almacenamiento ---
        info_card = _section_card(
            "Ubicacion de los Respaldos",
            "Los archivos exportados se guardan dentro de la carpeta de datos de la "
            "app (carpeta 'exports'). Desde ahi podes compartirlos o copiarlos a tu PC.",
        )
        self.column.add_widget(info_card)

        # --- Zona de peligro ---
        danger_card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(130),
            md_bg_color=colors.BG_900,
            line_color=(0.95, 0.27, 0.34, 0.3),
            radius=[16, 16, 16, 16],
        )
        danger_card.add_widget(
            MDLabel(
                text="Zona de Peligro",
                bold=True,
                font_style="Subtitle1",
                theme_text_color="Custom",
                text_color=colors.ROSE_400,
                size_hint_y=None,
                height=dp(24),
            )
        )
        lbl = MDLabel(
            text="Borra todo el historial de cargas guardado en el celular.",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=colors.TEXT_SLATE_400,
            size_hint_y=None,
            height=dp(18),
        )
        danger_card.add_widget(lbl)
        clear_btn = MDRaisedButton(
            text="Borrar Todos los Datos",
            md_bg_color=colors.ROSE_500_SOFT,
            theme_text_color="Custom",
            text_color=colors.ROSE_400,
            size_hint_x=1,
        )
        clear_btn.bind(on_release=lambda *_: self.app.confirm_clear_all_data())
        danger_card.add_widget(clear_btn)
        self.column.add_widget(danger_card)
