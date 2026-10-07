# -*- coding: utf-8 -*-
"""
Datos estaticos de la rutina de entrenamiento (GymTrack Pro).
Migrados 1:1 desde WORKOUT_PROGRAM en el archivo HTML original.
"""

WORKOUT_PROGRAM = [
    {
        "id": "day1",
        "title": "Dia 1: Empujes (Push)",
        "subtitle": "Pecho, Hombros y Triceps",
        "color": [0.23, 0.33, 0.80, 1],  # indigo/blue
        "badge": "Push",
        "exercises": [
            {"id": "d1_e1", "name": "Press Banco Inclinado", "target": "Pecho Superior", "sets": 3, "reps": "8-10", "rest": 90, "note": "Banco a 30-45 grados. Controlar la bajada."},
            {"id": "d1_e2", "name": "Press Plano", "target": "Pecho Medio/Inferior", "sets": 3, "reps": "8-10", "rest": 90, "note": "Barra o mancuernas. Escapulas retraidas."},
            {"id": "d1_e3", "name": "Press Militar", "target": "Hombro Anterior", "sets": 3, "reps": "8-10", "rest": 90, "note": "De pie o sentado. Gluteos y abdomen firmes."},
            {"id": "d1_e4", "name": "Vuelos Laterales", "target": "Hombro Lateral", "sets": 4, "reps": "12-15", "rest": 60, "note": "Polea o mancuernas. Codos sutilmente flexionados."},
            {"id": "d1_e5", "name": "Extension Triceps Polea Cuerda", "target": "Triceps (Lateral)", "sets": 3, "reps": "12-15", "rest": 60, "note": "Abrir la cuerda abajo al maximo."},
            {"id": "d1_e6", "name": "Press Frances / Fondos", "target": "Triceps (Larga)", "sets": 3, "reps": "10-12", "rest": 75, "note": "Mantener codos fijos mirando al frente."},
        ],
    },
    {
        "id": "day2",
        "title": "Dia 2: Tracciones (Pull)",
        "subtitle": "Espalda, Hombro Post. y Biceps",
        "color": [0.06, 0.47, 0.42, 1],  # emerald/teal
        "badge": "Pull",
        "exercises": [
            {"id": "d2_e1", "name": "Dominadas (o Asistidas)", "target": "Espalda Ancho", "sets": 3, "reps": "6-8 / Fallo", "rest": 120, "note": "Agarre prono. Traccionar con codos hacia abajo."},
            {"id": "d2_e2", "name": "Jalon al Pecho", "target": "Dorsal Ancho", "sets": 3, "reps": "10-12", "rest": 90, "note": "Llevar barra a la zona clavicular."},
            {"id": "d2_e3", "name": "Remo con Barra o Polea", "target": "Espalda Densidad", "sets": 3, "reps": "8-10", "rest": 90, "note": "Traccionar hacia el ombligo."},
            {"id": "d2_e4", "name": "Cruzados en Polea (Pajaros)", "target": "Hombro Posterior", "sets": 4, "reps": "12-15", "rest": 60, "note": "Polea alta cruzada manteniendo tension constante."},
            {"id": "d2_e5", "name": "Curl de Biceps Barra Z", "target": "Biceps", "sets": 3, "reps": "10-12", "rest": 75, "note": "Evitar inercia o balanceo del torso."},
            {"id": "d2_e6", "name": "Curl Martillo", "target": "Braquial y Antebrazo", "sets": 3, "reps": "10-12", "rest": 60, "note": "Mancuernas en agarre neutro."},
        ],
    },
    {
        "id": "day3",
        "title": "Dia 3: Piernas (Legs)",
        "subtitle": "Cuadriceps, Femoral, Aductor y Gemelos",
        "color": [0.78, 0.42, 0.04, 1],  # amber/orange
        "badge": "Legs",
        "exercises": [
            {"id": "d3_e1", "name": "Sentadilla Libre / Hack", "target": "Cuadriceps", "sets": 3, "reps": "8-10", "rest": 120, "note": "Bajar controlado. Mantener la espalda neutra."},
            {"id": "d3_e2", "name": "Sillon de Extensiones", "target": "Cuadriceps Aislamiento", "sets": 3, "reps": "12-15", "rest": 60, "note": "Pausa de 1s en la parte alta del movimiento."},
            {"id": "d3_e3", "name": "Peso Muerto Rumano", "target": "Isquiotibiales", "sets": 3, "reps": "8-10", "rest": 90, "note": "Llevar cadera hacia atras sintiendo estiramiento."},
            {"id": "d3_e4", "name": "Curl Femoral Acostado/Sentado", "target": "Isquiotibiales", "sets": 3, "reps": "10-12", "rest": 75, "note": "Retorno lento sin dejar caer el peso."},
            {"id": "d3_e5", "name": "Maquina Aductores", "target": "Aductores", "sets": 3, "reps": "12-15", "rest": 60, "note": "Rango amplio y controlado."},
            {"id": "d3_e6", "name": "Elevacion de Gemelos de Pie", "target": "Gemelos", "sets": 4, "reps": "12-15", "rest": 60, "note": "Pausa de 2s abajo y arriba."},
        ],
    },
    {
        "id": "day4",
        "title": "Dia 4: Cardio & Core",
        "subtitle": "Resistencia Aerobica y Abdomen",
        "color": [0.76, 0.10, 0.29, 1],  # rose/pink
        "badge": "Cardio",
        "exercises": [
            {"id": "d4_e1", "name": "Cinta (Inclinada / Trote)", "target": "Cardiovascular", "sets": 1, "reps": "20-30 min", "rest": 0, "note": "Caminata con elevacion o trote suave."},
            {"id": "d4_e2", "name": "Bici Estatica / HIIT", "target": "Cardiovascular", "sets": 1, "reps": "20 min", "rest": 0, "note": "Ritmo moderado o intervalos intensos."},
            {"id": "d4_e3", "name": "Plancha Abdominal", "target": "Core", "sets": 3, "reps": "45-60 seg", "rest": 60, "note": "Mantener cuerpo alineado y gluteos contraidos."},
            {"id": "d4_e4", "name": "Rueda Abdominal / Crunch", "target": "Abdomen Frontal", "sets": 3, "reps": "12-15", "rest": 60, "note": "Flexionar columna sin tirar del cuello."},
        ],
    },
    {
        "id": "day5",
        "title": "Dia 5: Tren Superior",
        "subtitle": "Pecho, Espalda, Hombro y Brazos",
        "color": [0.49, 0.23, 0.93, 1],  # violet/purple
        "badge": "Upper",
        "exercises": [
            {"id": "d5_e1", "name": "Press Pecho Maquina / Fondos", "target": "Pecho", "sets": 3, "reps": "10-12", "rest": 90, "note": "Mantener tension constante en el pectoral."},
            {"id": "d5_e2", "name": "Cruce de Poleas (Aperturas)", "target": "Pecho Aislamiento", "sets": 3, "reps": "12-15", "rest": 60, "note": "Juntar manos adelante apretando el pecho."},
            {"id": "d5_e3", "name": "Remo Unilateral Mancuerna", "target": "Espalda Latitud", "sets": 3, "reps": "10-12", "rest": 75, "note": "Llevar la mancuerna en direccion a la cadera."},
            {"id": "d5_e4", "name": "Pullover Polea Cuerda/Barra", "target": "Dorsal Aislamiento", "sets": 3, "reps": "12-15", "rest": 60, "note": "Mantener codos ligeramente semiflexionados."},
            {"id": "d5_e5", "name": "Vuelos Laterales Polea", "target": "Hombro Lateral", "sets": 3, "reps": "12-15", "rest": 60, "note": "Polea baja por detras o delante del cuerpo."},
            {"id": "d5_e6", "name": "Curl Inclinado / Copa Triceps", "target": "Bicep / Tricep", "sets": 3, "reps": "10-12", "rest": 75, "note": "Aislamiento de brazos."},
        ],
    },
]


def find_exercise_name(ex_id):
    """Busca el nombre de un ejercicio por su id en todo el programa."""
    for day in WORKOUT_PROGRAM:
        for ex in day["exercises"]:
            if ex["id"] == ex_id:
                return ex["name"]
    return ex_id


def get_day(day_id):
    for day in WORKOUT_PROGRAM:
        if day["id"] == day_id:
            return day
    return WORKOUT_PROGRAM[0]


def is_cardio(exercise):
    return exercise["sets"] == 1 and "min" in exercise["reps"]
