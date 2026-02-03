import json
import os
from datetime import datetime

DATA_FILE = "data.json"


def load_notes():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_notes(notes):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


catatan = load_notes()


def tambah_catatan():
    tanggal = input("Tanggal (YYYY-MM-DD) [kosong untuk hari ini]: ").strip()
    if not tanggal:
        tanggal = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
        except ValueError:
            print("Format tanggal salah. Gunakan YYYY-MM-DD.")
            return

    durasi = input("Durasi (menit): ").strip()
    try:
        durasi_menit = int(durasi)
        if durasi_menit < 0:
            raise ValueError
    except Exception:
        print("Durasi harus berupa angka menit (contoh: 60).")
        return

    deskripsi = input("Deskripsi: ").strip()
    note = {
        "tanggal": tanggal,
        "durasi_menit": durasi_menit,
        "deskripsi": deskripsi,
        "created_at": datetime.now().isoformat(),
    }
    catatan.append(note)
    save_notes(catatan)
    print("Catatan berhasil ditambahkan.")


def lihat_catatan():
    if not catatan:
        print("Belum ada catatan.")
        input("Tekan Enter untuk kembali ke menu utama...")
        return

    print("\nDaftar catatan:")
    for i, n in enumerate(catatan, 1):
        h = n.get("durasi_menit", 0) // 60
        m = n.get("durasi_menit", 0) % 60
        dur = f"{h}j {m}m" if h else f"{m}m"
        print(f"{i}. {n.get('tanggal')} — {dur} — {n.get('deskripsi')}")

    input("\nTekan Enter untuk kembali ke menu utama...")


def total_waktu():
    total = sum(n.get("durasi_menit", 0) for n in catatan)
    h = total // 60
    m = total % 60
    print(f"Total waktu belajar: {h} jam {m} menit ({total} menit)")
    input("Tekan Enter untuk kembali ke menu utama...")


def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Total waktu belajar")
    print("4. Keluar")


if __name__ == "__main__":
    while True:
        menu()
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_catatan()
        elif pilihan == "2":
            lihat_catatan()
        elif pilihan == "3":
            total_waktu()
        elif pilihan == "4":
            print("Terima kasih, terus semangat belajar!")
            break
        else:
            print("Pilihan tidak valid")