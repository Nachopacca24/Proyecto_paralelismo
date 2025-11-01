"""
@tortolala
Pokemon image processing pipeline - versión optimizada con paralelismo y concurrencia.
"""

from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from pika_banner import print_pikachu
from tqdm import tqdm
import requests
import time
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# =========================================================
# FUNCIONES DE DESCARGA (I/O BOUND)
# =========================================================

def download_single_pokemon(i, dir_name, base_url):
    """Descarga una sola imagen de Pokémon."""
    file_name = f'{i:03d}.png'
    url = f'{base_url}/{file_name}'
    img_path = os.path.join(dir_name, file_name)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(img_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        return f'Error con {file_name}: {e}'

def download_pokemon_concurrent(n=150, dir_name='pokemon_dataset'):
    """Descarga concurrentemente las imágenes."""
    os.makedirs(dir_name, exist_ok=True)
    base_url = 'https://raw.githubusercontent.com/HybridShivam/Pokemon/master/assets/imagesHQ' 

    print(f'\nDescargando {n} pokemones concurrentemente...\n')
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_single_pokemon, i, dir_name, base_url) for i in range(1, n + 1)]
        for f in tqdm(as_completed(futures), total=n, desc='Descargando', unit='img'):
            result = f.result()
            if result is not True:
                tqdm.write(result)

    total_time = time.time() - start_time
    print(f'  Descarga completada en {total_time:.2f} segundos')
    print(f'  Promedio: {total_time/n:.2f} s/img')
    return total_time

# =========================================================
# FUNCIONES DE PROCESAMIENTO (CPU BOUND)
# =========================================================

def process_single_image(image, dir_origin, dir_name):
    """Procesa una sola imagen aplicando transformaciones."""
    try:
        path_origin = os.path.join(dir_origin, image)
        img = Image.open(path_origin).convert('RGB')

        img = img.filter(ImageFilter.GaussianBlur(radius=10))
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img_inv = ImageOps.invert(img)
        img_inv = img_inv.filter(ImageFilter.GaussianBlur(radius=5))
        width, height = img_inv.size
        img_inv = img_inv.resize((width * 2, height * 2), Image.LANCZOS)
        img_inv = img_inv.resize((width, height), Image.LANCZOS)

        saving_path = os.path.join(dir_name, image)
        img_inv.save(saving_path, quality=95)
        return True
    except Exception as e:
        return f'Error procesando {image}: {e}'

def process_pokemon_parallel(dir_origin='pokemon_dataset', dir_name='pokemon_processed'):
    """Procesa las imágenes en paralelo usando multiprocessing."""
    os.makedirs(dir_name, exist_ok=True)
    images = sorted([f for f in os.listdir(dir_origin) if f.endswith('.png')])
    total = len(images)
    
    print(f'\nProcesando {total} imágenes en paralelo...\n')
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_single_image, image, dir_origin, dir_name) for image in images]
        for f in tqdm(as_completed(futures), total=total, desc='Procesando', unit='img'):
            result = f.result()
            if result is not True:
                tqdm.write(result)

    total_time = time.time() - start_time
    print(f'  Procesamiento completado en {total_time:.2f} segundos')
    print(f'  Promedio: {total_time/total:.2f} s/img\n')
    return total_time

# =========================================================
# MAIN
# =========================================================

if __name__ == '__main__':
    print('='*60)
    print_pikachu()
    print('   POKEMON IMAGE PROCESSING PIPELINE (Optimizado)')
    print('='*60)

    # Fase 1: Descarga concurrente (I/O Bound)
    download_time = download_pokemon_concurrent()

    # Fase 2: Procesamiento paralelo (CPU Bound)
    processing_time = process_pokemon_parallel()

    # Resumen final
    total_time = download_time + processing_time

    print('='*60)
    print('RESUMEN DE TIEMPOS\n')
    print(f'  Descarga:        {download_time:.2f} seg')
    print(f'  Procesamiento:   {processing_time:.2f} seg\n')
    print(f'  Total:           {total_time:.2f} seg')
    print('='*60)
