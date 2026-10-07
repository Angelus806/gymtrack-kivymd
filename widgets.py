# -*- coding: utf-8 -*-
"""Barra de navegacion inferior, implementada a mano (en vez de
MDBottomNavigation) para evitar un bug de animacion de KivyMD 1.2.0 que
deja la pantalla anterior dibujada al volver a la primera pestana."""
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon, MDLabel

import colors


class NavButton(ButtonBehavior, MDBoxLayout):
    def __init__(self, name, icon, text, on_press_cb, **kwargs):
        super().__init__(orientation="vertical", padding=[0, dp(8)], **kwargs)
        self.name = name
        self._on_press_cb = on_press_cb

        self.icon_widget = MDIcon(
            icon=icon,
            halign="center",
            theme_text_color="Custom",
            text_color=colors.TEXT_SLATE_400,
            font_size="22sp",
        )
        self.label_widget = MDLabel(
            text=text,
            halign="center",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=colors.TEXT_SLATE_400,
            size_hint_y=None,
            height=dp(16),
            bold=False,
        )
        self.add_widget(self.icon_widget)
        self.add_widget(self.label_widget)

    def on_release(self):
        if self._on_press_cb:
            self._on_press_cb(self.name)

    def set_active(self, active):
        color = colors.INDIGO_400 if active else colors.TEXT_SLATE_400
        self.icon_widget.text_color = color
        self.label_widget.text_color = color
        self.label_widget.bold = active


class BottomNavBar(MDBoxLayout):
    def __init__(self, tabs, on_tab_press, **kwargs):
        """tabs: lista de tuplas (name, icon, text)."""
        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(64),
            md_bg_color=colors.BG_900,
            **kwargs,
        )
        self.buttons = {}
        self._on_tab_press = on_tab_press
        for name, icon, text in tabs:
            btn = NavButton(name, icon, text, self._handle_press)
            self.buttons[name] = btn
            self.add_widget(btn)

    def _handle_press(self, name):
        if self._on_tab_press:
            self._on_tab_press(name)

    def set_active_tab(self, name):
        for tab_name, btn in self.buttons.items():
            btn.set_active(tab_name == name)
