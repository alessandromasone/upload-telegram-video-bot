import os
import ffmpeg
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_file_size(file_path):
    """
    Restituisce la dimensione del file in byte.

    Args:
        file_path (str): Il percorso del file.

    Returns:
        int: Dimensione del file in byte.
    """
    return os.path.getsize(file_path)

def split_video(input_file, output_dir, max_size_gb=1.7):
    """
    Divide un video in più parti, ciascuna con una dimensione massima specificata.

    Args:
        input_file (str): Il percorso del file video di input.
        output_dir (str): Il percorso della directory di output dove salvare le parti.
        max_size_gb (float): Dimensione massima di ciascuna parte in gigabyte (default è 1.7 GB).
    """
    max_size_bytes = max_size_gb * 1024**3  # Converti GB in byte
    base_name = os.path.basename(input_file)
    base_name_without_ext = os.path.splitext(base_name)[0]
    
    # Creazione directory di output se non esiste
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Prima passata per ottenere la durata del video
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])
        avg_bitrate = float(probe['format']['bit_rate'])
        
        # Calcola la durata massima di ciascuna parte in secondi
        max_size_bits = max_size_bytes * 8  # Converti byte in bit
        max_part_duration = max_size_bits / avg_bitrate  # Durata massima di una parte in secondi
        
        logger.info(f"Durata totale del video: {duration} secondi")
        logger.info(f"Bitrate medio: {avg_bitrate} bps")
        logger.info(f"Durata massima di una parte: {max_part_duration} secondi")
        
        part_number = 0
        start_time = 0
        parts = []

        while start_time < duration:
            part_number += 1
            end_time = start_time + max_part_duration
            if end_time > duration:
                end_time = duration
            
            output_file = os.path.join(output_dir, f"{base_name_without_ext}_part{part_number}.mp4")
            
            # Usa ffmpeg per dividere il video
            (
                ffmpeg
                .input(input_file, ss=start_time, to=end_time)
                .output(output_file, c='copy')
                .run(overwrite_output=True)
            )
            
            logger.info(f"Parte {part_number} salvata come {output_file}")
            
            parts.append(output_file)
            
            start_time = end_time
        
        return parts

    except ffmpeg.Error as e:
        logger.error(f"Errore nell'elaborazione del file {input_file}: {e.stderr.decode('utf8')}")
    except Exception as e:
        logger.error(f"Errore sconosciuto nell'elaborazione del file {input_file}: {e}")

