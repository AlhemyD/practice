import zipfile

def check_zip_integrity(zip_file):
    try:
        with zipfile.ZipFile(zip_file, 'r') as z:
            zip_test = z.testzip()
            if zip_test is None:
                print("Архив целостный")
            else:
                print(f"Архив поврежден: {zip_test}")
    except zipfile.BadZipFile as e:
        print(f"Ошибка при открытии архива: {e}")


zip_file = 'download_and_unzip/2024-06-16.zip'
check_zip_integrity(zip_file)
