"""Create the Lab 7 deliverable PDF from actual saved screenshots and output."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Lab_7_Fuzz_Testing_Report.pdf"
NAVY = colors.HexColor("#17324d")
styles = getSampleStyleSheet()
for name, size, leading, color in [
    ("Title7", 23, 27, NAVY), ("Subtitle7", 11, 15, colors.HexColor("#087c83")),
    ("Body7", 10, 14, colors.black), ("Heading7", 13, 17, NAVY),
    ("Caption7", 9, 12, colors.HexColor("#445466")),
]:
    styles.add(ParagraphStyle(name, fontSize=size, leading=leading, textColor=color, spaceAfter=8))


def p(text, style="Body7"):
    return Paragraph(text, styles[style])


def table(data, widths):
    rows = [[p(escape(str(cell)), "Caption7") for cell in row] for row in data]
    result = Table(rows, colWidths=widths, hAlign="LEFT")
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce9f2")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f0f5f8"), colors.white]),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return result


def footer(canvas, doc):
    width, _ = landscape(A4)
    canvas.setStrokeColor(colors.HexColor("#d9e2eb"))
    canvas.line(32, 29, width - 32, 29)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526172"))
    canvas.drawString(32, 17, "HEMA SUSHMITHA N | PES1UG24CS667 | Software Engineering Lab 7")
    canvas.drawRightString(width - 32, 17, f"Page {doc.page}")


def build():
    before = (ROOT / "reports/failing_tests/terminal_output.txt").read_text(encoding="utf-8")
    after = (ROOT / "reports/passing_tests/terminal_output.txt").read_text(encoding="utf-8")
    assert "34 failed, 10 passed" in before and "44 passed" in after
    story = [
        p("Lab 7: Fuzzing for Input Validation Bugs", "Title7"),
        p("Coffee Shop Processor | HEMA SUSHMITHA N | PES1UG24CS667", "Subtitle7"),
        p("Objective and method", "Heading7"),
        p("Use Hypothesis to generate unexpected inputs for drink-code lookup, shot-price averaging and "
          "modifier parsing. Complete the starter properties, record failures, fix input validation, "
          "and rerun the identical tests. The assigned buggy files are preserved under originals/."),
        p("Work completed", "Heading7"),
        p("1. Created an isolated Python 3.14.6 environment with Hypothesis 6.170.14 and pytest 9.2.0.<br/>"
          "2. Ran the buggy interactive script and completed all three starter properties using @given.<br/>"
          "3. Added behavior properties, boundary regressions and CLI tests; reproduced failures on the original.<br/>"
          "4. Hardened processor.py and reran the same suite; captured all four required stages."),
        table([
            ["Measurement", "Observed result"],
            ["Buggy application, input moc", "KeyError: 'MOC'; exit code 1"],
            ["Completed suite on original source", "34 failed, 10 passed (44 collected tests)"],
            ["Fixed application, same inputs", "Price 5.0; average 1.5; valid modifiers; exit code 0"],
            ["Identical completed suite on fixed source", "44 passed; exit code 0"],
        ], [250, 490]),
        Spacer(1, 10),
        p("Testing scope", "Heading7"),
        p("Eight Hypothesis properties use up to 200 generated examples each, with deterministic generation, "
          "shrinking and no saved example database. Thirty-three parametrized regressions and three CLI "
          "checks bring the pytest total to 44. Generated-example counts differ from pytest test counts."),
        p("Deliverables: fixed processor.py, updated test_processor.py, and this PDF containing all four "
          "required screenshots. The failing-test screenshot selects the three starter properties "
          "(3 failed, 41 deselected); the complete 34/10 baseline transcript is also saved."),
        p('<a href="https://github.com/SETAPESU26/L6_L7_03_coffee_shop_order/tree/main/Lab%207">Assigned source</a> | '
          '<a href="https://github.com/Hema-sushmitha-N/PES1UG24CS667_SE_Lab/tree/main/Lab-7">Lab-7 submission</a>', "Caption7"),
        PageBreak(),
        p("Bugs, counterexamples and fixes", "Title7"),
        p("Hypothesis failures are complemented by explicit regressions for known boundary cases.", "Subtitle7"),
        table([
            ["Area / example", "Original behavior", "Fix and expected behavior"],
            ["All functions: generated None", "AttributeError on .upper() / .split()", "Type checks; lookup/average return None, modifiers return {}"],
            ["Lookup: generated whitespace; regression moc", "KeyError; MOC does not match MOc", "Strip and uppercase; correct MOC key; safe lookup"],
            ["Average: empty CSV, 1,,3, one,two", "Unhandled ValueError", "Reject invalid CSV as a whole; return None"],
            ["Average: nan, inf, 1e309, negative prices", "Non-finite / invalid monetary values accepted", "Require finite nonnegative prices"],
            ["Average: 1e308,1e308", "Intermediate sum overflows to infinity", "Scale by maximum; math.fsum; return finite 1e308"],
            ["Modifiers: generated empty text; malformed segments", "Unpacking ValueError or empty keys/values", "Skip invalid segments; preserve valid nonempty pairs"],
            ["Modifiers: note:extra:hot", "Too many values to unpack", "Split once; preserve extra:hot as value"],
            ["CLI: invalid input / EOF", "Unhandled exception stops processing", "Clear validation messages; safe EOF termination"],
        ], [216, 234, 290]),
        Spacer(1, 10),
        p("Input policy and conclusions", "Heading7"),
        p("Unknown/invalid drink and price input returns None. Empty or invalid modifier segments are ignored; "
          "duplicate keys use the last value. These policies are explicit design choices where the handout "
          "does not prescribe behavior. Valid menu prices and ordinary calculations remain supported."),
        p("Hypothesis minimized the three starter failures to None. The original empty CSV raises ValueError "
          "during float conversion, rather than an observed divide-by-zero. Passing the suite demonstrates "
          "improved robustness for the tested properties, not proof for every input size or resource limit.", "Caption7"),
    ]
    stages = [
        ("buggy_app", "Step 2: Buggy Application", "Same demo inputs: moc | 1.0,1.5,2.0 | milk:oat;syrup:vanilla", "The original application crashes at the drink lookup with KeyError: 'MOC'."),
        ("failing_tests", "Step 4: Failing Hypothesis Tests", "Three completed starter properties against original source | 3 failed, 41 deselected", "All three no-crash properties fail. Complete counterexamples and the full 34-failed/10-passed baseline are retained in the raw report."),
        ("fixed_app", "Step 5: Fixed Application", "Same demo inputs | price 5.0 | average 1.5 | modifiers parsed | exit 0", "The corrected application handles the same inputs and reaches all three processing stages."),
        ("passing_tests", "Step 6: Passing Tests After Fixes", "Identical completed test suite against fixed processor.py | 44 passed", "All eight generated properties, 33 regression cases and three CLI tests pass after hardening."),
    ]
    for stage, title, subtitle, caption in stages:
        image = Image(str(ROOT / "reports" / stage / "terminal_screenshot.png"))
        ratio = min(744 / image.imageWidth, 415 / image.imageHeight)
        image.drawWidth, image.drawHeight = image.imageWidth * ratio, image.imageHeight * ratio
        image.hAlign = "CENTER"
        story += [PageBreak(), p(title, "Title7"), p(subtitle, "Subtitle7"), image,
                  Spacer(1, 5), p(escape(caption), "Caption7")]
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=landscape(A4), leftMargin=32,
        rightMargin=32, topMargin=26, bottomMargin=37,
        title="Lab 7: Fuzzing for Input Validation Bugs", author="HEMA SUSHMITHA N - PES1UG24CS667")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
