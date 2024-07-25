import requests
from colorama import Fore, Style, init
from datetime import datetime, timedelta
import time
import os

# Inisialisasi colorama untuk sistem operasi Windows
init()

# Header yang tetap digunakan dalam setiap permintaan HTTP
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'Referer': 'https://zavod.mdaowallet.com/',
    'Referrer-Policy': 'strict-origin-when-cross-origin'
}

def print_welcome_message():
    """Fungsi untuk mencetak pesan selamat datang."""
    print(r"""      

▒█▀▀▀█ █▀▀█ ░█▀█░ ▒█▄░▒█ 
░▀▀▀▄▄ ░░▀▄ █▄▄█▄ ▒█▒█▒█ 
▒█▄▄▄█ █▄▄█ ░░░█░ ▒█░░▀█
          """)
    print(Fore.GREEN + Style.BRIGHT + "JAVOD BOT")
    print(Fore.RED + Style.BRIGHT + "Jangan di rename la bang :)\n\n")

def fetch_data(url, telegram_init_data):
    """Fungsi untuk mengirim permintaan GET dan mengembalikan respons JSON."""
    try:
        headers['telegram-init-data'] = telegram_init_data
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError jika respons tidak berhasil
        return response.json()
    except requests.RequestException as e:
        print(Fore.RED + Style.BRIGHT + f'An error occurred: {str(e)}')
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f'Unexpected error: {str(e)}')
    return None

def fetch_user_data(telegram_init_data):
    """Fungsi untuk mengambil data pengguna dari API."""
    url = 'https://zavod-api.mdaowallet.com/user/profile'
    return fetch_data(url, telegram_init_data)

def fetch_farm_data(telegram_init_data):
    """Fungsi untuk mengambil data farm dari API."""
    url = 'https://zavod-api.mdaowallet.com/user/farm'
    return fetch_data(url, telegram_init_data)

def print_rainbow(text):
    """Fungsi untuk mencetak teks dengan gaya rainbow."""
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE]  # Daftar warna yang akan digunakan
    reset = Style.RESET_ALL  # Reset warna setelah mencetak teks

    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        print(color + char, end='')

    print(reset)  # Mengembalikan warna terminal ke default setelah mencetak

def claim_farm(last_auth_str, telegram_init_data):
    """Fungsi untuk melakukan klaim farm dengan delay 2 jam dari lastAuth."""
    url = 'https://zavod-api.mdaowallet.com/user/claim'

    while True:
        try:
            # Ambil waktu terakhir autentikasi
            last_auth = datetime.fromisoformat(last_auth_str[:-1])  # Parsing string waktu ke objek datetime

            # Tambahkan delay 2 jam dari waktu terakhir autentikasi
            delay_hours = 2
            claim_time = last_auth + timedelta(hours=delay_hours)

            # Hitung waktu tidur (delay) dalam detik
            current_time = datetime.now()
            sleep_seconds = (claim_time - current_time).total_seconds()

            # Cek apakah sudah waktunya untuk melakukan klaim
            if sleep_seconds > 0:
                print(f"Tunggu {sleep_seconds} detik sebelum melakukan klaim...")
                time.sleep(sleep_seconds)

            # Mengirim permintaan POST untuk klaim
            headers['telegram-init-data'] = telegram_init_data
            response = requests.post(url, headers=headers)

            # Memeriksa status respons
            if response.status_code == 200:
                # Tidak perlu menampilkan pesan sukses klaim di sini
                print(Fore.GREEN + Style.BRIGHT + "Klaim farm berhasil!")
                break  # Keluar dari loop setelah berhasil klaim
            else:
                print(Fore.RED + Style.BRIGHT + f'Gagal mengirim permintaan POST. Kode status: {response.status_code}')
                # Langsung menuju akun berikutnya setelah gagal klaim
                break

        except requests.RequestException as e:
            print(Fore.RED + Style.BRIGHT + f'Gagal mengirim permintaan POST: {str(e)}')
            # Langsung menuju akun berikutnya setelah gagal klaim
            break

        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f'Unexpected error: {str(e)}')
            # Langsung menuju akun berikutnya setelah gagal klaim
            break

def read_telegram_init_data(init_file):
    """Fungsi untuk membaca semua data inisialisasi dari file."""
    telegram_init_data_list = []
    try:
        with open(init_file, 'r') as file:
            for line in file:
                telegram_init_data_list.append(line.strip())
    except FileNotFoundError:
        print(Fore.RED + Style.BRIGHT + f"File '{init_file}' tidak ditemukan.")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + f"Error saat membaca file '{init_file}': {str(e)}")
    return telegram_init_data_list

def auto_upgrade(endpoint):
    """Fungsi untuk melakukan auto upgrade pada toolkit atau workbench."""
    # Define the URL based on the endpoint parameter
    if endpoint == "Toolkit":
        url = "https://zavod-api.mdaowallet.com/user/upgradeToolkit"
    elif endpoint == "Workbench":
        url = "https://zavod-api.mdaowallet.com/user/upgradeWorkbench"
    else:
        print("Invalid endpoint specified.")
        return
    
    telegram_init_data_list = read_telegram_init_data('init.txt')
    
    if telegram_init_data_list:
        for telegram_init_data in telegram_init_data_list:
            headers['telegram-init-data'] = telegram_init_data
            
            try:
                response = requests.post(url, headers=headers)
                response.raise_for_status()
                
                # Cek status respons untuk menentukan pesan yang sesuai
                if response.status_code == 200:
                    print(Fore.GREEN + f"upgrade {endpoint} successful!")
                else:
                    print(Fore.RED + f"upgrade {endpoint} failed. HTTP status: {response.status_code}")
            
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"upgrade {endpoint} failed. Duit lu kurang !!!")
            
            except Exception as e:
                print(f"Unexpected error during upgrade {endpoint} : {e}")
            
            # Add a short delay between upgrades
            time.sleep(5)  # Adjust as needed

def confirm_auto_upgrade():
    """Fungsi untuk konfirmasi pengguna sebelum melakukan auto upgrade."""
    while True:
        choice = input(Fore.BLACK + f"Apakah Anda ingin melakukan auto upgrade? (y/n): ").strip().lower()
        if choice == 'y':
            auto_upgrade("Toolkit")
            auto_upgrade("Workbench")
            break
        elif choice == 'n':
            break
        else:
            print("Pilihan tidak valid. Harap masukkan 'y' atau 'n'.")

def get_task(telegram_init_data):
    url = "https://zavod-api.mdaowallet.com/missions"
    params = {
        "offset": 0,
        "status": "ACTIVE"
    }
    headers['telegram-init-data'] = telegram_init_data
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def select_and_claim_tasks(telegram_init_data):
    tasks = get_task(telegram_init_data)
    if tasks and tasks.get("missions"):
        for task in tasks["missions"]:
            mission_id = task["id"]
            print(f"Selecting and claiming task with ID: {mission_id}")
            if task["type"] == "LINK":
                click_link_task(mission_id, telegram_init_data)
            select_task(mission_id, telegram_init_data)
            claim_task(mission_id, telegram_init_data)
    else:
        print(Fore.RED + f"Tidak ada task")

def select_task(mission_id, telegram_init_data):
    url = f"https://zavod-api.mdaowallet.com/missions/confirm/telegram/{mission_id}"
    headers['telegram-init-data'] = telegram_init_data
    
    payload = {
        "state": "COMPLETED",
        "status": "COMPLETED"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(Fore.GREEN + f"Task {mission_id} confirmed successfully.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error occurred while confirming task {mission_id}: {e}")

def click_link_task(mission_id, telegram_init_data):
    url = f"https://zavod-api.mdaowallet.com/missions/confirm/link/{mission_id}"
    headers['telegram-init-data'] = telegram_init_data
    
    payload = {
        "state": "CLICKED",
        "status": "CLICKED"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(Fore.GREEN + f"Clicked link for task {mission_id} successfully.")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error occurred while clicking link for task {mission_id}: {e}")

def claim_task(task_id, telegram_init_data):
    url = f"https://zavod-api.mdaowallet.com/missions/claim/{task_id}"
    headers['telegram-init-data'] = telegram_init_data
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            print(Fore.GREEN + f"Task {task_id} claimed successfully.")
        else:
            print(Fore.RED + f"Failed to claim task {task_id}. Status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while claiming task {task_id}: {e}")            

def clear_screen():
    """Fungsi untuk membersihkan layar konsol."""
    os.system('cls' if os.name == 'nt' else 'clear')        

def main():

    # Baca semua data inisialisasi dari init.txt
    telegram_init_data_list = read_telegram_init_data('init.txt')

    if telegram_init_data_list:
        idx = 0
        while idx < len(telegram_init_data_list):
            telegram_init_data = telegram_init_data_list[idx]

            """Fungsi utama untuk menjalankan bot."""
            print_welcome_message()

            # Konfirmasi Auto Upgrade
            confirm_auto_upgrade()

            # Konfirmasi Auto Clear Task
            clear_auto_task = input(Fore.BLACK + "Apakah Anda ingin auto clear task ? (y/n): ").strip().lower()
            if clear_auto_task == 'y':
                select_and_claim_tasks(telegram_init_data)            

            # Mengambil data pengguna dari API untuk akun tertentu
            user_data = fetch_user_data(telegram_init_data)
            if user_data:
                # Pencetakan data pengguna dengan gaya rainbow
                print_rainbow(f'\n================== Account Detail : ==================\n')
                print(Fore.YELLOW + Style.BRIGHT + f"Username   : {user_data.get('username')}")
                print(Fore.BLUE + Style.BRIGHT + f"Tokens     : {user_data.get('tokens')}")
                print(Fore.GREEN + Style.BRIGHT + f"Guild ID   : {user_data.get('guildId')}")

            else:
                print(Fore.RED + Style.BRIGHT + f'Gagal memperoleh data pengguna.')

            # Mengambil data farm dari API untuk akun tertentu
            farm_data = fetch_farm_data(telegram_init_data)
            if farm_data:
                # Pencetakan data farm dengan gaya rainbow
                print_rainbow(f'\n=================== Farm Details : ===================\n')
                print(f"Tokens per Hour   : {farm_data.get('tokensPerHour', 'Not Available')}")
                print(f"Claim Interval    : {farm_data.get('claimInterval', 'Not Available')} milliseconds")
                print(f"Toolkit Level     : {farm_data.get('toolkitLevel', 'Not Available')}")
                print(f"Workbench Level   : {farm_data.get('workbenchLevel', 'Not Available')}")
                print(f"Helmet Level      : {farm_data.get('helmetLevel', 'Not Available')}")
                print(f"Last Claim        : {farm_data.get('lastClaim', 'Not Available')}")
                print_rainbow(f'\n=================== Claim Farm ===================\n')
                # Menggunakan lastClaim sebagai last_auth_str untuk claim_farm
                last_auth_str = farm_data.get('lastClaim')
                claim_farm(last_auth_str, telegram_init_data)

                # Menampilkan pesan bahwa akun ini selesai
                print(Fore.GREEN + Style.BRIGHT + f"Akun {idx + 1} (Username: {user_data.get('username')}) selesai.")

            else:
                print(Fore.RED + Style.BRIGHT + 'Gagal memperoleh data farm.')

            # Menunggu 5 menit sebelum melanjutkan ke akun berikutnya
            if idx < len(telegram_init_data_list) - 1:
                print(f"Menunggu 5 menit sebelum melanjutkan ke akun {idx + 2}...")
                time.sleep(5)  # 300 detik = 5 menit
            else:
                print("Ini adalah akun terakhir dalam daftar. Program akan berhenti setelah klaim terakhir.")    

            # Increment index untuk mengambil akun selanjutnya di iterasi berikutnya
            idx += 1

            # Untuk membersihkan tampilan
            clear_screen()
    else:
        print(Fore.RED + Style.BRIGHT + "Tidak ada data inisialisasi yang dibaca dari 'init.txt'.")

if __name__ == "__main__":
    main()
