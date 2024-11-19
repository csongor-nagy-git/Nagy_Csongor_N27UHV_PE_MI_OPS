import os
import zipfile
import kaggle
from pathlib import Path

# Kaggle dataset ID
DATASET_ID = "tanlikesmath/diabetic-retinopathy-resized"  

# OneDrive mappa elérési útja
ONEDRIVE_FOLDER = Path(r"C:\Users\Csocsesz\OneDrive - Pannon Egyetem\Adatok\DR_Detection")

def download_kaggle_dataset(dataset_id, output_folder):
    """
    Kaggle dataset letöltése és kicsomagolása
    """
    try:
        # Adatok letöltése
        print(f"Letöltés indítása: {dataset_id}")
        kaggle.api.dataset_download_files(dataset_id, path=str(output_folder), unzip=False)
        print(f"Sikeresen letöltve: {output_folder}")

        # Kitömörítés
        zip_path = output_folder / f"{dataset_id.split('/')[-1]}.zip"
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        os.remove(zip_path)  # Tömörített fájl törlése
        print("Kitömörítés kész!")
    except Exception as e:
        print(f"Hiba történt: {e}")

def main():
    # Ellenőrizd, hogy a OneDrive mappa létezik-e
    if not ONEDRIVE_FOLDER.exists():
        print(f"OneDrive mappa nem létezik: {ONEDRIVE_FOLDER}")
        return
    
    # Adatok letöltése
    download_kaggle_dataset(DATASET_ID, ONEDRIVE_FOLDER)
    print(f"Adatok sikeresen mentve ide: {ONEDRIVE_FOLDER}")

if __name__ == "__main__":
    main()
