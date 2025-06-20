import socket
import ipaddress
import concurrent.futures
import psutil
import time
import platform

# Hanya Windows: Cek status service
def check_service_status(service_name="Spooler"):
    if platform.system() == "Windows":
        try:
            import wmi
            c = wmi.WMI()
            for service in c.Win32_Service(Name=service_name):
                print(f"Service '{service_name}': {service.State}")
        except ImportError:
            print("Modul wmi belum diinstal. Jalankan: pip install wmi")
    else:
        print("Fitur ini hanya berjalan di Windows.")

# 1. Network Scanner
def scan(ip):
    try:
        socket.gethostbyaddr(str(ip))
        return str(ip)
    except:
        return None

def network_scanner(network_range="192.168.1.0/24"):
    print("Memindai jaringan...")
    live_hosts = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(scan, ipaddress.IPv4Network(network_range))

        for result in results:
            if result:
                live_hosts.append(result)

    print("Host aktif:")
    for host in live_hosts:
        print(f"- {host}")

# 2. Uptime Komputer
def show_uptime():
    boot_time = psutil.boot_time()
    up_time = time.time() - boot_time
    jam = int(up_time // 3600)
    menit = int((up_time % 3600) // 60)
    print(f"Uptime: {jam} jam {menit} menit")

# 3. Proses Aktif
def show_running_processes():
    print("Proses yang sedang berjalan:")
    for proc in psutil.process_iter(['pid', 'name']):
        print(f"{proc.info['pid']:>6} - {proc.info['name']}")

# 4. Notifikasi Desktop
def send_notification(title, message):
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )
    except ImportError:
        print("Modul plyer belum diinstal. Jalankan: pip install plyer")

# 5. Menu Utama
def main():
    while True:
        print("\n=== Menu Monitoring Sistem ===")
        print("1. Scan Jaringan Lokal")
        print("2. Tampilkan Uptime")
        print("3. Tampilkan Proses Berjalan")
        print("4. Cek Status Service (khusus Windows)")
        print("5. Kirim Notifikasi Desktop")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-5): ")

        if pilihan == "1":
            network_scanner()
        elif pilihan == "2":
            show_uptime()
        elif pilihan == "3":
            show_running_processes()
        elif pilihan == "4":
            nama_service = input("Masukkan nama service: ")
            check_service_status(nama_service)
        elif pilihan == "5":
            send_notification("Status Sistem", "Sistem berjalan norpmal.")
        elif pilihan == "0":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()