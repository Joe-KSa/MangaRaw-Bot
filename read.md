# MangaRaw Bot

MangaRaw Bot es un bot de Discord diseñado para facilitar la búsqueda y lectura de mangas desde el sitio RawKuma. Este bot incluye funcionalidades para buscar mangas, mostrar las últimas actualizaciones, navegar por los capítulos y mostrar imágenes de los capítulos dentro de los hilos de Discord.

## Características

- Buscar mangas por nombre.
- Mostrar las últimas actualizaciones de mangas.
- Navegar por capítulos de manga.
- Crear hilos en Discord para mostrar imágenes de los capítulos seleccionados.

## Requisitos

- Python 3.8 o superior.
- Paquetes especificados en `requirements.txt`.

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/Joe-KSa/MangaRaw-Bot.git
    cd MangaRaw-Bot
    ```

2. Crea y activa un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

4. Configura tus variables de entorno. Crea un archivo `.env` en la carpeta `private/` con el siguiente contenido:

    ```env
    DISCORD_TOKEN=your_discord_bot_token
    DISCORD_ALLOWED_CHANNELS=channel_id1,channel_id2,channel_id3
    ```

    Reemplaza `your_discord_bot_token` con el token de tu bot de Discord y `channel_id1,channel_id2,channel_id3` con los IDs de los canales permitidos.    

## Uso

Para ejecutar el bot, simplemente ejecuta el archivo `main.py` :

    
    python main.py
    

## Comandos

- `?test`: Verifica si el bot está funcionando correctamente en los canales permitidos.
- `?latestUpdate`: Muestra las últimas actualizaciones de mangas.
- `?search [nombre del manga]`: Busca mangas por nombre.
