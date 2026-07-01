#!/usr/bin/env python3
'''
Bill Summary Report Generator
Generates professional PDF reimbursement report + email draft.
Usage: python generate_bill_summary.py --input step_2_summary.json --output outputs/campaign/
'''
import sys, json, argparse
from pathlib import Path
from datetime import datetime


def load_data(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    summary = data if 'grand_total' in data else None
    bills = data.get('bills', [])
    return summary, bills


def generate_pdf_report(summary, output_path):
    try:
        from fpdf import FPDF
    except ImportError:
        raise RuntimeError('fpdf2 not installed. pip install fpdf2')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    cur = summary.get('currencies', ['USD'])[0]
    if len(summary.get('currencies', [])) > 1:
        cur = ''
    c = cur
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 12, 'Bill Reimbursement Report', ln=True, align='C')
    pdf.set_font('Helvetica', '', 10)
    now_str = datetime.now().strftime('%B %d, %Y')
    pdf.cell(0, 6, 'Generated: ' + now_str, ln=True, align='C')
    pdf.ln(8)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Summary', ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(60, 6, 'Total Bills:', ln=False)
    pdf.cell(0, 6, str(summary['total_bills']), ln=True)
    pdf.cell(60, 6, 'Grand Subtotal:', ln=False)
    pdf.cell(0, 6, c + '{:.2f}'.format(summary['grand_subtotal']), ln=True)
    pdf.cell(60, 6, 'Total Tax:', ln=False)
    pdf.cell(0, 6, c + '{:.2f}'.format(summary['grand_tax']), ln=True)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(60, 8, 'GRAND TOTAL:', ln=False)
    pdf.cell(0, 8, c + '{:.2f}'.format(summary['grand_total']), ln=True)
    pdf.ln(6)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Breakdown by ' + summary['group_by'].title(), ln=True)
    pdf.ln(2)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(230, 230, 230)
    col_w = [70, 25, 30, 30, 35]
    for header, w in zip(
        ['Vendor / Group', 'Bills', 'Subtotal', 'Tax', 'Total'], col_w):
        pdf.cell(w, 7, header, border=1, fill=True, align='C')
    pdf.ln()
    pdf.set_font('Helvetica', '', 9)
    for gk, gd in summary['groups'].items():
        pdf.cell(col_w[0], 6, gk[:28], border=1)
        pdf.cell(col_w[1], 6, str(gd['count']), border=1, align='C')
        pdf.cell(col_w[2], 6, c + '{:.2f}'.format(gd['subtotal']),
                 border=1, align='R')
        pdf.cell(col_w[3], 6, c + '{:.2f}'.format(gd['tax_total']),
                 border=1, align='R')
        pdf.cell(col_w[4], 6, c + '{:.2f}'.format(gd['total']),
                 border=1, align='R')
        pdf.ln()
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(col_w[0], 7, 'GRAND TOTAL', border=1, fill=True)
    pdf.cell(col_w[1], 7, str(summary['total_bills']),
             border=1, fill=True, align='C')
    pdf.cell(col_w[2], 7, c + '{:.2f}'.format(summary['grand_subtotal']),
             border=1, fill=True, align='R')
    pdf.cell(col_w[3], 7, c + '{:.2f}'.format(summary['grand_tax']),
             border=1, fill=True, align='R')
    pdf.cell(col_w[4], 7, c + '{:.2f}'.format(summary['grand_total']),
             border=1, fill=True, align='R')
    pdf.ln(12)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 8, 'Detailed Line Items', ln=True)
    pdf.ln(2)
    for gk, gd in summary['groups'].items():
        if pdf.get_y() > 240:
            pdf.add_page()
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(0, 7, gk + ' (' + str(gd['count']) + ' bills)', ln=True)
        pdf.set_font('Helvetica', '', 8)
        sub_w = [35, 55, 65, 35]
        for header, w in zip(
            ['Date', 'Reference', 'Description', 'Amount'], sub_w):
            pdf.cell(w, 5, header, border=1, align='C')
        pdf.ln()
        for b in gd['bills']:
            pdf.cell(sub_w[0], 5,
                     (b.get('date_paid', '') or '')[:12], border=1)
            pdf.cell(sub_w[1], 5,
                     (b.get('payment_number', '') or '')[:20], border=1)
            pdf.cell(sub_w[2], 5,
                     (b.get('description', '') or '')[:30], border=1)
            pdf.cell(sub_w[3], 5,
                     c + '{:.2f}'.format(b.get('total', 0)),
                     border=1, align='R')
            pdf.ln()
        pdf.ln(3)
    pdf.ln(6)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.cell(0, 6,
             'Auto-generated reimbursement report. Receipts attached.',
             ln=True, align='C')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    return output_path


def generate_email_body(summary):
    cur = summary.get('currencies', ['USD'])[0]
    if len(summary.get('currencies', [])) > 1:
        cur = ''
    c = cur
    lines = [
        'Subject: Reimbursement Request - '
        + str(summary['total_bills']) + ' receipts, Total: '
        + c + '{:.2f}'.format(summary['grand_total']),
        '',
        'Hi Accounts Team,',
        '',
        'I am submitting a reimbursement request for '
        + '**' + str(summary['total_bills']) + ' bills** with a grand '
        + 'total of **' + c
        + '{:.2f}'.format(summary['grand_total'])
        + '** (Subtotal: ' + c
        + '{:.2f}'.format(summary['grand_subtotal'])
        + ' + Tax: ' + c
        + '{:.2f}'.format(summary['grand_tax']) + ').',
        '',
        '**Breakdown:**',
    ]
    for gk, gd in summary['groups'].items():
        lines.append('- **' + gk + '**: ' + str(gd['count'])
                     + ' receipt(s) - ' + c
                     + '{:.2f}'.format(gd['total']))
    lines.extend([
        '',
        'The PDF summary report and all original receipts are attached '
        + 'for your reference.',
        '',
        'Please let me know if you need any additional information.',
        '',
        'Thank you!',
        '',
        'Best regards,',
        '[Your Name]',
    ])
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(
        description='Generate reimbursement PDF and email')
    p.add_argument('--input', '-i', required=True,
                   help='Input JSON (summary or bills)')
    p.add_argument('--output', '-o', required=True,
                   help='Output directory')
    p.add_argument('--email-only', action='store_true',
                   help='Only generate email, skip PDF')
    args = p.parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary, bills = load_data(input_path)
    if summary is None:
        from summarize_bills import summarize_bills
        summary = summarize_bills(bills)
    email_body = generate_email_body(summary)
    ep = output_dir / 'reimbursement_email.txt'
    ep.write_text(email_body, encoding='utf-8')
    print('OK Email -> ' + str(ep))
    if not args.email_only:
        pp = output_dir / 'reimbursement_report.pdf'
        generate_pdf_report(summary, pp)
        print('OK PDF -> ' + str(pp))
    c = summary.get('currencies', ['USD'])[0]
    print('\nREADY: ' + c + '{:.2f}'.format(summary['grand_total'])
          + ' | ' + str(summary['total_bills']) + ' bills')


if __name__ == '__main__':
    main()
