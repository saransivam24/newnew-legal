import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

TARGET_DIR = r"D:\LEGAL IQ\ready_to_upload_pdfs"
os.makedirs(TARGET_DIR, exist_ok=True)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'LegalTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    alignment=1, # Center
    textColor=colors.HexColor('#111827')
)

subtitle_style = ParagraphStyle(
    'LegalSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=14,
    alignment=1,
    textColor=colors.HexColor('#374151')
)

header_style = ParagraphStyle(
    'LegalSectionHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#1f2937'),
    spaceBefore=10,
    spaceAfter=4
)

body_style = ParagraphStyle(
    'LegalBody',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor('#1f2937'),
    spaceAfter=6
)

bold_body = ParagraphStyle(
    'LegalBoldBody',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor('#111827'),
    spaceAfter=4
)

mono_style = ParagraphStyle(
    'LegalMono',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor('#374151')
)

def build_pdf(filename, story):
    filepath = os.path.join(TARGET_DIR, filename)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=40
    )
    doc.build(story)
    print(f"Generated: {filepath} ({os.path.getsize(filepath)} bytes)")

# ================= 1. FIR_No_042_2023_Chennai_Police.pdf =================
def create_fir_pdf():
    story = []
    story.append(Paragraph("TAMIL NADU POLICE DEPARTMENT", subtitle_style))
    story.append(Paragraph("FIRST INFORMATION REPORT (CRIME RECORD DOSSIER)", title_style))
    story.append(Paragraph("(Under Section 154 of Code of Criminal Procedure, 1973)", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#111827'), spaceBefore=2, spaceAfter=8))

    meta_data = [
        [Paragraph("<b>District:</b> Chennai City", body_style), Paragraph("<b>Police Station:</b> Anna Nagar (K-4)", body_style)],
        [Paragraph("<b>FIR Number:</b> 042 / 2023", body_style), Paragraph("<b>Date & Time:</b> 14-Aug-2023, 11:30 hrs", body_style)],
        [Paragraph("<b>Acts & Sections:</b> IPC Sections 420 & 406", body_style), Paragraph("<b>Investigating Officer:</b> SI K. Velmurugan", body_style)]
    ]
    t = Table(meta_data, colWidths=[260, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#d1d5db')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. PARTICULARS OF COMPLAINANT", header_style))
    story.append(Paragraph("<b>Name:</b> Shri M. Sundaram (Age 48 years), S/o K. Muthusamy.<br/>"
                           "<b>Designation:</b> Managing Director, Sri Balaji Garments Pvt Ltd.<br/>"
                           "<b>Registered Office:</b> Corporate Tower, 5th Main Road, Anna Nagar West, Chennai - 600040.<br/>"
                           "<b>Contact:</b> +91 98401-22910 | Corporate Bank: HDFC Bank, Anna Nagar Branch.", body_style))

    story.append(Paragraph("2. PARTICULARS OF ACCUSED / SUSPECT", header_style))
    story.append(Paragraph("<b>Name:</b> Rajesh Kumar (Age 44 years), S/o Late S. Ramanathan.<br/>"
                           "<b>Enterprise:</b> Proprietor, Precision Machines India (Est. 2012).<br/>"
                           "<b>Address:</b> Plot No. 14, 2nd Avenue, Anna Nagar, Chennai - 600040.<br/>"
                           "<b>Bankers:</b> Precision Machines India A/C with HDFC Bank and ICICI Bank.", body_style))

    story.append(Paragraph("3. SUBSTANCE OF INFORMATION & OCCURRENCE", header_style))
    story.append(Paragraph("On 12-June-2023, the Complainant entered into a commercial agreement with the Accused for the supply and installation of two high-speed German automated industrial textile printing units for a total contract value of <b>Rs. 25,00,000/-</b>.<br/><br/>"
                           "Pursuant to contractual terms, the Complainant disbursed an advance payment of <b>Rs. 15,00,000/- (Rupees Fifteen Lakhs only)</b> via RTGS on 15-June-2023 from HDFC Bank to the Accused's account. Delivery was assured within 30 days (on or before 15-July-2023).<br/><br/>"
                           "The Accused failed to deliver the machinery. During a dispute meeting on 10-August-2023 at 10:30 AM at the Corporate Office, the Accused issued ICICI Bank Cheque No. 892110 for <b>Rs. 5,00,000/-</b> as interim refund. The said cheque was presented and returned dishonoured on 12-August-2023 with the endorsement <b>'Insufficient Funds'</b>.", body_style))

    story.append(Paragraph("4. STATUTORY CLASSIFICATION OF CHARGES", header_style))
    story.append(Paragraph("• <b>IPC Section 420:</b> Cheating and dishonestly inducing delivery of property (cognizable, bailable/non-bailable as per schedule, triable by Magistrate).<br/>"
                           "• <b>IPC Section 406:</b> Criminal breach of trust (maximum punishment 3 years imprisonment or fine).", body_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph("Verified by: Sub-Inspector K. Velmurugan, Station House Officer, Anna Nagar (K-4) PS", mono_style))
    build_pdf("FIR_No_042_2023_Chennai_Police.pdf", story)

# ================= 2. Witness_Statement_Senior_Accountant_Suresh.pdf =================
def create_witness_pdf():
    story = []
    story.append(Paragraph("TAMIL NADU POLICE - INVESTIGATION BRANCH", subtitle_style))
    story.append(Paragraph("WITNESS DEPOSITION UNDER SECTION 161 Cr.P.C.", title_style))
    story.append(Paragraph("CRIME NO. 42/2023 | ANNA NAGAR (K-4) POLICE STATION", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#111827'), spaceBefore=4, spaceAfter=10))

    story.append(Paragraph("<b>Deponent:</b> Suresh Natarajan, S/o V. Natarajan, Age: 42 Years<br/>"
                           "<b>Occupation:</b> Senior Accountant, Sri Balaji Garments Pvt Ltd (Employee ID: BG-408)<br/>"
                           "<b>Date of Recording:</b> 17-August-2023 | <b>Investigating Officer:</b> SI K. Velmurugan", body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("SWORN TESTIMONY & FINANCIAL AUDIT FINDINGS:", header_style))
    story.append(Paragraph("1. I have been serving as the Senior Accountant at Sri Balaji Garments Pvt Ltd for over 6 years and oversee procurement records, bank reconciliation, and vendor payments.<br/><br/>"
                           "2. I confirm that on 15-June-2023, our MD Shri M. Sundaram remitted an advance payment of <b>Rs. 15,00,000/-</b> via RTGS to Precision Machines India.", body_style))

    story.append(Paragraph("EXCULPATORY FINANCIAL EVIDENCE (OVERSEAS WIRE):", header_style))
    story.append(Paragraph("3. On 24-June-2023, Rajesh Kumar provided our accounts department with verified documentary proof of procurement: He had remitted <b>USD 16,500 (approx. Rs. 13,65,000/-)</b> on 22-June-2023 via Outward Telegraphic Transfer (TT Reference: HDFC-SW-99210) to <b>Heidelberg Tech GMBH</b>, Stuttgart, Germany for the precision printing assemblies.<br/><br/>"
                           "4. The consignment landed at Chennai Port on 28-July-2023 aboard vessel <i>MV Northern Star</i> under Bill of Lading No. MSC-DE-77821. However, the Customs Commissionerate detained the cargo under revised automated bill-of-entry semiconductor inspection scrutiny. This was a bona fide customs delay and not fraudulent diversion.", body_style))

    story.append(Paragraph("MATERIAL CONTRADICTION ON DISPUTE MEETING:", header_style))
    story.append(Paragraph("5. <b>Contradiction:</b> In the complaint, MD Sundaram stated that the dispute meeting occurred on 10-August-2023 at 10:30 AM at our Corporate Office.<br/>"
                           "<b>Actual Fact:</b> The meeting took place on <b>10-August-2023 at 03:00 PM (15:00 hrs) inside our Factory Premises</b>, not at 10:30 AM. Rajesh Kumar presented the German bills of lading and tendered the Rs. 5,00,000 ICICI cheque as interim goodwill security.", body_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph("Deposition recorded accurately. Read over and confirmed. Signature: Suresh Natarajan (Deponent)", mono_style))
    build_pdf("Witness_Statement_Senior_Accountant_Suresh.pdf", story)

# ================= 3. Accused_Dossier_and_SCRB_Verification.pdf =================
def create_accused_dossier_pdf():
    story = []
    story.append(Paragraph("STATE CRIME RECORDS BUREAU (SCRB) - TAMIL NADU", subtitle_style))
    story.append(Paragraph("ANTECEDENTS VERIFICATION & BACKGROUND DOSSIER", title_style))
    story.append(Paragraph("REFERENCE NO: SCRB/TN/CR-2023-88219 | CRIME NO. 42/2023", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#111827'), spaceBefore=4, spaceAfter=10))

    story.append(Paragraph("1. PERSONAL & SOCIAL ROOTS IN SOCIETY", header_style))
    story.append(Paragraph("<b>Name:</b> Rajesh Kumar<br/>"
                           "<b>Father's Name:</b> Late S. Ramanathan<br/>"
                           "<b>Age:</b> 44 Years | <b>Education:</b> B.E. (Mechanical Engineering, Anna University)<br/>"
                           "<b>Permanent Residence:</b> Plot No. 14, 2nd Avenue, Anna Nagar, Chennai - 600040.<br/>"
                           "<b>Family Composition:</b> Residing with wife Smt. Kavitha Kumar (M.Sc., High School Teacher) and two minor school-going children (Ages 12 and 8). Permanent resident of Anna Nagar for over 18 years.", body_style))

    story.append(Paragraph("2. OFFICIAL CRIMINAL RECORD VERIFICATION (SCRB CLEARANCE)", header_style))
    story.append(Paragraph("A biometric and database background search conducted across the Tamil Nadu Police Inter-operable Criminal Justice System (ICJS) and CCTNS reveals:<br/>"
                           "• <b>Prior FIRs:</b> NIL (ZERO)<br/>"
                           "• <b>Pending Criminal Cases / Trials:</b> NIL (ZERO)<br/>"
                           "• <b>Previous Convictions:</b> NIL (ZERO)<br/>"
                           "• <b>Gang Affiliations / Anti-social Register:</b> CLEAN RECORD", body_style))

    story.append(Paragraph("3. FLIGHT RISK & INVESTIGATION COOPERATION MATRIX", header_style))
    story.append(Paragraph("• <b>Travel Documents:</b> The Accused has voluntarily surrendered his Indian Passport (No. Z-4829101) to the Investigating Officer.<br/>"
                           "• <b>Section 41A CrPC Compliance:</b> Accused responded immediately to police notice and produced business bank passbooks.<br/>"
                           "• <b>Commercial Standing:</b> Precision Machines India has operated since 2012 with an annual turnover exceeding Rs. 2 Crores, employing 14 local technicians.", body_style))

    story.append(Spacer(1, 15))
    story.append(Paragraph("Official Police Record Certified: K-4 Police Station & SCRB Chennai", mono_style))
    build_pdf("Accused_Dossier_and_SCRB_Verification.pdf", story)

# ================= 4. Bail_Application_Petition_CrPC_437.pdf =================
def create_bail_petition_pdf():
    story = []
    story.append(Paragraph("IN THE COURT OF THE PRINCIPAL SESSIONS JUDGE AT CHENNAI", subtitle_style))
    story.append(Paragraph("CRIMINAL MISCELLANEOUS PETITION NO. ______ / 2023", title_style))
    story.append(Paragraph("IN CRIME NO. 42 OF 2023 OF ANNA NAGAR (K-4) POLICE STATION", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#111827'), spaceBefore=4, spaceAfter=10))

    story.append(Paragraph("<b>Rajesh Kumar</b>, S/o Late S. Ramanathan, Age: 44 Years,<br/>"
                           "Proprietor of Precision Machines India, No. 14, 2nd Avenue, Anna Nagar, Chennai.<br/>"
                           "<b>... Petitioner / Accused</b>", bold_body))
    story.append(Paragraph("<br/><b>VERSUS</b><br/>", subtitle_style))
    story.append(Paragraph("<b>State represented by the Inspector of Police</b>,<br/>"
                           "Anna Nagar (K-4) Police Station, Chennai City.<br/>"
                           "<b>... Respondent / Complainant State</b>", bold_body))
    story.append(Spacer(1, 8))

    story.append(Paragraph("APPLICATION FOR REGULAR BAIL UNDER SECTION 437 Cr.P.C. / SECTION 480 BNSS", header_style))
    story.append(Paragraph("The Petitioner respectfully submits the following grounds for enlargement on regular bail:<br/><br/>"
                           "<b>1. Purely Civil & Contractual Genesis:</b> The dispute originates strictly from a commercial purchase agreement dated 12-June-2023. As settled by the Hon'ble Supreme Court in <i>Satishchandra Ratanlal Shah v. State of Gujarat (2019) 9 SCC 148</i>, breach of contract cannot be colored into criminal cheating in the absence of dishonest intent at inception.<br/><br/>"
                           "<b>2. Complete Refutation of Mens Rea:</b> The Petitioner remitted USD 16,500 (approx. Rs. 13.65 Lakhs) to German manufacturer Heidelberg Tech GMBH via TT on 22-June-2023. The shipment arrived at Chennai Port on 28-July-2023 and was delayed solely due to customs clearance, affirmatively disproving dishonest conversion under Section 406 IPC.<br/><br/>"
                           "<b>3. Mandatory Arnesh Kumar Safeguards:</b> The alleged offences carry sentences under 7 years imprisonment. In accordance with <i>Arnesh Kumar v. State of Bihar (2014) 8 SCC 273</i>, custodial detention is wholly unwarranted where the accused cooperates.<br/><br/>"
                           "<b>4. Impeccable Antecedents:</b> Verification by the State Crime Records Bureau (SCRB) confirms zero prior criminal cases.<br/><br/>"
                           "<b>5. No Flight Risk:</b> Petitioner has deep family roots in Chennai and has surrendered his passport (No. Z-4829101).", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>PRAYER:</b> The Petitioner prays that this Hon'ble Court may be pleased to enlarge the Petitioner on bail on such terms and conditions as deem fit.", bold_body))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Advocate for Petitioner | Chennai Sessions Bar Association", mono_style))
    build_pdf("Bail_Application_Petition_CrPC_437.pdf", story)

if __name__ == "__main__":
    create_fir_pdf()
    create_witness_pdf()
    create_accused_dossier_pdf()
    create_bail_petition_pdf()
    print("All 4 legal PDFs created successfully in:", TARGET_DIR)
