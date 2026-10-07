# -*- coding: utf-8 -*-
"""Funciones utilitarias: calculo de 1RM, apertura de URLs, vibracion, sonido."""
import os
import webbrowser
from urllib.parse import quote

from kivy.utils import platform
from kivy.core.audio import SoundLoader

_beep_sound = None


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def epley_1rm(weight, reps):
    """Formula de Epley: 1RM = W * (1 + R/30)"""
    w = safe_float(weight)
    r = safe_float(reps)
    if w <= 0 or r <= 0:
        return 0.0
    return w * (1 + r / 30.0)


def percentages_table(one_rm, percents=(95, 90, 85, 80, 75, 70)):
    return {p: one_rm * (p / 100.0) for p in percents}


def youtube_search_url(exercise_name):
    query = quote(f"ejercicio {exercise_name}")
    return f"https://www.youtube.com/results?search_query={query}"


def open_url(url):
    """Abre una URL en el navegador/app correspondiente, multiplataforma."""
    if platform == "android":
        try:
            from jnius import autoclass, cast

            Intent = autoclass("android.content.Intent")
            Uri = autoclass("android.net.Uri")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            activity = cast("android.app.Activity", PythonActivity.mActivity)
            activity.startActivity(intent)
            return
        except Exception:
            pass
    try:
        webbrowser.open(url)
    except Exception:
        pass


def vibrate(pattern_ms=None):
    """Vibra el dispositivo (si es posible). pattern_ms en milisegundos."""
    try:
        from plyer import vibrator

        duration = 0.3 if not pattern_ms else sum(pattern_ms) / 1000.0
        vibrator.vibrate(duration)
    except Exception:
        pass


def play_beep():
    """Reproduce el beep del final del descanso (equivalente al osc. del HTML)."""
    global _beep_sound
    try:
        if _beep_sound is None:
            here = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(here, "assets", "beep.wav")
            _beep_sound = SoundLoader.load(sound_path)
        if _beep_sound:
            _beep_sound.stop()
            _beep_sound.play()
    except Exception:
        pass


def format_mmss(total_seconds):
    total_seconds = max(0, int(total_seconds))
    mins = total_seconds // 60
    secs = total_seconds % 60
    return f"{mins:02d}:{secs:02d}"
