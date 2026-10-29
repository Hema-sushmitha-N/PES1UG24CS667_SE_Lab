"""Build the consolidated report from saved measurements and original screenshots.

Requires reportlab only for report generation, not for the lab tests.
"""

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Lab_6_Code_and_Branch_Coverage_Report.pdf"
REPO = "https://github.com/Hema-sushmitha-N/PES1UG24CS667_SE_Lab"
SOURCE = "https://github.com/SETAPESU26/L6_L7_03_coffee_shop_order"
NAVY = colors.HexColor("#17324d")
TEAL = colors.HexColor("#087c83")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle("ReportTitle", fontSize=24, leading=28, textColor=NAVY, spaceAfter=8))
styles.add(ParagraphStyle("ReportSubtitle", fontSize=11, leading=15, textColor=TEAL, spaceAfter=12))
styles.add(ParagraphStyle("ReportBody", fontSize=10, leading=14, spaceAfter=7))
styles.add(ParagraphStyle("ReportHeading", fontSize=13, leading=17, textColor=NAVY, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle("ReportCaption", fontSize=9, leading=12, textColor=colors.HexColor("#445466"), spaceAfter=6))
styles.add(ParagraphStyle("ReportCode", fontName="Courier", fontSize=8.5, leading=12, spaceAfter=5))


def p(text, style="ReportBody"):
    return Paragraph(text, styles[style])


def totals(stage):
    return json.loads((ROOT / "reports" / stage / "coverage.json").read_text())["totals"]


def footer(canvas, document):
    width, _ = landscape(A4)
    canvas.setStrokeColor(colors.HexColor("#d9e2eb"))
    canvas.line(32, 29, width - 32, 29)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526172"))
    canvas.drawString(32, 17, "PES1UG24CS667 | Software Engineering Lab 6 | Coffee Shop Order")
    canvas.drawRightString(width - 32, 17, f"Page {document.page}")


def screenshot(stage):
    img = Image(str(ROOT / "reports" / stage / "terminal_screenshot.png"))
    ratio = min(744 / img.imageWidth, 422 / img.imageHeight)
    img.drawWidth = img.imageWidth * ratio
    img.drawHeight = img.imageHeight * ratio
    img.hAlign = "CENTER"
    return img


def build():
    initial = totals("baseline_branch")
    line = totals("line")
    branch = totals("branch")
    assert line["covered_lines"] == line["num_statements"] == 54
    assert branch["covered_branches"] == branch["num_branches"] == 38
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=landscape(A4), leftMargin=32, rightMargin=32,
        topMargin=26, bottomMargin=37,
        title="Lab 6: Code and Branch Coverage - Coffee Shop Order",
        author="HEMA SUSHMITHA N - PES1UG24CS667",
    )
    story = [
        p("Lab 6: Code and Branch Coverage", "ReportTitle"),
        p("Coffee Shop Order | HEMA SUSHMITHA N | PES1UG24CS667", "ReportSubtitle"),
        p("Objective and scope", "ReportHeading"),
        p("Measure the original test coverage and improve it to at least 90% by adding test cases. "
          "The original <b>coffee_shop_order.py</b> application and starter test were preserved unchanged. "
          "Both original files were verified byte for byte against the assigned source."),
        p("Work completed", "ReportHeading"),
        p("1. Checked Python, Git and VS Code; created an isolated Python 3.14.6 environment with "
          "pytest 9.2.0 and coverage 7.17.0.<br/>"
          "2. Ran the starter test for initial line and branch coverage.<br/>"
          "3. Added separate line and branch test suites, asserted expected totals, statuses and exceptions, "
          "and reran coverage against the application only.<br/>"
          "4. Saved final terminal screenshots, text and JSON reports; submitted two coverage commits in "
          "the existing SE repository under <b>Lab-6</b>."),
        p("Measured results", "ReportHeading"),
    ]
    data = [
        ["Suite", "Passing tests", "Statement coverage", "Branch outcomes"],
        ["Original starter", "1", f"{initial['covered_lines']}/54 (48.15%)", f"{initial['covered_branches']}/38 (36.84%)"],
        ["Code coverage tests", "8", "54/54 (100%)", "Not measured in line-only run"],
        ["Branch coverage tests", "39", "54/54 (100%)", "38/38 (100%)"],
    ]
    table = Table(data, colWidths=[180, 95, 180, 220], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#eef4f8"), colors.white]),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#ccd8e3")),
    ]))
    story.extend([
        table, Spacer(1, 8),
        p("All <b>48 tests pass</b> together (1 starter + 8 line + 39 branch). In a branch-enabled report, "
          "the Cover column combines statement and branch outcomes: the initial displayed 43% is "
          "(26 + 14) / (54 + 38), rather than the branch-only percentage.", "ReportCaption"),
        p("Test coverage and submission", "ReportHeading"),
        p("Cases include invalid input, paid/unpaid orders, sizes, defaults, membership, tax, syrup cap "
          "boundaries, negative costs, strict/non-strict allergies, four/five rejection thresholds, and "
          "machine temperature boundaries and streak resets. Final results meet the handout target; "
          "100% coverage does not establish correctness for all possible inputs."),
        p(f'<a href="{SOURCE}">Assigned source</a> | '
          f'<a href="{REPO}/tree/main/Lab-6">Submission folder</a> | '
          f'<a href="{REPO}/commit/d86bbb7">Line commit: d86bbb7</a> | '
          f'<a href="{REPO}/commit/121ac8d">Branch commit: 121ac8d</a>', "ReportCaption"),
        PageBreak(),
        p("Deliverable 1: Code Coverage Evidence", "ReportTitle"),
        p("CodeCoverageTest_coffee_shop_order.py | 8 passed | 54/54 statements | 100%", "ReportSubtitle"),
        screenshot("line"), Spacer(1, 5),
        p("Actual terminal screenshot from the submission checkout. Coverage is limited to "
          "coffee_shop_order.py; no application statements are missed.", "ReportCaption"),
        PageBreak(),
        p("Deliverable 2: Branch Coverage Evidence", "ReportTitle"),
        p("BranchCoverageTest_coffee_shop_order.py | 39 passed | 38/38 branch outcomes | 100%", "ReportSubtitle"),
        screenshot("branch"), Spacer(1, 5),
        p("Actual terminal screenshot from the submission checkout. Both statement and branch coverage "
          "are 100%, with no missing statements or partially covered branch locations.", "ReportCaption"),
    ])
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
