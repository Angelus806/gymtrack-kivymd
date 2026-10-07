# GymTrack Pro — version KivyMD (Android)

Esta carpeta es la migracion de `gymtrack_pro_rutina_diario_de_cargas.html`
a una app nativa hecha con **Kivy + KivyMD**, pensada para compilarse como
APK de Android con **buildozer**, conservando toda la funcionalidad
original:

- Rutina de 5 dias (Push / Pull / Legs / Cardio / Upper) con ejercicios,
  series/reps objetivo, descanso sugerido y notas tecnicas.
- Registro diario de cargas: peso y repeticiones por serie, con calculo
  automatico de volumen por ejercicio.
- Marcado de ejercicios completados (incluye el caso especial de cardio).
- Temporizador de descanso con tarjeta flotante, +30s, boton de parar,
  **vibracion y sonido** al llegar a cero.
- Calculadora de 1RM (formula de Epley) con tabla de porcentajes de carga.
- Historial por fecha con estadisticas acumuladas (ejercicios hechos,
  volumen total).
- Exportar respaldo en JSON y CSV, importar un JSON previamente exportado,
  y borrar todo el historial.
- Boton "Video" que busca el ejercicio en YouTube.

Los datos se guardan localmente en un archivo JSON dentro de la carpeta
privada de datos de la app (equivalente nativo de `localStorage`), asi que
la app funciona **100% offline**, igual que la version web.

## Por que no te entrego directamente el .apk

Compilar un APK de Android con buildozer requiere descargar el Android
SDK, el NDK, Gradle y dependencias de Google durante el primer build. El
entorno en la nube donde arme este proyecto tiene bloqueado el acceso a
esos servidores (`dl.google.com`, `services.gradle.org`, etc.) por
politica de seguridad del sandbox, asi que no pude generar el .apk desde
aca directamente. Intente conectar tu cuenta de GitHub a esta sesion para
hacerlo de forma automatica compilando en la nube de GitHub (que si tiene
acceso a esos servidores), pero el permiso que me dio esa conexion no
alcanza para crear o subir un repositorio desde el chat — asi que el
unico paso manual que te queda es subir esta carpeta a GitHub vos mismo
(2 minutos, sin instalar nada) y la compilacion corre sola. Mas abajo
tambien dejo la alternativa con WSL2 por si preferis compilar en tu
propia PC.

## Probar la app en Windows (sin compilar APK)

Util para ver la app funcionando antes de meterte con la compilacion del
APK.

```powershell
cd gymtrack_kivymd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Se abre una ventana con la app (controlable con mouse/touch si tu PC
tiene pantalla tactil). Los datos se guardan en
`%APPDATA%\gymtrackpro\gymtrackpro\gymtrack_pro_logs.json`
(la carpeta exacta depende de Kivy, se imprime en la consola al arrancar
si la buscas por "user_data_dir").

## Opcion A (recomendada): compilar en GitHub Actions — sin instalar nada

Ya te deje armado el archivo `.github/workflows/build-apk.yml` dentro del
proyecto, que le dice a GitHub que compile el APK automaticamente. Solo
necesitas una cuenta de GitHub (gratis) y subir la carpeta.

### 1. Crear el repositorio

1. Entra a [github.com/new](https://github.com/new) (con tu usuario
   `Angelus806`).
2. Nombre del repositorio: `gymtrack-kivymd` (o el que quieras).
3. Dejalo **Public** (o Private, cualquiera sirve) y no marques ninguna
   opcion de inicializar con README/licencia.
4. Click en "Create repository".

### 2. Subir la carpeta (sin git, directo desde el navegador)

1. En la pagina del repo recien creado, click en el link **"uploading an
   existing file"**.
2. Arrastra **todo el contenido** de la carpeta `gymtrack_kivymd` (los
   archivos y carpetas de adentro: `main.py`, `buildozer.spec`,
   `.github`, `screens`, `assets`, etc. — no la carpeta contenedora en
   si).
   - Importante: la carpeta `.github` a veces el explorador de Windows la
     esconde por ser "oculta". Si al arrastrar no ves que se suba
     `.github/workflows/build-apk.yml`, arrastra esa carpeta aparte, o
     usa `git` (ver nota abajo) para no perderte ese archivo: es el que
     le dice a GitHub que compile el APK.
3. Click en "Commit changes" (abajo de la pagina).

   *Nota: si GitHub no te deja subir la carpeta `.github` por el
   explorador web, instala [GitHub Desktop](https://desktop.github.com/)
   (con interfaz grafica, sin comandos) y usa "Add local repository" +
   "Publish repository" apuntando a la carpeta `gymtrack_kivymd` — eso sí
   sube todo, incluidas las carpetas ocultas.*

### 3. Ver la compilacion y descargar el APK

1. Andá a la pestaña **"Actions"** del repositorio (arriba).
2. Deberia aparecer un workflow "Build Android APK" corriendo solo
   (si no aparecio, click en "Build Android APK" a la izquierda y despues
   en "Run workflow").
3. Esperá entre 15 y 25 minutos (la primera vez descarga el Android
   SDK/NDK completo). Vas a ver un circulo amarillo girando mientras
   corre, y un tilde verde cuando termina.
4. Click en el run terminado, bajá hasta "Artifacts", y descargá
   **`gymtrackpro-apk`** (es un .zip que contiene el .apk adentro).
5. Descomprimi ese .zip: ahi esta tu archivo **.apk unico**, listo para
   pasar al celular e instalar.

Si el paso de compilación falla con un error que menciona
`chown: invalid user`, es un bug conocido de la Action que uso — abrí
`.github/workflows/build-apk.yml`, comentá la línea
`uses: ArtemSBulgakov/buildozer-action@v1` y descomentá la línea de abajo
que dice `n8marti/buildozer-action@fix-user-doesnt-exist`, subí ese
cambio, y volvé a correr el workflow.

### 4. Instalar el APK en tu celular

Pasa el archivo `.apk` a tu telefono (por Drive, WhatsApp Web, cable, lo
que te resulte mas comodo) y abrilo desde el explorador de archivos del
celular. Android va a pedir permiso para "instalar apps de origen
desconocido" la primera vez — aceptalo solo para este archivo.

## Opcion B: compilar vos mismo en tu PC con WSL2

Si preferis no usar GitHub, o queres poder iterar y recompilar mas
rapido en tu propia maquina, esta es la alternativa local. Buildozer
**no corre en Windows nativo**, necesita Linux — la forma mas simple sin
salir de tu PC es usar WSL2 (Windows Subsystem for Linux).

### 1. Instalar WSL2 + Ubuntu

En PowerShell como administrador:

```powershell
wsl --install -d Ubuntu
```

Reinicia si te lo pide, y completa la creacion de usuario/contrasena de
Ubuntu la primera vez que lo abras (buscalo como "Ubuntu" en el menu
inicio).

### 2. Instalar dependencias del sistema (dentro de Ubuntu/WSL)

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv \
    autoconf libtool pkg-config zlib1g-dev libncurses-dev cmake \
    libffi-dev libssl-dev build-essential ccache
```

### 3. Copiar el proyecto a tu filesystem de Linux (importante)

Buildozer es muchisimo mas rapido (y mas confiable) si el proyecto vive
dentro del filesystem de Linux, no en `/mnt/c/...`. Desde Ubuntu/WSL:

```bash
mkdir -p ~/proyectos
cp -r /mnt/c/Proyectos/gym_app/gymtrack_kivymd ~/proyectos/
cd ~/proyectos/gymtrack_kivymd
```

### 4. Crear entorno virtual e instalar buildozer

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install buildozer cython==0.29.36
```

### 5. Compilar

```bash
buildozer -v android debug
```

La **primera vez** esto va a descargar el Android SDK, NDK y otras
herramientas (varios GB), asi que puede tardar bastante segun tu
conexion (20-60+ minutos). Las siguientes compilaciones son mucho mas
rapidas porque todo queda cacheado en `~/.buildozer`.

Si te pregunta por aceptar licencias del SDK, respondé que si
(`android.accept_sdk_license = True` ya esta puesto en `buildozer.spec`
para que no te lo pregunte, pero por las dudas).

Al terminar, el APK queda en:

```
bin/gymtrackpro-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

### 6. Instalar el APK en tu celular

**Opcion A — por cable (recomendada), con el celular conectado por USB y
"Depuracion USB" activada (Ajustes > Opciones de desarrollador):**

```bash
buildozer android deploy run logcat
```

Esto instala, abre la app y te muestra el log en vivo (util si algo
falla). Si solo queres instalar sin ver el log:

```bash
adb install -r bin/gymtrackpro-*-debug.apk
```

**Opcion B — sin cable:** copia el archivo `.apk` de `bin/` a tu celular
(por ejemplo subiendolo a Drive o mandandotelo por chat) y abrilo desde
el explorador de archivos del telefono. Android va a pedir permiso para
"instalar apps de origen desconocido" la primera vez.

### Problemas comunes

- **"Aidl not found" / fallos de licencia del SDK**: corre de nuevo
  `buildozer android debug` (a veces el SDK manager necesita dos pasadas
  para terminar de aceptar licencias).
- **Falla por memoria durante el build de NDK**: si WSL2 tiene poca RAM
  asignada, crea/edita `%UserProfile%\.wslconfig` en Windows con:
  ```
  [wsl2]
  memory=6GB
  ```
  y reinicia WSL (`wsl --shutdown` desde PowerShell).
- **Build viejo con errores raros**: borra la cache con
  `buildozer android clean` y volve a compilar.
- **Querés un build de release firmado (para subir a Play Store)**: eso
  requiere generar un keystore y firmar el APK/AAB; es un paso aparte,
  avisame si llegas a necesitarlo y te paso los comandos.

## Estructura del proyecto

```
gymtrack_kivymd/
├── .github/workflows/
│   └── build-apk.yml   # Compila el APK solo en GitHub Actions (Opcion A)
├── main.py              # App principal, navegacion, timer, export/import
├── gymtrack.kv           # Layout del header y la tarjeta flotante del timer
├── data.py               # Rutina de 5 dias (igual a WORKOUT_PROGRAM del HTML)
├── storage.py             # Persistencia en JSON (equivalente a localStorage)
├── utils.py                # 1RM (Epley), vibracion, sonido, abrir YouTube
├── colors.py                # Paleta de colores (igual a la paleta Tailwind)
├── widgets.py                 # Barra de navegacion inferior (hecha a mano)
├── screens/
│   ├── workout.py              # Pestana "Rutina"
│   ├── history.py               # Pestana "Historial"
│   ├── rm.py                     # Pestana "Calc 1RM"
│   └── settings.py                # Pestana "Ajustes"
├── assets/
│   └── beep.wav                    # Sonido del timer (generado, 880Hz)
├── buildozer.spec                   # Configuracion para compilar el APK
└── requirements.txt                  # Dependencias para probar en escritorio
```

## Notas sobre la migracion

- **Almacenamiento**: `localStorage` del navegador se reemplazo por un
  archivo `gymtrack_pro_logs.json` guardado en la carpeta privada de
  datos de la app (`app.user_data_dir`). En Android eso vive dentro de
  `Android/data/org.mau.gymtrack.gymtrackpro/files/` y no requiere
  permisos especiales.
- **Exportar/Importar**: los archivos exportados (JSON/CSV) se guardan
  en una subcarpeta `exports` dentro de esa misma carpeta privada, y
  desde ahi se pueden importar de vuelta con el boton "Importar copia de
  seguridad" (abre un selector de archivos). Si queres compartir el
  archivo exportado (por WhatsApp, mail, etc.), por ahora hay que
  sacarlo manualmente con un explorador de archivos — si te sirve, puedo
  agregar despues un boton de "Compartir" nativo de Android.
- **Boton "Video"**: abre la busqueda de YouTube para el ejercicio, igual
  que en la version web.
- **Vibracion**: usa `plyer`, que en Android llama a la vibracion nativa
  del telefono. En la PC (Windows/Linux de escritorio) simplemente no
  hace nada, no es necesaria para probar la app.
- **package.domain** en `buildozer.spec` esta como `org.mau.gymtrack` —
  cambialo si queres publicarla con tu propio dominio/firma.

## Que probe antes de entregarte esto

Corri la app con renderizado real (Xvfb) dentro del entorno de nube y
verifique automaticamente: navegacion entre las 4 pestanas, calculo de
1RM con la formula de Epley, el temporizador de descanso completo (inicio
y fin de cuenta regresiva), exportacion a JSON y CSV (contenido
verificado), y el borrado de todos los datos. Tambien revise capturas de
pantalla de cada pestana para confirmar que el diseño se ve bien. Lo
unico que **no pude probar aca** es la compilacion real del APK (por el
bloqueo de red mencionado arriba, y porque el acceso que me diste a
GitHub no incluye poder crear/subir repositorios desde el chat) ni el
comportamiento en un celular Android real (vibracion, permisos de
Android, etc.) — por eso vale la pena que, despues de compilarlo con la
Opcion A o B, lo pruebes a fondo en tu telefono antes de darlo por
terminado.
