#!/usr/bin/env python3
"""
Aichouchm_AttributeImport — Technical Reference Document
Complete class-by-class documentation in workflow order.
"""

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
    c.drawCentredString(PAGE_W / 2, 1.3*cm, "MIT License  |  Mehdi Aichouch")
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
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.2*cm, "Technical Reference")
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
    """Return one wrapped block, or a list of blocks if too tall for a single page."""
    MAX_LINES = 48
    lines = text.strip("\n").split("\n")
    if len(lines) <= MAX_LINES:
        pre = Preformatted(text.strip("\n"), S_MONO)
        return _wrap(pre, bg=CODE_BG, line_color=BLUE, line_width=3,
                     top_pad=10, bot_pad=10, left_pad=14, right_pad=10)
    chunks = []
    for i in range(0, len(lines), MAX_LINES):
        chunk = "\n".join(lines[i:i + MAX_LINES])
        pre = Preformatted(chunk, S_MONO)
        chunks.append(_wrap(pre, bg=CODE_BG, line_color=BLUE, line_width=3,
                            top_pad=10, bot_pad=10, left_pad=14, right_pad=10))
    return chunks

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

def filepath(text):
    return _wrap(Paragraph(text, S("fp", fontName="Courier", fontSize=9,
                 textColor=HexColor("#1e3a8a"), spaceAfter=0)),
                 bg=BLUE_LT, line_color=BLUE, line_width=3,
                 top_pad=5, bot_pad=5, left_pad=10)

# ── Cover page ────────────────────────────────────────────────────────────────
def cover_page():
    items = []
    items.append(Spacer(1, 6.5*cm))
    items.append(Paragraph("Aichouchm_AttributeImport", S_COVER_TITLE))
    items.append(Spacer(1, 0.5*cm))
    items.append(Paragraph("Technical Reference", S_COVER_SUB))
    items.append(Spacer(1, 0.25*cm))
    items.append(Paragraph(
        "Complete class documentation in workflow order", S_COVER_SUB))
    items.append(Spacer(1, 2.5*cm))

    meta = [
        ["Module",  "Aichouchm_AttributeImport"],
        ["Package", "aichouchm/magento2-module-attribute-import"],
        ["Magento", "2.4.x"],
        ["PHP",     ">= 8.1"],
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

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 1 — Overview
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("1  Module Overview"), space()]
    story += [
        p("Aichouchm_AttributeImport lets a Magento 2 admin upload a CSV file and bulk-import "
          "product attribute options (colours, sizes, materials, etc.) with per-store-view labels "
          "and hex-colour swatches. Without this module an admin must click <i>Add Option</i> one "
          "row at a time — 200 colours across 3 store views = 600 manual interactions."),
        space(),
        h2("1.1  Full Data Flow"),
        code(
"""Admin uploads CSV via browser form
        |
        v
  [Index controller]   renders the import page (layout + blocks)
        |
        v (user clicks Check Data)
  [Preview controller] receives multipart POST
        |
        v
  [StreamingReader]    opens file, yields one row[] per line
        |
        v
  [Validator]          validateHeaders() -- checks column count and names
                       validateRows()    -- checks every rule, row by row
        |
        v (if valid)
  [Preview block]      renders an HTML table preview, returned as JSON
        |
        v (user clicks Import)
  [Process controller] receives multipart POST
        |
        v
  [ImportService]      re-validates, then groups rows by option
        |
        v
  [OptionProcessor]    writes to DB:
                         INSERT INTO eav_attribute_option         (one per option)
                         insertOnDuplicate eav_attribute_option_value  (all labels)
                         insertOnDuplicate eav_attribute_option_swatch (all swatches)
        |
        v
  [CacheManager]       clean(['eav', 'full_page', 'block_html'])
        |
        v
  [Logger]             writes to var/log/attribute_import.log"""),
        space(),
        h2("1.2  Running Example CSV"),
        p("Every method in this document is explained using this CSV. "
          "The attribute <b>color</b> is a visual swatch (hex) attribute."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
color,default,Coral,#FF6B6B,1,1    <- group 1: admin row (sort_order + is_default here)
color,fr,Corail,#FF6B6B,1,1        <- group 1: French translation
color,en,Coral,#FF6B6B,1,1         <- group 1: English translation
color,default,Teal,#008080,2,0     <- group 2: admin row
color,fr,Sarcelle,#008080,2,0      <- group 2: French translation
color,en,Teal,#008080,2,0          <- group 2: English translation"""),
        space(),
        h2("1.3  Folder Structure"),
        code(
"""Aichouchm_AttributeImport/
|-- Api/
|   `-- ImportServiceInterface.php      <- public contract (interface)
|-- Service/
|   `-- StoreResolver.php               <- store code -> store_id lookup
|-- Model/
|   |-- Csv/
|   |   |-- StreamingReader.php         <- fgetcsv generator, O(1) memory
|   |   `-- Validator.php               <- stateless, returns error list
|   |-- Attribute/
|   |   `-- OptionProcessor.php         <- bulk DB writes
|   |-- Import/Source/Attributes.php    <- attribute dropdown source model
|   `-- ImportService.php               <- main orchestrator
|-- Controller/Adminhtml/
|   |-- AbstractAction.php              <- ADMIN_RESOURCE + shared request helpers
|   `-- Import/
|       |-- Index.php                   <- render the import page
|       |-- Preview.php                 <- AJAX: Check Data
|       |-- Process.php                 <- AJAX: Import
|       `-- Log.php                     <- log viewer page
|-- Block/Adminhtml/
|   |-- Import/
|   |   |-- Form.php                    <- page container (buttons)
|   |   |-- Form/Form.php               <- fieldset + form fields
|   |   |-- Form/Before.php             <- passes URLs to JS template
|   |   `-- Preview.php                 <- preview table block
|   `-- Log.php                         <- log viewer block
|-- etc/
|   |-- module.xml  registration.php
|   |-- di.xml  acl.xml
|   `-- adminhtml/  menu.xml  routes.xml
|-- view/adminhtml/
|   |-- layout/  attributeimport_import_index.xml
|   |            attributeimport_import_log.xml
|   `-- templates/import/  form/before.phtml
|                           preview.phtml  log.phtml
`-- Test/sample/  valid_color.csv  invalid_color.csv
                  duplicate_color.csv
                  valid_material.csv  invalid_material.csv"""),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 2 — Configuration Layer
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("2  Configuration Layer"), space()]
    story += [
        p("These files wire the module into Magento before a single line of business logic runs. "
          "Magento reads them at compile time and caches the result."),
        space(),

        h2("registration.php"),
        filepath("Aichouchm_AttributeImport/registration.php"),
        p("Every Magento module must call <b>ComponentRegistrar::register()</b> so Magento's "
          "module loader can discover it. Without this file the module is invisible — no routes, "
          "no blocks, no DI."),
        code(
"""ComponentRegistrar::register(
    ComponentRegistrar::MODULE,
    'Aichouchm_AttributeImport',
    __DIR__
);"""),
        callout("info", "'__DIR__' is the absolute path to the module root. Magento uses it to "
                "resolve all relative paths inside the module (templates, layout XML, etc.)."),
        space(),

        h2("etc/module.xml"),
        filepath("Aichouchm_AttributeImport/etc/module.xml"),
        p("Declares the module name and its setup version. The <b>sequence</b> tag tells Magento "
          "to load Magento_Swatches before this module, ensuring swatch tables exist before "
          "this module tries to write to them."),
        code(
"""<module name="Aichouchm_AttributeImport">
    <sequence>
        <module name="Magento_Swatches"/>
    </sequence>
</module>"""),
        space(),

        h2("etc/adminhtml/routes.xml"),
        filepath("Aichouchm_AttributeImport/etc/adminhtml/routes.xml"),
        p("Registers the URL front-name <b>attributeimport</b> for the admin router. "
          "This is the first segment of every URL this module handles."),
        code(
"""<router id="admin">
    <route id="attributeimport" frontName="attributeimport">
        <module name="Aichouchm_AttributeImport"/>
    </route>
</router>"""),
        p("URL pattern: <b>/admin/attributeimport/{controller}/{action}</b>"),
        simple_table(
            ["URL", "Controller file", "Action"],
            [
                ["/admin/attributeimport/import/index",   "Controller/Adminhtml/Import/Index.php",   "Render import page"],
                ["/admin/attributeimport/import/preview", "Controller/Adminhtml/Import/Preview.php", "AJAX: Check Data"],
                ["/admin/attributeimport/import/process", "Controller/Adminhtml/Import/Process.php", "AJAX: Import"],
                ["/admin/attributeimport/import/log",     "Controller/Adminhtml/Import/Log.php",     "Log viewer page"],
            ],
            col_widths=[6*cm, 6.5*cm, 4.5*cm]
        ),
        space(),

        h2("etc/adminhtml/menu.xml"),
        filepath("Aichouchm_AttributeImport/etc/adminhtml/menu.xml"),
        p("Adds the <i>Import Attributes</i> item to the admin menu under "
          "<b>Stores &rarr; Attributes</b>. Every attribute is declarative — "
          "Magento merges all modules' menu.xml files at cache-build time."),
        code(
"""<add id="Aichouchm_AttributeImport::import_attributes"
     title="Import Attributes"
     parent="Magento_Backend::stores_attributes"
     action="attributeimport/import/index"
     sortOrder="70"
     resource="Aichouchm_AttributeImport::import_attributes"/>"""),
        simple_table(
            ["Attribute", "Value", "Purpose"],
            [
                ["id",        "Aichouchm_AttributeImport::import_attributes", "Unique menu item identifier"],
                ["parent",    "Magento_Backend::stores_attributes",           "Places item under Stores > Attributes"],
                ["action",    "attributeimport/import/index",                 "frontName/controller/action URL"],
                ["sortOrder", "70",                                           "Position after Rating (sortOrder 60)"],
                ["resource",  "Aichouchm_AttributeImport::import_attributes", "ACL resource that gates access"],
            ],
            col_widths=[2.5*cm, 6.5*cm, 8*cm]
        ),
        space(),

        h2("etc/acl.xml"),
        filepath("Aichouchm_AttributeImport/etc/acl.xml"),
        p("Registers the ACL resource in the Magento permission tree. Admin roles can be granted "
          "or denied this resource under <b>System &rarr; Permissions &rarr; User Roles</b>."),
        code(
"""Magento_Backend::stores
  `-- Magento_Backend::stores_attributes
        `-- Aichouchm_AttributeImport::import_attributes
              <- "Import Attributes" resource"""),
        space(),

        h2("etc/di.xml"),
        filepath("Aichouchm_AttributeImport/etc/di.xml"),
        p("Wires three things: the dedicated Monolog logger, the service interface binding, "
          "and injects the logger into the classes that need it."),
        code(
"""<!-- 1. Dedicated log handler: writes to var/log/attribute_import.log -->
<virtualType name="Aichouchm\\AttributeImport\\Logger\\Handler"
             type="Magento\\Framework\\Logger\\Handler\\Base">
    <arguments>
        <argument name="fileName">/var/log/attribute_import.log</argument>
    </arguments>
</virtualType>

<!-- 2. Named Monolog channel using the handler above -->
<virtualType name="Aichouchm\\AttributeImport\\Logger\\Logger"
             type="Magento\\Framework\\Logger\\Monolog">
    <arguments>
        <argument name="name">AttributeImport</argument>
        <argument name="handlers" xsi:type="array">
            <item name="default" xsi:type="object">
                Aichouchm\\AttributeImport\\Logger\\Handler
            </item>
        </argument>
    </arguments>
</virtualType>

<!-- 3. Inject the logger into classes that declare LoggerInterface $logger -->
<type name="Aichouchm\\AttributeImport\\Model\\ImportService">
    <arguments>
        <argument name="logger" xsi:type="object">
            Aichouchm\\AttributeImport\\Logger\\Logger
        </argument>
    </arguments>
</type>

<!-- 4. Bind interface -> concrete class -->
<preference for="Aichouchm\\AttributeImport\\Api\\ImportServiceInterface"
            type="Aichouchm\\AttributeImport\\Model\\ImportService"/>"""),
        callout("info", "Virtual types create a named DI object without a PHP class file. "
                "Magento's DI container builds the Monolog logger with the correct handler "
                "purely from XML. No Logger.php needed."),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 3 — Loading the Import Page
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("3  Loading the Import Page"), space()]
    story += [
        p("When the admin clicks <i>Import Attributes</i> in the menu, Magento routes the request "
          "to the Index controller, which returns a Page result. Magento then merges layout XML "
          "to build the page structure."),
        space(),

        h2("Controller/Adminhtml/AbstractAction.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/AbstractAction.php"),
        p("Base class for all four admin controllers. Defines <b>ADMIN_RESOURCE</b> once and "
          "houses the two request-validation helpers shared by Preview and Process."),
        code(
"""abstract class AbstractAction extends Action
{
    public const ADMIN_RESOURCE = 'Aichouchm_AttributeImport::import_attributes';

    // Shared by Preview and Process — moved here to avoid duplication.
    protected function assertValidRequest(): void
    {
        $files = $this->getRequest()->getFiles()->toArray();

        if (empty($files['import_file']['tmp_name'])) {
            throw new Exception('Please upload a CSV file.');
        }
        if (strtolower(pathinfo($files['import_file']['name'], PATHINFO_EXTENSION)) !== 'csv') {
            throw new Exception('Only CSV files are allowed.');
        }
        if (empty($this->getRequest()->getParam('attribute_code'))) {
            throw new Exception('Please select an attribute.');
        }
    }

    protected function getUploadedFilePath(): string
    {
        $files    = $this->getRequest()->getFiles()->toArray();
        $filePath = $files['import_file']['tmp_name'] ?? '';

        if (!is_readable($filePath)) {
            throw new Exception('Cannot read the uploaded file.');
        }
        return $filePath;
    }
}"""),
        callout("info", "All four controllers (Index, Preview, Process, Log) extend this class. "
                "Before this refactor each controller redeclared the same constant — a rename "
                "would have required four edits."),
        space(),

        h2("Controller/Adminhtml/Import/Index.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/Import/Index.php"),
        p("The simplest possible admin controller. Its only job is to declare which page to render."),
        code(
"""class Index extends AbstractAction implements HttpGetActionInterface
{
    public function execute(): Page
    {
        $resultPage = $this->resultPageFactory->create();
        $resultPage->setActiveMenu('Aichouchm_AttributeImport::import_attributes');
        $resultPage->getConfig()->getTitle()->prepend(__('Import Attribute Options'));
        return $resultPage;
    }
}"""),
        simple_table(
            ["Item", "Purpose"],
            [
                ["extends AbstractAction", "Inherits ADMIN_RESOURCE; Action auto-runs _isAllowed()"],
                ["resultPageFactory",      "Creates a Page result — never use 'new Page()' in Magento"],
                ["setActiveMenu()",        "Highlights the correct item in the left sidebar menu"],
                ["getTitle()->prepend()",  "Sets the browser tab title and admin page heading"],
            ],
            col_widths=[4.5*cm, 12.5*cm]
        ),
        space(),

        h2("view/adminhtml/layout/attributeimport_import_index.xml"),
        filepath("Aichouchm_AttributeImport/view/adminhtml/layout/attributeimport_import_index.xml"),
        p("The file name <b>attributeimport_import_index.xml</b> is not arbitrary — it is the "
          "page handle, built from frontName_controller_action. Magento loads this file "
          "automatically for every request to that URL."),
        code(
"""<page>
    <head>
        <css src="Aichouchm_AttributeImport::css/styles.css"/>
    </head>
    <body>
        <referenceContainer name="content">

            <block class="...Import\\Form"
                   name="attributeimport.form"/>

            <block class="...Import\\Preview"
                   name="attributeimport.preview"
                   template="...::import/preview.phtml"/>

            <block class="...Import\\Form\\Before"
                   name="attributeimport.before"
                   template="...::import/form/before.phtml"/>

        </referenceContainer>
    </body>
</page>"""),
        p("<b>referenceContainer name=\"content\"</b> targets the main content area that Magento's "
          "base admin layout already defines. This module adds its three blocks into that slot "
          "without touching the admin shell (header, sidebar, footer)."),
        simple_table(
            ["Block", "Class", "Responsibility"],
            [
                ["attributeimport.form",    "Import\\Form",        "Page wrapper with button bar"],
                ["attributeimport.preview", "Import\\Preview",     "Validation results table (hidden until Check Data)"],
                ["attributeimport.before",  "Import\\Form\\Before","JS logic + AJAX URLs"],
            ],
            col_widths=[4.5*cm, 4*cm, 8.5*cm]
        ),
        PageBreak(),

        h2("Block/Adminhtml/Import/Form.php  (Container)"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Import/Form.php"),
        p("Extends <b>Magento\\Backend\\Block\\Widget\\Form\\Container</b> which provides the "
          "standard admin page card with a button bar at the top. All buttons are managed via "
          "the <b>buttonList</b> API — no HTML written by hand."),
        code(
"""class Form extends Container
{
    protected $_mode = 'form';

    protected function _construct(): void
    {
        parent::_construct();

        // Remove buttons that do not apply to this page
        $this->buttonList->remove('back');
        $this->buttonList->remove('reset');

        // Rename the default Save button
        $this->buttonList->update('save', 'label',   __('Import'));
        $this->buttonList->update('save', 'id',      'import-button');
        $this->buttonList->update('save', 'class',   'primary disabled');
        $this->buttonList->update('save', 'onclick', 'attributeImport.submit()');

        // Add the Check Data button
        $this->buttonList->add('check-data-button', [
            'label'   => __('Check Data'),
            'id'      => 'check-data-button',
            'onclick' => 'attributeImport.checkData();',
        ]);

        // These three properties tell Container where to find its child form block
        $this->_objectId   = 'import_ids';
        $this->_blockGroup = 'Aichouchm_AttributeImport';
        $this->_controller = 'adminhtml_import';
    }
}"""),
        callout("info", "The three protected properties (_objectId, _blockGroup, _controller) "
                "tell Container to auto-discover its child block. It constructs the class name "
                "Block/Adminhtml/Import/Form/Form.php from _blockGroup + _controller. "
                "That is why the inner form class lives at exactly that path."),
        space(),

        h2("Block/Adminhtml/Import/Form/Form.php  (Generic)"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Import/Form/Form.php"),
        p("Extends <b>Magento\\Backend\\Block\\Widget\\Form\\Generic</b> which provides the "
          "<b>_formFactory</b> and the <b>_prepareForm()</b> hook. Override _prepareForm() "
          "to describe fields — Magento renders the HTML."),
        code(
"""protected function _prepareForm(): static
{
    $form = $this->_formFactory->create([
        'data' => [
            'id'      => 'attribute-import-form',
            'method'  => 'post',
            'enctype' => 'multipart/form-data',  // required for file uploads
        ],
    ]);

    $fieldset = $form->addFieldset('base_fieldset', [
        'legend' => __('Import Settings'),
    ]);

    // Dropdown: all user-defined select/multiselect attributes
    $fieldset->addField('attribute_code', 'select', [
        'name'     => 'attribute_code',
        'label'    => __('Select Attribute'),
        'required' => true,
        'values'   => $this->sourceAttributes->toOptionArray(),
        'onchange' => 'attributeImport.onAttributeChange();',
    ]);

    // File upload input
    $fieldset->addField('import_file', 'file', [
        'name'     => 'import_file',
        'label'    => __('CSV File'),
        'required' => true,
        'onchange' => 'attributeImport.onFileChange();',
    ]);

    $form->setUseContainer(true);  // renders the <form> tag
    $this->setForm($form);
    return parent::_prepareForm();
}"""),
        callout("warn", "setUseContainer(true) is mandatory. Without it the form tag is not "
                "rendered and the file upload POST never reaches the controller."),
        space(),

        h2("Model/Import/Source/Attributes.php"),
        filepath("Aichouchm_AttributeImport/Model/Import/Source/Attributes.php"),
        p("A Magento source model — implements <b>ArrayInterface</b> and provides "
          "<b>toOptionArray()</b> for the attribute dropdown. Only user-defined select and "
          "multiselect attributes are listed (visual swatch attributes also have "
          "frontend_input='select' in the database)."),
        code(
"""public function toOptionArray(): array
{
    if ($this->options !== null) {
        return $this->options;  // memoized: only loads once per request
    }

    $this->options = [['value' => '', 'label' => __('-- Please Select --')]];

    // Both filters pushed to SQL — only matching rows are loaded from DB
    $searchCriteria = $this->searchCriteriaBuilder
        ->addFilter('frontend_input', ['select', 'multiselect'], 'in')
        ->addFilter('is_user_defined', 1)
        ->create();

    $items = $this->attributeRepository
        ->getList('catalog_product', $searchCriteria)
        ->getItems();

    foreach ($items as $attribute) {
        $this->options[] = [
            'value' => $attribute->getAttributeCode(),
            'label' => sprintf('%s [%s]',
                $attribute->getDefaultFrontendLabel() ?? $attribute->getAttributeCode(),
                $attribute->getAttributeCode()
            ),
        ];
    }

    return $this->options;
}"""),
        p("Result for a store with color and size attributes:"),
        code(
"""[
    ['value' => '',      'label' => '-- Please Select --'],
    ['value' => 'color', 'label' => 'Color [color]'],
    ['value' => 'size',  'label' => 'Size [size]'],
]"""),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 4 — The Before Block & JavaScript
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("4  The Before Block and JavaScript"), space()]
    story += [
        p("The Before block's job is to generate server-side URLs and pass them into the "
          "JavaScript template. This is necessary because Magento appends a secret key "
          "to every admin URL (CSRF protection) — a URL hardcoded in JS would be rejected."),
        space(),

        h2("Block/Adminhtml/Import/Form/Before.php"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Import/Form/Before.php"),
        code(
"""class Before extends Template
{
    public function getPreviewUrl(): string
    {
        return $this->getUrl('attributeimport/import/preview');
        // e.g. https://magento.local/admin/attributeimport/import/preview/key/abc123/
    }

    public function getProcessUrl(): string
    {
        return $this->getUrl('attributeimport/import/process');
        // e.g. https://magento.local/admin/attributeimport/import/process/key/abc123/
    }
}"""),
        p("<b>getUrl()</b> is inherited from <b>Magento\\Backend\\Block\\Template</b>. "
          "It appends the admin secret key automatically:"),
        code(
"""// What getUrl() returns:
// https://magento.local/admin/attributeimport/import/preview/key/abc123/

// The key= parameter changes per session. Without it Magento returns 403.
// Generating URLs in PHP and passing them to JS is the only correct approach."""),
        space(),

        h2("view/adminhtml/templates/import/form/before.phtml"),
        filepath("Aichouchm_AttributeImport/view/adminhtml/templates/import/form/before.phtml"),
        p("The template renders the notification div, the preview container, and all the "
          "JavaScript. The JS is rendered via <b>$secureRenderer->renderTag()</b> — Magento's "
          "CSP-safe way to output inline scripts."),
        space(),
        h3("HTML structure rendered by this template"),
        code(
"""<!-- Notification bar: hidden by default, shown by showMessage() -->
<div id="import-notification" class="hidden"></div>

<!-- Preview section: hidden until Check Data is clicked -->
<div id="preview-section">
    <h2 id="validation-heading" class="hidden">Validation Results</h2>
    <div id="preview-container"></div>  <!-- Preview HTML injected here by AJAX -->
</div>"""),
        space(),
        h3("JavaScript: window.attributeImport object"),
        p("A single object exposed on window. All button onclick handlers call methods on it."),
        code(
"""window.attributeImport = {

    // Called by Check Data button: onclick="attributeImport.checkData()"
    checkData: function () {
        var formData = new FormData($('#attribute-import-form')[0]);
        $.ajax({
            url:         '$previewUrl',   // from block->getPreviewUrl()
            type:        'POST',
            data:        formData,
            contentType: false,           // must be false for multipart
            processData: false,           // must be false for FormData
            dataType:    'json',
            success: function (response) {
                if (!response.success) {
                    attributeImport.showMessage(response.message, 'error');
                    return;
                }
                $('#preview-container').html(response.data); // inject preview HTML
                $('#validation-heading').removeClass('hidden');

                if (response.is_valid) {
                    attributeImport.hideMessage();
                    attributeImport.enableImport();   // enable Import button
                } else {
                    attributeImport.showMessage('Validation failed...', 'error');
                    attributeImport.resetButtons();
                }
            },
            error: function () {
                attributeImport.showMessage('$serverError', 'error');
            }
        });
    },"""),
        code(
"""    // Called by Import button: onclick="attributeImport.submit()"
    submit: function () {
        var formData = new FormData($('#attribute-import-form')[0]);
        $.ajax({
            url:         '$processUrl',   // from block->getProcessUrl()
            type:        'POST',
            data:        formData,
            contentType: false,
            processData: false,
            dataType:    'json',
            success: function (response) {
                attributeImport.resetAfterSubmit();
                if (response.success) {
                    var msg = response.messages.join('<br>');
                    if (response.skipped > 0) {
                        msg += '<br><em>' + response.skipped + ' skipped (already exist)</em>';
                    }
                    attributeImport.showMessage(msg, 'success');
                } else {
                    attributeImport.showMessage(response.messages.join('<br>'), 'error');
                }
            }
        });
    },"""),
        code(
"""    // UI state helpers
    onAttributeChange: function () { this.resetState(); },
    onFileChange:      function () { this.resetState(); },

    resetState: function () {
        this.resetButtons();                           // Import disabled, Check enabled
        $('#validation-heading').addClass('hidden');
        $('#preview-container').html('');
        this.hideMessage();
    },

    enableImport: function () {
        $('#import-button').removeClass('disabled');
        $('#check-data-button').addClass('disabled');  // prevent double-validation
    },

    resetButtons: function () {
        $('#import-button').addClass('disabled');
        $('#check-data-button').removeClass('disabled');
    },

    showMessage: function (text, type) {
        $('#import-notification')
            .removeClass('hidden message-error message-success')
            .addClass('message ' + (type === 'success' ? 'message-success' : 'message-error'))
            .html('<div>' + text + '</div>');
    },

    hideMessage: function () {
        $('#import-notification')
            .addClass('hidden')
            .removeClass('message message-error message-success')
            .html('');
    }
};"""),
        callout("info", "contentType: false and processData: false are mandatory for jQuery AJAX "
                "file uploads. They tell jQuery not to serialize the FormData object and not to "
                "set a Content-Type header (the browser sets multipart/form-data with the correct "
                "boundary automatically)."),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 5 — Check Data Flow
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("5  Check Data Flow  (AJAX POST -> Preview controller)"), space()]
    story += [
        p("When the admin clicks <b>Check Data</b>, the JS sends a multipart POST to "
          "/attributeimport/import/preview. The controller validates the CSV and returns "
          "a JSON object containing rendered HTML."),
        space(),

        h2("Controller/Adminhtml/Import/Preview.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/Import/Preview.php"),
        code(
"""public function execute(): Json
{
    $result = $this->resultJsonFactory->create();
    try {
        // Step 1 — guard: reject bad HTTP requests before touching the file
        $this->assertValidRequest();

        // Step 2 — read the two POST inputs
        $attributeCode = $this->getRequest()->getParam('attribute_code');  // e.g. 'color'
        $filePath      = $this->getUploadedFilePath();                     // e.g. '/tmp/phpAb3x9'

        // Step 3 — validate the CSV (headers + every data row)
        $validation = $this->importService->validate($filePath, $attributeCode);

        // Step 4 — render the preview table as an HTML string (whether valid or not)
        $html = $this->renderPreviewBlock($validation['rows'], $validation['errors']);

        // Step 5 — return JSON; JS uses is_valid to decide whether to enable Import button
        return $result->setData([
            'success'  => true,
            'data'     => $html,
            'is_valid' => $validation['is_valid'],
        ]);
    } catch (Exception $e) {
        // assertValidRequest() or getUploadedFilePath() threw — return error JSON
        return $result->setData(['success' => false, 'message' => $e->getMessage()]);
    }
}"""),
        space(),
        h3("Step 1  —  assertValidRequest()"),
        p("Checks the HTTP layer before any file reading happens. Three conditions, each "
          "throws an Exception that is caught and returned as error JSON:"),
        code(
"""private function assertValidRequest(): void
{
    $files = $this->getRequest()->getFiles()->toArray();

    // 1a. A file must have been uploaded
    if (empty($files['import_file']['tmp_name'])) {
        throw new Exception('Please upload a CSV file.');
    }
    // 1b. Extension must be .csv  (pathinfo() reads the name, never executes it)
    if (strtolower(pathinfo($files['import_file']['name'], PATHINFO_EXTENSION)) !== 'csv') {
        throw new Exception('Only CSV files are allowed.');
    }
    // 1c. The attribute dropdown must have a selection
    if (empty($this->getRequest()->getParam('attribute_code'))) {
        throw new Exception('Please select an attribute.');
    }
}

// If any check fails, execute() catches the Exception and returns:
// { "success": false, "message": "Only CSV files are allowed." }"""),
        callout("warn", "This validates the HTTP request only — not the CSV content. "
                "CSV content (column names, row values) is validated later by Validator, "
                "never here."),
        space(),
        h3("Step 2  —  getUploadedFilePath()"),
        p("Reads the tmp path PHP wrote the upload to and confirms it is readable:"),
        code(
"""private function getUploadedFilePath(): string
{
    $files    = $this->getRequest()->getFiles()->toArray();
    $filePath = $files['import_file']['tmp_name'] ?? '';  // e.g. '/tmp/phpAb3x9'

    if (!is_readable($filePath)) {
        throw new Exception('Cannot read the uploaded file.');
    }
    return $filePath;
}"""),
        space(),
        h3("Step 3  —  importService->validate()  (the key call)"),
        p("This is where all CSV logic runs. The controller passes the tmp path and the "
          "selected attribute code. The return value is a three-key array:"),
        code(
"""$validation = $this->importService->validate('/tmp/phpAb3x9', 'color');

// What $validation contains for our running example (valid_color.csv):
[
    'is_valid'    => true,
    'errors'      => [],          // empty — no validation errors
    'swatch_type' => 1,           // SWATCH_VISUAL — color is a visual swatch attribute
    'rows'        => [
        ['attribute_code','store_view','value','hex_code','sort_order','is_default'],  // header
        ['color','default','Coral','#FF6B6B','1','1'],
        ['color','fr','Corail','#FF6B6B','1','1'],
        ['color','en','Coral','#FF6B6B','1','1'],
        ['color','default','Teal','#008080','2','0'],
        ['color','fr','Sarcelle','#008080','2','0'],
        ['color','en','Teal','#008080','2','0'],
        // ... Indigo rows
    ],
]

// What $validation contains when a row is invalid:
[
    'is_valid' => false,
    'errors'   => [
        'Row 2: hex_code "#ZZZ" is not a valid hex colour.',
        'Row 4: sort_order "abc" must be a positive integer.',
    ],
    'rows'     => [ ... ],   // all rows still returned so the table can be shown
]"""),
        callout("info", "rows is always returned even when is_valid is false. "
                "The preview table shows the full CSV with the error list above it — "
                "the admin can see exactly which rows failed without re-uploading."),
        space(),
        h3("Step 4  —  renderPreviewBlock()"),
        p("Turns the rows + errors arrays into an HTML string. Uses a minimal standalone "
          "layout — no full admin page load:"),
        code(
"""private function renderPreviewBlock(array $rows, array $errors): string
{
    return $this->layoutFactory->create()
        ->createBlock(PreviewBlock::class)
        ->setTemplate('Aichouchm_AttributeImport::import/preview.phtml')
        ->setData(compact('rows', 'errors'))   // passes both variables to the template
        ->toHtml();                            // executes template, returns HTML string
}

// $html will be something like:
// '<div class=\"admin__data-grid-outer-wrap\"><table ...>...</table></div>
//  <p class=\"note\">6 data rows found. <strong>All rows are valid...</strong></p>'"""),
        space(),
        h3("Step 5  —  JSON response"),
        p("The JSON the controller returns. jQuery reads it in <b>checkData()</b>:"),
        code(
"""// Valid CSV — JS injects $html into #preview-container and enables Import button:
{
    "success":  true,
    "data":     "<table ...>...</table>",   // rendered HTML
    "is_valid": true
}

// Invalid CSV — JS shows error messages, Import button stays disabled:
{
    "success":  true,
    "data":     "<div class=\\"messages\\">...</div><table ...>",
    "is_valid": false
}

// HTTP/request error (assertValidRequest threw) — JS shows the message string:
{
    "success": false,
    "message": "Please upload a CSV file."
}"""),
        space(),

        h2("Api/ImportServiceInterface.php"),
        filepath("Aichouchm_AttributeImport/Api/ImportServiceInterface.php"),
        p("Defines the public contract for the import service. Controllers type-hint this "
          "interface, not the concrete class. This makes unit testing possible — tests inject "
          "a mock instead of a real ImportService."),
        code(
"""interface ImportServiceInterface
{
    // Returns: ['is_valid' => bool, 'errors' => string[], 'rows' => array[]]
    public function validate(string $filePath, string $attributeCode): array;

    // Returns: ['success' => bool, 'messages' => string[],
    //           'imported' => int, 'skipped' => int]
    public function import(string $filePath, string $attributeCode): array;
}"""),
        space(),

        h2("Model/Csv/StreamingReader.php"),
        filepath("Aichouchm_AttributeImport/Model/Csv/StreamingReader.php"),
        p("Opens a CSV file and yields one row at a time via a PHP Generator. "
          "Peak memory is always one row (~1 KB) regardless of file size."),
        code(
"""public function read(string $filePath): Generator
{
    $handle = @fopen($filePath, 'r');
    if ($handle === false) {
        throw new RuntimeException('Cannot open CSV file: ' . $filePath);
    }

    try {
        $lineNumber = 0;
        while (($row = fgetcsv($handle, 0, ',', '"', '\\\\')) !== false) {
            yield $lineNumber => array_map('trim', $row);
            $lineNumber++;
        }
    } finally {
        fclose($handle);  // always closed, even if the caller throws mid-iteration
    }
}"""),
        p("Using our running example CSV, the generator yields:"),
        code(
"""$reader->read('/tmp/upload.csv'):

yield 0 => ['attribute_code','store_view','value','hex_code','sort_order','is_default']
yield 1 => ['color','default','Coral','#FF6B6B','1','1']
yield 2 => ['color','fr','Corail','#FF6B6B','1','1']
yield 3 => ['color','en','Coral','#FF6B6B','1','1']
yield 4 => ['color','default','Teal','#008080','2','0']
yield 5 => ['color','fr','Sarcelle','#008080','2','0']
yield 6 => ['color','en','Teal','#008080','2','0']"""),
        PageBreak(),

        h2("Model/Csv/Validator.php"),
        filepath("Aichouchm_AttributeImport/Model/Csv/Validator.php"),
        p("Stateless validator. Every method initialises its tracking variables locally "
          "and returns a value. No state is stored in class properties. This is critical "
          "because Magento DI creates services as singletons — a stateful validator would "
          "carry errors from one request into the next."),
        code(
"""class Validator
{
    public const SWATCH_NONE   = -1;  // plain select / multiselect / text swatch
    public const SWATCH_VISUAL =  1;  // visual swatch (hex colour per option)

    // Unified 6-column CSV — hex_code is always present; leave empty for non-visual attributes
    // attribute_code | store_view | value | hex_code | sort_order | is_default
    public const COL_ATTRIBUTE_CODE = 0;
    public const COL_STORE_VIEW     = 1;
    public const COL_VALUE          = 2;
    public const COL_SWATCH         = 3;
    public const COL_SORT_ORDER     = 4;
    public const COL_IS_DEFAULT     = 5;

    private const EXPECTED_HEADERS = [
        'attribute_code','store_view','value','hex_code','sort_order','is_default'
    ];
}"""),
        space(),
        h3("getSwatchType(string $attributeCode): int"),
        p("Loads the attribute from the database and reads its <b>additional_data</b> JSON. "
          "Returns a constant that controls whether <b>hex_code</b> must be validated and "
          "whether a row must be written to <b>eav_attribute_option_swatch</b>."),
        p("Important: all swatch attributes (visual and text) store "
          "<b>frontend_input = 'select'</b> in the database — the swatch type is kept "
          "separately in the <b>additional_data</b> JSON column of <b>catalog_eav_attribute</b>. "
          "That is why they appear in the attribute dropdown alongside plain select attributes."),
        simple_table(
            ["Attribute", "frontend_input (DB)", "additional_data (DB)", "getSwatchType() returns"],
            [
                ["color",    "select",      '{"swatch_input_type":"visual"}', "SWATCH_VISUAL = 1"],
                ["size",     "select",      '{"swatch_input_type":"text"}',   "SWATCH_NONE = -1"],
                ["material", "multiselect", "NULL",                           "SWATCH_NONE = -1"],
            ],
            col_widths=[3*cm, 4*cm, 7*cm, 4*cm]
        ),
        space(),
        code(
"""// Uses Magento\\Eav\\Model\\Config — three cache layers:
//   1. in-memory $this->attributes[...] — free on repeated calls within a request
//   2. Magento cache (eav cache type) — survives across requests
//   3. DB fallback — only on a cold cache
// Old approach: attributeFactory->create()->loadByCode() — always hits the DB.

public function getSwatchType(string $attributeCode): int
{
    $attribute  = $this->eavConfig->getAttribute(Product::ENTITY, $attributeCode);
    $additional = json_decode($attribute->getAdditionalData() ?? '{}', true, 512, JSON_THROW_ON_ERROR);

    return match ($additional['swatch_input_type'] ?? null) {
        'visual' => self::SWATCH_VISUAL,  // hex_code must be a valid #RRGGBB
        default  => self::SWATCH_NONE,    // hex_code column exists but is ignored
    };
}

// color    → {"swatch_input_type":"visual"} → SWATCH_VISUAL → hex validated
// size     → {"swatch_input_type":"text"}   → SWATCH_NONE   → hex ignored
// material → NULL                           → SWATCH_NONE   → hex ignored"""),
        space(),
        h3("validateHeaders(array $headerRow): array"),
        p("Checks the header row against the single fixed format. "
          "Returns early if the column count is wrong — no point checking names if offsets are off."),
        code(
"""// One format for all attribute types:
// ['attribute_code','store_view','value','hex_code','sort_order','is_default']
//
// For visual swatch:  hex_code filled  → color,default,Coral,#FF6B6B,1,1
// For plain select:   hex_code empty   → material,default,Linen,,1,1

public function validateHeaders(array $headerRow): array
{
    if (count($headerRow) !== count(self::EXPECTED_HEADERS)) {
        return ['Invalid column count: expected 6, got N. Expected: ...'];
    }

    $errors = [];
    foreach ($headerRow as $i => $cell) {
        if (strtolower(trim($cell)) !== self::EXPECTED_HEADERS[$i]) {
            $errors[] = 'Column 4: expected "hex_code", got "swatch"';
        }
    }
    return $errors;
}

// Running example: validateHeaders(['attribute_code','store_view','value','hex_code','sort_order','is_default'])
// -> [] (no errors)"""),
        space(),
        h3("validateRows(array $rows, string $attributeCode, int $swatchType): array"),
        p("The most complex method. Loops through all data rows (header excluded) and "
          "enforces rules that span multiple rows. Uses four tracking variables:"),
        simple_table(
            ["Variable", "Type", "Tracks"],
            [
                ["$adminValues",     "array",  "All default-store values seen — detects CSV duplicates"],
                ["$optionStores",    "array",  "Store codes in the current option group — detects duplicate stores"],
                ["$defaultSelected", "bool",   "Whether any row has is_default=1 — only one allowed"],
            ],
            col_widths=[3.5*cm, 2*cm, 11.5*cm]
        ),
        space(),
        p("Step-by-step walk through the running example:"),
        code(
"""// Input: data rows only (header already stripped by ImportService)
Row 1: ['color','default','Coral','#FF6B6B','1','1']
  isAdmin=true  -> new group starts
  $optionStores = []   (reset for this new group)
  'Coral' not in $adminValues -> add it: $adminValues=['Coral']
  sort_order='1'  -> is_numeric(1) OK
  is_default='1'  -> $defaultSelected=true
  hex '#FF6B6B'   -> matches /^#[A-Fa-f0-9]{6}$/ OK

Row 2: ['color','fr','Corail','#FF6B6B','1','1']
  isAdmin=false -> translation row (fr store)
  'fr' is a valid Magento store code -> OK
  'fr' not in $optionStores -> add it: $optionStores=['fr']

Row 3: ['color','en','Coral','#FF6B6B','1','1']
  isAdmin=false -> translation row (en store)
  'en' is a valid store code -> OK
  'en' not in $optionStores -> $optionStores=['fr','en']

Row 4: ['color','default','Teal','#008080','2','0']
  isAdmin=true  -> new group starts
  $optionStores = []   (reset for this new group)
  'Teal' not in $adminValues -> $adminValues=['Coral','Teal']
  is_default='0' -> $defaultSelected still true from row 1, no conflict

Result: [] — empty array means the file is valid, Import button enabled"""),
        callout("good", "Adding a duplicate row ['color','default','Coral','#FF6B6B','4','0'] "
                "at the end would produce: \"Row 7: Duplicate option value Coral within the CSV\". "
                "The check is O(n) per row — in_array scans the already-built $adminValues array."),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 6 — Import Flow
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("6  Import Flow  (AJAX POST -> Process controller)"), space()]
    story += [
        p("After successful Check Data the Import button is enabled. Clicking it sends "
          "the same multipart POST to the Process controller, which calls "
          "ImportService::import()."),
        space(),

        h2("Controller/Adminhtml/Import/Process.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/Import/Process.php"),
        p("Same structure as Preview: validate request, call service, return JSON. "
          "The difference is it calls <b>import()</b> instead of <b>validate()</b> "
          "and returns counts instead of HTML."),
        code(
"""public function execute(): Json
{
    $result = $this->resultJsonFactory->create();
    try {
        $this->assertValidRequest();
        $attributeCode = $this->getRequest()->getParam('attribute_code');
        $filePath      = $this->getUploadedFilePath();

        $importResult = $this->importService->import($filePath, $attributeCode);

        return $result->setData([
            'success'  => $importResult['success'],
            'messages' => $importResult['messages'],
            'imported' => $importResult['imported'],
            'skipped'  => $importResult['skipped'],
        ]);
    } catch (Exception $e) {
        $this->logger->error('Controller error: ' . $e->getMessage());
        return $result->setData([
            'success'  => false,
            'messages' => ['An unexpected error occurred. See attribute_import.log for details.'],
            'imported' => 0,
            'skipped'  => 0,
        ]);
    }
}"""),
        space(),

        h2("Model/ImportService.php"),
        filepath("Aichouchm_AttributeImport/Model/ImportService.php"),
        p("The main orchestrator. Implements ImportServiceInterface and coordinates "
          "StreamingReader, Validator, OptionProcessor, CacheManager, and Logger."),
        space(),
        h3("validate(string $filePath, string $attributeCode): array"),
        code(
"""public function validate(string $filePath, string $attributeCode): array
{
    try {
        [$swatchType, $allRows] = $this->readAllRows($filePath, $attributeCode);

        // Step 1: validate headers (column count + names — always 6 columns)
        $headerErrors = $this->csvValidator->validateHeaders($allRows[0] ?? []);
        if (!empty($headerErrors)) {
            // Wrong columns means row offsets are wrong too — stop immediately
            return ['is_valid' => false, 'errors' => $headerErrors, 'rows' => []];
        }

        // Step 2: validate all data rows
        $dataRows  = array_slice($allRows, 1);
        $rowErrors = $this->csvValidator->validateRows($dataRows, $attributeCode, $swatchType);

        return [
            'is_valid' => empty($rowErrors),
            'errors'   => $rowErrors,
            'rows'     => $allRows,  // passed back for the preview table
        ];
    } catch (Throwable $e) {
        return ['is_valid' => false, 'errors' => [$e->getMessage()], 'rows' => []];
    }
}"""),
        space(),
        h3("readAllRows(string $filePath, string $attributeCode): array"),
        p("Reads all CSV rows into memory. Validation requires cross-row rules (duplicates, "
          "is_default uniqueness), so the entire file must be in memory at once."),
        code(
"""private function readAllRows(string $filePath, string $attributeCode): array
{
    return [
        $this->csvValidator->getSwatchType($attributeCode),
        // iterator_to_array() drains the generator into a plain array.
        // false = do not preserve generator keys (gives 0,1,2,... not the line numbers)
        iterator_to_array($this->streamingReader->read($filePath), false),
    ];
}

// Result for the running example (valid_color.csv with Coral + Teal):
// [
//   SWATCH_VISUAL,   // swatchType — color is a visual swatch attribute
//   [
//     ['attribute_code','store_view','value','hex_code','sort_order','is_default'], // row 0 (header)
//     ['color','default','Coral','#FF6B6B','1','1'],   // row 1
//     ['color','fr','Corail','#FF6B6B','1','1'],        // row 2
//     ...
//   ]
// ]"""),
        space(),
        h3("import(string $filePath, string $attributeCode): array"),
        code(
"""public function import(string $filePath, string $attributeCode): array
{
    $this->logger->info('Import started — attribute: ' . $attributeCode);

    try {
        // 1. Re-validate (safety net: import should never run on bad data)
        $validation = $this->validate($filePath, $attributeCode);
        if (!$validation['is_valid']) {
            foreach ($validation['errors'] as $error) {
                $this->logger->error('Validation error: ' . $error);
            }
            return ['success' => false, 'messages' => $validation['errors'],
                    'imported' => 0, 'skipped' => 0];
        }

        // 2. Reuse swatch type and rows from validate() — no second file read, no second DB call
        $attribute       = $this->eavConfig->getAttribute('catalog_product', $attributeCode);
        $swatchType      = $validation['swatch_type'];
        $existingOptions = $this->loadExistingOptions((int) $attribute->getAttributeId());

        // 3. Group already-loaded rows by option (no file re-read — rows were loaded in validate())
        $groups = $this->groupRowsByOption($validation['rows']);

        // 4. Write to DB
        $result = $this->optionProcessor->processGroups(
            $groups, $existingOptions, $swatchType, $attribute
        );

        // 5. Log skipped values
        foreach ($result['skippedValues'] as $val) {
            $this->logger->warning('Skipped: "' . $val . '" already exists.');
        }

        // 6. Flush caches
        $this->cacheManager->clean(['eav', 'full_page', 'block_html']);

        $summary = 'Import complete. Imported: ' . $result['imported'] .
                   ', Skipped: ' . $result['skipped'];
        $this->logger->info($summary);

        return ['success' => true, 'messages' => [$summary],
                'imported' => $result['imported'], 'skipped' => $result['skipped']];

    } catch (Throwable $e) {
        $this->logger->error('Unexpected error: ' . $e->getMessage());
        return ['success' => false,
                'messages' => ['An unexpected error occurred. Please check the import log.'],
                'imported' => 0, 'skipped' => 0];
    }
}"""),
        space(),
        h3("loadExistingOptions(int $attributeId): array"),
        p("Pre-loads all existing option labels for the attribute at store_id=0 (admin store). "
          "This is a single DB query. The result is used as a hash map for O(1) duplicate checks — "
          "no DB call per option during import."),
        code(
"""private function loadExistingOptions(int $attributeId): array
{
    $connection = $this->resourceConnection->getConnection();
    $select = $connection->select()
        ->from(['v' => 'eav_attribute_option_value'], ['value', 'v.option_id'])
        ->join(['o' => 'eav_attribute_option'], 'v.option_id = o.option_id', [])
        ->where('o.attribute_id = ?', $attributeId)
        ->where('v.store_id = ?', 0);  // store_id=0 = admin (global) store

    $result = [];
    foreach ($connection->fetchAll($select) as $row) {
        $result[$row['value']] = (int) $row['option_id'];
    }
    return $result;
}

// If Coral and Teal already exist in the DB, returns:
// ['Coral' => 45, 'Teal' => 46]
// Used as an O(1) hash-map: array_key_exists('Coral', $existing) is true -> skip."""),
        space(),
        h3("groupRowsByOption(array $rows): array"),
        p("Receives the already-loaded rows array (from <b>readAllRows</b>) and groups them "
          "into logical option objects. A new group starts every time a default/admin row "
          "appears. The header row (index 0) is skipped with <b>array_slice($rows, 1)</b>. "
          "The result is a flat list of groups — each group has one 'admin' key (the global "
          "row with sort_order and is_default) and a 'stores' key (translation rows)."),
        code(
"""private function groupRowsByOption(array $rows): array
{
    $groups       = [];
    $currentGroup = null;

    foreach (array_slice($rows, 1) as $row) {   // skip header row at index 0
        $storeCode = strtolower(trim($row[CsvValidator::COL_STORE_VIEW] ?? ''));
        $isAdmin   = in_array($storeCode, ['admin', 'default'], true);

        if ($isAdmin) {
            if ($currentGroup !== null) {
                $groups[] = $currentGroup;  // save the just-completed group
            }
            $currentGroup = ['admin' => $row, 'stores' => []];
        } elseif ($currentGroup !== null) {
            $currentGroup['stores'][] = $row;   // add translation row to current group
        }
    }

    if ($currentGroup !== null) {
        $groups[] = $currentGroup;  // save the last group (no next admin row follows it)
    }

    return $groups;
}

// Running example — applying this to the 6-row CSV (2 options, 2 stores each):
//
// Input $rows (after array_slice, no header):
//   row 0: ['color','default','Coral','#FF6B6B','1','1']  <- isAdmin=true  -> starts group 1
//   row 1: ['color','fr','Corail','#FF6B6B','1','1']      <- isAdmin=false -> goes to group 1 stores
//   row 2: ['color','en','Coral','#FF6B6B','1','1']       <- isAdmin=false -> goes to group 1 stores
//   row 3: ['color','default','Teal','#008080','2','0']   <- isAdmin=true  -> saves group 1, starts group 2
//   row 4: ['color','fr','Sarcelle','#008080','2','0']    <- isAdmin=false -> goes to group 2 stores
//   row 5: ['color','en','Teal','#008080','2','0']        <- isAdmin=false -> goes to group 2 stores
//   (loop ends)                                           -> saves group 2
//
// Output $groups:
// [
//   [
//     'admin'  => ['color','default','Coral','#FF6B6B','1','1'],
//     'stores' => [
//       ['color','fr','Corail','#FF6B6B','1','1'],
//       ['color','en','Coral','#FF6B6B','1','1'],
//     ]
//   ],
//   [
//     'admin'  => ['color','default','Teal','#008080','2','0'],
//     'stores' => [
//       ['color','fr','Sarcelle','#008080','2','0'],
//       ['color','en','Teal','#008080','2','0'],
//     ]
//   ],
// ]"""),
        PageBreak(),

        h2("Service/StoreResolver.php"),
        filepath("Aichouchm_AttributeImport/Service/StoreResolver.php"),
        p("Maps store codes from the CSV to Magento store_ids for database writes. "
          "The brief (Section 4) defines the CSV format with <b>store_view = 'default'</b> "
          "as the global row — so both 'default' and 'admin' are accepted as aliases for store_id=0."),
        code(
"""public function getStoreId(string $storeCode): int
{
    // Brief section 4 CSV uses 'default' for the global row.
    // 'admin' accepted as well since it is Magento's internal admin store code.
    if (in_array(strtolower($storeCode), ['admin', 'default'], true)) {
        return 0;
    }
    return (int) $this->storeManager->getStore($storeCode)->getId();
}

public function isValidStoreCode(string $storeCode): bool
{
    if (in_array(strtolower($storeCode), ['admin', 'default'], true)) {
        return true;
    }
    return in_array($storeCode, $this->getAllStoreCodes(), true);
}

// Memoized — storeManager->getStores() is only called once per request.
// validateRows() calls isValidStoreCode() once per data row — without memoization
// a 500-row CSV would hit StoreManager 500 times.
private array $storeCodes = [];

public function getAllStoreCodes(): array
{
    if (!empty($this->storeCodes)) {
        return $this->storeCodes;
    }
    foreach ($this->storeManager->getStores() as $store) {
        $this->storeCodes[] = $store->getCode();
    }
    return $this->storeCodes;
}"""),
        p("Running example — mapping every CSV store_view to a DB store_id:"),
        code(
"""// store_view column values from the running example CSV:
getStoreId('default') -> 0   // intercepted — brief defines this as the global row
getStoreId('fr')      -> 2   // StoreManager lookup — French store view
getStoreId('en')      -> 3   // StoreManager lookup — English store view

// getAllStoreCodes() on a store with fr + en views returns:
['default', 'fr', 'en']"""),
        callout("warn", "StoreManager->getStore('default') returns store_id=1 (the Default "
                "Store View), NOT store_id=0. Passing 'default' through StoreManager would "
                "save labels to the wrong store. The explicit alias intercepts 'default'/'admin' "
                "before reaching StoreManager, as required by the brief's CSV format."),
        space(),

        h2("Model/Attribute/OptionProcessor.php"),
        filepath("Aichouchm_AttributeImport/Model/Attribute/OptionProcessor.php"),
        p("Writes all new options to the database in the minimum number of queries. "
          "Skips options whose label already exists in $existingOptions."),
        space(),
        h3("processGroups() — the core DB write loop"),
        code(
"""public function processGroups(
    array $groups,
    array $existingOptions,  // e.g. [] if DB is empty, or ['Coral' => 45] if Coral already exists
    int $swatchType,
    AttributeInterface $attribute
): array {
    $newOptions = [];  // keyed by 'new_0', 'new_1', etc. (before DB insert)
    $labelRows  = [];  // flat array of all label rows to batch-insert
    $swatchRows = [];  // flat array of all swatch rows to batch-insert
    $defaultKey = null;
    $skipped    = [];

    foreach ($groups as $group) {
        $adminRow = $group['admin'];
        $value    = $adminRow[CsvValidator::COL_VALUE];   // col 2

        // O(1) duplicate check using the pre-loaded hash map
        if (array_key_exists($value, $existingOptions)) {
            $skipped[] = $value;
            continue;
        }

        $key = 'new_' . count($newOptions);  // temporary key before INSERT

        $newOptions[$key] = [
            'attribute_id' => $attribute->getAttributeId(),
            'sort_order'   => (int) ($adminRow[CsvValidator::COL_SORT_ORDER] ?? 0),  // col 4
        ];

        if (($adminRow[CsvValidator::COL_IS_DEFAULT] ?? '0') === '1') {  // col 5
            $defaultKey = $key;  // remember which option is the default
        }

        // Admin (global) label
        $labelRows[] = ['key' => $key, 'store_id' => 0, 'value' => $value];

        // Swatch row — col 3 (hex_code) only written when attribute is visual swatch
        if ($swatchType !== CsvValidator::SWATCH_NONE) {
            $swatchRows[] = [
                'key'      => $key,
                'store_id' => 0,
                'type'     => 1,      // 1 = visual hex colour
                'value'    => $adminRow[CsvValidator::COL_SWATCH] ?? '',  // col 3
            ];
        }

        // Per-store-view translation labels
        foreach ($group['stores'] as $storeRow) {
            $storeId     = $this->storeResolver->getStoreId($storeRow[CsvValidator::COL_STORE_VIEW]);
            $labelRows[] = ['key' => $key, 'store_id' => $storeId,
                            'value' => $storeRow[CsvValidator::COL_VALUE]];
        }
    }

    if (!empty($newOptions)) {
        $this->bulkSave($newOptions, $labelRows, $swatchRows, $defaultKey, $attribute);
    }

    return [
        'imported'      => count($newOptions),
        'skipped'       => count($skipped),
        'skippedValues' => $skipped,
    ];
}"""),
        space(),
        h3("bulkSave() — the actual DB writes"),
        code(
"""private function bulkSave(
    array $newOptions, array $labelRows, array $swatchRows,
    ?string $defaultKey, AttributeInterface $attribute
): void {
    $connection = $this->resourceConnection->getConnection();

    // All writes wrapped in a transaction — if any query fails, everything rolls back cleanly.
    $connection->beginTransaction();
    try {
        // 1. One INSERT per option — required to capture each lastInsertId
        //    Cannot use insertMultiple here because we need the DB-assigned option_id
        //    for each row before we can build the label/swatch rows.
        $keyToOptionId = [];
        foreach ($newOptions as $key => $optionData) {
            $connection->insert('eav_attribute_option', $optionData);
            $keyToOptionId[$key] = (int) $connection->lastInsertId();
        }

        // 2. ALL labels in ONE batch query.
        $labelInserts = [];
        foreach ($labelRows as $lr) {
            $labelInserts[] = [
                'option_id' => $keyToOptionId[$lr['key']],
                'store_id'  => $lr['store_id'],
                'value'     => $lr['value'],
            ];
        }
        $connection->insertOnDuplicate('eav_attribute_option_value', $labelInserts, ['value']);

        // 3. Set is_default on the attribute record if any option had is_default=1
        if ($defaultKey !== null && isset($keyToOptionId[$defaultKey])) {
            $connection->update('eav_attribute',
                ['default_value' => (string) $keyToOptionId[$defaultKey]],
                ['attribute_id = ?' => $attribute->getAttributeId()]
            );
        }

        // 4. ALL swatches in ONE query
        if (!empty($swatchRows)) {
            $swatchInserts = [];
            foreach ($swatchRows as $sr) {
                $swatchInserts[] = [
                    'option_id' => $keyToOptionId[$sr['key']],
                    'store_id'  => $sr['store_id'],
                    'type'      => $sr['type'],
                    'value'     => $sr['value'],
                ];
            }
            $connection->insertOnDuplicate('eav_attribute_option_swatch',
                $swatchInserts, ['type', 'value']);
        }

        $connection->commit();
    } catch (Throwable $e) {
        $connection->rollBack();
        throw $e;  // re-throw so ImportService can log and return failure
    }
}"""),
        p("Total DB queries for N new options (each with S store views):"),
        simple_table(
            ["Query", "Count", "Description"],
            [
                ["INSERT eav_attribute_option",       "N",   "One per new option (needs lastInsertId)"],
                ["INSERT eav_attribute_option_value",  "1",   "All labels in one batch INSERT"],
                ["UPDATE eav_attribute",               "0-1", "Only if any option has is_default=1"],
                ["INSERT eav_attribute_option_swatch", "0-1", "All swatches in one batch INSERT"],
            ],
            col_widths=[5.5*cm, 1.5*cm, 10*cm]
        ),
        callout("good", "For 200 options with 3 store views: N+2 = 202 queries total. "
                "Compared to attributeRepository->save() per option which triggers a full "
                "EAV load + save cycle (~600 queries). Measured ~40x faster on a local Docker stack."),
        space(),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 7 — Preview Block and Template
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("7  Preview Block and Template"), space()]
    story += [
        h2("Block/Adminhtml/Import/Preview.php"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Import/Preview.php"),
        p("Minimal block — extends Template and exposes one helper method used by the template."),
        code(
"""class Preview extends Template
{
    public function formatHeader(string $value): string
    {
        return ucwords(str_replace('_', ' ', strtolower($value)));
    }
}

// Examples:
// formatHeader('attribute_code') -> 'Attribute Code'
// formatHeader('hex_code')       -> 'Hex Code'
// formatHeader('is_default')     -> 'Is Default'"""),
        space(),

        h2("view/adminhtml/templates/import/preview.phtml"),
        filepath("Aichouchm_AttributeImport/view/adminhtml/templates/import/preview.phtml"),
        p("Receives <b>$rows</b> (full CSV as 2D array including header) and <b>$errors</b> "
          "(validation error strings). If $errors is non-empty, shows red messages. "
          "If $rows has more than one row (header + at least one data row), renders a table."),
        code(
"""<?php if (!empty($errors)): ?>
    <div class="messages">
        <?php foreach ($errors as $error): ?>
            <!-- No inner <div> — avoids Magento's ::before icon pseudo-element -->
            <div class="message message-error">
                <?= $block->escapeHtml($error) ?>
            </div>
        <?php endforeach; ?>
    </div>
<?php endif; ?>

<?php if (!empty($rows) && count($rows) > 1): ?>
    <div class="admin__data-grid-outer-wrap">
        <table class="data-grid admin__table-primary">
            <thead>
                <tr>
                    <?php foreach ($rows[0] as $header): ?>
                        <th><?= $block->escapeHtml($block->formatHeader($header)) ?></th>
                    <?php endforeach; ?>
                </tr>
            </thead>
            <tbody>
                <?php foreach (array_slice($rows, 1) as $rowIndex => $row): ?>
                    <tr class="<?= $rowIndex % 2 === 0 ? '_even-row' : '_odd-row' ?>">
                        <?php foreach ($row as $cell): ?>
                            <td><?= $block->escapeHtml($cell) ?></td>
                        <?php endforeach; ?>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    <p class="note">
        <?= count($rows) - 1 ?> data rows found.
        <?php if (empty($errors)): ?>
            <strong>All rows are valid. You can proceed with the import.</strong>
        <?php endif; ?>
    </p>
<?php endif; ?>"""),
        callout("info", "array_slice($rows, 1) skips row 0 (the header) when building the "
                "table body. $rows[0] is used only for the header row. "
                "count($rows) > 1 prevents rendering an empty table if the CSV has only a header."),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 8 — Log Viewer
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("8  Log Viewer"), space()]
    story += [
        h2("Controller/Adminhtml/Import/Log.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/Import/Log.php"),
        p("Standard page controller. Returns a Page result and sets the page title. "
          "Same structure as Index — only the title string differs."),
        code(
"""class Log extends AbstractAction
{
    public function __construct(
        Context                      $context,
        private readonly PageFactory $resultPageFactory
    ) {
        parent::__construct($context);
    }

    public function execute(): Page
    {
        $resultPage = $this->resultPageFactory->create();
        $resultPage->setActiveMenu('Aichouchm_AttributeImport::import_attributes');
        $resultPage->getConfig()->getTitle()->prepend(__('Attribute Import Log'));
        return $resultPage;
    }
}"""),
        space(),

        h2("Block/Adminhtml/Log.php"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Log.php"),
        p("Reads the log file from the filesystem and returns the lines in reverse order "
          "(newest first) for display in the admin."),
        code(
"""class Log extends Template
{
    private const LOG_FILE      = 'log/attribute_import.log';
    private const DEFAULT_LINES = 200;

    public function getLogLines(int $limit = self::DEFAULT_LINES): array
    {
        try {
            $varDir = $this->filesystem->getDirectoryRead(DirectoryList::VAR_DIR);

            if (!$varDir->isExist(self::LOG_FILE)) {
                return [];
            }

            $content = $varDir->readFile(self::LOG_FILE);
            $lines   = array_reverse(array_filter(explode("\\n", $content)));
            return array_slice($lines, 0, $limit);

        } catch (\\Throwable) {
            return [];
        }
    }

    public function getLogUrl():    string { return $this->getUrl('attributeimport/import/log'); }
    public function getImportUrl(): string { return $this->getUrl('attributeimport/import/index'); }
}"""),
        p("Key decisions:"),
        simple_table(
            ["Decision", "Reason"],
            [
                ["LOG_FILE = 'log/attribute_import.log'",
                 "Path relative to VAR_DIR. Using Magento's Filesystem abstraction instead of "
                 "fopen() means the path resolves correctly regardless of deployment type (local, cloud)."],
                ["array_reverse()",
                 "Newest entries at the top — the admin sees the most recent import immediately "
                 "without scrolling to the bottom."],
                ["array_filter()",
                 "Removes empty strings that appear when explode() splits on a trailing newline "
                 "at the end of the file."],
                ["catch Throwable return []",
                 "If the log file is unreadable (permissions, missing), the page shows an empty "
                 "state instead of a 500 error."],
            ],
            col_widths=[5*cm, 12*cm]
        ),
        space(),

        h2("view/adminhtml/templates/import/log.phtml"),
        filepath("Aichouchm_AttributeImport/view/adminhtml/templates/import/log.phtml"),
        p("Renders the log lines in a dark monospace terminal-style box. Lines are colour-coded "
          "by Monolog log level, detected by searching for the level string in the line."),
        code(
"""// Monolog line format:
// [2026-04-15 14:32:01] AttributeImport.INFO: Import started — attribute: color [] []
// [2026-04-15 14:32:01] AttributeImport.WARNING: Skipped: "Coral" already exists. [] []
// [2026-04-15 14:32:01] AttributeImport.ERROR: Validation error: Row 2... [] []

// Colour detection:
$colour = '#d4d4d4';                                 // default: light grey
if (stripos($trimmed, '.ERROR')   !== false) $colour = '#f88585';  // red
if (stripos($trimmed, '.WARNING') !== false) $colour = '#ffd580';  // amber
if (stripos($trimmed, '.INFO')    !== false) $colour = '#87d7a0';  // green"""),
        simple_table(
            ["Level", "Colour", "When logged"],
            [
                ["INFO",    "Green (#87d7a0)", "Import started; import completed with counts"],
                ["WARNING", "Amber (#ffd580)", "Option skipped because it already exists in DB"],
                ["ERROR",   "Red (#f88585)",   "Validation failure; unexpected exception"],
            ],
            col_widths=[2.5*cm, 4.5*cm, 10*cm]
        ),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 9 — Refactoring Log
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("9  Refactoring Log"), space()]
    story += [
        p("Changes made during development to simplify the code. Each entry explains "
          "what was removed and why."),
        space(),
        simple_table(
            ["What", "Before", "After", "Why"],
            [
                ["Swatch column aliases",
                 "SWATCH_COL_NAMES = ['swatch','hex_code','swatch_value','color']",
                 "SWATCH_COLUMN = 'hex_code'",
                 "Only hex_code is documented. Other aliases were never in the spec."],
                ["validateHeaders() loop",
                 "if (is_array($exp)) { in_array(...) } elseif ($cell !== $exp) ...",
                 "if ($cell !== $expected[$i]) ...",
                 "Once SWATCH_COL_NAMES became a single string, the is_array branch became dead code."],
                ["Text swatch support",
                 "SWATCH_TEXT constant, SWATCH_TEXT branch in processGroups(), detectSwatchType() returning 0/1/2",
                 "Removed entirely",
                 "Not in the functional spec. The spec shows only hex colour swatches."],
                ["Image URL swatches",
                 "isValidSwatchValue() checked both hex and URL regex",
                 "Only hex /^#[A-Fa-f0-9]{6}$/ checked",
                 "Not in the spec. Simplifies validation."],
                ["Store code '0' alias",
                 "in_array(..., ['admin','default','0'])",
                 "in_array(..., ['admin','default'])",
                 "Nobody writes '0' as a store code in a CSV. Undocumented edge case."],
                ["Log block DI injection",
                 "$logFile injected via di.xml as '/var/log/attribute_import.log', then stripped with str_replace('/var/','',...)",
                 "private const LOG_FILE = 'log/attribute_import.log'",
                 "Circular: injecting /var/log/x only to strip /var/ immediately. Constant is simpler."],
                ["readAllRows() loop",
                 "foreach ($reader->read()) as $row) { $rows[] = $row; }",
                 "iterator_to_array($reader->read(), false)",
                 "PHP built-in that does the same thing in one line."],
                ["AJAX URL generation",
                 "toRelativePath() stripped scheme/host/port from getUrl()",
                 "getUrl() used directly",
                 "toRelativePath() was a workaround for a dev environment port mismatch. Not a module concern."],
                ["Magic column indexes",
                 "$row[0], $row[1], $row[3] scattered across Validator, OptionProcessor, ImportService",
                 "Public COL_* constants on Validator, referenced everywhere",
                 "Magic numbers are silent bugs. A column rename or addition broke three files at once."],
                ["Dual CSV formats",
                 "5-column CSV for plain select, 6-column for visual swatch. dataColumnOffsets() computed shifting offsets at runtime.",
                 "Single 6-column format. hex_code always present, empty for non-swatch. COL_SORT_ORDER=4, COL_IS_DEFAULT=5 are fixed.",
                 "The shifting offset logic existed only to support the dual format. One format eliminates the complexity entirely and gives the admin a single CSV template."],
                ["ADMIN_RESOURCE duplication",
                 "public const ADMIN_RESOURCE = '...' redeclared identically in all four controllers (Index, Preview, Process, Log).",
                 "Single declaration in AbstractAction; all controllers extend it.",
                 "A rename of the ACL resource required four edits and could silently diverge. Single source of truth eliminates the risk."],
            ],
            col_widths=[3.5*cm, 4.5*cm, 3.5*cm, 5.5*cm]
        ),
        space(2),
        hr(),
        PageBreak(),

        # ── Section 10 — Demo Test Plan ────────────────────────────────────────
        h1("10  Demo Test Plan"),
        p("All test files are in <b>Test/sample/</b>. Run the tests in order — "
          "Tests 4 and 7 depend on data written by earlier tests."),
        space(),
        simple_table(
            ["File", "Attribute", "Purpose"],
            [
                ["valid_color.csv",    "color (visual swatch)", "3 options: Coral, Teal, Indigo — fr + en translations"],
                ["invalid_color.csv",  "color (visual swatch)", "4 deliberate errors — validation smoke test"],
                ["duplicate_color.csv","color (visual swatch)", "Coral + Teal already in DB from Test 4, Navy is new — duplicate skip test"],
                ["valid_material.csv", "material (plain select)","2 options: Linen, Wool — hex_code empty throughout"],
                ["invalid_material.csv","material (plain select)","3 deliberate errors — validation for non-swatch attribute"],
            ],
            col_widths=[5*cm, 4.5*cm, 7.5*cm]
        ),
        space(),

        h2("Test 1 — Installation"),
        code(
"""bin/magento module:enable Aichouchm_AttributeImport
bin/magento setup:upgrade
bin/magento cache:flush"""),
        p("Expected: no errors. Module appears in <b>bin/magento module:status</b> as enabled."),
        space(),

        h2("Test 2 — Navigation & UI"),
        p("Go to <b>Stores → Attributes → Import Attributes</b>."),
        simple_table(
            ["What to verify", "Expected"],
            [
                ["Menu entry",      "\"Import Attributes\" appears under Stores → Attributes"],
                ["Attribute dropdown","Shows only user-defined select/multiselect — no system attributes"],
                ["File upload",     "Accepts .csv files"],
                ["Check Data btn",  "Present and clickable"],
                ["Import btn",      "Present — enabled only after a successful Check Data"],
            ],
            col_widths=[5*cm, 12*cm]
        ),
        space(),

        h2("Test 3 — Color: Validation Errors  (invalid_color.csv)"),
        p("Select <b>color</b>. Upload <b>invalid_color.csv</b>. Click <b>Check Data</b>."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
color,default,Coral,#FF6B6B,abc,1    ← Row 2: sort_order not numeric
color,fr,Corail,#FF6B6B,1,1
color,default,Teal,notahex,2,1       ← Row 4: bad hex + is_default=1 duplicate
color,fr,Sarcelle,#008080,2,0
color,default,Coral,#FF6B6B,3,0      ← Row 6: "Coral" duplicate (same as row 2)
color,fr,Corail,#FF6B6B,3,0"""),
        simple_table(
            ["Row", "Expected error"],
            [
                ["2", "sort_order must be a number, got \"abc\""],
                ["4", "is_default=1 is already set for another option"],
                ["4", "hex_code \"notahex\" is not a valid hex colour (expected #RRGGBB)"],
                ["6", "Duplicate option value \"Coral\" within the CSV (admin store)"],
            ],
            col_widths=[2*cm, 15*cm]
        ),
        callout("warn", "4 errors shown. Import button stays blocked. Nothing written to DB."),
        space(),

        h2("Test 4 — Color: Happy Path  (valid_color.csv)"),
        p("Select <b>color</b>. Upload <b>valid_color.csv</b>. Click <b>Check Data</b>."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
color,default,Coral,#FF6B6B,1,1
color,fr,Corail,#FF6B6B,1,1
color,en,Coral,#FF6B6B,1,1
color,default,Teal,#008080,2,0
color,fr,Sarcelle,#008080,2,0
color,en,Teal,#008080,2,0
color,default,Indigo,#4B0082,3,0
color,fr,Indigo,#4B0082,3,0
color,en,Indigo,#4B0082,3,0"""),
        simple_table(
            ["Step", "Expected"],
            [
                ["Check Data", "Preview shows all 9 rows. 0 errors. Import button enabled."],
                ["Import",     "\"Import complete. Imported: 3, Skipped (already exist): 0\""],
                ["Verify",     "Stores → Attributes → Product → color → Manage Options: Coral, Teal, Indigo with fr/en labels and hex swatches"],
            ],
            col_widths=[3*cm, 14*cm]
        ),
        space(),

        h2("Test 5 — Color: Duplicate Skip  (duplicate_color.csv)"),
        p("Run AFTER Test 4. Select <b>color</b>. Upload <b>duplicate_color.csv</b>."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
color,default,Coral,#FF6B6B,1,1      ← already in DB from Test 4
color,fr,Corail,#FF6B6B,1,1
color,en,Coral,#FF6B6B,1,1
color,default,Teal,#008080,2,0       ← already in DB from Test 4
color,fr,Sarcelle,#008080,2,0
color,en,Teal,#008080,2,0
color,default,Navy,#001F5B,5,0       ← new option (not in DB yet)
color,fr,Marine,#001F5B,5,0
color,en,Navy,#001F5B,5,0"""),
        simple_table(
            ["Step", "Expected"],
            [
                ["Check Data", "0 validation errors — duplicates are a DB-level check, not a CSV check."],
                ["Import",     "\"Imported: 1, Skipped (already exist): 2\" — only Navy created."],
                ["Verify",     "color attribute now has Coral, Teal, Indigo (from Test 4) + Navy."],
            ],
            col_widths=[3*cm, 14*cm]
        ),
        callout("info", "Per brief Rule 5: duplicates are logged as warnings and skipped — never overwritten."),
        space(),

        h2("Test 6 — Material: Validation Errors  (invalid_material.csv)"),
        p("Select <b>material</b>. Upload <b>invalid_material.csv</b>. Click <b>Check Data</b>."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
material,default,Linen,,abc,1        ← Row 2: sort_order not numeric
material,fr,Lin,,1,1
material,default,Wool,,2,2           ← Row 4: is_default must be 0 or 1, got "2"
material,fr,Laine,,2,0
material,default,Linen,,3,0          ← Row 6: "Linen" duplicate
material,fr,Lin,,3,0"""),
        simple_table(
            ["Row", "Expected error"],
            [
                ["2", "sort_order must be a number, got \"abc\""],
                ["4", "is_default must be 0 or 1, got \"2\""],
                ["6", "Duplicate option value \"Linen\" within the CSV (admin store)"],
            ],
            col_widths=[2*cm, 15*cm]
        ),
        callout("warn", "3 errors shown. hex_code is empty throughout — no swatch errors because material is plain select."),
        space(),

        h2("Test 7 — Material: Happy Path  (valid_material.csv)"),
        p("Select <b>material</b>. Upload <b>valid_material.csv</b>. "
          "hex_code column is empty — module must not error."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
material,default,Linen,,1,1
material,fr,Lin,,1,1
material,en,Linen,,1,1
material,default,Wool,,2,0
material,fr,Laine,,2,0
material,en,Wool,,2,0"""),
        simple_table(
            ["Step", "Expected"],
            [
                ["Check Data", "0 errors. Empty hex_code cells ignored — material is not a visual swatch."],
                ["Import",     "\"Imported: 2, Skipped (already exist): 0\""],
                ["Verify",     "material attribute has Linen + Wool with fr/en labels."],
            ],
            col_widths=[3*cm, 14*cm]
        ),
        space(),

        h2("Test 8 — Log Viewer"),
        p("Navigate to <b>Stores → Attributes → Import Attributes → View Log</b>."),
        simple_table(
            ["What to verify", "Expected"],
            [
                ["INFO entries",    "\"Import started\" + \"Import complete\" for every import run"],
                ["WARNING entries", "\"Skipped: Coral already exists\" and \"Skipped: Teal already exists\" from Test 5"],
                ["ERROR entries",   "Validation error messages from Tests 3 and 6"],
                ["Colour coding",   "INFO=green, WARNING=amber, ERROR=red"],
                ["Timestamps",      "Every line has date + time prefix"],
            ],
            col_widths=[5*cm, 12*cm]
        ),
        space(),

        h2("Test 9 — ACL / Permissions"),
        p("Go to <b>System → Permissions → User Roles</b>. Edit any role."),
        simple_table(
            ["What to verify", "Expected"],
            [
                ["Resource tree", "Stores → Stores Attributes → Import Attributes is a grantable resource"],
                ["Deny access",   "Role without resource sees no menu entry and gets 403 on direct URL"],
            ],
            col_widths=[4*cm, 13*cm]
        ),
        space(),
        hr(),
        space(0.5),
        Paragraph(
            "Aichouchm_AttributeImport  |  MIT License  |  Mehdi Aichouch",
            S("foot", fontSize=8, textColor=GREY, alignment=TA_CENTER)
        ),
    ]

    # Flatten: code() may return a list when a block was too tall for one page
    flat = []
    for item in story:
        if isinstance(item, list):
            flat.extend(item)
        else:
            flat.append(item)
    return flat

# ── Build PDF ─────────────────────────────────────────────────────────────────
def main():
    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=2.0*cm, bottomMargin=2.5*cm,
    )

    cover_frame  = Frame(0, 0, PAGE_W, PAGE_H, leftPadding=0, rightPadding=0,
                         topPadding=0, bottomPadding=0)
    body_frame   = Frame(MARGIN, 2.5*cm, BODY_W, PAGE_H - 4.0*cm,
                         leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=on_cover),
        PageTemplate(id="body",  frames=[body_frame],  onPage=on_page),
    ])

    story = []
    story += cover_page()
    story.append(NextPageTemplate("body"))
    story.append(PageBreak())
    story += build_body()

    doc.build(story)
    print("Generated:", OUTPUT)

if __name__ == "__main__":
    main()
