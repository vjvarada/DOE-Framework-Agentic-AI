#!/usr/bin/env python3
"""
Indian Legal Document Generator

Generates legal document templates, clauses, notices, and policies
compliant with Indian law. Outputs Markdown for easy editing.

Usage:
    python legal_doc_generator.py --mode template --type offer_letter --company "Acme Pvt Ltd" --state Maharashtra --output .tmp/offer_letter.md
    python legal_doc_generator.py --mode clause --type non_compete --context "IT services" --output .tmp/clause.md
    python legal_doc_generator.py --mode notice --type termination --company "Acme Pvt Ltd" --output .tmp/notice.md
    python legal_doc_generator.py --mode policy --type posh_policy --company "Acme Pvt Ltd" --output .tmp/posh_policy.md
    python legal_doc_generator.py --list-templates
"""

import os
import sys
import json
import argparse
from datetime import datetime, date
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ─── Template Database ──────────────────────────────────────────────────────

TEMPLATES = {
    # ── Employment Documents ──────────────────────────────────────────────
    "offer_letter": {
        "name": "Offer Letter / Appointment Letter",
        "category": "Employment",
        "description": "Standard offer/appointment letter for new employees",
        "applicable_acts": ["Indian Contract Act, 1872", "Shops & Establishments Act (state-specific)"],
        "template": """# OFFER OF EMPLOYMENT

**{company_name}**
{company_address}

**Date:** {date}

**To:**
{employee_name}
{employee_address}

**Subject:** Offer of Employment — {designation}

Dear {employee_name},

We are pleased to offer you the position of **{designation}** at **{company_name}** on the following terms and conditions:

## 1. Position & Department
- **Designation:** {designation}
- **Department:** {department}
- **Reporting To:** {reporting_manager}
- **Location:** {work_location}

## 2. Date of Joining
Your employment will commence on **{joining_date}**. Please report to {work_location} at {reporting_time}.

## 3. Compensation
| Component | Monthly (₹) | Annual (₹) |
|-----------|-------------|------------|
| Basic Salary | {basic_monthly} | {basic_annual} |
| House Rent Allowance | {hra_monthly} | {hra_annual} |
| Special Allowance | {special_monthly} | {special_annual} |
| **Total CTC** | **{ctc_monthly}** | **{ctc_annual}** |

*Statutory deductions (EPF, ESI, Professional Tax, TDS) will apply as per applicable laws.*

## 4. Probation Period
You will be on probation for a period of **{probation_months} months** from the date of joining. During probation, either party may terminate employment with **{probation_notice_days} days** written notice. Upon successful completion, your employment will be confirmed in writing.

## 5. Working Hours & Leave
- **Working Hours:** {working_hours} (as per {state} Shops and Establishments Act)
- **Weekly Off:** {weekly_off}
- **Leave Entitlement:** As per company leave policy and applicable statutory provisions
  - Earned Leave: {earned_leave} days/year
  - Casual Leave: {casual_leave} days/year
  - Sick Leave: {sick_leave} days/year
  - Public Holidays: As declared by company

## 6. Notice Period
After confirmation, either party must provide **{notice_period_days} days** written notice or salary in lieu thereof to terminate employment.

## 7. Confidentiality
You shall maintain strict confidentiality of all proprietary information, trade secrets, business strategies, client data, and other confidential information of the Company, both during and after your employment.

## 8. Intellectual Property
All work product, inventions, designs, software, and creative works developed during the course of your employment shall be the exclusive property of the Company as per the Copyright Act, 1957 and Patents Act, 1970.

## 9. Code of Conduct
You are expected to comply with the Company's policies including but not limited to:
- Code of Conduct and Ethics
- Anti-Harassment Policy (as per POSH Act, 2013)
- IT and Data Security Policy
- Leave and Attendance Policy

## 10. Governing Law
This offer letter shall be governed by and construed in accordance with the laws of India, and courts in {state} shall have exclusive jurisdiction.

## 11. Terms of Acceptance
Please sign and return a copy of this letter within **{acceptance_days} days** as confirmation of your acceptance.

This offer is contingent upon:
- Satisfactory background verification
- Submission of required documents (ID proof, address proof, educational certificates, relieving letter from previous employer)
- Medical fitness (if applicable)

---

**For {company_name}**

Authorized Signatory: ___________________________
Name: {authorized_signatory}
Designation: {signatory_designation}
Date: {date}

---

**ACCEPTANCE**

I, {employee_name}, hereby accept the offer of employment on the terms and conditions stated above.

Signature: ___________________________
Date: _______________

---

*This is a template. Please review with your legal counsel before use.*
*Applicable Laws: Indian Contract Act, 1872; {state} Shops and Establishments Act; Payment of Wages Act; Minimum Wages Act*
"""
    },

    "nda": {
        "name": "Non-Disclosure Agreement (NDA)",
        "category": "Employment / Commercial",
        "description": "Mutual or one-way NDA for protecting confidential information",
        "applicable_acts": ["Indian Contract Act, 1872", "IT Act, 2000", "DPDP Act, 2023"],
        "template": """# NON-DISCLOSURE AGREEMENT

**This Non-Disclosure Agreement** ("Agreement") is entered into on **{date}** ("Effective Date")

**BETWEEN:**

**{party_a_name}**, a company incorporated under the Companies Act, 2013, having its registered office at {party_a_address} (hereinafter referred to as the **"Disclosing Party"**)

**AND**

**{party_b_name}**, {party_b_description}, having address at {party_b_address} (hereinafter referred to as the **"Receiving Party"**)

*(The Disclosing Party and Receiving Party are individually referred to as "Party" and collectively as "Parties")*

## RECITALS

WHEREAS, the Disclosing Party possesses certain confidential and proprietary information relating to {purpose_description};

WHEREAS, the Receiving Party desires to receive such information for the purpose of {purpose} ("Purpose");

NOW, THEREFORE, in consideration of the mutual covenants contained herein, the Parties agree as follows:

## 1. DEFINITION OF CONFIDENTIAL INFORMATION

1.1 "Confidential Information" shall mean all information disclosed by the Disclosing Party to the Receiving Party, whether orally, in writing, electronically, or by any other means, including but not limited to:
   - Business plans, strategies, and financial information
   - Technical data, trade secrets, know-how, and inventions
   - Customer lists, vendor information, and pricing data
   - Software, source code, algorithms, and databases
   - Marketing plans and business development strategies
   - Employee information and organizational structures
   - Any information marked or identified as "Confidential"

1.2 Confidential Information shall NOT include information that:
   (a) Is or becomes publicly available without breach of this Agreement;
   (b) Was known to the Receiving Party prior to disclosure;
   (c) Is independently developed by the Receiving Party without use of Confidential Information;
   (d) Is received from a third party without restrictions on disclosure;
   (e) Is required to be disclosed by law, regulation, or court order (with prior written notice to Disclosing Party).

## 2. OBLIGATIONS OF RECEIVING PARTY

2.1 The Receiving Party shall:
   (a) Hold Confidential Information in strict confidence;
   (b) Not disclose Confidential Information to any third party without prior written consent;
   (c) Use Confidential Information solely for the Purpose;
   (d) Limit access to those employees/agents who have a need-to-know and are bound by similar confidentiality obligations;
   (e) Implement reasonable security measures no less protective than those used for its own confidential information, and in no event less than reasonable care.

2.2 The Receiving Party shall implement adequate technical and organizational security measures in compliance with the Information Technology Act, 2000 and the Digital Personal Data Protection Act, 2023 (where applicable) to protect Confidential Information.

## 3. TERM AND TERMINATION

3.1 This Agreement shall remain in effect for a period of **{term_years} year(s)** from the Effective Date.

3.2 The confidentiality obligations shall survive termination for a period of **{survival_years} year(s)**.

3.3 Upon termination or request, the Receiving Party shall promptly return or destroy all Confidential Information and certify such destruction in writing.

## 4. INTELLECTUAL PROPERTY

4.1 No license, right, or interest in any intellectual property is granted under this Agreement.

4.2 All Confidential Information remains the property of the Disclosing Party.

## 5. REMEDIES

5.1 The Receiving Party acknowledges that breach may cause irreparable harm for which monetary damages may be inadequate.

5.2 The Disclosing Party shall be entitled to seek injunctive relief under the Specific Relief Act, 1963 in addition to any other remedies available at law.

## 6. GENERAL PROVISIONS

6.1 **Governing Law:** This Agreement shall be governed by and construed in accordance with the laws of India.

6.2 **Jurisdiction:** The courts of {jurisdiction_city}, India shall have exclusive jurisdiction.

6.3 **Dispute Resolution:** Any disputes arising out of this Agreement shall first be attempted to be resolved through mediation. If unresolved within 30 days, the dispute shall be referred to arbitration under the Arbitration and Conciliation Act, 1996, with the seat of arbitration in {jurisdiction_city}.

6.4 **No Assignment:** Neither Party may assign this Agreement without the prior written consent of the other Party.

6.5 **Entire Agreement:** This Agreement constitutes the entire understanding between the Parties regarding confidentiality and supersedes all prior communications.

6.6 **Amendment:** No amendment shall be effective unless in writing and signed by both Parties.

6.7 **Severability:** If any provision is held invalid, the remaining provisions shall remain in full force.

6.8 **Stamp Duty:** The stamp duty on this Agreement, if any, shall be borne by {stamp_duty_bearer} as per the Indian Stamp Act, 1899 / {state} Stamp Act.

---

**IN WITNESS WHEREOF**, the Parties have executed this Agreement as of the Effective Date.

**{party_a_name}**
Authorized Signatory: ___________________________
Name: {party_a_signatory}
Designation: {party_a_signatory_designation}
Date: {date}

**{party_b_name}**
Authorized Signatory: ___________________________
Name: {party_b_signatory}
Designation: {party_b_signatory_designation}
Date: {date}

---

*This is a template. Please review with your legal counsel before use.*
*Stamp duty requirements vary by state — verify applicable rates.*
"""
    },

    "board_resolution": {
        "name": "Board Resolution",
        "category": "Company Law",
        "description": "Template for common board resolutions",
        "applicable_acts": ["Companies Act, 2013 — Section 179, 180"],
        "template": """# BOARD RESOLUTION

## {company_name}
### (CIN: {cin})

**Certified True Copy of the Resolution passed at the Meeting of the Board of Directors of {company_name} held on {date} at {time} at {venue}.**

---

**PRESENT:**
| S.No | Name | DIN | Designation |
|------|------|-----|-------------|
| 1 | {director_1_name} | {director_1_din} | {director_1_designation} |
| 2 | {director_2_name} | {director_2_din} | {director_2_designation} |
| 3 | {director_3_name} | {director_3_din} | {director_3_designation} |

**QUORUM:** The quorum being present, the Chairman called the meeting to order.

**IN ATTENDANCE:**
- {company_secretary_name}, Company Secretary

---

## RESOLUTION {resolution_number}

**Subject: {resolution_subject}**

**RESOLVED THAT** {resolution_text}

**FURTHER RESOLVED THAT** {further_resolution_text}

**FURTHER RESOLVED THAT** Mr./Ms. {authorized_person}, {authorized_designation}, be and is hereby authorized to do all such acts, deeds, matters and things as may be necessary, proper, or expedient to give effect to this resolution including but not limited to signing, executing, and filing all necessary documents with the Registrar of Companies / relevant authorities.

---

The resolution was passed **unanimously / by majority** (with {votes_for} votes in favor and {votes_against} against).

---

**For {company_name}**

Director: ___________________________
Name: {director_1_name}
DIN: {director_1_din}

Company Secretary: ___________________________
Name: {company_secretary_name}

Date: {date}
Place: {place}

---

*Certified to be a true copy*
*Company Secretary / Director*

*This is a template. Customize as per specific resolution requirements.*
*Relevant sections: Companies Act, 2013 — Sec 173 (meetings), Sec 179 (powers of board), Sec 180 (restrictions)*
"""
    },

    "service_agreement": {
        "name": "Service Agreement / SLA",
        "category": "Commercial Contracts",
        "description": "Template for B2B service agreements",
        "applicable_acts": ["Indian Contract Act, 1872", "IT Act, 2000", "DPDP Act, 2023"],
        "template": """# SERVICE AGREEMENT

**This Service Agreement** ("Agreement") is entered into on **{date}** ("Effective Date")

**BETWEEN:**

**{service_provider_name}**, a {provider_entity_type} incorporated/registered under the laws of India, having its registered office at {provider_address}, (PAN: {provider_pan}, GSTIN: {provider_gstin}) (hereinafter referred to as the **"Service Provider"**)

**AND**

**{client_name}**, a {client_entity_type} incorporated/registered under the laws of India, having its registered office at {client_address}, (PAN: {client_pan}, GSTIN: {client_gstin}) (hereinafter referred to as the **"Client"**)

## 1. SCOPE OF SERVICES

1.1 The Service Provider shall provide the following services to the Client:
{scope_of_services}

1.2 **Service Levels:**
| Metric | Target | Measurement Period |
|--------|--------|--------------------|
| {sla_metric_1} | {sla_target_1} | {sla_period_1} |
| {sla_metric_2} | {sla_target_2} | {sla_period_2} |

1.3 Any changes to the scope shall be mutually agreed in writing through a Change Order.

## 2. TERM

2.1 This Agreement shall commence on the Effective Date and continue for **{term_months} months** ("Initial Term").

2.2 Thereafter, it shall automatically renew for successive periods of {renewal_months} months unless either Party provides {termination_notice_days} days' written notice of non-renewal.

## 3. CONSIDERATION AND PAYMENT

3.1 The Client shall pay the Service Provider **₹{service_fee}** {payment_frequency} (plus applicable GST).

3.2 **Payment Terms:** Within **{payment_days} days** of receipt of invoice.

3.3 **Late Payment:** Interest at **{late_interest_rate}% per month** on overdue amounts (subject to maximum under applicable law).

3.4 **GST:** All amounts are exclusive of GST. The Service Provider shall raise GST-compliant tax invoices. Both parties shall comply with the CGST Act, 2017.

3.5 **TDS:** The Client shall deduct TDS at applicable rates under the Income Tax Act, 1961 and provide TDS certificates (Form 16A) within prescribed timelines.

## 4. INTELLECTUAL PROPERTY

4.1 **Pre-existing IP:** Each Party retains ownership of its pre-existing intellectual property.

4.2 **Work Product:** All deliverables created specifically for the Client under this Agreement shall be assigned to the Client upon full payment, as per the Copyright Act, 1957.

4.3 **License:** The Service Provider grants the Client a non-exclusive, perpetual license to use any tools, frameworks, or methodologies incorporated in the deliverables.

## 5. CONFIDENTIALITY

5.1 Each Party shall maintain the confidentiality of the other Party's Confidential Information.

5.2 Confidentiality obligations shall survive termination for **{confidentiality_survival_years} years**.

## 6. DATA PROTECTION

6.1 Both parties shall comply with the Digital Personal Data Protection Act, 2023 and the IT Act, 2000 regarding any personal data processed under this Agreement.

6.2 The Service Provider shall implement reasonable security practices as prescribed under Section 43A of the IT Act and the DPDP Act.

## 7. INDEMNIFICATION

7.1 Each Party shall indemnify the other against all claims, damages, and expenses arising from:
   (a) Breach of this Agreement;
   (b) Negligence or willful misconduct;
   (c) Violation of applicable laws;
   (d) Infringement of third-party intellectual property rights.

## 8. LIMITATION OF LIABILITY

8.1 Neither Party's aggregate liability shall exceed **{liability_cap_description}**.

8.2 Neither Party shall be liable for indirect, consequential, or punitive damages.

8.3 The above limitations shall not apply to breaches of confidentiality, IP infringement, or willful misconduct.

## 9. TERMINATION

9.1 Either Party may terminate this Agreement:
   (a) With {termination_notice_days} days' written notice;
   (b) Immediately, if the other Party commits a material breach not cured within 30 days of written notice;
   (c) Immediately, if the other Party becomes insolvent or enters liquidation.

9.2 Upon termination, the Service Provider shall deliver all work-in-progress and transition assistance for up to {transition_days} days.

## 10. DISPUTE RESOLUTION

10.1 The Parties shall first attempt to resolve disputes through good-faith negotiation.

10.2 If unresolved within 30 days, disputes shall be referred to arbitration under the **Arbitration and Conciliation Act, 1996**, with:
   - Seat of Arbitration: {arbitration_city}
   - Number of Arbitrators: {arbitrator_count}
   - Language: English
   - Rules: Ad-hoc / {arbitration_institution} Rules

10.3 The courts in {jurisdiction_city} shall have exclusive jurisdiction for matters not subject to arbitration.

## 11. FORCE MAJEURE

11.1 Neither Party shall be liable for delays caused by events beyond reasonable control, including natural disasters, pandemics, government orders, strikes, or war.

## 12. GENERAL PROVISIONS

12.1 **Governing Law:** Laws of India.
12.2 **Entire Agreement:** This supersedes all prior agreements on the subject.
12.3 **Amendment:** In writing, signed by both Parties.
12.4 **Severability:** Invalid provisions do not affect remaining provisions.
12.5 **No Agency:** Neither Party is an agent of the other.
12.6 **Notices:** In writing to the addresses above.
12.7 **Stamp Duty:** As per {state} Stamp Act.

---

**IN WITNESS WHEREOF**, the Parties have executed this Agreement.

**{service_provider_name}**
Authorized Signatory: ___________________________
Name: {provider_signatory}
Designation: {provider_signatory_designation}

**{client_name}**
Authorized Signatory: ___________________________
Name: {client_signatory}
Designation: {client_signatory_designation}

Date: {date}

---

*This is a template. Please review with your legal counsel before use.*
*Ensure proper stamp duty is paid as per applicable state Stamp Act.*
"""
    },

    "posh_policy": {
        "name": "POSH Policy (Prevention of Sexual Harassment)",
        "category": "HR Policy",
        "description": "Compliant POSH policy as required by the Sexual Harassment of Women at Workplace Act, 2013",
        "applicable_acts": ["Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013"],
        "template": """# POLICY ON PREVENTION OF SEXUAL HARASSMENT AT WORKPLACE

## {company_name}
**Effective Date:** {date}
**Policy Version:** 1.0

---

## 1. PURPOSE AND SCOPE

1.1 **{company_name}** ("Company") is committed to providing a safe, respectful, and harassment-free workplace for all employees, as mandated by the **Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013** ("POSH Act") and rules made thereunder.

1.2 This policy applies to:
- All employees (permanent, temporary, contractual, trainees, interns, apprentices)
- All workplaces including offices, client locations, travel, events, and virtual/remote workplaces
- All persons visiting the workplace (vendors, clients, consultants, delivery personnel)

## 2. DEFINITION OF SEXUAL HARASSMENT

2.1 As defined under Section 2(n) of the POSH Act, sexual harassment includes any unwelcome:
- Physical contact and advances
- Demand or request for sexual favours
- Making sexually coloured remarks
- Showing pornography
- Any other unwelcome physical, verbal, or non-verbal conduct of a sexual nature

2.2 The following circumstances, if connected to the above acts, also constitute sexual harassment:
- Implied or explicit promise of preferential treatment in employment
- Implied or explicit threat of detrimental treatment
- Implied or explicit threat about present or future employment status
- Interference with work or creating an intimidating/hostile work environment
- Humiliating treatment likely to affect health or safety

## 3. INTERNAL COMPLAINTS COMMITTEE (ICC)

3.1 The Company has constituted an Internal Complaints Committee (ICC) as per Section 4 of the POSH Act:

| Role | Name | Designation | Contact |
|------|------|-------------|---------|
| Presiding Officer (Senior Woman) | {icc_presiding_officer} | {icc_po_designation} | {icc_po_email} |
| Member (Employee) | {icc_member_1} | {icc_member_1_designation} | {icc_member_1_email} |
| Member (Employee) | {icc_member_2} | {icc_member_2_designation} | {icc_member_2_email} |
| External Member (NGO/Legal) | {icc_external_member} | {icc_external_designation} | {icc_external_email} |

3.2 The ICC has a minimum of 4 members with at least 50% women members.

3.3 The external member is from an NGO / association / person familiar with issues of sexual harassment.

3.4 ICC members serve for a term of **3 years** from the date of nomination.

## 4. COMPLAINT MECHANISM

4.1 **Who can file:** Any aggrieved woman (or her legal heir/representative with written consent, in case of physical/mental incapacity or death).

4.2 **How to file:** Written complaint to the ICC within **3 months** of the last incident (extendable by 3 months for cause).

4.3 **Mode:** Physical letter, email to {icc_email}, or through the Company's grievance portal.

4.4 **Third Party:** A complaint may also be made by any person who has knowledge of the incident, with the written consent of the aggrieved woman.

## 5. INQUIRY PROCESS

5.1 Upon receiving a complaint, the ICC shall:
- Send a copy to the respondent within 7 working days
- Attempt conciliation (if requested by aggrieved woman) — no monetary settlement permitted
- If conciliation fails or is not requested, commence inquiry
- Complete inquiry within **90 days**
- Provide reasoned findings to the employer within **10 days** of completion

5.2 During inquiry, the ICC may recommend:
- Transfer of aggrieved woman or respondent
- Grant leave to the aggrieved woman (up to 3 months)
- Restrain the respondent from reporting on or assessing the work of the aggrieved woman

5.3 Both parties shall be given opportunity to be heard. The inquiry shall follow principles of natural justice.

## 6. ACTION UPON FINDING

6.1 If harassment is established, the ICC shall recommend:
- Disciplinary action as per service rules (warning, censure, withholding promotion, termination)
- Deduction from salary or wages of the respondent
- Compensation to the aggrieved woman (considering mental trauma, medical expenses, career impact)

6.2 The employer shall act on ICC recommendations within **60 days**.

## 7. CONFIDENTIALITY

7.1 The identity and details of the complainant, respondent, witnesses, and inquiry proceedings shall be kept strictly confidential as per Section 16 of the POSH Act.

7.2 Violation of confidentiality shall attract a penalty of **₹5,000**.

## 8. PROTECTION AGAINST RETALIATION

8.1 No adverse action shall be taken against anyone for filing or supporting a complaint in good faith.

8.2 False or malicious complaints made with intent to defame shall attract action. However, mere inability to prove a complaint does not constitute a false complaint.

## 9. EMPLOYER'S OBLIGATIONS

9.1 The Company shall:
- Display this policy at a conspicuous place at the workplace
- Conduct awareness and sensitization workshops at least **once a year**
- Include POSH awareness in employee induction/orientation
- Provide necessary facilities to the ICC
- Assist in filing complaints with police (IPC Section 354A) if the aggrieved woman requests
- Monitor timely submission of annual report

## 10. ANNUAL REPORT

10.1 The ICC shall prepare an annual report containing:
- Number of complaints received
- Number of complaints disposed of
- Number of cases pending for more than 90 days
- Nature of action taken
- Number of awareness programs conducted

10.2 The report shall be filed with the **District Officer** by **31st January** each year (for the preceding calendar year), as per Section 21 of the POSH Act.

## 11. PENALTIES FOR NON-COMPLIANCE

11.1 As per the POSH Act:
- First offence: Fine up to **₹50,000**
- Repeat offence: **Double penalty** and/or **cancellation** of business license/registration

---

**This policy has been approved by the Board of Directors of {company_name} on {approval_date}.**

Authorized Signatory: ___________________________
Name: {authorized_signatory}
Designation: {signatory_designation}

---

*This policy template complies with the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013.*
*Review with your legal counsel. Update annually or when relevant amendments are enacted.*
"""
    },

    "termination_notice": {
        "name": "Termination / Separation Notice",
        "category": "Employment",
        "description": "Notice of termination of employment",
        "applicable_acts": ["Indian Contract Act, 1872", "Shops & Establishments Act", "Industrial Disputes Act, 1947"],
        "template": """# NOTICE OF TERMINATION OF EMPLOYMENT

**{company_name}**
{company_address}

**Date:** {date}
**Ref No:** {reference_number}

**To:**
{employee_name}
Employee ID: {employee_id}
Designation: {designation}
Department: {department}

**Subject: Termination of Employment**

Dear {employee_name},

This is to inform you that your employment with **{company_name}** shall stand terminated effective **{termination_date}** ("Last Working Day").

## Reason for Termination
{termination_reason}

## Notice Period
{notice_period_details}

## Settlement of Dues

The following shall be settled on or before **{settlement_date}**:

| Component | Amount (₹) |
|-----------|------------|
| Salary up to Last Working Day | {salary_due} |
| Leave Encashment (Earned Leave) | {leave_encashment} |
| Gratuity (if eligible under Payment of Gratuity Act, 1972) | {gratuity_amount} |
| Bonus (if applicable) | {bonus_amount} |
| Reimbursements Pending | {reimbursements} |
| **Less: Deductions** | |
| Notice Period Shortfall (if any) | ({notice_shortfall}) |
| Recovery of Advances | ({advance_recovery}) |
| **Net Payable** | **{net_payable}** |

*Statutory deductions (EPF, ESI, TDS) will apply as per law.*

## Return of Company Property

Please return the following by your Last Working Day:
- Laptop and accessories
- ID card and access cards
- Company credit/debit cards
- Documents, files, and data
- Any other company property

## Post-Employment Obligations

You are reminded of your obligations regarding:
- **Confidentiality:** As per your employment agreement, confidentiality obligations continue post-employment
- **Intellectual Property:** All work product created during employment remains Company property
- **Non-solicitation:** As per your employment agreement (if applicable)

## Experience / Relieving Letter

Upon completion of handover and clearance of all dues, a relieving letter and experience certificate shall be issued.

## Form 16 / Tax Documents

Form 16 for the relevant financial year will be issued within the statutory timeline.

---

We wish you the best in your future endeavors.

**For {company_name}**

Authorized Signatory: ___________________________
Name: {authorized_signatory}
Designation: HR Manager / Director

---

**ACKNOWLEDGMENT**

I, {employee_name}, acknowledge receipt of this notice on {acknowledgment_date}.

Signature: ___________________________
Date: _______________

---

*Ensure compliance with applicable notice period requirements under the {state} Shops and Establishments Act and/or Industrial Disputes Act, 1947.*
*For workmen under the Industrial Disputes Act: additional requirements may apply including retrenchment compensation (15 days' wages per year of service).*
"""
    },

    "privacy_policy": {
        "name": "Privacy Policy (DPDP Act Compliant)",
        "category": "Data Privacy",
        "description": "Privacy policy compliant with Digital Personal Data Protection Act, 2023",
        "applicable_acts": ["Digital Personal Data Protection Act, 2023", "IT Act, 2000 — Section 43A"],
        "template": """# PRIVACY POLICY

**{company_name}**
**Last Updated:** {date}

## 1. INTRODUCTION

{company_name} ("Company", "we", "us") is committed to protecting the privacy and personal data of individuals ("Data Principals") in compliance with the **Digital Personal Data Protection Act, 2023** ("DPDP Act"), the **Information Technology Act, 2000**, and applicable rules.

This Privacy Policy explains how we collect, use, store, and protect your personal data.

## 2. DATA FIDUCIARY INFORMATION

| Detail | Information |
|--------|------------|
| Data Fiduciary | {company_name} |
| CIN/Registration | {cin_registration} |
| Registered Address | {company_address} |
| Data Protection Officer / Contact | {dpo_name}, {dpo_email} |
| Grievance Officer | {grievance_officer_name}, {grievance_email} |

## 3. PERSONAL DATA WE COLLECT

We collect the following categories of personal data:

**3.1 Information you provide:**
- Name, email address, phone number
- Address and identification documents
- Employment-related information
- Financial information (bank details, PAN, Aadhaar — only where legally required)

**3.2 Information collected automatically:**
- Device and browser information
- IP address and location data
- Usage data and cookies

**3.3 Information from third parties:**
- Background verification partners
- Payment processors
- Government databases (as permitted by law)

## 4. PURPOSE OF PROCESSING

We process personal data for the following purposes:
{processing_purposes}

## 5. LEGAL BASIS — CONSENT

5.1 We process personal data based on your **free, specific, informed, unconditional, and unambiguous consent** as required under Section 6 of the DPDP Act.

5.2 For certain legitimate uses as specified under Section 7 of the DPDP Act, processing may occur without explicit consent (e.g., compliance with law, employment purposes, medical emergencies).

5.3 You may **withdraw consent** at any time by contacting {dpo_email}. Withdrawal does not affect the lawfulness of processing prior to withdrawal.

## 6. DATA RETENTION

6.1 Personal data is retained only for as long as necessary to fulfill the purpose for which it was collected.

6.2 Upon fulfillment of purpose or withdrawal of consent, personal data shall be erased within a reasonable period, unless retention is required by law.

## 7. YOUR RIGHTS AS DATA PRINCIPAL

Under the DPDP Act, 2023, you have the right to:
- **Access** — Obtain a summary of your personal data and processing activities
- **Correction** — Request correction of inaccurate or incomplete data
- **Erasure** — Request deletion of your personal data
- **Grievance Redressal** — File a complaint with our Grievance Officer
- **Nominate** — Nominate a person to exercise your rights in case of death or incapacity

## 8. DATA SECURITY

8.1 We implement reasonable security safeguards including encryption, access controls, and regular security assessments as required under Section 8 of the DPDP Act.

8.2 In the event of a personal data breach, we will notify the **Data Protection Board of India** and affected Data Principals as required under Section 8(6) of the DPDP Act.

## 9. CROSS-BORDER DATA TRANSFER

9.1 Personal data may be transferred outside India only to countries/territories not restricted by the Central Government under Section 16 of the DPDP Act.

## 10. CHILDREN'S DATA

10.1 We do not knowingly collect personal data of children (below 18 years) without verifiable consent from a parent or lawful guardian, as per Section 9 of the DPDP Act.

## 11. GRIEVANCE REDRESSAL

For any concerns regarding your personal data:
- **Grievance Officer:** {grievance_officer_name}
- **Email:** {grievance_email}
- **Response Time:** Within 30 days
- **Escalation:** Data Protection Board of India (if unresolved)

## 12. CHANGES TO THIS POLICY

We may update this policy periodically. Material changes will be communicated through {notification_method}.

## 13. GOVERNING LAW

This policy is governed by the laws of India. Disputes shall be subject to the jurisdiction of courts in {jurisdiction_city}.

---

**{company_name}**
Date: {date}

---

*This policy template complies with the Digital Personal Data Protection Act, 2023.*
*Note: DPDP Act rules are still being finalized — update this policy when rules are notified.*
*Review with your legal counsel before adoption.*
"""
    }
}

# Available clause types
CLAUSE_TEMPLATES = {
    "non_compete": {
        "name": "Non-Compete Clause",
        "note": "Non-compete clauses are generally UNENFORCEABLE in India (Section 27, Indian Contract Act, 1872) during employment and post-employment. Only reasonable non-solicitation clauses are enforceable.",
        "template": """## Non-Competition and Non-Solicitation Clause

### Important Legal Note
Under **Section 27 of the Indian Contract Act, 1872**, agreements in restraint of trade are void. Indian courts have consistently held that **post-employment non-compete clauses are unenforceable**. However, **non-solicitation clauses** (restricting solicitation of customers/employees) and **confidentiality obligations** during and after employment are generally upheld if reasonable.

### Recommended Clause (Enforceable)

**During Employment:**
During the term of your employment, you shall not, directly or indirectly, engage in or render services to any business that competes with the Company's business without prior written consent.

**Post-Employment — Non-Solicitation:**
For a period of **{restriction_months} months** following termination of employment, you shall not:
(a) Directly or indirectly solicit, divert, or take away any client or customer with whom you had direct dealings during the last 12 months of your employment;
(b) Directly or indirectly solicit, recruit, or hire any employee of the Company;
(c) Use or disclose any Confidential Information of the Company.

**Note:** This clause is subject to Section 27 of the Indian Contract Act, 1872. The Company acknowledges that post-employment restrictions on competing are unenforceable under Indian law.
"""
    },
    "arbitration": {
        "name": "Arbitration Clause",
        "template": """## Dispute Resolution — Arbitration Clause

Any dispute, controversy, or claim arising out of or relating to this Agreement, or the breach, termination, or invalidity thereof, shall be settled by arbitration in accordance with the **Arbitration and Conciliation Act, 1996** (as amended in 2015, 2019, and 2021).

**Arbitration Terms:**
- **Seat of Arbitration:** {arbitration_city}, India
- **Number of Arbitrators:** {arbitrator_count} (sole arbitrator / panel of three)
- **Appointing Authority:** {appointing_authority} (or as per Section 11 of the Act)
- **Language:** English / {language}
- **Rules:** Ad-hoc / {institution_rules}
- **Governing Law:** Laws of India

The arbitral award shall be final and binding on both parties. Courts in {jurisdiction_city} shall have exclusive jurisdiction for matters relating to the arbitration, including appointment of arbitrators under Section 11 and enforcement of the award under Section 36.

The arbitration proceedings and the award shall be kept confidential by both parties.

Each party shall bear its own costs unless the tribunal directs otherwise.
"""
    },
    "indemnity": {
        "name": "Indemnity Clause",
        "template": """## Indemnification

{indemnifying_party} ("Indemnifying Party") shall indemnify, defend, and hold harmless {indemnified_party} ("Indemnified Party"), its directors, officers, employees, and agents from and against all claims, damages, losses, liabilities, costs, and expenses (including reasonable attorney's fees) arising out of or relating to:

(a) Any breach of this Agreement by the Indemnifying Party;
(b) Any negligent or wrongful act or omission of the Indemnifying Party;
(c) Any violation of applicable laws by the Indemnifying Party;
(d) Any infringement of third-party intellectual property rights by the Indemnifying Party;
(e) Any personal data breach caused by the Indemnifying Party's failure to implement reasonable security measures under the IT Act, 2000 and DPDP Act, 2023.

The Indemnified Party shall:
(i) Promptly notify the Indemnifying Party of any claim;
(ii) Allow the Indemnifying Party to control the defense;
(iii) Cooperate in the defense at the Indemnifying Party's expense.
"""
    },
    "force_majeure": {
        "name": "Force Majeure Clause",
        "template": """## Force Majeure

Neither Party shall be liable for any failure or delay in performance under this Agreement due to causes beyond its reasonable control, including but not limited to:

- Natural disasters (earthquake, flood, cyclone, tsunami)
- Epidemics or pandemics
- War, terrorism, civil unrest, or armed conflict
- Government orders, sanctions, embargoes, or regulatory changes
- Strikes, lockouts, or labor disputes (not involving the affected Party's employees)
- Fire, explosion, or equipment failure
- Power failure or internet/telecommunications outage
- Any act of God

**Obligations during Force Majeure:**
(a) The affected Party shall notify the other Party within **{notice_days} days** of the occurrence;
(b) The affected Party shall use reasonable efforts to mitigate the impact;
(c) Performance obligations shall be suspended for the duration of the force majeure event;
(d) If the force majeure event continues for more than **{termination_days} days**, either Party may terminate this Agreement with written notice.

This clause shall be interpreted in accordance with Section 56 of the **Indian Contract Act, 1872** (doctrine of frustration).
"""
    },
    "data_processing": {
        "name": "Data Processing Clause (DPDP Compliant)",
        "template": """## Data Processing Terms

### Compliance with DPDP Act, 2023

Where {processor_party} ("Data Processor") processes personal data on behalf of {controller_party} ("Data Fiduciary") under this Agreement:

1. **Purpose Limitation:** The Data Processor shall process personal data only for the purposes specified in this Agreement and as instructed by the Data Fiduciary.

2. **Security Measures:** The Data Processor shall implement reasonable security safeguards to protect personal data from unauthorized access, use, disclosure, or breach, as required under **Section 8 of the DPDP Act, 2023**.

3. **Breach Notification:** In the event of a personal data breach, the Data Processor shall notify the Data Fiduciary **without unreasonable delay** (and in any event within **72 hours**) to enable the Data Fiduciary to comply with its notification obligations to the Data Protection Board of India.

4. **Sub-processing:** The Data Processor shall not engage sub-processors without prior written consent of the Data Fiduciary.

5. **Data Return/Deletion:** Upon termination or completion of processing, the Data Processor shall return or securely delete all personal data within **{deletion_days} days**.

6. **Audit Rights:** The Data Fiduciary shall have the right to audit the Data Processor's compliance with these terms.

7. **Cross-Border Transfer:** Personal data shall not be transferred to countries restricted by the Central Government under Section 16 of the DPDP Act.

8. **Indemnification:** The Data Processor shall indemnify the Data Fiduciary for any penalties, claims, or damages arising from the Data Processor's breach of this clause or the DPDP Act.
"""
    }
}


def list_templates():
    """List all available templates."""
    print(f"\n{'='*60}")
    print("AVAILABLE DOCUMENT TEMPLATES")
    print(f"{'='*60}\n")
    
    print("── Full Document Templates ──")
    for key, tmpl in TEMPLATES.items():
        print(f"  {key:25s}  {tmpl['name']}")
        print(f"  {'':25s}  Category: {tmpl['category']}")
        print(f"  {'':25s}  Acts: {', '.join(tmpl['applicable_acts'][:2])}")
        print()
    
    print("── Clause Templates ──")
    for key, clause in CLAUSE_TEMPLATES.items():
        print(f"  {key:25s}  {clause['name']}")
        if clause.get("note"):
            print(f"  {'':25s}  ⚠ {clause['note'][:80]}...")
        print()


def generate_template(template_type: str, company: str = None, state: str = None) -> dict:
    """Generate a document template with placeholder variables."""
    if template_type not in TEMPLATES:
        return {"error": f"Unknown template: {template_type}. Use --list-templates to see available options."}
    
    tmpl = TEMPLATES[template_type]
    content = tmpl["template"]
    
    # Set basic defaults
    today = date.today().strftime("%d %B %Y")
    content = content.replace("{date}", today)
    if company:
        content = content.replace("{company_name}", company)
    if state:
        content = content.replace("{state}", state)
    
    return {
        "type": template_type,
        "name": tmpl["name"],
        "category": tmpl["category"],
        "applicable_acts": tmpl["applicable_acts"],
        "content": content,
        "placeholders_remaining": sorted(set(
            p.strip("{}") for p in 
            __import__("re").findall(r'\{[a-z_]+\}', content)
        )),
        "instructions": "Fill in the remaining placeholders (shown in {curly_braces}) before use. "
                       "Have a qualified legal professional review the document.",
        "disclaimer": "This is a template for reference only and does not constitute legal advice."
    }


def generate_clause(clause_type: str, context: str = None) -> dict:
    """Generate a specific legal clause."""
    if clause_type not in CLAUSE_TEMPLATES:
        return {"error": f"Unknown clause: {clause_type}. Available: {', '.join(CLAUSE_TEMPLATES.keys())}"}
    
    clause = CLAUSE_TEMPLATES[clause_type]
    content = clause["template"]
    
    return {
        "type": clause_type,
        "name": clause["name"],
        "note": clause.get("note"),
        "content": content,
        "placeholders_remaining": sorted(set(
            p.strip("{}") for p in
            __import__("re").findall(r'\{[a-z_]+\}', content)
        )),
        "disclaimer": "This is a clause template. Review with legal counsel before incorporation."
    }


def main():
    parser = argparse.ArgumentParser(description="Indian Legal Document Generator")
    parser.add_argument("--mode", choices=["template", "clause", "notice", "policy"],
                       help="Generation mode")
    parser.add_argument("--type", help="Document/clause type (use --list-templates to see options)")
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--state", help="Indian state")
    parser.add_argument("--context", help="Additional context for clauses")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--list-templates", action="store_true", help="List all available templates")
    parser.add_argument("--copilot", action="store_true",
                       help="Copilot mode — output prompt for customization")
    
    args = parser.parse_args()
    
    if args.list_templates:
        list_templates()
        return
    
    if not args.mode or not args.type:
        parser.print_help()
        print("\nUse --list-templates to see available document types")
        return
    
    print(f"\n{'='*60}")
    print(f"LEGAL DOCUMENT GENERATOR — {args.mode.upper()}")
    print(f"{'='*60}")
    
    if args.mode in ("template", "notice", "policy"):
        result = generate_template(args.type, args.company, args.state)
    elif args.mode == "clause":
        result = generate_clause(args.type, args.context)
    
    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)
    
    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if args.output.endswith(".md"):
            # Write markdown directly
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result["content"])
            print(f"✓ Document saved to {output_path}")
        else:
            # Write JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✓ Output saved to {output_path}")
    
    if args.copilot:
        print(f"\n{'='*60}")
        print("COPILOT MODE — Customize this document:")
        print(f"{'='*60}")
        print(f"\nDocument: {result.get('name', args.type)}")
        print(f"File: {args.output}")
        print(f"\nRemaining placeholders to fill:")
        for p in result.get("placeholders_remaining", []):
            print(f"  - {{{p}}}")
        print("\nPlease help the user fill in these placeholders with their specific details.")
    else:
        print(f"\nDocument: {result.get('name', args.type)}")
        remaining = result.get("placeholders_remaining", [])
        if remaining:
            print(f"Placeholders to fill: {len(remaining)}")


if __name__ == "__main__":
    main()
