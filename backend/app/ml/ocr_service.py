import re
from datetime import date
from io import BytesIO

import pytesseract
from PIL import Image, ImageOps
from dateutil import parser as dateutil_parser

# Indonesian month names dateutil doesn't recognize out of the box.
INDONESIAN_MONTHS = {
    "januari": "January", "februari": "February", "maret": "March",
    "april": "April", "mei": "May", "juni": "June", "juli": "July",
    "agustus": "August", "september": "September", "oktober": "October",
    "november": "November", "desember": "December",
}

TOTAL_LINE_KEYWORDS = [
    "grand total", "total bayar", "total belanja", "total harga",
    "jumlah bayar", "total", "jumlah", "amount due", "amount",
]

# Matches things like: Rp 150.000 | Rp150,000.00 | 150000 | IDR 1.234.567
AMOUNT_PATTERN = re.compile(r"(?:rp\.?|idr)?\s*([\d][\d.,]*\d|\d)", re.IGNORECASE)

DATE_HINT_PATTERN = re.compile(
    r"(\d{1,2}[\/\-\s.]\d{1,2}[\/\-\s.]\d{2,4}|"
    r"\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2}|"
    r"\d{1,2}\s+[A-Za-zÀ-ÿ]+\s+\d{2,4})"
)


def extract_text(image_bytes: bytes) -> str:
    """Run OCR on raw image bytes and return the extracted text."""

    image = Image.open(BytesIO(image_bytes))

    # Basic preprocessing: normalize to grayscale + autocontrast. This is
    # a cheap, dependency-free way to meaningfully improve OCR accuracy on
    # photographed (as opposed to scanned) receipts.
    image = ImageOps.exif_transpose(image)  # respect phone camera orientation
    image = image.convert("L")
    image = ImageOps.autocontrast(image)

    return pytesseract.image_to_string(image)


def normalize_amount(raw: str) -> float | None:
    """
    Turn a messy OCR'd number like "150.000", "150,000.00", "Rp 1.234.567",
    or "50000" into a float. Handles both Indonesian-style (.=thousands,
    ,=decimal) and US-style (,=thousands, .=decimal) formatting.
    """

    cleaned = re.sub(r"[^\d.,]", "", raw).strip(".,")

    if not cleaned:
        return None

    has_dot = "." in cleaned
    has_comma = "," in cleaned

    if has_dot and has_comma:
        # Whichever separator appears last is the decimal separator.
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")

    elif has_dot:
        # Ambiguous: "150.000" (ID thousands) vs "150.00" (decimal).
        # Heuristic: a lone "." followed by exactly 2 digits at the very
        # end is a decimal point; groups of exactly 3 digits are thousands.
        last_group = cleaned.split(".")[-1]

        if len(last_group) == 2 and cleaned.count(".") == 1:
            pass  # keep as decimal, e.g. "150.00" -> 150.00
        else:
            cleaned = cleaned.replace(".", "")

    elif has_comma:
        last_group = cleaned.split(",")[-1]

        if len(last_group) == 2 and cleaned.count(",") == 1:
            cleaned = cleaned.replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")

    try:
        return float(cleaned)
    except ValueError:
        return None


def extract_total_amount(text: str) -> float | None:

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Pass 1: look for a line containing a "total"-like keyword.
    for keyword in TOTAL_LINE_KEYWORDS:
        for line in lines:
            if keyword in line.lower():
                match = AMOUNT_PATTERN.search(line.lower().replace(keyword, ""))

                if match:
                    amount = normalize_amount(match.group(1))

                    if amount is not None and amount > 0:
                        return amount

    # Pass 2: fall back to the largest number found anywhere in the
    # receipt — on most receipts the grand total is the biggest amount.
    candidates = []

    for line in lines:
        for match in AMOUNT_PATTERN.finditer(line):
            amount = normalize_amount(match.group(1))

            if amount is not None and amount >= 100:  # filter out qty/line noise
                candidates.append(amount)

    return max(candidates) if candidates else None


ISO_DATE_PATTERN = re.compile(r"^(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})$")


def extract_date(text: str) -> date | None:

    match = DATE_HINT_PATTERN.search(text)

    if not match:
        return None

    candidate = match.group(1).strip()

    # Unambiguous ISO form (YYYY-MM-DD) — parse directly rather than
    # letting dateutil's dayfirst=True (needed for DD/MM/YYYY receipts)
    # misinterpret it.
    iso_match = ISO_DATE_PATTERN.match(candidate)

    if iso_match:
        year, month, day = (int(g) for g in iso_match.groups())

        try:
            return date(year, month, day)
        except ValueError:
            return None

    lowered = candidate.lower()

    for id_month, en_month in INDONESIAN_MONTHS.items():
        if id_month in lowered:
            candidate = re.sub(id_month, en_month, candidate, flags=re.IGNORECASE)
            break

    try:
        parsed = dateutil_parser.parse(candidate, dayfirst=True, fuzzy=True)
        return parsed.date()
    except (ValueError, OverflowError):
        return None


def extract_merchant(text: str) -> str | None:

    for line in text.splitlines():
        cleaned = line.strip()

        # Skip empty lines, pure numbers/symbols, and very short noise.
        if len(cleaned) < 3:
            continue

        if not re.search(r"[A-Za-z]{2,}", cleaned):
            continue

        return cleaned[:100]

    return None


def parse_receipt(text: str) -> dict:

    return {
        "merchant": extract_merchant(text),
        "date": extract_date(text),
        "amount": extract_total_amount(text),
    }
