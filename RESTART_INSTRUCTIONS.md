# PENTING: Cara Restart Aplikasi

## Masalah
Aplikasi masih menggunakan kode lama karena belum di-restart setelah perubahan.

## Solusi: Restart Aplikasi

### Langkah 1: Tutup Aplikasi
1. Klik tombol **X** di pojok kanan atas window aplikasi
2. ATAU tekan **Alt+F4** saat window aplikasi aktif
3. ATAU di terminal, tekan **Ctrl+C** untuk menghentikan

### Langkah 2: Jalankan Ulang
Di terminal PowerShell, jalankan:
```powershell
python main.py
```

### Langkah 3: Test Paste Image
1. Copy/screenshot gambar apapun (Win+Shift+S)
2. Di aplikasi, tekan **Ctrl+V**
3. Lihat di **log area** - akan muncul debug info:
   ```
   [DEBUG] Using PIL Image object
   [DEBUG] Original image mode: RGBA, size: (1920, 1080)
   [DEBUG] Converting image from RGBA to RGB...
   [DEBUG] RGBA converted to RGB with white background
   [DEBUG] Final image mode before OCR: RGB
   [DEBUG] Starting OCR with language: eng+ind
   ```
4. Klik "Extract Text" atau "Extract & Translate"

## Jika Masih Error
Jika setelah restart masih muncul error "unsupported image format", 
COPY semua text dari log area dan kirim ke saya untuk analisis lebih lanjut.

Debug info akan menunjukkan:
- Mode gambar original (RGBA, RGB, P, dll)
- Proses konversi yang terjadi
- Error detail jika ada

## Catatan
Setiap kali ada perubahan kode, aplikasi HARUS di-restart agar perubahan berlaku!
