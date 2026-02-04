import json
import os
import csv
from datetime import datetime, timedelta

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
    # Meminta input mapel, topik, durasi, dan tanggal (opsional)
    mapel = input("Mapel: ").strip()
    if not mapel:
        print("Mapel tidak boleh kosong.")
        return

    topik = input("Topik: ").strip()
    if not topik:
        print("Topik tidak boleh kosong.")
        return

    durasi = input("Durasi belajar (menit): ").strip()
    try:
        durasi_menit = int(durasi)
        if durasi_menit < 0:
            raise ValueError
    except Exception:
        print("Durasi harus berupa angka menit (contoh: 60).")
        return

    tanggal = input("Tanggal (YYYY-MM-DD) [kosong untuk hari ini]: ").strip()
    if not tanggal:
        tanggal = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
        except ValueError:
            print("Format tanggal salah. Gunakan YYYY-MM-DD.")
            return

    # Struktur data sederhana: dictionary per catatan, disimpan dalam list `catatan`
    note = {
        "mapel": mapel,
        "topik": topik,
        "tanggal": tanggal,
        "durasi_menit": durasi_menit,
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

    # Tampilkan daftar catatan dalam format tabel yang rapi
    print("\n📋 Daftar Catatan Belajar")
    print("=" * 100)

    # Siapkan kolom dan lebar dinamis berdasarkan data
    jumlah = len(catatan)
    idx_w = len(str(jumlah))
    mapel_w = max((len(n.get("mapel", "")) for n in catatan), default=8)
    topik_w = max((len(n.get("topik", "")) for n in catatan), default=15)
    tanggal_w = 10

    durasi_strs = []
    for n in catatan:
        total = n.get("durasi_menit", 0)
        h = total // 60
        m = total % 60
        durasi_strs.append(f"{h}j {m}m" if h else f"{m}m")

    dur_w = max((len(s) for s in durasi_strs), default=8)

    # Header
    header = f"{'No':>{idx_w}} │ {'Mapel':<{mapel_w}} │ {'Topik':<{topik_w}} │ {'Tanggal':<{tanggal_w}} │ {'Durasi':>{dur_w}}"
    print(header)
    print("=" * 100)

    # Baris data
    for i, n in enumerate(catatan, 1):
        mapel = n.get('mapel', '')[:mapel_w]
        topik = n.get('topik', '')[:topik_w]
        tanggal = n.get('tanggal', '')
        dur = durasi_strs[i - 1]
        print(f"{i:>{idx_w}} │ {mapel:<{mapel_w}} │ {topik:<{topik_w}} │ {tanggal:<{tanggal_w}} │ {dur:>{dur_w}}")

    print("=" * 100)
    input("Tekan Enter untuk kembali ke menu utama...")


def total_waktu():
    if not catatan:
        print("Belum ada catatan.")
        input("Tekan Enter untuk kembali ke menu utama...")
        return

    total = sum(n.get("durasi_menit", 0) for n in catatan)
    h = total // 60
    m = total % 60
    print(f"Total waktu belajar: {h} jam {m} menit ({total} menit)")
    input("Tekan Enter untuk kembali ke menu utama...")


def refleksi_mingguan():
    if not catatan:
        print("Belum ada catatan belajar.")
        input("Tekan Enter untuk kembali...")
        return

    hari_ini = datetime.now().date()
    batas = hari_ini - timedelta(days=6)

    catatan_minggu = [
        n for n in catatan
        if batas <= datetime.strptime(n["tanggal"], "%Y-%m-%d").date() <= hari_ini
    ]

    if not catatan_minggu:
        print("Tidak ada catatan dalam 7 hari terakhir.")
        input("Tekan Enter untuk kembali...")
        return

    total_menit = sum(n["durasi_menit"] for n in catatan_minggu)
    hari_aktif = len(set(n["tanggal"] for n in catatan_minggu))

    mapel_count = {}
    for n in catatan_minggu:
        mapel_count[n["mapel"]] = mapel_count.get(n["mapel"], 0) + n["durasi_menit"]

    mapel_favorit = max(mapel_count, key=mapel_count.get)

    print("\n📊 Refleksi Belajar Mingguan")
    print(f"• Total belajar : {total_menit // 60} jam {total_menit % 60} menit")
    print(f"• Hari aktif   : {hari_aktif} dari 7 hari")
    print(f"• Mapel dominan: {mapel_favorit}")

    print("\n💡 Refleksi:")
    if hari_aktif >= 5:
        print("Keren! Kamu sudah konsisten belajar 👏")
    elif hari_aktif >= 3:
        print("Lumayan, tapi masih bisa lebih konsisten 💪")
    else:
        print("Yuk tingkatkan kebiasaan belajarmu minggu depan 🌱")

    input("\nTekan Enter untuk kembali...")


def detail_7_hari():
    """Tampilkan detail per-hari untuk 7 hari terakhir: total, sesi, dan breakdown per mapel."""
    if not catatan:
        print("Belum ada catatan.")
        input("Tekan Enter untuk kembali ke menu utama...")
        return

    today = datetime.now().date()
    start = today - timedelta(days=6)

    # Siapkan struktur data per tanggal
    days = []
    for i in range(7):
        d = start + timedelta(days=i)
        days.append(d)

    records_by_day = {d: [] for d in days}

    for n in catatan:
        try:
            t = datetime.strptime(n.get("tanggal", ""), "%Y-%m-%d").date()
        except Exception:
            continue
        if start <= t <= today:
            records_by_day.setdefault(t, []).append(n)

    print("\nDetail 7 hari terakhir:")
    for d in days:
        recs = records_by_day.get(d, [])
        if not recs:
            print(f"{d.isoformat()}: Tidak ada aktivitas.")
            continue

        total = sum(int(r.get("durasi_menit", 0)) for r in recs)
        sesi = len(recs)
        h = total // 60
        m = total % 60

        # Breakdown per mapel
        per_mapel = {}
        for r in recs:
            mapel = r.get("mapel", "(Tanpa mapel)")
            per_mapel[mapel] = per_mapel.get(mapel, 0) + int(r.get("durasi_menit", 0))

        print(f"{d.isoformat()}: {h} jam {m} menit — {sesi} sesi")
        for mp, dur in per_mapel.items():
            hh = dur // 60
            mm = dur % 60
            dur_str = f"{hh}j {mm}m" if hh else f"{mm}m"
            print(f"  - {mp}: {dur_str}")

    input("\nTekan Enter untuk kembali ke menu utama...")


def filter_mapel():
    nama = input("Masukkan nama mapel: ").strip()
    hasil = [n for n in catatan if n["mapel"].lower() == nama.lower()]

    if not hasil:
        print("Tidak ada catatan untuk mapel tersebut.")
        input("Tekan Enter...")
        return

    print(f"\nCatatan untuk mapel: {nama}")
    for i, n in enumerate(hasil, 1):
        print(f"{i}. {n['tanggal']} | {n['topik']} | {n['durasi_menit']} menit")

    input("Tekan Enter...")


def target_harian():
    try:
        target = int(input("Masukkan target belajar harian (menit): "))
    except ValueError:
        print("Harus angka.")
        return

    hari_ini = datetime.now().strftime("%Y-%m-%d")
    total = sum(n["durasi_menit"] for n in catatan if n["tanggal"] == hari_ini)

    print(f"\nTarget hari ini : {target} menit")
    print(f"Belajar hari ini: {total} menit")

    if total >= target:
        print("🎉 Target tercapai! Keren!")
    else:
        print(f"💪 Kurang {target - total} menit lagi")

    input("Tekan Enter...")


def simpan_ke_file():
    """Simpan catatan ke file CSV dengan format rapi."""
    if not catatan:
        print("Belum ada data untuk disimpan.")
        input("Tekan Enter...")
        return

    nama_file = "study_log.csv"

    try:
        with open(nama_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tanggal", "Mapel", "Topik", "Durasi (menit)"])
            for n in catatan:
                writer.writerow([
                    n["tanggal"],
                    n["mapel"],
                    n["topik"],
                    n["durasi_menit"]
                ])

        # Tampilkan tabel saat disimpan
        print(f"\n✅ Data berhasil disimpan ke file '{nama_file}'")
        print("📂 File bisa dibuka dengan Excel atau Google Sheets\n")
        print("📋 Tabel Data yang Disimpan:")
        print("=" * 80)

        # Header tabel
        header = f"{'Tanggal':<12} │ {'Mapel':<15} │ {'Topik':<20} │ {'Durasi':<12}"
        print(header)
        print("=" * 80)

        # Baris data
        for n in catatan:
            tanggal = n["tanggal"]
            mapel = n["mapel"][:15]
            topik = n["topik"][:20]
            durasi = f"{n['durasi_menit']} menit"
            print(f"{tanggal:<12} │ {mapel:<15} │ {topik:<20} │ {durasi:<12}")

        print("=" * 80)

    except Exception as e:
        print(f"❌ Gagal menyimpan: {e}")

    input("\nTekan Enter untuk kembali...")


def menu_utama():
    print("\n=== Study Log App ===")
    print("📚 Fitur Utama")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Total waktu belajar")
    print("\n⭐ Pengembangan Diri")
    print("4. Refleksi mingguan (Mapel favorit)")
    print("5. Filter catatan per mapel")
    print("6. Target harian")
    print("7. Simpan ke file")
    print("\n0. Keluar")


def pengembangan_diri():
    """Submenu Pengembangan Diri."""
    while True:
        print("\n⭐ Menu Pengembangan Diri")
        print("1. Refleksi mingguan (Mapel favorit)")
        print("2. Filter catatan per mapel")
        print("3. Target harian")
        print("4. Simpan ke file")
        print("0. Kembali ke menu utama")
        pilihan = input("Pilih: ").strip()

        if pilihan == "1":
            refleksi_mingguan()
        elif pilihan == "2":
            filter_mapel()
        elif pilihan == "3":
            target_harian()
        elif pilihan == "4":
            simpan_ke_file()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")


def menu():
    print("\n=== Study Log App ===")
    print("1. Tambah catatan belajar")
    print("2. Lihat catatan belajar")
    print("3. Total waktu belajar")
    print("4. Pengembangan Diri ⭐")
    print("5. Keluar")


if __name__ == "__main__":
    while True:
        menu()
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            tambah_catatan()

        elif pilihan == "2":
            lihat_catatan()

        elif pilihan == "3":
            total_waktu()

        elif pilihan == "4":
            pengembangan_diri()

        elif pilihan == "5":
            print("Terima kasih, terus semangat belajar! 🌟")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")