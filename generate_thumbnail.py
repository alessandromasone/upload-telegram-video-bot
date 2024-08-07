import os
import ffmpeg
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_thumbnail_for_single_video(video_path, thumbnail_path):
    """
    Genera una miniatura per un singolo video.

    Args:
        video_path (str): Il percorso del video.
        thumbnail_path (str): Il percorso dove salvare la miniatura.
    """
    try:
        logger.info(f"Inizio elaborazione del file: {video_path}")
        
        # Ottieni informazioni sul video
        probe = ffmpeg.probe(video_path)
        duration = float(probe['format']['duration'])
        midpoint = duration / 2
        
        # Estrai il frame centrale
        (
            ffmpeg
            .input(video_path, ss=midpoint)
            .output(thumbnail_path, vframes=1)
            .run(overwrite_output=True)
        )
        
        logger.info(f"Thumbnail creata per {os.path.basename(video_path)} e salvata come {thumbnail_path}")
    except ffmpeg.Error as e:
        logger.error(f"Errore nell'elaborazione del file {os.path.basename(video_path)}: {e.stderr.decode('utf8')}")
    except Exception as e:
        logger.error(f"Errore sconosciuto nell'elaborazione del file {os.path.basename(video_path)}: {e}")

def generate_thumbnails(input_folder, output_folder):
    """
    Genera miniature per tutti i video in una cartella.

    Args:
        input_folder (str): Il percorso della cartella di input contenente i video.
        output_folder (str): Il percorso della cartella di output dove salvare le miniature.
    """
    # Crea la cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Cartella di output creata: {output_folder}")

    # Scorri tutti i file nella cartella di input
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            video_path = os.path.join(input_folder, filename)
            thumbnail_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_thumbnail.jpeg")
            logger.info(f"Elaborazione del file: {filename}")
            generate_thumbnail_for_single_video(video_path, thumbnail_path)
