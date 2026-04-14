#!/usr/bin/env python3
"""
Aichouchm_AttributeImport — Technical Strategy & Decision Record
Professional PDF layout using ReportLab canvas callbacks + Table wrappers.
"""

import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Preformatted, NextPageTemplate
)
from reportlab.lib.colors import HexColor

OUTPUT = "/mnt/seconddrive/PhpstormProjects/Aichouchm-AttributeImport/STRATEGY.pdf"

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY     = HexColor("#0f172a")
NAVY2    = HexColor("#1e293b")
NAVY3    = HexColor("#334155")
BLUE     = HexColor("#2563eb")
BLUE_LT  = HexColor("#eff6ff")
BLUE_MD  = HexColor("#dbeafe")
ORANGE   = HexColor("#f97316")
ORANGE_LT= HexColor("#fff7ed")
GREEN    = HexColor("#16a34a")
GREEN_LT = HexColor("#f0fdf4")
RED      = HexColor("#dc2626")
RED_LT   = HexColor("#fff5f5")
AMBER    = HexColor("#d97706")
AMBER_LT = HexColor("#fef3c7")
GREY     = HexColor("#6b7280")
GREY_LT  = HexColor("#f8fafc")
GREY_BD  = HexColor("#e2e8f0")
WHITE    = colors.white
BLACK    = colors.black
CODE_BG  = HexColor("#1e293b")
CODE_FG  = HexColor("#e2e8f0")

PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm
BODY_W = PAGE_W - 2 * MARGIN

# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=10, leading=15,
                    textColor=NAVY2, spaceAfter=4, spaceBefore=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

S_BODY   = S("body",   fontSize=10, leading=15, textColor=NAVY2, alignment=TA_JUSTIFY, spaceAfter=6)
S_SMALL  = S("small",  fontSize=9,  leading=13, textColor=NAVY3, spaceAfter=4)
S_BULLET = S("bullet", fontSize=10, leading=14, textColor=NAVY2, leftIndent=14, spaceAfter=3)
S_MONO   = S("mono",   fontName="Courier", fontSize=8.5, leading=12.5, textColor=CODE_FG,
             leftIndent=10, rightIndent=10, spaceBefore=2, spaceAfter=2)

S_H1_CELL  = S("h1c", fontName="Helvetica-Bold", fontSize=16, textColor=WHITE,
               spaceBefore=0, spaceAfter=0, leading=20)
S_H2_CELL  = S("h2c", fontName="Helvetica-Bold", fontSize=12, textColor=NAVY,
               spaceBefore=0, spaceAfter=0, leading=16)
S_H3       = S("h3",  fontName="Helvetica-Bold", fontSize=11, textColor=ORANGE,
               spaceBefore=8, spaceAfter=3)

S_TH       = S("th",  fontName="Helvetica-Bold", fontSize=9, textColor=WHITE,
               alignment=TA_CENTER, leading=12)
S_TD       = S("td",  fontSize=9, textColor=NAVY2, leading=12)

S_COVER_TITLE = S("ct", fontName="Helvetica-Bold", fontSize=30, textColor=WHITE,
                  alignment=TA_CENTER, leading=38)
S_COVER_SUB   = S("cs", fontName="Helvetica", fontSize=13, textColor=HexColor("#94a3b8"),
                  alignment=TA_CENTER, leading=18)
S_META_KEY    = S("mk", fontName="Helvetica-Bold", fontSize=10, textColor=WHITE, spaceAfter=0)
S_META_VAL    = S("mv", fontSize=10, textColor=HexColor("#94a3b8"), spaceAfter=0)

# ── Canvas callbacks ──────────────────────────────────────────────────────────
def on_cover(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, PAGE_H - 8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
    c.setFillColor(NAVY2)
    c.rect(0, 0, PAGE_W, 3.2*cm, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, 3.2*cm, PAGE_W, 1.5*mm, fill=1, stroke=0)
    c.setFont("Helvetica", 8)
    c.setFillColor(GREY)
    c.drawCentredString(PAGE_W / 2, 1.3*cm,
        "Generated %s  |  MIT License  |  Mehdi Aichouch" % datetime.date.today().strftime("%B %d, %Y"))
    c.restoreState()

def on_page(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(MARGIN, PAGE_H - 1.5*cm, BODY_W, 1*mm, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(NAVY)
    c.drawString(MARGIN, PAGE_H - 1.2*cm, "Aichouchm_AttributeImport")
    c.setFont("Helvetica", 8)
    c.setFillColor(GREY)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.2*cm, "Technical Strategy & Decision Record")
    c.setFillColor(GREY_BD)
    c.rect(MARGIN, 1.5*cm, BODY_W, 0.5*mm, fill=1, stroke=0)
    c.setFont("Helvetica", 8)
    c.setFillColor(GREY)
    c.drawCentredString(PAGE_W / 2, 1.0*cm, str(doc.page - 1))
    c.restoreState()

# ── Flowable helpers ──────────────────────────────────────────────────────────
def _wrap(flowable, bg=None, line_color=None, line_width=4,
          top_pad=8, bot_pad=8, left_pad=12, right_pad=12, top_line=None, top_line_w=3):
    t = Table([[flowable]], colWidths=[BODY_W])
    cmds = [
        ("TOPPADDING",    (0,0),(-1,-1), top_pad),
        ("BOTTOMPADDING", (0,0),(-1,-1), bot_pad),
        ("LEFTPADDING",   (0,0),(-1,-1), left_pad),
        ("RIGHTPADDING",  (0,0),(-1,-1), right_pad),
    ]
    if bg:
        cmds.append(("BACKGROUND", (0,0),(-1,-1), bg))
    if line_color:
        cmds.append(("LINEBEFORE", (0,0),(0,-1), line_width, line_color))
    if top_line:
        cmds.append(("LINEABOVE", (0,0),(-1,0), top_line_w, top_line))
    t.setStyle(TableStyle(cmds))
    return t

def h1(text):
    return _wrap(Paragraph("  " + text, S_H1_CELL), bg=NAVY,
                 top_line=ORANGE, top_line_w=4, top_pad=12, bot_pad=12, left_pad=16)

def h2(text):
    return _wrap(Paragraph(text, S_H2_CELL), bg=BLUE_MD,
                 line_color=BLUE, line_width=4, top_pad=8, bot_pad=8, left_pad=12)

def h3(text):
    return Paragraph(text, S_H3)

def p(text):
    return Paragraph(text, S_BODY)

def ps(text):
    return Paragraph(text, S_SMALL)

def bullet(text):
    return Paragraph("&#8226;  " + text, S_BULLET)

def code(text):
    pre = Preformatted(text.strip("\n"), S_MONO)
    return _wrap(pre, bg=CODE_BG, line_color=BLUE, line_width=3,
                 top_pad=10, bot_pad=10, left_pad=14, right_pad=10)

def callout(kind, text):
    if kind == "warn":
        icon, bg, border = "!", AMBER_LT, AMBER
        st = S("cw", fontSize=9.5, leading=14, textColor=HexColor("#92400e"))
    elif kind == "good":
        icon, bg, border = "OK", GREEN_LT, GREEN
        st = S("cg", fontSize=9.5, leading=14, textColor=HexColor("#14532d"))
    else:
        icon, bg, border = "i", BLUE_LT, BLUE
        st = S("ci", fontSize=9.5, leading=14, textColor=HexColor("#1e3a8a"))
    return _wrap(Paragraph("<b>%s</b>  %s" % (icon, text), st),
                 bg=bg, line_color=border, line_width=4, top_pad=8, bot_pad=8, left_pad=14)

def space(n=1):
    return Spacer(1, n * 0.35 * cm)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=GREY_BD, spaceAfter=3, spaceBefore=3)

def simple_table(headers, rows, col_widths=None):
    hrow = [Paragraph(h, S_TH) for h in headers]
    data = [hrow] + [[Paragraph(str(c), S_TD) for c in row] for row in rows]
    if col_widths is None:
        col_widths = [BODY_W / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  NAVY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, GREY_LT]),
        ("GRID",          (0,0),(-1,-1), 0.5, GREY_BD),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 7),
        ("RIGHTPADDING",  (0,0),(-1,-1), 7),
    ]))
    return t

def comparison_table(rows):
    hrow = [Paragraph(h, S_TH) for h in
            ["Aspect", "Reference Module (Egio)", "Aichouchm Module"]]
    data = [hrow] + [[Paragraph(c, S_TD) for c in row] for row in rows]
    t = Table(data, colWidths=[3.5*cm, 6*cm, 7.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  NAVY),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [WHITE, GREY_LT]),
        ("GRID",          (0,0),(-1,-1), 0.5, GREY_BD),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 7),
        ("RIGHTPADDING",  (0,0),(-1,-1), 7),
    ]))
    return t

def before_after(label_l, code_l, label_r, code_r):
    lh = Paragraph("<b>Before (Reference)</b>", S("lh", fontSize=9, textColor=RED, fontName="Helvetica-Bold"))
    rh = Paragraph("<b>After (Aichouchm)</b>",  S("rh", fontSize=9, textColor=GREEN, fontName="Helvetica-Bold"))
    lc = Preformatted(code_l.strip("\n"), S_MONO)
    rc = Preformatted(code_r.strip("\n"), S_MONO)
    half = BODY_W / 2
    t = Table([[lh, rh], [lc, rc]], colWidths=[half, half])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0), RED_LT),
        ("BACKGROUND",    (1,0),(1,0), GREEN_LT),
        ("BACKGROUND",    (0,1),(0,1), CODE_BG),
        ("BACKGROUND",    (1,1),(1,1), CODE_BG),
        ("BOX",           (0,0),(0,-1), 1, RED),
        ("BOX",           (1,0),(1,-1), 1, GREEN),
        ("LINEAFTER",     (0,0),(0,-1), 1, GREY_BD),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
    ]))
    return t

# ── Cover page ────────────────────────────────────────────────────────────────
def cover_page():
    items = []
    items.append(Spacer(1, 6.5*cm))
    items.append(Paragraph("Aichouchm_AttributeImport", S_COVER_TITLE))
    items.append(Spacer(1, 0.5*cm))
    items.append(Paragraph("Technical Strategy &amp; Decision Record", S_COVER_SUB))
    items.append(Spacer(1, 0.25*cm))
    items.append(Paragraph(
        "How we designed a production-grade Magento 2 attribute import module", S_COVER_SUB))
    items.append(Spacer(1, 2.5*cm))

    meta = [
        ["Module",  "Aichouchm_AttributeImport"],
        ["Package", "aichouchm/magento2-module-attribute-import"],
        ["Version", "1.0.0"],
        ["Magento", "2.4.x"],
        ["PHP",     ">= 8.1"],
        ["Date",    datetime.date.today().strftime("%B %d, %Y")],
        ["Author",  "Mehdi Aichouch"],
    ]
    rows = [[Paragraph(k, S_META_KEY), Paragraph(v, S_META_VAL)] for k, v in meta]
    tbl = Table(rows, colWidths=[4*cm, 9*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,-1), NAVY2),
        ("BACKGROUND",    (1,0),(1,-1), NAVY3),
        ("LINEBELOW",     (0,0),(-1,-2), 0.5, HexColor("#475569")),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("BOX",           (0,0),(-1,-1), 2, ORANGE),
    ]))
    items.append(tbl)
    return items

# ── Body ──────────────────────────────────────────────────────────────────────
def build_body():
    story = []

    # Section 1
    story += [h1("1  Context & Business Problem"), space()]
    story += [
        p("This document records every architectural decision made while designing and building "
          "<b>Aichouchm_AttributeImport</b>, a production-grade Magento 2 module for bulk-importing "
          "product attribute options from CSV files via the Admin panel."),
        p("It explains the problem being solved, the reference code that was analysed, what was "
          "wrong in it, and exactly how each issue was addressed with code examples for every decision."),
        space(),
        h2("1.1  Why This Module Exists"),
        p("Magento 2 has no built-in mechanism for importing <b>attribute options</b> — the individual "
          "selectable values of a <i>select</i> or <i>multiselect</i> attribute (colours, sizes, "
          "materials, etc.). The only native path is clicking <i>Add Option</i> one row at a time."),
        space(0.5),
        p("For 200 colours across 3 store views that means <b>600 individual form interactions</b>."),
        space(0.5),
        callout("warn", "Real-world case: a fashion retailer with 350 colour options in French, "
                "English, and German needed to migrate from a legacy PIM. Manual entry was estimated "
                "at 2-3 days of admin work. With this module: one CSV upload, under 10 seconds."),
        space(),
        h2("1.2  The Reference Module"),
        p("A reference implementation (Egio_AttributeImport) was analysed. It demonstrated the right "
          "idea and provided a useful starting point, but analysis revealed "
          "<b>seven concrete production problems</b>. Each is documented in Section 3 with before/after code."),
        PageBreak(),
    ]

    # Section 2
    story += [h1("2  Module Architecture"), space()]
    story += [
        h2("2.1  Folder Structure"),
        code(
"""Aichouchm_AttributeImport/
|-- Api/
|   `-- ImportServiceInterface.php      <- public service contract
|-- Service/
|   `-- StoreResolver.php               <- store code to store_id mapping
|-- Model/
|   |-- Csv/
|   |   |-- StreamingReader.php         <- generator-based fgetcsv reader
|   |   `-- Validator.php               <- stateless validator
|   |-- Attribute/
|   |   `-- OptionProcessor.php         <- bulk DB writes
|   |-- Import/Source/Attributes.php    <- attribute dropdown source model
|   `-- ImportService.php               <- main orchestrator
|-- Controller/Adminhtml/Import/
|   |-- Index.php                       <- renders the import form page
|   |-- Preview.php                     <- AJAX: validate + preview HTML
|   |-- Process.php                     <- AJAX: run the import
|   `-- Log.php                         <- log viewer page
|-- Block/Adminhtml/Import/  Log.php
|-- etc/   di.xml  acl.xml  module.xml
|   `-- adminhtml/  menu.xml  routes.xml
|-- view/adminhtml/  layout/  templates/
`-- Test/Unit/  Csv/  Attribute/"""),
        space(),
        h2("2.2  Data Flow"),
        code(
"""CSV upload (multipart/form-data POST)
      |
      v
  StreamingReader.read($filePath)       -- fgetcsv generator, O(1) memory
      | yields one row[] at a time
      v
  Validator.validateHeaders()           -- check column names & count
  Validator.validateRows()              -- stateless; returns string[] errors
      | (empty = valid, proceed)
      v
  ImportService.groupRowsByOption()     -- second streaming pass, group rows
      | [{admin: row, stores: [row...]}, ...]
      v
  OptionProcessor.processGroups()       -- bulk DB writes:
      |  . INSERT INTO eav_attribute_option        (one per new option)
      |  . insertMultiple -> eav_attribute_option_value   (all labels)
      |  . insertOnDuplicate -> eav_attribute_option_swatch (all swatches)
      v
  CacheManager.clean([eav, full_page])  -- invalidate EAV + FPC
      v
  Logger (PSR-3 virtual type)           -- var/log/attribute_import.log"""),
        space(),
        h2("2.3  Key Classes"),
        simple_table(
            ["Class", "Responsibility", "Pattern"],
            [
                ["StreamingReader", "Reads CSV row-by-row via fgetcsv generator", "Generator / Iterator"],
                ["Validator", "Returns error list, holds no state", "Stateless Service"],
                ["ImportService", "Orchestrates the entire import flow", "Facade / Service"],
                ["OptionProcessor", "Bulk DB writes with batch queries", "Repository / Batch"],
                ["StoreResolver", "Maps store codes to store_ids", "Lookup Service"],
            ],
            col_widths=[4.5*cm, 7*cm, 5.5*cm]
        ),
        PageBreak(),
    ]

    # Section 3
    story += [h1("3  Seven Problems Solved"), space()]
    story += [
        p("Each subsection names the problem, shows the reference code, explains why it fails in "
          "production, and shows the improved version with the reasoning."),
        space(),
        h2("Problem 1 -- Memory: Full CSV Load vs. Streaming Generator"),
        p("The reference reader used <code>Magento\\Framework\\File\\Csv::getData()</code> which "
          "reads the entire file into a PHP array. A 50,000-row file consumes tens of MB of memory."),
        space(0.5),
        before_after(
            "getData() -- entire file in RAM",
            """// CsvReader.php
$data = $this->csvProcessor
    ->getData($filePath);
// getData() = one giant array
// 50k rows ~ 30 MB RAM
// PHP limit: 256 MB -> OOM risk""",
            "fgetcsv generator -- O(1) memory",
            """// StreamingReader.php
public function read(string $path): \\Generator
{
    $h = fopen($path, 'r');
    $bom = fread($h, 3);
    if ($bom !== "\\xEF\\xBB\\xBF") {
        rewind($h);
    }
    try {
        $i = 0;
        while (($r = fgetcsv($h)) !== false)
            yield $i++ => array_map('trim', $r);
    } finally { fclose($h); }
}"""
        ),
        space(0.5),
        callout("good", "Peak memory is now one row at a time (~1 KB) regardless of file size. "
                "The BOM strip also handles Excel-exported CSVs; without it the first header reads "
                "as 0xEF 0xBB 0xBF + 'attribute_code' and all header validation fails silently."),
        space(),
        h2("Problem 2 -- State Leakage in Validator"),
        p("Magento's DI container instantiates services as singletons by default. Storing errors in "
          "an instance variable means errors from a previous validation call persist into the next one."),
        space(0.5),
        before_after(
            "Stateful -- accumulates errors",
            """// CsvValidator.php
private array $messageErrors = [];

public function validate(array $rows): bool
{
    // errors from PREVIOUS call still here!
    foreach ($rows as $row) {
        if (empty($row[2])) {
            $this->messageErrors[] = 'Empty';
        }
    }
    return empty($this->messageErrors);
}""",
            "Stateless -- returns value",
            """// Validator.php
public function validateRows(
    array $rows,
    string $code,
    int $swatchType
): array {
    $errors = [];  // local, discarded after return
    foreach ($rows as $i => $row) {
        if (empty($row[2])) {
            $errors[] = "Row $i: value empty";
        }
    }
    return $errors;  // no mutation of $this
}"""
        ),
        space(0.5),
        callout("warn", "The singleton bug: validate File A (1 error), then validate File B "
                "(0 errors) -> second call still reports 1 error from File A. This causes false "
                "validation failures that are extremely hard to reproduce in production."),
        space(),
        h2("Problem 3 -- N x M DB Queries vs. Batch Writes"),
        p("The reference called <code>attributeRepository->save()</code> once per option. For "
          "200 options x 3 store views that is 200+ full EAV save cycles (~600 DB round-trips)."),
        space(0.5),
        before_after(
            "One save() per option",
            """// Import.php
foreach ($options as $value) {
    $option = $this->optionFactory->create();
    $option->setLabel($value);
    $attribute->addData([
        'option' => $option
    ]);
    // Full EAV load + save + cache bust
    $this->attributeRepository->save($attribute);
}
// 200 options = 200 DB round-trips""",
            "Batch inserts -- N+2 queries total",
            """// OptionProcessor.php
// 1. One INSERT per option (need lastInsertId)
$conn->insert('eav_attribute_option', [
    'attribute_id' => $attrId,
    'sort_order'   => $order,
]);
$optId = (int) $conn->lastInsertId();

// 2. ALL labels in ONE query
$conn->insertMultiple(
    'eav_attribute_option_value', $labelRows
);

// 3. ALL swatches in ONE query
$conn->insertOnDuplicate(
    'eav_attribute_option_swatch', $swatchRows
);"""
        ),
        space(0.5),
        callout("good", "200 options x 3 store views: reference = ~200 save() calls. "
                "Improved = 200 option INSERTs + 1 label batch + 1 swatch batch = 202 queries. "
                "Measured ~40x faster on a local Docker stack."),
        PageBreak(),
        h2("Problem 4 -- Wrong Store ID for 'default' Store Code"),
        p("In Magento's EAV schema, <code>store_id = 0</code> is the admin (global) store. "
          "Labels saved with store_id = 0 are the fallback for every store view. "
          "The reference mapped CSV store code <code>'default'</code> via StoreManager which "
          "returns store_id = 1 (the default store view), not store_id = 0."),
        space(0.5),
        before_after(
            "Default maps to store_id=1 (wrong)",
            """// Helper/Store.php
public function getStoreId(string $code): int
{
    // StoreManager('default') -> store_id = 1
    // This is the DEFAULT STORE VIEW, not admin
    return (int) $this->storeManager
        ->getStore($code)->getId();
}""",
            "Explicit alias -> store_id=0 (correct)",
            """// Service/StoreResolver.php
public function getStoreId(string $code): int
{
    if (in_array(
        strtolower($code),
        ['admin', 'default', '0'],
        true
    )) {
        return 0;  // admin store = global fallback
    }
    return (int) $this->storeManager
        ->getStore($code)->getId();
}"""
        ),
        space(0.5),
        callout("warn", "Without this fix, labels land in store_id=1 instead of store_id=0. "
                "Magento then has no global fallback and shows empty option labels on store views "
                "that have no explicit translation."),
        space(),
        h2("Problem 5 -- Overwriting Existing Options"),
        p("The reference re-imported options that already existed, silently overwriting any "
          "manual adjustments (sort_order, swatch colour) made by an admin since the last import."),
        space(0.5),
        before_after(
            "Overwrites existing options",
            """// Import.php
foreach ($csvOptions as $value) {
    // No existence check
    $option->setLabel($value);
    $attribute->addData([
        'option' => $option
    ]);
    // Previous admin tweaks lost
    $this->attributeRepository->save($attribute);
}""",
            "Pre-load then skip duplicates",
            """// ImportService.php
private function loadExisting(
    AttributeInterface $attr
): array {
    return $conn->fetchPairs(
        $select->where('store_id = 0')
               ->where('attribute_id = ?', $attrId)
    ); // ['Red' => 100, 'Blue' => 101, ...]
}

// OptionProcessor.php
if (array_key_exists($label, $existing)) {
    $result['skipped']++;
    $result['skippedValues'][] = $label;
    continue;  // O(1) hash lookup, no DB call
}"""
        ),
        space(0.5),
        callout("info", "Skip-not-overwrite is intentional. Admins often fine-tune sort_order "
                "or swatch colours after initial import. Silently overwriting those changes on "
                "re-import causes confusion and data loss. Skipped values are logged as WARNINGs."),
        space(),
        h2("Problem 6 -- No Service Interface"),
        p("Controllers called the import logic via a concrete class, making unit testing "
          "impossible without bootstrapping Magento or using reflection to swap dependencies."),
        space(0.5),
        before_after(
            "Concrete class dependency",
            """// Controller/Adminhtml/Import/Index.php
public function __construct(
    // ...
    Import $import,  // concrete class
) {}
// Test must instantiate real Import
// with all its DB/Magento dependencies""",
            "Service interface + DI binding",
            """// Api/ImportServiceInterface.php
interface ImportServiceInterface
{
    public function validate(
        string $filePath,
        string $attributeCode
    ): array;

    public function import(
        string $filePath,
        string $attributeCode
    ): array;
}

// di.xml: interface -> concrete class
// Controllers type-hint the interface"""
        ),
        space(0.5),
        callout("good", "With the interface, unit tests inject a mock that returns controlled "
                "fixtures -- no database, no Magento bootstrap. All 14 unit tests run in under 1 second."),
        space(),
        h2("Problem 7 -- Logger Semantics"),
        p("The reference used a custom Helper/Logger class that manually prepended timestamps "
          "(Monolog already handles that) and had no PSR-3 interface. Magento provides a clean "
          "way to create a dedicated logger using only a virtual type in di.xml."),
        space(0.5),
        before_after(
            "Custom Logger helper class",
            """// Helper/Logger.php
class Logger
{
    public function log(
        string $msg,
        string $level
    ): void {
        $ts = date('Y-m-d H:i:s');
        $line = "[$ts][$level] $msg";
        fwrite($this->handle, $line . PHP_EOL);
    }
    // No PSR-3, no Monolog features
}""",
            "Monolog virtual type in di.xml",
            """<!-- etc/di.xml -->
<virtualType
  name="AttributeImportLogger"
  type="Magento\\Framework\\Logger\\Monolog">
  <arguments>
    <argument name="name"
              xsi:type="string">attributeimport
    </argument>
    <argument name="handlers" xsi:type="array">
      <item name="system" xsi:type="object">
        AttributeImportStreamHandler
      </item>
    </argument>
  </arguments>
</virtualType>
<!-- No PHP class needed -->
<!-- Inject as LoggerInterface $logger -->"""
        ),
        space(0.5),
        callout("info", "Virtual types create a named DI object without a PHP class. "
                "The result is a fully PSR-3 compliant Monolog logger that writes to "
                "var/log/attribute_import.log with timestamps, levels, and context built in."),
        PageBreak(),
    ]

    # Section 4
    story += [h1("4  Swatch Support"), space()]
    story += [
        p("Magento stores swatches in <code>eav_attribute_option_swatch</code>. "
          "The <code>type</code> column encodes the kind:"),
        simple_table(
            ["type value", "Swatch kind", "value column content"],
            [
                ["0", "Text swatch", "Styled label string (e.g. 'XL')"],
                ["1", "Colour (hex)", "Hex string e.g. #FF0000"],
                ["2", "Image URL", "Path e.g. /media/swatch/red.jpg"],
            ],
            col_widths=[3*cm, 4*cm, 10*cm]
        ),
        space(),
        h2("4.1  Auto-detecting Swatch Type"),
        p("The Validator checks the attribute's <code>frontend_input</code> to determine the type:"),
        code(
"""// Validator.php
public const SWATCH_NONE   = -1;  // plain select / multiselect
public const SWATCH_TEXT   =  0;  // swatch_text attribute
public const SWATCH_VISUAL =  1;  // swatch_visual attribute

public function detectSwatchType(
    AttributeInterface $attribute
): int {
    $input = $attribute->getFrontendInput();
    if ($input === 'swatch_visual') return self::SWATCH_VISUAL;
    if ($input === 'swatch_text')   return self::SWATCH_TEXT;
    return self::SWATCH_NONE;
}"""),
        space(),
        h2("4.2  CSV Format by Attribute Type"),
        simple_table(
            ["Attribute type", "Columns", "swatch column"],
            [
                ["select / multiselect", "attribute_code, store_view, value, sort_order, is_default", "Not present"],
                ["swatch_visual", "attribute_code, store_view, value, swatch, sort_order, is_default", "#RRGGBB or /url"],
                ["swatch_text", "Same 6 columns as visual", "Styled label string"],
            ],
            col_widths=[3.5*cm, 8.5*cm, 5*cm]
        ),
        PageBreak(),
    ]

    # Section 5
    story += [h1("5  CSV Format & Row Grouping"), space()]
    story += [
        p("Each attribute option is represented as a <b>group</b> of rows. The first row must "
          "have <code>store_view = default</code> (or <code>admin</code>) — this is the global "
          "admin label, and is where sort_order and is_default are read from. Subsequent rows "
          "in the same group are store-view translations."),
        space(),
        h2("5.1  Example CSV (swatch_visual)"),
        code(
"""attribute_code,store_view,value,swatch,sort_order,is_default
color,default,Red,#FF0000,1,1        <- group 1 starts (admin row)
color,fr,Rouge,#FF0000,1,1           <- French translation
color,en,Red,#FF0000,1,1             <- English translation
color,default,Blue,#0000FF,2,0       <- group 2 starts
color,fr,Bleu,#0000FF,2,0
color,en,Blue,#0000FF,2,0"""),
        space(),
        h2("5.2  Column Reference"),
        simple_table(
            ["Column", "Required", "Description"],
            [
                ["attribute_code", "Always", "Must match the selected attribute on every row"],
                ["store_view", "Always", "'default'/'admin' = global (store_id=0). Others must be valid Magento store codes"],
                ["value", "Always", "The option label for this store view"],
                ["swatch / hex_code", "Swatch attrs only", "Hex colour (#RRGGBB) or image URL. Ignored for plain select"],
                ["sort_order", "Admin row only", "Integer. Controls display order in dropdowns"],
                ["is_default", "Admin row only", "1 = default selected value. Only one option per import may have is_default=1"],
            ],
            col_widths=[3.5*cm, 3*cm, 10.5*cm]
        ),
        PageBreak(),
    ]

    # Section 6
    story += [h1("6  Validation Rules"), space()]
    story += [
        p("All validation runs in a single pass before any DB write. If any error is found, "
          "the import is blocked entirely -- no partial state."),
        space(),
        simple_table(
            ["Rule", "Severity"],
            [
                ["Column count must match expected layout", "Error -- blocks import"],
                ["Column names must match expected names", "Error -- blocks import"],
                ["attribute_code must match selected attribute on every row", "Error -- blocks import"],
                ["store_view and value must not be empty", "Error -- blocks import"],
                ["First row of each group must be a default/admin row", "Error -- blocks import"],
                ["sort_order must be a number", "Error -- blocks import"],
                ["is_default must be 0 or 1", "Error -- blocks import"],
                ["Only one option may have is_default=1", "Error -- blocks import"],
                ["No duplicate values in the same admin store within the CSV", "Error -- blocks import"],
                ["No duplicate store codes within the same option group", "Error -- blocks import"],
                ["Non-existent store codes", "Error -- blocks import"],
                ["Option value already exists in the database", "Warning -- logs and skips"],
            ],
            col_widths=[12*cm, 5*cm]
        ),
        space(),
        callout("info", "The two-pass strategy (validate then import) guarantees atomicity: "
                "either all new options are imported, or none are. There is no partially-imported "
                "state to roll back."),
        PageBreak(),
    ]

    # Section 7
    story += [h1("7  Admin UI Design"), space()]
    story += [
        h2("7.1  Import Form Page  (Stores -> Attributes -> Import Attributes)"),
        bullet("Attribute selector -- dropdown of all user-defined select/multiselect/swatch attributes"),
        bullet("File upload field -- CSV only"),
        bullet("<b>Check Data</b> button -- triggers AJAX validation, shows preview table"),
        bullet("<b>Import</b> button -- only enabled after successful validation"),
        bullet("Notification area -- success / error messages"),
        bullet("Link to the import log viewer"),
        space(),
        h2("7.2  Two-Step Import Flow"),
        code(
"""Step 1 -- Check Data  (AJAX POST -> /attributeimport/import/preview)
  |-- Validates headers and all rows
  |-- If errors: shows error list, Import button stays disabled
  `-- If valid: shows preview table with first 10 rows, enables Import button

Step 2 -- Import  (AJAX POST -> /attributeimport/import/process)
  |-- Runs the actual import
  |-- Returns: {success, imported, skipped, skippedValues, messages}
  `-- Shows: "Imported 47 options. Skipped 3 (already existed)." """),
        space(),
        h2("7.3  Log Viewer"),
        simple_table(
            ["Log level", "Colour", "When written"],
            [
                ["INFO",    "Green", "Import started; import completed with summary counts"],
                ["WARNING", "Amber", "Option skipped because it already exists in the database"],
                ["ERROR",   "Red",   "Validation failure; unexpected exception during import"],
            ],
            col_widths=[2.5*cm, 2.5*cm, 12*cm]
        ),
        PageBreak(),
    ]

    # Section 8
    story += [h1("8  DI Configuration"), space()]
    story += [
        h2("8.1  di.xml: Virtual Logger"),
        code(
"""<!-- No PHP class needed -- Magento wires this automatically -->
<virtualType name="AttributeImportLogger"
             type="Magento\\Framework\\Logger\\Monolog">
  <arguments>
    <argument name="name" xsi:type="string">attributeimport</argument>
    <argument name="handlers" xsi:type="array">
      <item name="system" xsi:type="object">
        AttributeImportStreamHandler
      </item>
    </argument>
  </arguments>
</virtualType>

<virtualType name="AttributeImportStreamHandler"
             type="Magento\\Framework\\Logger\\Handler\\Base">
  <arguments>
    <argument name="fileName" xsi:type="string">
      /var/log/attribute_import.log
    </argument>
  </arguments>
</virtualType>"""),
        space(),
        h2("8.2  di.xml: Service Interface Binding"),
        code(
"""<preference for="Aichouchm\\AttributeImport\\Api\\ImportServiceInterface"
            type="Aichouchm\\AttributeImport\\Model\\ImportService"/>"""),
        space(),
        h2("8.3  ACL Resource Tree"),
        code(
"""Magento_Backend::stores
  `-- Magento_Backend::stores_attributes
        `-- Aichouchm_AttributeImport::import_attributes
              <- "Import Attributes" -- assign to any admin role"""),
        PageBreak(),
    ]

    # Section 9
    story += [h1("9  Unit Tests"), space()]
    story += [
        simple_table(
            ["Test class", "Tests", "What is covered"],
            [
                ["StreamingReaderTest", "6", "BOM stripping, whitespace trim, missing file exception, empty file, multi-row yield"],
                ["ValidatorTest", "13", "Header validation, row validation, statelessness, default store alias, duplicate detection"],
                ["OptionProcessorTest", "5", "New option insert, existing option skip, mixed skip/import, swatch persistence, empty groups"],
            ],
            col_widths=[5.5*cm, 1.5*cm, 10*cm]
        ),
        space(),
        h2("Running the Tests"),
        code(
"""docker compose exec maintenance bash -c \\
  "cd /var/www/html && \\
   vendor/bin/phpunit \\
   app/code/Aichouchm/AttributeImport/Test/Unit" """),
        space(),
        h2("Key Test: Validator Statelessness"),
        code(
"""public function testValidatorIsStateless(): void
{
    $rows = [['color', 'admin', 'Red', '1', '1']];
    // First call
    $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
    // Second call: must still be valid (no leftover state from first call)
    $errors = $this->validator->validateRows($rows, 'color', Validator::SWATCH_NONE);
    $this->assertEmpty($errors);
}"""),
        PageBreak(),
    ]

    # Section 10
    story += [h1("10  Decision Summary"), space()]
    story += [
        comparison_table([
            ["CSV reading",
             "getData() -- full file into RAM array",
             "fgetcsv generator -- O(1) memory, any file size"],
            ["Validator state",
             "Errors stored in private property (singleton bug)",
             "Stateless -- returns string[] errors, no mutation of $this"],
            ["DB writes",
             "attributeRepository->save() per option (~N x M queries)",
             "insertMultiple + insertOnDuplicate (N+2 queries total)"],
            ["Store 'default'",
             "StoreManager lookup -> store_id=1 (wrong)",
             "Explicit alias: 'default'/'admin' -> store_id=0 (correct)"],
            ["Duplicate options",
             "Overwrites existing options silently",
             "Pre-loads existing, skips with WARNING log entry"],
            ["Service contract",
             "Controller depends on concrete Import class",
             "ImportServiceInterface -- mockable, DI-swappable"],
            ["Logger",
             "Custom Helper/Logger with manual timestamps",
             "Monolog virtual type via di.xml, fully PSR-3 compliant"],
        ]),
        space(1.5),
        callout("good", "All seven improvements are independently testable. The test suite "
                "validates each concern in isolation without requiring a running Magento instance."),
        space(2),
        hr(),
        space(0.5),
        Paragraph(
            "Aichouchm_AttributeImport  |  v1.0.0  |  MIT License  |  Mehdi Aichouch  |  " +
            datetime.date.today().strftime("%B %d, %Y"),
            S("foot", fontSize=8, textColor=GREY, alignment=TA_CENTER)
        ),
    ]

    return story

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    HEADER_H = 1.8 * cm
    FOOTER_H = 1.8 * cm

    cover_frame = Frame(
        0, 0, PAGE_W, PAGE_H,
        leftPadding=MARGIN, rightPadding=MARGIN,
        topPadding=0, bottomPadding=0, id="cover"
    )
    body_frame = Frame(
        MARGIN, FOOTER_H, BODY_W, PAGE_H - HEADER_H - FOOTER_H,
        leftPadding=0, rightPadding=0,
        topPadding=8, bottomPadding=8, id="body"
    )

    cover_tpl = PageTemplate(id="Cover", frames=[cover_frame], onPage=on_cover)
    body_tpl  = PageTemplate(id="Body",  frames=[body_frame],  onPage=on_page)

    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=A4,
        pageTemplates=[cover_tpl, body_tpl],
        title="Aichouchm_AttributeImport -- Technical Strategy & Decision Record",
        author="Mehdi Aichouch",
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=HEADER_H, bottomMargin=FOOTER_H,
    )

    story = cover_page()
    story.append(NextPageTemplate("Body"))
    story.append(PageBreak())
    story += build_body()

    doc.build(story)
    print("PDF written to: " + OUTPUT)

if __name__ == "__main__":
    build()
