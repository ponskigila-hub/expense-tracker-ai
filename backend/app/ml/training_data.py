# Bundled training examples for the AI expense categorizer (Sprint 17).
#
# This is intentionally hand-curated rather than pulled from a real
# transaction history (there isn't one to pull from yet). As real user
# data accumulates, this is the natural place to retrain from actual
# transactions instead of these synthetic examples.

CATEGORY_EXAMPLES: list[tuple[str, str]] = [
    # --- Food ---
    ("McDonald's", "Food"),
    ("KFC dinner", "Food"),
    ("Starbucks coffee", "Food"),
    ("Kopi Kenangan", "Food"),
    ("Nasi padang Sederhana", "Food"),
    ("Warteg makan siang", "Food"),
    ("Sate ayam Pak Kumis", "Food"),
    ("Pizza Hut delivery", "Food"),
    ("Burger King", "Food"),
    ("Bakso Malang", "Food"),
    ("Es teh dan gorengan", "Food"),
    ("Chatime bubble tea", "Food"),
    ("Sushi Tei dinner", "Food"),
    ("GoFood order McD", "Food"),
    ("GrabFood ayam geprek", "Food"),
    ("Martabak manis", "Food"),
    ("Restoran Jepang Sushi", "Food"),
    ("Dapur Solo catering", "Food"),
    ("Janji Jiwa kopi susu", "Food"),
    ("Ramen Ichiran", "Food"),

    # --- Groceries ---
    ("Indomaret belanja bulanan", "Groceries"),
    ("Alfamart snack", "Groceries"),
    ("Superindo belanja sayur", "Groceries"),
    ("Hypermart groceries", "Groceries"),
    ("Pasar tradisional sayur buah", "Groceries"),
    ("Ranch Market belanja mingguan", "Groceries"),
    ("Transmart belanja bulanan", "Groceries"),
    ("Beli beras dan minyak goreng", "Groceries"),
    ("Sayurbox order sayuran", "Groceries"),
    ("HappyFresh belanja online", "Groceries"),

    # --- Transportation ---
    ("Gojek ke kantor", "Transportation"),
    ("Grab ride to airport", "Transportation"),
    ("Isi bensin Pertamax", "Transportation"),
    ("Parkir mall", "Transportation"),
    ("Tol Jagorawi", "Transportation"),
    ("MRT Jakarta top up", "Transportation"),
    ("KRL commuter line", "Transportation"),
    ("Uber ride downtown", "Transportation"),
    ("Servis motor bulanan", "Transportation"),
    ("Ganti oli mobil", "Transportation"),
    ("Ojek online ke stasiun", "Transportation"),
    ("Bayar parkir motor", "Transportation"),

    # --- Entertainment ---
    ("Steam game purchase", "Entertainment"),
    ("Tiket bioskop CGV", "Entertainment"),
    ("PlayStation Plus subscription", "Entertainment"),
    ("Konser musik tiket", "Entertainment"),
    ("Karaoke bareng teman", "Entertainment"),
    ("XXI cinema tiket weekend", "Entertainment"),
    ("Nintendo eShop game", "Entertainment"),
    ("Tiket taman hiburan Dufan", "Entertainment"),
    ("Board game cafe", "Entertainment"),
    ("Beli game di Epic Games Store", "Entertainment"),

    # --- Subscription ---
    ("Netflix monthly subscription", "Subscription"),
    ("Spotify premium", "Subscription"),
    ("Disney+ Hotstar bulanan", "Subscription"),
    ("YouTube Premium", "Subscription"),
    ("Amazon Prime subscription", "Subscription"),
    ("iCloud storage bulanan", "Subscription"),
    ("Adobe Creative Cloud", "Subscription"),
    ("ChatGPT Plus subscription", "Subscription"),
    ("Vidio Platinum bulanan", "Subscription"),
    ("Apple Music subscription", "Subscription"),

    # --- Shopping ---
    ("Belanja baju Uniqlo", "Shopping"),
    ("Sepatu Nike baru", "Shopping"),
    ("Tokopedia belanja elektronik", "Shopping"),
    ("Shopee checkout skincare", "Shopping"),
    ("Beli tas H&M", "Shopping"),
    ("Zara jaket musim dingin", "Shopping"),
    ("Beli laptop baru", "Shopping"),
    ("Handphone iPhone terbaru", "Shopping"),
    ("Aksesoris kamera", "Shopping"),
    ("Beli buku di Gramedia", "Shopping"),

    # --- Bills & Utilities ---
    ("Bayar listrik PLN", "Bills"),
    ("Tagihan air PDAM", "Bills"),
    ("Internet Indihome bulanan", "Bills"),
    ("Pulsa dan paket data", "Bills"),
    ("Tagihan kartu kredit", "Bills"),
    ("BPJS Kesehatan bulanan", "Bills"),
    ("Sewa apartemen bulanan", "Bills"),
    ("Cicilan KPR rumah", "Bills"),
    ("Bayar gas LPG", "Bills"),
    ("Tagihan telepon rumah", "Bills"),

    # --- Health ---
    ("Konsultasi dokter umum", "Health"),
    ("Beli obat di apotek", "Health"),
    ("Vitamin dan suplemen", "Health"),
    ("Medical check up tahunan", "Health"),
    ("Gym membership bulanan", "Health"),
    ("Terapi fisio", "Health"),
    ("Vaksinasi booster", "Health"),
    ("Kacamata baru optik", "Health"),
    ("Dokter gigi scaling", "Health"),
    ("Yoga class bulanan", "Health"),

    # --- Education ---
    ("Kursus online Udemy", "Education"),
    ("SPP kuliah semester", "Education"),
    ("Beli buku pelajaran", "Education"),
    ("Kelas coding bootcamp", "Education"),
    ("Kursus bahasa Inggris", "Education"),
    ("Sertifikasi AWS exam", "Education"),
    ("Webinar berbayar", "Education"),
    ("Alat tulis sekolah anak", "Education"),

    # --- Travel ---
    ("Tiket pesawat Jakarta Bali", "Travel"),
    ("Hotel booking Traveloka", "Travel"),
    ("Airbnb liburan keluarga", "Travel"),
    ("Sewa mobil liburan", "Travel"),
    ("Tiket kereta api antar kota", "Travel"),
    ("Asuransi perjalanan", "Travel"),
    ("Visa dan paspor", "Travel"),
    ("Oleh-oleh liburan", "Travel"),

    # --- Income ---
    ("Gaji bulanan kantor", "Income"),
    ("Bonus tahunan", "Income"),
    ("Transfer dari klien freelance", "Income"),
    ("Dividen saham", "Income"),
    ("Cashback e-wallet", "Income"),
    ("Hasil jual barang bekas", "Income"),
    ("Refund pembelian online", "Income"),
    ("Pendapatan sewa kos", "Income"),
]

CATEGORIES: list[str] = sorted(set(cat for _, cat in CATEGORY_EXAMPLES))
