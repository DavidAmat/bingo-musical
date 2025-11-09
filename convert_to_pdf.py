#!/usr/bin/env python3
"""
HTML → PDF helpers.

This script tries multiple methods:
1) Google Chrome / Chromium headless
2) WeasyPrint (pip install weasyprint)
3) pdfkit + wkhtmltopdf (requires system binary)

Usage examples:
  python convert_to_pdf.py output/sheets/sheet_01.html --out output/sheets/sheet_01.pdf
  python convert_to_pdf.py output/sheets --glob "sheet_*.html" --outdir output/sheets/pdf
"""
import argparse
import shutil
import subprocess
from pathlib import Path

def try_chrome(input_html: Path, output_pdf: Path) -> bool:
    chrome = shutil.which("google-chrome") or shutil.which("chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        return False
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--print-to-pdf=" + str(output_pdf),
        "--no-margins",
        str(input_html.resolve()),
    ]
    try:
        subprocess.run(cmd, check=True)
        return output_pdf.exists() and output_pdf.stat().st_size > 0
    except Exception:
        return False

def try_weasyprint(input_html: Path, output_pdf: Path) -> bool:
    try:
        from weasyprint import HTML
    except Exception:
        return False
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    try:
        HTML(filename=str(input_html)).write_pdf(str(output_pdf))
        return output_pdf.exists() and output_pdf.stat().st_size > 0
    except Exception:
        return False

def try_pdfkit(input_html: Path, output_pdf: Path) -> bool:
    try:
        import pdfkit
    except Exception:
        return False
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    try:
        pdfkit.from_file(str(input_html), str(output_pdf))
        return output_pdf.exists() and output_pdf.stat().st_size > 0
    except Exception:
        return False

def convert_one(input_html: Path, output_pdf: Path) -> bool:
    if try_chrome(input_html, output_pdf):
        print(f"Chrome OK -> {output_pdf}")
        return True
    if try_weasyprint(input_html, output_pdf):
        print(f"WeasyPrint OK -> {output_pdf}")
        return True
    if try_pdfkit(input_html, output_pdf):
        print(f"pdfkit OK -> {output_pdf}")
        return True
    print(f"FAILED to convert {input_html}")
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="HTML file or directory")
    ap.add_argument("--out", help="Output PDF (single file mode)")
    ap.add_argument("--glob", default="*.html", help="Glob pattern when input is a directory")
    ap.add_argument("--outdir", help="Output directory when input is a directory")
    args = ap.parse_args()

    input_path = Path(args.input)
    if input_path.is_file():
        if not args.out:
            raise SystemExit("--out is required when converting a single HTML file")
        convert_one(input_path, Path(args.out))
    else:
        outdir = Path(args.outdir or (input_path / "pdf"))
        outdir.mkdir(parents=True, exist_ok=True)
        for html in sorted(input_path.glob(args.glob)):
            pdf_path = outdir / (html.stem + ".pdf")
            convert_one(html, pdf_path)

if __name__ == "__main__":
    main()
