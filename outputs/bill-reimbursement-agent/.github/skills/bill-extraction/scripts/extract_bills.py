#!/usr/bin/env python3
'''
Bill PDF Extractor - extracts structured data from PDF bills/receipts.
Uses PyMuPDF for text extraction with flexible vendor-format detection.
Usage: python extract_bills.py --input bills/ --output step_1_bills.json
'''
import sys, re, json, csv, argparse
from pathlib import Path
from datetime import datetime


def extract_text_from_pdf(pdf_path):
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = ''
        for page in doc:
            text += page.get_text('text') + '\n'
        doc.close()
        return text.strip()
    except ImportError:
        raise RuntimeError('PyMuPDF not installed. pip install pymupdf')
    except Exception as e:
        raise RuntimeError('Failed: ' + pdf_path.name + ': ' + str(e))


def parse_bill_text(text, filename):
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    data = {
        'filename': filename, 'vendor': None, 'vendor_email': None,
        'vendor_address': [], 'bill_to_name': None, 'bill_to_address': [],
        'payment_number': None, 'date_paid': None, 'payment_method': None,
        'currency': 'USD', 'items': [], 'subtotal': None, 'tax_rate': None,
        'tax_amount': None, 'tax_description': None, 'total': None,
        'amount_paid': None, 'raw_text': text,
    }
    vendor_patterns = [
        (r'^DeepSeek$', 'DeepSeek'), (r'^OpenAI', 'OpenAI'),
        (r'^Anthropic', 'Anthropic'), (r'^Google', 'Google'),
        (r'^Amazon', 'Amazon Web Services'), (r'^Microsoft', 'Microsoft'),
        (r'^GitHub', 'GitHub'),
    ]
    for i, line in enumerate(lines):
        for pat, name in vendor_patterns:
            if re.match(pat, line, re.IGNORECASE):
                data['vendor'] = name
                break
        if data['vendor']:
            break
    if not data['vendor']:
        for i, line in enumerate(lines[:10]):
            if re.search(r'(Inc\.|LLC|Ltd\.|Corp\.)', line):
                data['vendor'] = line.strip()
                break
        if not data['vendor']:
            data['vendor'] = 'Unknown Vendor'
    for line in lines:
        m = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)
        if m:
            data['vendor_email'] = m.group()
            break
    bt = False
    for line in lines:
        if 'bill to' in line.lower():
            bt = True
            continue
        if bt:
            if re.search(r'paid on|Date paid|Payment method|Description', line):
                break
            if not data['bill_to_name']:
                data['bill_to_name'] = line
            elif len(line) > 3:
                data['bill_to_address'].append(line)
    for i, line in enumerate(lines):
        if re.search(r'(Payment|Receipt|Invoice)\s*(number|#|No)',
                     line, re.IGNORECASE):
            if i + 1 < len(lines):
                data['payment_number'] = lines[i + 1].strip()
            break
    for i, line in enumerate(lines):
        if re.search(r'Date\s*paid', line, re.IGNORECASE):
            if i + 1 < len(lines):
                data['date_paid'] = lines[i + 1].strip()
            break
    for i, line in enumerate(lines):
        if re.search(r'Payment\s*method', line, re.IGNORECASE):
            if i + 1 < len(lines):
                data['payment_method'] = lines[i + 1].strip()
            break
    for line in lines:
        if '\u20b9' in line or 'INR' in line:
            data['currency'] = 'INR'
            break
        if '\u20ac' in line or 'EUR' in line:
            data['currency'] = 'EUR'
            break
    ap = re.compile(r'[\$]?([\d,]+\.?\d*)')
    for i, line in enumerate(lines):
        if re.match(r'^\s*Subtotal\s*$', line, re.IGNORECASE):
            if i + 1 < len(lines):
                m = ap.search(lines[i + 1])
                if m:
                    data['subtotal'] = float(m.group(1).replace(',', ''))
            break
    for i, line in enumerate(lines):
        if re.match(r'^\s*Total\s*$', line, re.IGNORECASE):
            if i + 1 < len(lines):
                m = ap.search(lines[i + 1])
                if m:
                    data['total'] = float(m.group(1).replace(',', ''))
            break
    tax_pat = re.compile(
        r'(VAT|GST|HST|Tax|Sales\s*Tax)[^@\d]*[@\s]*([\d.]+)\s*%',
        re.IGNORECASE)
    for i, line in enumerate(lines):
        tax = tax_pat.search(line)
        if tax:
            data['tax_description'] = line.strip()
            if tax.group(2):
                data['tax_rate'] = float(tax.group(2))
            # Tax amount is typically on the next line (DeepSeek, etc.)
            # Only try same line if it doesn't contain "on $" (base amount)
            ta = None
            if 'on $' not in line.lower():
                ta = re.search(r'[\$]?([\d,]+\.\d{2})\s*$', line)
            if not ta and i + 1 < len(lines):
                ta = re.search(r'[\$]?([\d,]+\.\d{2})', lines[i + 1])
            if ta:
                data['tax_amount'] = float(ta.group(1).replace(',', ''))
            break
    for line in lines:
        if re.search(r'Amount\s*paid', line, re.IGNORECASE):
            m = ap.search(line)
            if m:
                data['amount_paid'] = float(m.group(1).replace(',', ''))
            break
    hi = None
    for i, line in enumerate(lines):
        if re.search(r'Description.*(Quantity|Qty).*(Price|Rate).*(Tax|Amount)',
                     line, re.IGNORECASE):
            hi = i
            break
        if line.strip().lower() == 'description':
            hi = i
            break
    if hi is not None:
        for i in range(hi + 1, len(lines)):
            line = lines[i].strip()
            if re.match(r'^\s*(Subtotal|Total|Amount)', line, re.IGNORECASE):
                break
            if not line:
                break
            m = re.search(r'(.+?)\s+[\$]?([\d,]+\.?\d{0,2})\s*$', line)
            if m:
                data['items'].append({
                    'description': m.group(1).strip(),
                    'amount': float(m.group(2).replace(',', '')),
                })
    if not data['items'] and data['total']:
        data['items'].append({
            'description': data['vendor'] + ' services',
            'amount': data['total'],
        })
    for k in ['vendor_address', 'bill_to_address']:
        if k in data and not data[k]:
            del data[k]
    return data


def main():
    p = argparse.ArgumentParser(description='Extract data from PDF bills')
    p.add_argument('--input', '-i', required=True, help='Folder of PDFs')
    p.add_argument('--output', '-o', required=True, help='Output JSON path')
    p.add_argument('--csv', action='store_true', help='Also export CSV')
    args = p.parse_args()
    input_dir = Path(args.input)
    output_path = Path(args.output)
    if not input_dir.is_dir():
        print('Error: ' + str(input_dir) + ' not found')
        sys.exit(1)
    pdfs = sorted(input_dir.glob('*.pdf'))
    if not pdfs:
        print('No PDFs in ' + str(input_dir))
        sys.exit(1)
    bills, errors = [], []
    for fp in pdfs:
        try:
            text = extract_text_from_pdf(fp)
            bd = parse_bill_text(text, fp.name)
            bills.append(bd)
            v = bd.get('vendor', '?')
            cur = bd.get('currency', '$')
            t = bd.get('total', '?')
            print('  OK  ' + fp.name + ': ' + v + ' - ' + cur + str(t))
        except Exception as e:
            errors.append({'file': fp.name, 'error': str(e)})
            print('  FAIL  ' + fp.name + ': ' + str(e))
    result = {
        'extracted_at': datetime.now().isoformat(),
        'total_bills': len(bills),
        'errors': errors,
        'bills': bills,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, default=str, ensure_ascii=False),
        encoding='utf-8')
    print('\nDone: ' + str(len(bills)) + ' bills -> ' + str(output_path))
    if args.csv:
        cp = output_path.with_suffix('.csv')
        with open(cp, 'w', newline='', encoding='utf-8') as f:
            fields = ['filename', 'vendor', 'vendor_email', 'date_paid',
                      'payment_method', 'currency', 'subtotal', 'tax_rate',
                      'tax_amount', 'total', 'amount_paid', 'payment_number']
            w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            w.writeheader()
            for b in bills:
                w.writerow(b)
        print('CSV -> ' + str(cp))


if __name__ == '__main__':
    main()
