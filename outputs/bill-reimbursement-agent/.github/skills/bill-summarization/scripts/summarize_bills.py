#!/usr/bin/env python3
'''
Bill Summarizer - aggregates extracted bills into grouped totals.
Usage: python summarize_bills.py --input step_1_bills.json --output step_2
'''
import sys, json, argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def load_bills(p):
    return json.loads(Path(p).read_text(encoding='utf-8')).get('bills', [])


def summarize_bills(bills, group_by='vendor'):
    groups = defaultdict(
        lambda: {'bills': [], 'total': 0.0, 'tax_total': 0.0, 'count': 0})
    gt, gtax, currencies = 0.0, 0.0, set()
    for b in bills:
        if group_by == 'vendor':
            key = b.get('vendor', 'Unknown')
        elif group_by == 'month':
            ds = b.get('date_paid', '')
            try:
                key = datetime.strptime(ds, '%B %d, %Y').strftime('%Y-%m')
            except Exception:
                key = ds[:7] if len(ds) >= 7 else 'Unknown'
        else:
            key = 'All'
        total = b.get('total') or 0.0
        tax = b.get('tax_amount') or 0.0
        curr = b.get('currency', 'USD')
        groups[key]['bills'].append(b)
        groups[key]['total'] += total
        groups[key]['tax_total'] += tax
        groups[key]['count'] += 1
        groups[key]['currency'] = curr
        gt += total
        gtax += tax
        currencies.add(curr)
    sg = dict(sorted(groups.items(), key=lambda x: x[1]['total'], reverse=True))
    serialized_groups = {}
    for k, v in sg.items():
        serialized_groups[k] = {
            'count': v['count'],
            'total': round(v['total'], 2),
            'tax_total': round(v['tax_total'], 2),
            'subtotal': round(v['total'] - v['tax_total'], 2),
            'currency': v.get('currency', 'USD'),
            'bills': [{
                'filename': b.get('filename', ''),
                'date_paid': b.get('date_paid', ''),
                'payment_number': b.get('payment_number', ''),
                'total': b.get('total', 0),
                'tax_amount': b.get('tax_amount') or 0,
                'description': (
                    b.get('items', [{}])[0].get('description', '')
                    if b.get('items') else ''),
            } for b in v['bills']],
        }
    return {
        'summary_at': datetime.now().isoformat(),
        'group_by': group_by,
        'total_bills': len(bills),
        'groups': serialized_groups,
        'grand_total': round(gt, 2),
        'grand_tax': round(gtax, 2),
        'grand_subtotal': round(gt - gtax, 2),
        'currencies': list(currencies),
    }


def generate_markdown(summary):
    cur = summary.get('currencies', ['USD'])[0]
    if len(summary.get('currencies', [])) > 1:
        cur = ''
    c = cur
    lines = [
        '# Bill Reimbursement Summary',
        '',
        '**Generated:** ' + datetime.now().strftime('%B %d, %Y'),
        '**Total Bills:** ' + str(summary['total_bills']),
        '**Grouped by:** ' + summary['group_by'].title(),
        '',
        '## Summary',
        '',
        '| # | Group | Bills | Subtotal | Tax | Total |',
        '|---|-------|-------|----------|-----|-------|',
    ]
    for i, (gk, gd) in enumerate(summary['groups'].items(), 1):
        lines.append(
            '| ' + str(i) + ' | **' + gk + '** | '
            + str(gd['count']) + ' | '
            + c + '{:.2f}'.format(gd['subtotal']) + ' | '
            + c + '{:.2f}'.format(gd['tax_total']) + ' | '
            + '**' + c + '{:.2f}'.format(gd['total']) + '** |')
    lines.append(
        '| | **GRAND TOTAL** | **' + str(summary['total_bills'])
        + '** | **' + c + '{:.2f}'.format(summary['grand_subtotal'])
        + '** | **' + c + '{:.2f}'.format(summary['grand_tax'])
        + '** | **' + c + '{:.2f}'.format(summary['grand_total']) + '** |')
    lines.extend(['', '## Detailed Breakdown', ''])
    for gk, gd in summary['groups'].items():
        lines.extend([
            '### ' + gk + ' (' + str(gd['count']) + ' bills - '
            + c + '{:.2f}'.format(gd['total']) + ')',
            '',
            '| Date | Reference | Description | Amount | Tax |',
            '|------|-----------|-------------|--------|-----|',
        ])
        for b in gd['bills']:
            lines.append(
                '| ' + (b.get('date_paid', '') or '')[:12] + ' | '
                + (b.get('payment_number', '') or '')[:20] + ' | '
                + (b.get('description', '') or '')[:40] + ' | '
                + c + '{:.2f}'.format(b.get('total', 0)) + ' | '
                + c + '{:.2f}'.format(b.get('tax_amount', 0)) + ' |')
        lines.append('')
    lines.extend([
        '---', '',
        '## Email Draft for Accounts Team', '',
        '**Subject:** Reimbursement Request - '
        + str(summary['total_bills']) + ' receipts, Total: '
        + c + '{:.2f}'.format(summary['grand_total']), '',
        'Hi Accounts Team,', '',
        'Please find attached the reimbursement summary for '
        + '**' + str(summary['total_bills']) + ' bills** totaling '
        + '**' + c + '{:.2f}'.format(summary['grand_total'])
        + '** (including ' + c
        + '{:.2f}'.format(summary['grand_tax']) + ' tax).', '',
        '**Breakdown:**',
    ])
    for gk, gd in summary['groups'].items():
        lines.append('- **' + gk + '**: ' + str(gd['count'])
                     + ' bills - ' + c + '{:.2f}'.format(gd['total']))
    lines.extend([
        '',
        'The detailed breakdown and original receipts are attached.',
        'Please process this reimbursement at your earliest convenience.',
        '', 'Best regards,', '[Your Name]', '',
    ])
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description='Summarize bills')
    p.add_argument('--input', '-i', required=True,
                   help='Input JSON from extract_bills.py')
    p.add_argument('--output', '-o', required=True,
                   help='Output base path')
    p.add_argument('--group-by', default='vendor',
                   choices=['vendor', 'month'])
    args = p.parse_args()
    bills = load_bills(args.input)
    summary = summarize_bills(bills, args.group_by)
    jp = Path(args.output).with_name(
        Path(args.output).name + '_summary.json')
    jp.parent.mkdir(parents=True, exist_ok=True)
    jp.write_text(json.dumps(summary, indent=2, default=str,
                              ensure_ascii=False), encoding='utf-8')
    print('OK Summary JSON -> ' + str(jp))
    md = generate_markdown(summary)
    mp = Path(args.output).with_name(
        Path(args.output).name + '_summary.md')
    mp.write_text(md, encoding='utf-8')
    print('OK Summary MD -> ' + str(mp))
    c = summary.get('currencies', ['USD'])[0]
    print('\nTOTAL: ' + c + '{:.2f}'.format(summary['grand_total'])
          + ' | Bills: ' + str(summary['total_bills'])
          + ' | Tax: ' + c + '{:.2f}'.format(summary['grand_tax']))


if __name__ == '__main__':
    main()
