
import os

file_path = '../../config_SSH_parsing/download_config/fi_ssh_profile/qr/wgclient_10.png'

if os.path.exists(file_path):
    print("Файл существует")
else:
    print("Файл не найден")