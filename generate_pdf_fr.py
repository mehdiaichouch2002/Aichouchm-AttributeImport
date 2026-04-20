#!/usr/bin/env python3
"""
Aichouchm_AttributeImport — Document de Référence Technique
Documentation complète des classes dans l'ordre d'exécution.
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

OUTPUT = "/mnt/seconddrive/PhpstormProjects/Aichouchm-AttributeImport/STRATEGY_FR.pdf"

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
    c.drawCentredString(PAGE_W / 2, 1.3*cm, "Licence MIT  |  Mehdi Aichouch")
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
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.2*cm, "Reference Technique")
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

# ── Page de couverture ────────────────────────────────────────────────────────
def cover_page():
    items = []
    items.append(Spacer(1, 6.5*cm))
    items.append(Paragraph("Aichouchm_AttributeImport", S_COVER_TITLE))
    items.append(Spacer(1, 0.5*cm))
    items.append(Paragraph("Reference Technique", S_COVER_SUB))
    items.append(Spacer(1, 0.25*cm))
    items.append(Paragraph(
        "Documentation complete des classes dans l'ordre d'execution", S_COVER_SUB))
    items.append(Spacer(1, 2.5*cm))

    meta = [
        ["Module",  "Aichouchm_AttributeImport"],
        ["Paquet",  "aichouchm/magento2-module-attribute-import"],
        ["Magento", "2.4.x"],
        ["PHP",     ">= 8.1"],
        ["Auteur",  "Mehdi Aichouch"],
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

# ── Corps du document ─────────────────────────────────────────────────────────
def build_body():
    story = []

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 1 — Vue d'ensemble
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("1  Vue d'ensemble du module"), space()]
    story += [
        p("Aichouchm_AttributeImport permet a un administrateur Magento 2 de telecharger un "
          "fichier CSV et d'importer en masse les options d'attributs produits (couleurs, tailles, "
          "materiaux, etc.) avec des libelles par vue de magasin et des echantillons de couleur "
          "hexadecimaux. Sans ce module, l'administrateur doit cliquer sur <i>Ajouter une option</i> "
          "une ligne a la fois — 200 couleurs sur 3 vues de magasin = 600 interactions manuelles."),
        space(),
        h2("1.1  Flux de donnees complet"),
        code(
"""L'administrateur uploade un CSV via le formulaire navigateur
        |
        v
  [Controleur Index]     affiche la page d'import (layout + blocs)
        |
        v (clic sur Verifier les donnees)
  [Controleur Preview]   recoit le POST multipart
        |
        v
  [StreamingReader]      ouvre le fichier, retourne un tableau[] par ligne
        |
        v
  [Validator]            validateHeaders() -- verifie le nombre et les noms des colonnes
                         validateRows()    -- verifie chaque regle, ligne par ligne
        |
        v (si valide)
  [Bloc Preview]         genere un apercu HTML en tableau, retourne en JSON
        |
        v (clic sur Importer)
  [Controleur Process]   recoit le POST multipart
        |
        v
  [ImportService]        re-valide, puis regroupe les lignes par option
        |
        v
  [OptionProcessor]      ecrit en base de donnees :
                         INSERT INTO eav_attribute_option         (un par option)
                         insertOnDuplicate eav_attribute_option_value  (tous les libelles)
                         insertOnDuplicate eav_attribute_option_swatch (tous les echantillons)
        |
        v
  [CacheManager]         clean(['eav', 'full_page', 'block_html'])
        |
        v
  [Logger]               ecrit dans var/log/attribute_import.log"""),
        space(),
        h2("1.2  Exemple CSV de reference"),
        p("Chaque methode de ce document est expliquee en utilisant ce CSV. "
          "L'attribut <b>color</b> est un attribut de type echantillon visuel (hex)."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
color,default,Coral,#FF6B6B,1,1    <- groupe 1 : ligne admin (sort_order + is_default ici)
color,fr,Corail,#FF6B6B,1,1        <- groupe 1 : traduction francaise
color,en,Coral,#FF6B6B,1,1         <- groupe 1 : traduction anglaise
color,default,Teal,#008080,2,0     <- groupe 2 : ligne admin
color,fr,Sarcelle,#008080,2,0      <- groupe 2 : traduction francaise
color,en,Teal,#008080,2,0          <- groupe 2 : traduction anglaise"""),
        space(),
        h2("1.3  Structure des dossiers"),
        code(
"""Aichouchm_AttributeImport/
|-- Api/
|   `-- ImportServiceInterface.php      <- contrat public (interface)
|-- Service/
|   `-- StoreResolver.php               <- correspondance code magasin -> store_id
|-- Model/
|   |-- Csv/
|   |   |-- StreamingReader.php         <- generateur fgetcsv, memoire O(1)
|   |   `-- Validator.php               <- sans etat, retourne une liste d'erreurs
|   |-- Attribute/
|   |   `-- OptionProcessor.php         <- ecritures DB en masse
|   |-- Import/Source/Attributes.php    <- modele source pour la liste deroulante
|   `-- ImportService.php               <- orchestrateur principal
|-- Controller/Adminhtml/
|   |-- AbstractAction.php              <- ADMIN_RESOURCE + helpers de requete partages
|   `-- Import/
|       |-- Index.php                   <- affiche la page d'import
|       |-- Preview.php                 <- AJAX : Verifier les donnees
|       |-- Process.php                 <- AJAX : Importer
|       `-- Log.php                     <- page du journal
|-- Block/Adminhtml/
|   |-- Import/
|   |   |-- Form.php                    <- conteneur de page (boutons)
|   |   |-- Form/Form.php               <- champs du formulaire
|   |   |-- Form/Before.php             <- transmet les URLs au template JS
|   |   `-- Preview.php                 <- bloc tableau d'apercu
|   `-- Log.php                         <- bloc du journal
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
    # SECTION 2 — Couche de configuration
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("2  Couche de configuration"), space()]
    story += [
        p("Ces fichiers integrent le module dans Magento avant qu'une seule ligne de logique "
          "metier ne s'execute. Magento les lit a la compilation et met le resultat en cache."),
        space(),

        h2("registration.php"),
        filepath("Aichouchm_AttributeImport/registration.php"),
        p("Chaque module Magento doit appeler <b>ComponentRegistrar::register()</b> pour que "
          "le chargeur de modules Magento puisse le decouvrir. Sans ce fichier, le module est "
          "invisible — pas de routes, pas de blocs, pas de DI."),
        code(
"""ComponentRegistrar::register(
    ComponentRegistrar::MODULE,
    'Aichouchm_AttributeImport',
    __DIR__
);"""),
        callout("info", "'__DIR__' est le chemin absolu vers la racine du module. Magento "
                "l'utilise pour resoudre tous les chemins relatifs a l'interieur du module "
                "(templates, XML de layout, etc.)."),
        space(),

        h2("etc/module.xml"),
        filepath("Aichouchm_AttributeImport/etc/module.xml"),
        p("Declare le nom du module. La balise <b>sequence</b> indique a Magento de charger "
          "Magento_Swatches avant ce module, garantissant que les tables des echantillons "
          "existent avant que ce module tente d'y ecrire."),
        code(
"""<module name="Aichouchm_AttributeImport">
    <sequence>
        <module name="Magento_Swatches"/>
    </sequence>
</module>"""),
        space(),

        h2("etc/adminhtml/routes.xml"),
        filepath("Aichouchm_AttributeImport/etc/adminhtml/routes.xml"),
        p("Enregistre le nom de front <b>attributeimport</b> pour le routeur admin. "
          "C'est le premier segment de chaque URL geree par ce module."),
        code(
"""<router id="admin">
    <route id="attributeimport" frontName="attributeimport">
        <module name="Aichouchm_AttributeImport"/>
    </route>
</router>"""),
        p("Schema d'URL : <b>/admin/attributeimport/{controleur}/{action}</b>"),
        simple_table(
            ["URL", "Fichier controleur", "Action"],
            [
                ["/admin/attributeimport/import/index",   "Controller/Adminhtml/Import/Index.php",   "Affiche la page d'import"],
                ["/admin/attributeimport/import/preview", "Controller/Adminhtml/Import/Preview.php", "AJAX : Verifier les donnees"],
                ["/admin/attributeimport/import/process", "Controller/Adminhtml/Import/Process.php", "AJAX : Importer"],
                ["/admin/attributeimport/import/log",     "Controller/Adminhtml/Import/Log.php",     "Page du journal"],
            ],
            col_widths=[6*cm, 6.5*cm, 4.5*cm]
        ),
        space(),

        h2("etc/adminhtml/menu.xml"),
        filepath("Aichouchm_AttributeImport/etc/adminhtml/menu.xml"),
        p("Ajoute l'element <i>Import Attributes</i> au menu admin sous "
          "<b>Stores &rarr; Attributes</b>. Tout est declaratif — Magento fusionne "
          "les fichiers menu.xml de tous les modules au moment de la construction du cache."),
        code(
"""<add id="Aichouchm_AttributeImport::import_attributes"
     title="Import Attributes"
     parent="Magento_Backend::stores_attributes"
     action="attributeimport/import/index"
     sortOrder="70"
     resource="Aichouchm_AttributeImport::import_attributes"/>"""),
        simple_table(
            ["Attribut", "Valeur", "Objectif"],
            [
                ["id",        "Aichouchm_AttributeImport::import_attributes", "Identifiant unique de l'element de menu"],
                ["parent",    "Magento_Backend::stores_attributes",           "Place l'element sous Stores > Attributes"],
                ["action",    "attributeimport/import/index",                 "URL frontName/controleur/action"],
                ["sortOrder", "70",                                           "Position apres Rating (sortOrder 60)"],
                ["resource",  "Aichouchm_AttributeImport::import_attributes", "Ressource ACL qui controle l'acces"],
            ],
            col_widths=[2.5*cm, 6.5*cm, 8*cm]
        ),
        space(),

        h2("etc/acl.xml"),
        filepath("Aichouchm_AttributeImport/etc/acl.xml"),
        p("Enregistre la ressource ACL dans l'arbre des permissions Magento. Les roles admin "
          "peuvent se voir accorder ou refuser cette ressource sous "
          "<b>Systeme &rarr; Permissions &rarr; Roles utilisateurs</b>."),
        code(
"""Magento_Backend::stores
  `-- Magento_Backend::stores_attributes
        `-- Aichouchm_AttributeImport::import_attributes
              <- ressource "Import Attributes" """),
        space(),

        h2("etc/di.xml"),
        filepath("Aichouchm_AttributeImport/etc/di.xml"),
        p("Configure trois choses : le logger Monolog dedie, la liaison de l'interface de "
          "service, et injecte le logger dans les classes qui en ont besoin."),
        code(
"""<!-- 1. Handler de log dedie : ecrit dans var/log/attribute_import.log -->
<virtualType name="Aichouchm\\AttributeImport\\Logger\\Handler"
             type="Magento\\Framework\\Logger\\Handler\\Base">
    <arguments>
        <argument name="fileName">/var/log/attribute_import.log</argument>
    </arguments>
</virtualType>

<!-- 2. Canal Monolog nomme utilisant le handler ci-dessus -->
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

<!-- 3. Injecter le logger dans les classes declarant LoggerInterface $logger -->
<type name="Aichouchm\\AttributeImport\\Model\\ImportService">
    <arguments>
        <argument name="logger" xsi:type="object">
            Aichouchm\\AttributeImport\\Logger\\Logger
        </argument>
    </arguments>
</type>

<!-- 4. Lier l'interface a la classe concrete -->
<preference for="Aichouchm\\AttributeImport\\Api\\ImportServiceInterface"
            type="Aichouchm\\AttributeImport\\Model\\ImportService"/>"""),
        callout("info", "Les types virtuels creent un objet DI nomme sans fichier PHP. "
                "Le conteneur DI de Magento construit le logger Monolog avec le bon handler "
                "uniquement a partir du XML. Aucun fichier Logger.php n'est necessaire."),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 3 — Chargement de la page d'import
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("3  Chargement de la page d'import"), space()]
    story += [
        p("Quand l'administrateur clique sur <i>Import Attributes</i> dans le menu, Magento "
          "achemine la requete vers le controleur Index, qui retourne un resultat de type Page. "
          "Magento fusionne ensuite le XML de layout pour construire la structure de la page."),
        space(),

        h2("Controller/Adminhtml/AbstractAction.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/AbstractAction.php"),
        p("Classe de base pour les quatre controleurs admin. Definit <b>ADMIN_RESOURCE</b> "
          "une seule fois et contient les deux helpers de validation de requete partages par "
          "Preview et Process."),
        code(
"""abstract class AbstractAction extends Action
{
    public const ADMIN_RESOURCE = 'Aichouchm_AttributeImport::import_attributes';

    // Partage par Preview et Process — place ici pour eviter la duplication.
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
        callout("info", "Les quatre controleurs (Index, Preview, Process, Log) etendent cette "
                "classe. Avant ce refactoring, chaque controleur redeclarait la meme constante "
                "— un renommage aurait necessite quatre modifications."),
        space(),

        h2("Controller/Adminhtml/Import/Index.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/Import/Index.php"),
        p("Le controleur admin le plus simple possible. Son seul role est de declarer quelle "
          "page afficher."),
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
            ["Element", "Objectif"],
            [
                ["extends AbstractAction", "Herite de ADMIN_RESOURCE ; Action execute _isAllowed() automatiquement"],
                ["resultPageFactory",      "Cree un resultat Page — ne jamais utiliser 'new Page()' dans Magento"],
                ["setActiveMenu()",        "Met en evidence l'element correct dans la barre laterale gauche"],
                ["getTitle()->prepend()",  "Definit le titre de l'onglet navigateur et le titre de la page admin"],
            ],
            col_widths=[4.5*cm, 12.5*cm]
        ),
        space(),

        h2("view/adminhtml/layout/attributeimport_import_index.xml"),
        filepath("Aichouchm_AttributeImport/view/adminhtml/layout/attributeimport_import_index.xml"),
        p("Le nom du fichier <b>attributeimport_import_index.xml</b> n'est pas arbitraire — "
          "c'est le handle de page, construit a partir de frontName_controleur_action. Magento "
          "charge ce fichier automatiquement pour chaque requete vers cette URL."),
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
        p("<b>referenceContainer name=\"content\"</b> cible la zone de contenu principale "
          "deja definie par le layout admin de base de Magento. Ce module ajoute ses trois "
          "blocs dans cet emplacement sans toucher au shell admin (en-tete, barre laterale, pied)."),
        simple_table(
            ["Bloc", "Classe", "Responsabilite"],
            [
                ["attributeimport.form",    "Import\\Form",        "Conteneur de page avec barre de boutons"],
                ["attributeimport.preview", "Import\\Preview",     "Tableau des resultats de validation (cache jusqu'a Verifier)"],
                ["attributeimport.before",  "Import\\Form\\Before","Logique JS + URLs AJAX"],
            ],
            col_widths=[4.5*cm, 4*cm, 8.5*cm]
        ),
        PageBreak(),

        h2("Block/Adminhtml/Import/Form.php  (Conteneur)"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Import/Form.php"),
        p("Etend <b>Magento\\Backend\\Block\\Widget\\Form\\Container</b> qui fournit la carte "
          "de page admin standard avec une barre de boutons en haut. Tous les boutons sont "
          "geres via l'API <b>buttonList</b> — aucun HTML ecrit a la main."),
        code(
"""class Form extends Container
{
    protected $_mode = 'form';

    protected function _construct(): void
    {
        parent::_construct();

        // Supprimer les boutons qui ne s'appliquent pas a cette page
        $this->buttonList->remove('back');
        $this->buttonList->remove('reset');

        // Renommer le bouton Enregistrer par defaut
        $this->buttonList->update('save', 'label',   __('Import'));
        $this->buttonList->update('save', 'id',      'import-button');
        $this->buttonList->update('save', 'class',   'primary disabled');
        $this->buttonList->update('save', 'onclick', 'attributeImport.submit()');

        // Ajouter le bouton Verifier les donnees
        $this->buttonList->add('check-data-button', [
            'label'   => __('Check Data'),
            'id'      => 'check-data-button',
            'onclick' => 'attributeImport.checkData();',
        ]);

        // Ajouter le bouton Voir le journal — setLocation() est la redirection JS native Magento
        $this->buttonList->add('view-log-button', [
            'label'   => __('View Log'),
            'type'    => 'button',
            'class'   => 'action-default',
            'onclick' => 'setLocation(\'' . $this->getUrl('attributeimport/import/log') . '\')',
        ]);

        // Ces trois proprietes indiquent au Conteneur ou trouver son bloc enfant
        $this->_objectId   = 'import_ids';
        $this->_blockGroup = 'Aichouchm_AttributeImport';
        $this->_controller = 'adminhtml_import';
    }
}"""),
        callout("info", "Les trois proprietes protegees (_objectId, _blockGroup, _controller) "
                "indiquent au Conteneur de decouvrir automatiquement son bloc enfant. Il construit "
                "le nom de classe Block/Adminhtml/Import/Form/Form.php a partir de _blockGroup + "
                "_controller. C'est pourquoi la classe de formulaire interne se trouve exactement "
                "a ce chemin."),
        space(),

        h2("Block/Adminhtml/Import/Form/Form.php  (Generique)"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Import/Form/Form.php"),
        p("Etend <b>Magento\\Backend\\Block\\Widget\\Form\\Generic</b> qui fournit le "
          "<b>_formFactory</b> et le hook <b>_prepareForm()</b>. Surcharger _prepareForm() "
          "pour decrire les champs — Magento genere le HTML."),
        code(
"""protected function _prepareForm(): static
{
    $form = $this->_formFactory->create([
        'data' => [
            'id'      => 'attribute-import-form',
            'method'  => 'post',
            'enctype' => 'multipart/form-data',  // obligatoire pour les uploads de fichiers
        ],
    ]);

    $fieldset = $form->addFieldset('base_fieldset', [
        'legend' => __('Import Settings'),
    ]);

    // Liste deroulante : tous les attributs select/multiselect definis par l'utilisateur
    $fieldset->addField('attribute_code', 'select', [
        'name'     => 'attribute_code',
        'label'    => __('Select Attribute'),
        'required' => true,
        'values'   => $this->sourceAttributes->toOptionArray(),
        'onchange' => 'attributeImport.onAttributeChange();',
    ]);

    // Champ de telechargement de fichier
    $fieldset->addField('import_file', 'file', [
        'name'     => 'import_file',
        'label'    => __('CSV File'),
        'required' => true,
        'onchange' => 'attributeImport.onFileChange();',
    ]);

    $form->setUseContainer(true);  // genere la balise <form>
    $this->setForm($form);
    return parent::_prepareForm();
}"""),
        callout("warn", "setUseContainer(true) est obligatoire. Sans cela, la balise de formulaire "
                "n'est pas generee et le POST d'upload de fichier n'atteint jamais le controleur."),
        space(),

        h2("Model/Import/Source/Attributes.php"),
        filepath("Aichouchm_AttributeImport/Model/Import/Source/Attributes.php"),
        p("Un modele source Magento — implemente <b>ArrayInterface</b> et fournit "
          "<b>toOptionArray()</b> pour la liste deroulante des attributs. Seuls les attributs "
          "select et multiselect definis par l'utilisateur sont listes (les attributs "
          "d'echantillon visuel ont aussi frontend_input='select' en base de donnees)."),
        code(
"""public function toOptionArray(): array
{
    if ($this->options !== null) {
        return $this->options;  // memoisation : charge une seule fois par requete
    }

    $this->options = [['value' => '', 'label' => __('-- Please Select --')]];

    // Les deux filtres sont pousses vers SQL — seules les lignes correspondantes sont chargees
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
        p("Resultat pour un magasin avec les attributs color et size :"),
        code(
"""[
    ['value' => '',      'label' => '-- Please Select --'],
    ['value' => 'color', 'label' => 'Color [color]'],
    ['value' => 'size',  'label' => 'Size [size]'],
]"""),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 4 — Le bloc Before et JavaScript
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("4  Le bloc Before et le JavaScript"), space()]
    story += [
        p("Le role du bloc Before est de generer des URLs cote serveur et de les passer au "
          "template JavaScript. Cela est necessaire car Magento ajoute une cle secrete a chaque "
          "URL admin (protection CSRF) — une URL codee en dur dans le JS serait rejetee."),
        space(),

        h2("Block/Adminhtml/Import/Form/Before.php"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Import/Form/Before.php"),
        code(
"""class Before extends Template
{
    public function getPreviewUrl(): string
    {
        return $this->getUrl('attributeimport/import/preview');
        // ex. https://magento.local/admin/attributeimport/import/preview/key/abc123/
    }

    public function getProcessUrl(): string
    {
        return $this->getUrl('attributeimport/import/process');
        // ex. https://magento.local/admin/attributeimport/import/process/key/abc123/
    }
}"""),
        p("<b>getUrl()</b> est herite de <b>Magento\\Backend\\Block\\Template</b>. "
          "Il ajoute automatiquement la cle secrete admin :"),
        code(
"""// Ce que retourne getUrl() :
// https://magento.local/admin/attributeimport/import/preview/key/abc123/

// Le parametre key= change a chaque session. Sans lui, Magento retourne 403.
// Generer les URLs en PHP et les passer au JS est la seule approche correcte."""),
        space(),

        h2("view/adminhtml/templates/import/form/before.phtml"),
        filepath("Aichouchm_AttributeImport/view/adminhtml/templates/import/form/before.phtml"),
        p("Le template genere la div de notification, le conteneur d'apercu, et tout le "
          "JavaScript. Le JS est rendu via <b>$secureRenderer->renderTag()</b> — la methode "
          "Magento securisee CSP pour les scripts inline."),
        space(),
        h3("Structure HTML generee par ce template"),
        code(
"""<!-- Barre de notification : cachee par defaut, affichee par showMessage() -->
<div id="import-notification" class="hidden"></div>

<!-- Section apercu : cachee jusqu'au clic sur Verifier les donnees -->
<div id="preview-section">
    <h2 id="validation-heading" class="hidden">Validation Results</h2>
    <div id="preview-container"></div>  <!-- HTML d'apercu injecte ici par AJAX -->
</div>"""),
        space(),
        h3("JavaScript : objet window.attributeImport"),
        p("Un seul objet expose sur window. Tous les gestionnaires onclick des boutons "
          "appellent des methodes sur cet objet."),
        code(
"""window.attributeImport = {

    // Appele par le bouton Verifier : onclick="attributeImport.checkData()"
    checkData: function () {
        var formData = new FormData($('#attribute-import-form')[0]);
        $.ajax({
            url:         '$previewUrl',   // depuis block->getPreviewUrl()
            type:        'POST',
            data:        formData,
            contentType: false,           // obligatoire pour multipart
            processData: false,           // obligatoire pour FormData
            dataType:    'json',
            success: function (response) {
                if (!response.success) {
                    attributeImport.showMessage(response.message, 'error');
                    return;
                }
                $('#preview-container').html(response.data); // injecte le HTML d'apercu
                $('#validation-heading').removeClass('hidden');

                if (response.is_valid) {
                    attributeImport.hideMessage();
                    attributeImport.enableImport();   // active le bouton Importer
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
"""    // Appele par le bouton Importer : onclick="attributeImport.submit()"
    submit: function () {
        var formData = new FormData($('#attribute-import-form')[0]);
        $.ajax({
            url:         '$processUrl',   // depuis block->getProcessUrl()
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
                        msg += '<br><em>' + response.skipped + ' ignores (deja existants)</em>';
                    }
                    attributeImport.showMessage(msg, 'success');
                } else {
                    attributeImport.showMessage(response.messages.join('<br>'), 'error');
                }
            }
        });
    },"""),
        code(
"""    // Helpers d'etat de l'interface
    onAttributeChange: function () { this.resetState(); },
    onFileChange:      function () { this.resetState(); },

    resetState: function () {
        this.resetButtons();                           // Importer desactive, Verifier active
        $('#validation-heading').addClass('hidden');
        $('#preview-container').html('');
        this.hideMessage();
    },

    enableImport: function () {
        $('#import-button').removeClass('disabled');
        $('#check-data-button').addClass('disabled');  // evite la double validation
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
        callout("info", "contentType: false et processData: false sont obligatoires pour les "
                "uploads de fichiers AJAX avec jQuery. Ils indiquent a jQuery de ne pas serialiser "
                "l'objet FormData et de ne pas definir d'en-tete Content-Type (le navigateur "
                "definit multipart/form-data avec la bonne boundary automatiquement)."),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 5 — Flux de verification des donnees
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("5  Flux de verification  (POST AJAX -> controleur Preview)"), space()]
    story += [
        p("Quand l'administrateur clique sur <b>Verifier les donnees</b>, le JS envoie un POST "
          "multipart vers /attributeimport/import/preview. Le controleur valide le CSV et "
          "retourne un objet JSON contenant du HTML rendu."),
        space(),

        h2("Controller/Adminhtml/Import/Preview.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/Import/Preview.php"),
        code(
"""public function execute(): Json
{
    $result = $this->resultJsonFactory->create();
    try {
        // Etape 1 — garde : rejeter les mauvaises requetes HTTP avant de toucher au fichier
        $this->assertValidRequest();

        // Etape 2 — lire les deux entrees POST
        $attributeCode = $this->getRequest()->getParam('attribute_code');  // ex. 'color'
        $filePath      = $this->getUploadedFilePath();                     // ex. '/tmp/phpAb3x9'

        // Etape 3 — valider le CSV (en-tetes + chaque ligne de donnees)
        $validation = $this->importService->validate($filePath, $attributeCode);

        // Etape 4 — generer le tableau d'apercu en chaine HTML (valide ou non)
        $html = $this->renderPreviewBlock($validation['rows'], $validation['errors']);

        // Etape 5 — retourner JSON ; JS utilise is_valid pour activer le bouton Importer
        return $result->setData([
            'success'  => true,
            'data'     => $html,
            'is_valid' => $validation['is_valid'],
        ]);
    } catch (Exception $e) {
        // assertValidRequest() ou getUploadedFilePath() a lance une exception
        return $result->setData(['success' => false, 'message' => $e->getMessage()]);
    }
}"""),
        space(),
        h3("Etape 1  —  assertValidRequest()"),
        p("Verifie la couche HTTP avant toute lecture de fichier. Trois conditions, chacune "
          "lance une Exception qui est capturee et retournee en JSON d'erreur :"),
        code(
"""private function assertValidRequest(): void
{
    $files = $this->getRequest()->getFiles()->toArray();

    // 1a. Un fichier doit avoir ete uploade
    if (empty($files['import_file']['tmp_name'])) {
        throw new Exception('Please upload a CSV file.');
    }
    // 1b. L'extension doit etre .csv (pathinfo() lit le nom, ne l'execute jamais)
    if (strtolower(pathinfo($files['import_file']['name'], PATHINFO_EXTENSION)) !== 'csv') {
        throw new Exception('Only CSV files are allowed.');
    }
    // 1c. La liste deroulante de l'attribut doit avoir une selection
    if (empty($this->getRequest()->getParam('attribute_code'))) {
        throw new Exception('Please select an attribute.');
    }
}

// Si une verification echoue, execute() capture l'Exception et retourne :
// { "success": false, "message": "Only CSV files are allowed." }"""),
        callout("warn", "Cela valide uniquement la requete HTTP — pas le contenu du CSV. "
                "Le contenu CSV (noms de colonnes, valeurs de lignes) est valide plus tard "
                "par Validator, jamais ici."),
        space(),
        h3("Etape 2  —  getUploadedFilePath()"),
        p("Lit le chemin temporaire ou PHP a ecrit l'upload et confirme qu'il est lisible :"),
        code(
"""private function getUploadedFilePath(): string
{
    $files    = $this->getRequest()->getFiles()->toArray();
    $filePath = $files['import_file']['tmp_name'] ?? '';  // ex. '/tmp/phpAb3x9'

    if (!is_readable($filePath)) {
        throw new Exception('Cannot read the uploaded file.');
    }
    return $filePath;
}"""),
        space(),
        h3("Etape 3  —  importService->validate()  (l'appel cle)"),
        p("C'est ici que toute la logique CSV s'execute. Le controleur passe le chemin tmp "
          "et le code d'attribut selectionne. La valeur de retour est un tableau a trois cles :"),
        code(
"""$validation = $this->importService->validate('/tmp/phpAb3x9', 'color');

// Ce que contient $validation pour notre exemple (valid_color.csv) :
[
    'is_valid'    => true,
    'errors'      => [],          // vide — pas d'erreurs de validation
    'swatch_type' => 1,           // SWATCH_VISUAL — color est un attribut echantillon visuel
    'rows'        => [
        ['attribute_code','store_view','value','hex_code','sort_order','is_default'],  // en-tete
        ['color','default','Coral','#FF6B6B','1','1'],
        ['color','fr','Corail','#FF6B6B','1','1'],
        ['color','en','Coral','#FF6B6B','1','1'],
        ['color','default','Teal','#008080','2','0'],
        ['color','fr','Sarcelle','#008080','2','0'],
        ['color','en','Teal','#008080','2','0'],
        // ... lignes Indigo
    ],
]

// Ce que contient $validation quand une ligne est invalide :
[
    'is_valid' => false,
    'errors'   => [
        'Row 2: hex_code "#ZZZ" is not a valid hex colour.',
        'Row 4: sort_order "abc" must be a positive integer.',
    ],
    'rows'     => [ ... ],   // toutes les lignes retournees pour afficher le tableau
]"""),
        callout("info", "rows est toujours retourne meme quand is_valid est false. "
                "Le tableau d'apercu affiche le CSV complet avec la liste d'erreurs au-dessus — "
                "l'admin peut voir exactement quelles lignes ont echoue sans re-uploader."),
        space(),
        h3("Etape 4  —  renderPreviewBlock()"),
        p("Transforme les tableaux rows + errors en chaine HTML. Utilise un layout minimal "
          "autonome — pas de chargement complet de page admin :"),
        code(
"""private function renderPreviewBlock(array $rows, array $errors): string
{
    return $this->layoutFactory->create()
        ->createBlock(PreviewBlock::class)
        ->setTemplate('Aichouchm_AttributeImport::import/preview.phtml')
        ->setData(compact('rows', 'errors'))   // passe les deux variables au template
        ->toHtml();                            // execute le template, retourne une chaine HTML
}

// $html ressemblera a :
// '<div class=\"admin__data-grid-outer-wrap\"><table ...>...</table></div>
//  <p class=\"note\">6 lignes de donnees trouvees. <strong>Toutes les lignes sont valides...</strong></p>'"""),
        space(),
        h3("Etape 5  —  Reponse JSON"),
        p("Le JSON que le controleur retourne. jQuery le lit dans <b>checkData()</b> :"),
        code(
"""// CSV valide — JS injecte $html dans #preview-container et active le bouton Importer :
{
    "success":  true,
    "data":     "<table ...>...</table>",   // HTML rendu
    "is_valid": true
}

// CSV invalide — JS affiche les messages d'erreur, le bouton Importer reste desactive :
{
    "success":  true,
    "data":     "<div class=\\"messages\\">...</div><table ...>",
    "is_valid": false
}

// Erreur HTTP/requete (assertValidRequest a lance) — JS affiche la chaine message :
{
    "success": false,
    "message": "Please upload a CSV file."
}"""),
        space(),

        h2("Api/ImportServiceInterface.php"),
        filepath("Aichouchm_AttributeImport/Api/ImportServiceInterface.php"),
        p("Definit le contrat public pour le service d'import. Les controleurs typent cette "
          "interface, pas la classe concrete. Cela rend les tests unitaires possibles — "
          "les tests injectent un mock au lieu d'un ImportService reel."),
        code(
"""interface ImportServiceInterface
{
    // Retourne : ['is_valid' => bool, 'errors' => string[], 'rows' => array[]]
    public function validate(string $filePath, string $attributeCode): array;

    // Retourne : ['success' => bool, 'messages' => string[],
    //             'imported' => int, 'skipped' => int]
    public function import(string $filePath, string $attributeCode): array;
}"""),
        space(),

        h2("Model/Csv/StreamingReader.php"),
        filepath("Aichouchm_AttributeImport/Model/Csv/StreamingReader.php"),
        p("Ouvre un fichier CSV et retourne une ligne a la fois via un generateur PHP. "
          "La memoire de pointe est toujours une ligne (~1 Ko) quelle que soit la taille du fichier."),
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
        fclose($handle);  // toujours ferme, meme si l'appelant lance une exception
    }
}"""),
        p("En utilisant notre CSV d'exemple, le generateur produit :"),
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
        p("Validateur sans etat. Chaque methode initialise ses variables de suivi localement "
          "et retourne une valeur. Aucun etat n'est stocke dans les proprietes de classe. "
          "C'est crucial car le DI Magento cree les services en tant que singletons — un "
          "validateur avec etat transporterait les erreurs d'une requete a la suivante."),
        code(
"""class Validator
{
    public const SWATCH_NONE   = -1;  // select / multiselect simple / echantillon texte
    public const SWATCH_VISUAL =  1;  // echantillon visuel (couleur hex par option)

    // CSV unifie a 6 colonnes — hex_code toujours present ; laisser vide pour les non-visuels
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
        p("Charge l'attribut depuis la base de donnees et lit son JSON <b>additional_data</b>. "
          "Retourne une constante qui controle si <b>hex_code</b> doit etre valide et si une "
          "ligne doit etre ecrite dans <b>eav_attribute_option_swatch</b>."),
        p("Important : tous les attributs d'echantillon (visuel et texte) stockent "
          "<b>frontend_input = 'select'</b> en base de donnees — le type d'echantillon est "
          "conserve separement dans la colonne JSON <b>additional_data</b> de "
          "<b>catalog_eav_attribute</b>. C'est pourquoi ils apparaissent dans la liste "
          "deroulante avec les attributs select simples."),
        simple_table(
            ["Attribut", "frontend_input (DB)", "additional_data (DB)", "getSwatchType() retourne"],
            [
                ["color",    "select",      '{"swatch_input_type":"visual"}', "SWATCH_VISUAL = 1"],
                ["size",     "select",      '{"swatch_input_type":"text"}',   "SWATCH_NONE = -1"],
                ["material", "multiselect", "NULL",                           "SWATCH_NONE = -1"],
            ],
            col_widths=[3*cm, 4*cm, 7*cm, 4*cm]
        ),
        space(),
        code(
"""// Utilise Magento\\Eav\\Model\\Config — trois couches de cache :
//   1. en memoire $this->attributes[...] — gratuit pour les appels repetes dans une requete
//   2. cache Magento (type eav) — survit entre les requetes
//   3. fallback DB — uniquement sur cache froid
// Ancienne approche : attributeFactory->create()->loadByCode() — toujours en DB.

public function getSwatchType(string $attributeCode): int
{
    $attribute  = $this->eavConfig->getAttribute(Product::ENTITY, $attributeCode);
    $additional = json_decode($attribute->getAdditionalData() ?? '{}', true, 512, JSON_THROW_ON_ERROR);

    return match ($additional['swatch_input_type'] ?? null) {
        'visual' => self::SWATCH_VISUAL,  // hex_code doit etre un #RRGGBB valide
        default  => self::SWATCH_NONE,    // colonne hex_code presente mais ignoree
    };
}

// color    -> {"swatch_input_type":"visual"} -> SWATCH_VISUAL -> hex valide
// size     -> {"swatch_input_type":"text"}   -> SWATCH_NONE   -> hex ignore
// material -> NULL                           -> SWATCH_NONE   -> hex ignore"""),
        space(),
        h3("validateHeaders(array $headerRow): array"),
        p("Verifie la ligne d'en-tete par rapport au format fixe unique. "
          "Retourne tot si le nombre de colonnes est incorrect — inutile de verifier les noms "
          "si les decalages sont faux."),
        code(
"""// Un seul format pour tous les types d'attributs :
// ['attribute_code','store_view','value','hex_code','sort_order','is_default']
//
// Pour echantillon visuel : hex_code rempli  -> color,default,Coral,#FF6B6B,1,1
// Pour select simple :      hex_code vide    -> material,default,Linen,,1,1

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

// Exemple : validateHeaders(['attribute_code','store_view','value','hex_code','sort_order','is_default'])
// -> [] (aucune erreur)"""),
        space(),
        h3("validateRows(array $rows, string $attributeCode, int $swatchType): array"),
        p("La methode la plus complexe. Parcourt toutes les lignes de donnees (en-tete exclu) "
          "et applique des regles couvrant plusieurs lignes. Utilise quatre variables de suivi :"),
        simple_table(
            ["Variable", "Type", "Suit"],
            [
                ["$adminValues",     "array",  "Toutes les valeurs du magasin par defaut vues — detecte les doublons CSV"],
                ["$optionStores",    "array",  "Codes magasin dans le groupe d'option courant — detecte les magasins en double"],
                ["$defaultSelected", "bool",   "Si une ligne a is_default=1 — une seule autorisee"],
            ],
            col_widths=[3.5*cm, 2*cm, 11.5*cm]
        ),
        space(),
        p("Parcours etape par etape de l'exemple de reference :"),
        code(
"""// Entree : lignes de donnees uniquement (en-tete deja retire par ImportService)
Ligne 1 : ['color','default','Coral','#FF6B6B','1','1']
  isAdmin=true  -> nouveau groupe commence
  $optionStores = []   (reinitialise pour ce nouveau groupe)
  'Coral' absent de $adminValues -> ajouter : $adminValues=['Coral']
  sort_order='1'  -> is_numeric(1) OK
  is_default='1'  -> $defaultSelected=true
  hex '#FF6B6B'   -> correspond a /^#[A-Fa-f0-9]{6}$/ OK

Ligne 2 : ['color','fr','Corail','#FF6B6B','1','1']
  isAdmin=false -> ligne de traduction (magasin fr)
  'fr' est un code de vue de magasin Magento valide -> OK
  'fr' absent de $optionStores -> ajouter : $optionStores=['fr']

Ligne 3 : ['color','en','Coral','#FF6B6B','1','1']
  isAdmin=false -> ligne de traduction (magasin en)
  'en' est un code de magasin valide -> OK
  'en' absent de $optionStores -> $optionStores=['fr','en']

Ligne 4 : ['color','default','Teal','#008080','2','0']
  isAdmin=true  -> nouveau groupe commence
  $optionStores = []   (reinitialise pour ce nouveau groupe)
  'Teal' absent de $adminValues -> $adminValues=['Coral','Teal']
  is_default='0' -> $defaultSelected toujours true depuis ligne 1, pas de conflit

Resultat : [] — tableau vide signifie que le fichier est valide, bouton Importer active"""),
        callout("good", "Ajouter une ligne en double ['color','default','Coral','#FF6B6B','4','0'] "
                "a la fin produirait : \"Row 7: Duplicate option value Coral within the CSV\". "
                "La verification est O(n) par ligne — in_array parcourt le tableau $adminValues."),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 6 — Flux d'import
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("6  Flux d'import  (POST AJAX -> controleur Process)"), space()]
    story += [
        p("Apres une verification reussie, le bouton Importer est active. En cliquant dessus, "
          "le meme POST multipart est envoye au controleur Process, qui appelle "
          "ImportService::import()."),
        space(),

        h2("Controller/Adminhtml/Import/Process.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/Import/Process.php"),
        p("Meme structure que Preview : valider la requete, appeler le service, retourner JSON. "
          "La difference est qu'il appelle <b>import()</b> au lieu de <b>validate()</b> "
          "et retourne des compteurs au lieu de HTML."),
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
        p("L'orchestrateur principal. Implemente ImportServiceInterface et coordonne "
          "StreamingReader, Validator, OptionProcessor, CacheManager et Logger."),
        space(),
        h3("validate(string $filePath, string $attributeCode): array"),
        code(
"""public function validate(string $filePath, string $attributeCode): array
{
    try {
        [$swatchType, $allRows] = $this->readAllRows($filePath, $attributeCode);

        // Etape 1 : valider les en-tetes (nombre de colonnes + noms — toujours 6 colonnes)
        $headerErrors = $this->csvValidator->validateHeaders($allRows[0] ?? []);
        if (!empty($headerErrors)) {
            // Mauvaises colonnes = decalages de lignes faux aussi — arreter immediatement
            return ['is_valid' => false, 'errors' => $headerErrors, 'rows' => []];
        }

        // Etape 2 : valider toutes les lignes de donnees
        $dataRows  = array_slice($allRows, 1);
        $rowErrors = $this->csvValidator->validateRows($dataRows, $attributeCode, $swatchType);

        return [
            'is_valid' => empty($rowErrors),
            'errors'   => $rowErrors,
            'rows'     => $allRows,  // retourne pour le tableau d'apercu
        ];
    } catch (Throwable $e) {
        return ['is_valid' => false, 'errors' => [$e->getMessage()], 'rows' => []];
    }
}"""),
        space(),
        h3("readAllRows(string $filePath, string $attributeCode): array"),
        p("Charge toutes les lignes CSV en memoire. La validation necessite des regles "
          "inter-lignes (doublons, unicite is_default), donc le fichier entier doit etre "
          "en memoire a la fois."),
        code(
"""private function readAllRows(string $filePath, string $attributeCode): array
{
    return [
        $this->csvValidator->getSwatchType($attributeCode),
        // iterator_to_array() vide le generateur dans un tableau simple.
        // false = ne pas conserver les cles du generateur (donne 0,1,2,... pas les numeros de ligne)
        iterator_to_array($this->streamingReader->read($filePath), false),
    ];
}

// Resultat pour l'exemple (valid_color.csv avec Coral + Teal) :
// [
//   SWATCH_VISUAL,   // swatchType — color est un attribut echantillon visuel
//   [
//     ['attribute_code','store_view','value','hex_code','sort_order','is_default'], // ligne 0 (en-tete)
//     ['color','default','Coral','#FF6B6B','1','1'],   // ligne 1
//     ['color','fr','Corail','#FF6B6B','1','1'],        // ligne 2
//     ...
//   ]
// ]"""),
        space(),
        h3("import(string $filePath, string $attributeCode): array"),
        code(
"""public function import(string $filePath, string $attributeCode): array
{
    $this->logger->info('Import started - attribute: ' . $attributeCode);

    try {
        // 1. Re-valider (filet de securite : l'import ne doit jamais tourner sur des donnees invalides)
        $validation = $this->validate($filePath, $attributeCode);
        if (!$validation['is_valid']) {
            foreach ($validation['errors'] as $error) {
                $this->logger->error('Validation error: ' . $error);
            }
            return ['success' => false, 'messages' => $validation['errors'],
                    'imported' => 0, 'skipped' => 0];
        }

        // 2. Reutiliser le type echantillon et les lignes de validate() — pas de 2e lecture fichier
        $attribute       = $this->eavConfig->getAttribute('catalog_product', $attributeCode);
        $swatchType      = $validation['swatch_type'];
        $existingOptions = $this->loadExistingOptions((int) $attribute->getAttributeId());

        // 3. Regrouper les lignes deja chargees par option (pas de re-lecture fichier)
        $groups = $this->groupRowsByOption($validation['rows']);

        // 4. Ecrire en base de donnees
        $result = $this->optionProcessor->processGroups(
            $groups, $existingOptions, $swatchType, $attribute
        );

        // 5. Journaliser les valeurs ignorees
        foreach ($result['skippedValues'] as $val) {
            $this->logger->warning('Skipped: "' . $val . '" already exists.');
        }

        // 6. Vider les caches
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
        p("Pre-charge tous les libelles d'options existants pour l'attribut au store_id=0 "
          "(magasin admin). C'est une seule requete DB. Le resultat est utilise comme table "
          "de hachage pour des verifications de doublons en O(1) — pas d'appel DB par option."),
        code(
"""private function loadExistingOptions(int $attributeId): array
{
    $connection = $this->resourceConnection->getConnection();
    $select = $connection->select()
        ->from(['v' => 'eav_attribute_option_value'], ['value', 'v.option_id'])
        ->join(['o' => 'eav_attribute_option'], 'v.option_id = o.option_id', [])
        ->where('o.attribute_id = ?', $attributeId)
        ->where('v.store_id = ?', 0);  // store_id=0 = magasin admin (global)

    $result = [];
    foreach ($connection->fetchAll($select) as $row) {
        $result[$row['value']] = (int) $row['option_id'];
    }
    return $result;
}

// Si Coral et Teal existent deja en DB, retourne :
// ['Coral' => 45, 'Teal' => 46]
// Utilise comme table de hachage O(1) : array_key_exists('Coral', $existing) est true -> ignorer."""),
        space(),
        h3("groupRowsByOption(array $rows): array"),
        p("Recoit le tableau de lignes deja charge (depuis <b>readAllRows</b>) et les regroupe "
          "en objets d'options logiques. Un nouveau groupe commence a chaque fois qu'une ligne "
          "default/admin apparait. La ligne d'en-tete (index 0) est sautee avec "
          "<b>array_slice($rows, 1)</b>. Le resultat est une liste plate de groupes — chaque "
          "groupe a une cle 'admin' (la ligne globale avec sort_order et is_default) et une "
          "cle 'stores' (lignes de traduction)."),
        code(
"""private function groupRowsByOption(array $rows): array
{
    $groups       = [];
    $currentGroup = null;

    foreach (array_slice($rows, 1) as $row) {   // sauter la ligne d'en-tete a l'index 0
        $storeCode = strtolower(trim($row[CsvValidator::COL_STORE_VIEW] ?? ''));
        $isAdmin   = in_array($storeCode, StoreResolver::ADMIN_STORE_CODES, true);

        if ($isAdmin) {
            if ($currentGroup !== null) {
                $groups[] = $currentGroup;  // sauvegarder le groupe venant d'etre complete
            }
            $currentGroup = ['admin' => $row, 'stores' => []];
        } elseif ($currentGroup !== null) {
            $currentGroup['stores'][] = $row;   // ajouter la ligne de traduction au groupe courant
        }
    }

    if ($currentGroup !== null) {
        $groups[] = $currentGroup;  // sauvegarder le dernier groupe (aucune ligne admin ne suit)
    }

    return $groups;
}

// Exemple — application au CSV de 6 lignes (2 options, 2 magasins chacune) :
//
// Entree $rows (apres array_slice, sans en-tete) :
//   ligne 0 : ['color','default','Coral','#FF6B6B','1','1']  <- isAdmin=true  -> groupe 1
//   ligne 1 : ['color','fr','Corail','#FF6B6B','1','1']      <- isAdmin=false -> magasins groupe 1
//   ligne 2 : ['color','en','Coral','#FF6B6B','1','1']       <- isAdmin=false -> magasins groupe 1
//   ligne 3 : ['color','default','Teal','#008080','2','0']   <- isAdmin=true  -> sauve groupe 1, groupe 2
//   ligne 4 : ['color','fr','Sarcelle','#008080','2','0']    <- isAdmin=false -> magasins groupe 2
//   ligne 5 : ['color','en','Teal','#008080','2','0']        <- isAdmin=false -> magasins groupe 2
//   (fin boucle)                                             -> sauve groupe 2
//
// Sortie $groups :
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
        p("Convertit les codes de magasin du CSV en store_ids Magento pour les ecritures en DB. "
          "Le cahier des charges (Section 4) definit le format CSV avec <b>store_view = 'default'</b> "
          "comme ligne globale — donc 'default' et 'admin' sont acceptes comme alias pour store_id=0."),
        code(
"""// Source de verite unique — referencee aussi dans Validator et ImportService.
// Plus de litteraux ['admin','default'] eparpilles dans 4 fichiers.
public const ADMIN_STORE_CODES = ['admin', 'default'];

public function getStoreId(string $storeCode): int
{
    if (in_array(strtolower($storeCode), self::ADMIN_STORE_CODES, true)) {
        return 0;
    }
    return (int) $this->storeManager->getStore($storeCode)->getId();
}

public function isValidStoreCode(string $storeCode): bool
{
    if (in_array(strtolower($storeCode), self::ADMIN_STORE_CODES, true)) {
        return true;
    }
    return in_array($storeCode, $this->getAllStoreCodes(), true);
}

// Memoisation — storeManager->getStores() n'est appele qu'une fois par requete.
// validateRows() appelle isValidStoreCode() une fois par ligne de donnees — sans memoisation
// un CSV de 500 lignes appellerait StoreManager 500 fois.
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
        p("Exemple — correspondance de chaque store_view CSV vers un store_id DB :"),
        code(
"""// Valeurs de la colonne store_view de notre CSV d'exemple :
getStoreId('default') -> 0   // intercepte — le cahier des charges definit ceci comme ligne globale
getStoreId('fr')      -> 2   // recherche StoreManager — vue magasin francaise
getStoreId('en')      -> 3   // recherche StoreManager — vue magasin anglaise

// getAllStoreCodes() sur un magasin avec les vues fr + en retourne :
['default', 'fr', 'en']"""),
        callout("warn", "StoreManager->getStore('default') retourne store_id=1 (la vue de magasin "
                "par defaut), PAS store_id=0. Passer 'default' via StoreManager sauvegarderait "
                "les libelles dans le mauvais magasin. L'alias explicite intercepte 'default'/'admin' "
                "avant d'atteindre StoreManager, comme l'exige le format CSV du cahier des charges."),
        space(),

        h2("Model/Attribute/OptionProcessor.php"),
        filepath("Aichouchm_AttributeImport/Model/Attribute/OptionProcessor.php"),
        p("Ecrit toutes les nouvelles options en base de donnees avec le nombre minimal de "
          "requetes. Ignore les options dont le libelle existe deja dans $existingOptions."),
        space(),
        h3("processGroups() — la boucle principale d'ecriture DB"),
        code(
"""public function processGroups(
    array $groups,
    array $existingOptions,  // ex. [] si DB vide, ou ['Coral' => 45] si Coral existe deja
    int $swatchType,
    AttributeInterface $attribute
): array {
    $newOptions = [];  // cle 'new_0', 'new_1', etc. (avant insertion DB)
    $labelRows  = [];  // tableau plat de toutes les lignes de libelles a inserer en lot
    $swatchRows = [];  // tableau plat de tous les echantillons a inserer en lot
    $defaultKey = null;
    $skipped    = [];

    foreach ($groups as $group) {
        $adminRow = $group['admin'];
        $value    = $adminRow[CsvValidator::COL_VALUE];   // col 2

        // Verification de doublon O(1) via la table de hachage pre-chargee
        if (array_key_exists($value, $existingOptions)) {
            $skipped[] = $value;
            continue;
        }

        $key = 'new_' . count($newOptions);  // cle temporaire avant INSERT

        $newOptions[$key] = [
            'attribute_id' => $attribute->getAttributeId(),
            'sort_order'   => (int) ($adminRow[CsvValidator::COL_SORT_ORDER] ?? 0),  // col 4
        ];

        if (($adminRow[CsvValidator::COL_IS_DEFAULT] ?? '0') === '1') {  // col 5
            $defaultKey = $key;  // se souvenir quelle option est la valeur par defaut
        }

        // Libelle admin (global)
        $labelRows[] = ['key' => $key, 'store_id' => 0, 'value' => $value];

        // Ligne echantillon — col 3 (hex_code) ecrite uniquement si attribut echantillon visuel
        if ($swatchType !== CsvValidator::SWATCH_NONE) {
            $swatchRows[] = [
                'key'      => $key,
                'store_id' => 0,
                'type'     => 1,      // 1 = couleur hex visuelle
                'value'    => $adminRow[CsvValidator::COL_SWATCH] ?? '',  // col 3
            ];
        }

        // Libelles de traduction par vue de magasin
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
        h3("bulkSave() — les ecritures DB reelles"),
        code(
"""private function bulkSave(
    array $newOptions, array $labelRows, array $swatchRows,
    ?string $defaultKey, AttributeInterface $attribute
): void {
    $connection = $this->resourceConnection->getConnection();

    // Toutes les ecritures dans une transaction — si une requete echoue, tout est annule.
    $connection->beginTransaction();
    try {
        // 1. Un INSERT par option — necessaire pour capturer chaque lastInsertId
        //    Impossible d'utiliser insertMultiple car on a besoin de l'option_id assigne par DB
        //    pour chaque ligne avant de construire les lignes de libelles/echantillons.
        $keyToOptionId = [];
        foreach ($newOptions as $key => $optionData) {
            $connection->insert('eav_attribute_option', $optionData);
            $keyToOptionId[$key] = (int) $connection->lastInsertId();
        }

        // 2. TOUS les libelles en UNE SEULE requete.
        $labelInserts = [];
        foreach ($labelRows as $lr) {
            $labelInserts[] = [
                'option_id' => $keyToOptionId[$lr['key']],
                'store_id'  => $lr['store_id'],
                'value'     => $lr['value'],
            ];
        }
        $connection->insertOnDuplicate('eav_attribute_option_value', $labelInserts, ['value']);

        // 3. Definir is_default sur l'enregistrement d'attribut si une option avait is_default=1
        if ($defaultKey !== null && isset($keyToOptionId[$defaultKey])) {
            $connection->update('eav_attribute',
                ['default_value' => (string) $keyToOptionId[$defaultKey]],
                ['attribute_id = ?' => $attribute->getAttributeId()]
            );
        }

        // 4. TOUS les echantillons en UNE SEULE requete
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
        throw $e;  // re-lancer pour que ImportService puisse journaliser et retourner l'echec
    }
}"""),
        p("Nombre total de requetes DB pour N nouvelles options (chacune avec S vues de magasin) :"),
        simple_table(
            ["Requete", "Nombre", "Description"],
            [
                ["INSERT eav_attribute_option",       "N",   "Un par nouvelle option (besoin de lastInsertId)"],
                ["INSERT eav_attribute_option_value",  "1",   "Tous les libelles en un INSERT groupe"],
                ["UPDATE eav_attribute",               "0-1", "Uniquement si une option a is_default=1"],
                ["INSERT eav_attribute_option_swatch", "0-1", "Tous les echantillons en un INSERT groupe"],
            ],
            col_widths=[5.5*cm, 1.5*cm, 10*cm]
        ),
        callout("good", "Pour 200 options avec 3 vues de magasin : N+2 = 202 requetes au total. "
                "Contre attributeRepository->save() par option qui declenche un cycle complet "
                "de chargement + sauvegarde EAV (~600 requetes). Mesure ~40x plus rapide sur "
                "une stack Docker locale."),
        space(),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 7 — Bloc Preview et Template
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("7  Bloc Preview et Template"), space()]
    story += [
        h2("Block/Adminhtml/Import/Preview.php"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Import/Preview.php"),
        p("Bloc minimal — etend Template et expose une methode helper utilisee par le template."),
        code(
"""class Preview extends Template
{
    public function formatHeader(string $value): string
    {
        return ucwords(str_replace('_', ' ', strtolower($value)));
    }
}

// Exemples :
// formatHeader('attribute_code') -> 'Attribute Code'
// formatHeader('hex_code')       -> 'Hex Code'
// formatHeader('is_default')     -> 'Is Default'"""),
        space(),

        h2("view/adminhtml/templates/import/preview.phtml"),
        filepath("Aichouchm_AttributeImport/view/adminhtml/templates/import/preview.phtml"),
        p("Recoit <b>$rows</b> (CSV complet en tableau 2D avec en-tete) et <b>$errors</b> "
          "(chaines d'erreurs de validation). Si $errors n'est pas vide, affiche des messages "
          "en rouge. Si $rows a plus d'une ligne, genere un tableau."),
        code(
"""<?php if (!empty($errors)): ?>
    <div class="messages">
        <?php foreach ($errors as $error): ?>
            <!-- Pas de <div> interne — evite le pseudo-element icone ::before de Magento -->
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
        <?= count($rows) - 1 ?> lignes de donnees trouvees.
        <?php if (empty($errors)): ?>
            <strong>Toutes les lignes sont valides. Vous pouvez proceder a l'import.</strong>
        <?php endif; ?>
    </p>
<?php endif; ?>"""),
        callout("info", "array_slice($rows, 1) saute la ligne 0 (l'en-tete) lors de la "
                "construction du corps du tableau. $rows[0] est utilise uniquement pour la "
                "ligne d'en-tete. count($rows) > 1 evite de generer un tableau vide si le "
                "CSV n'a qu'un en-tete."),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 8 — Visualiseur de journal
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("8  Visualiseur de journal"), space()]
    story += [
        h2("Controller/Adminhtml/Import/Log.php"),
        filepath("Aichouchm_AttributeImport/Controller/Adminhtml/Import/Log.php"),
        p("Controleur de page standard. Retourne un resultat Page et definit le titre de la page. "
          "Meme structure que Index — seule la chaine de titre differe."),
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
        $resultPage->getConfig()->getTitle()->prepend(__('Import Attribute Log'));
        return $resultPage;
    }
}"""),
        space(),

        h2("Block/Adminhtml/Log.php"),
        filepath("Aichouchm_AttributeImport/Block/Adminhtml/Log.php"),
        p("Lit le fichier journal depuis le systeme de fichiers Magento et expose les lignes "
          "au template. Les 200 dernieres lignes sont chargees dans l'ordre inverse "
          "(plus recent en premier)."),
        code(
"""private const LOG_FILE    = 'log/attribute_import.log';
private const DEFAULT_LINES = 200;

public function getLogLines(int $limit = self::DEFAULT_LINES): array
{
    $varDir = $this->filesystem->getDirectoryRead(DirectoryList::VAR_DIR);

    if (!$varDir->isExist(self::LOG_FILE)) {
        return [];  // pas encore d'imports — fichier inexistant
    }

    $content = $varDir->readFile(self::LOG_FILE);
    $lines   = array_reverse(array_filter(explode("\\n", $content)));
    return array_slice($lines, 0, $limit);
}

public function getLogUrl():    string { return $this->getUrl('attributeimport/import/log'); }
public function getImportUrl(): string { return $this->getUrl('attributeimport/import/index'); }"""),
        callout("info", "filesystem->getDirectoryRead(VAR_DIR) abstrait le chemin du systeme de "
                "fichiers. readFile() lit le fichier sans l'executer. "
                "L'inversion de tableau rend les entrees les plus recentes visibles en premier "
                "sans charger tout le fichier en memoire au prealable."),
        space(),

        h2("view/adminhtml/templates/import/log.phtml"),
        filepath("Aichouchm_AttributeImport/view/adminhtml/templates/import/log.phtml"),
        p("Affiche les lignes du journal dans une boite sombre de style terminal monospace "
          "(<b>font-size: 1.5rem, padding: 0.5rem</b>). Les lignes sont colorees selon le "
          "niveau de log Monolog, detecte en cherchant la chaine de niveau dans la ligne."),
        code(
"""// Format de ligne Monolog :
// [2026-04-15 14:32:01] AttributeImport.INFO: Import started - attribute: color [] []
// [2026-04-15 14:32:01] AttributeImport.WARNING: Skipped: "Coral" already exists. [] []
// [2026-04-15 14:32:01] AttributeImport.ERROR: Validation error: Row 2... [] []

// Detection de couleur :
$colour = '#d4d4d4';                                 // defaut : gris clair
if (stripos($trimmed, '.ERROR')   !== false) $colour = '#f88585';  // rouge
if (stripos($trimmed, '.WARNING') !== false) $colour = '#ffd580';  // ambre
if (stripos($trimmed, '.INFO')    !== false) $colour = '#87d7a0';  // vert"""),
        simple_table(
            ["Niveau", "Couleur", "Quand journalise"],
            [
                ["INFO",    "Vert (#87d7a0)",  "Import demarre ; import termine avec les compteurs"],
                ["WARNING", "Ambre (#ffd580)", "Option ignoree car elle existe deja en DB"],
                ["ERROR",   "Rouge (#f88585)", "Echec de validation ; exception inattendue"],
            ],
            col_widths=[2.5*cm, 4.5*cm, 10*cm]
        ),
        PageBreak(),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 9 — Journal de refactoring
    # ─────────────────────────────────────────────────────────────────────────
    story += [h1("9  Journal de refactoring"), space()]
    story += [
        p("Modifications effectuees pendant le developpement pour simplifier le code. "
          "Chaque entree explique ce qui a ete supprime et pourquoi."),
        space(),
        simple_table(
            ["Quoi", "Avant", "Apres", "Pourquoi"],
            [
                ["Alias de colonne echantillon",
                 "SWATCH_COL_NAMES = ['swatch','hex_code','swatch_value','color']",
                 "SWATCH_COLUMN = 'hex_code'",
                 "Seul hex_code est documente. Les autres alias n'etaient jamais dans la spec."],
                ["Boucle validateHeaders()",
                 "if (is_array($exp)) { in_array(...) } elseif ($cell !== $exp) ...",
                 "if ($cell !== $expected[$i]) ...",
                 "Une fois SWATCH_COL_NAMES devenu une chaine, la branche is_array etait du code mort."],
                ["Support echantillon texte",
                 "Constante SWATCH_TEXT, branche SWATCH_TEXT dans processGroups(), detectSwatchType() retournant 0/1/2",
                 "Supprime entierement",
                 "Pas dans la spec fonctionnelle. La spec ne montre que les echantillons de couleur hex."],
                ["Echantillons URL image",
                 "isValidSwatchValue() verificait regex hex et URL",
                 "Uniquement hex /^#[A-Fa-f0-9]{6}$/ verifie",
                 "Pas dans la spec. Simplifie la validation."],
                ["Alias code magasin '0'",
                 "in_array(..., ['admin','default','0'])",
                 "in_array(..., StoreResolver::ADMIN_STORE_CODES)",
                 "Personne n'ecrit '0' comme code magasin dans un CSV. Litteraux extraits en constante."],
                ["Injection DI bloc journal",
                 "$logFile injecte via di.xml comme '/var/log/attribute_import.log', puis nettoye avec str_replace('/var/','',...)",
                 "private const LOG_FILE = 'log/attribute_import.log'",
                 "Circulaire : injecter /var/log/x pour retirer /var/ immediatement. La constante est plus simple."],
                ["Boucle readAllRows()",
                 "foreach ($reader->read()) as $row) { $rows[] = $row; }",
                 "iterator_to_array($reader->read(), false)",
                 "Fonction PHP integree qui fait la meme chose en une ligne."],
                ["Generation d'URL AJAX",
                 "toRelativePath() retirait schema/host/port de getUrl()",
                 "getUrl() utilise directement",
                 "toRelativePath() etait un contournement pour un probleme de port en dev. Pas une responsabilite du module."],
                ["Index de colonnes magiques",
                 "$row[0], $row[1], $row[3] eparpilles dans Validator, OptionProcessor, ImportService",
                 "Constantes COL_* publiques dans Validator, referencees partout",
                 "Les nombres magiques sont des bugs silencieux. Un renommage de colonne cassait trois fichiers."],
                ["Formats CSV doubles",
                 "CSV 5 colonnes pour select simple, 6 colonnes pour echantillon visuel. dataColumnOffsets() calculait les decalages dynamiquement.",
                 "Format unique 6 colonnes. hex_code toujours present, vide pour non-echantillon.",
                 "La logique de decalage existait uniquement pour le double format. Un seul format elimine la complexite."],
                ["Duplication ADMIN_RESOURCE",
                 "public const ADMIN_RESOURCE = '...' redeclare identiquement dans les 4 controleurs.",
                 "Declaration unique dans AbstractAction ; tous les controleurs l'etendent.",
                 "Un renommage de la ressource ACL necessitait 4 modifications. Source de verite unique."],
            ],
            col_widths=[3.5*cm, 4.5*cm, 3.5*cm, 5.5*cm]
        ),
        space(2),
        hr(),
        PageBreak(),

        # ── Section 10 — Plan de test de demonstration ─────────────────────
        h1("10  Plan de test de demonstration"),
        p("Tous les fichiers de test sont dans <b>Test/sample/</b>. Executer les tests dans "
          "l'ordre — les tests 4 et 7 dependent des donnees ecrites par les tests precedents."),
        space(),
        simple_table(
            ["Fichier", "Attribut", "Objectif"],
            [
                ["valid_color.csv",    "color (echantillon visuel)", "3 options : Coral, Teal, Indigo — traductions fr + en"],
                ["invalid_color.csv",  "color (echantillon visuel)", "4 erreurs deliberees — test de validation"],
                ["duplicate_color.csv","color (echantillon visuel)", "Coral + Teal deja en DB du test 4, Navy nouveau — test doublon"],
                ["valid_material.csv", "material (select simple)",   "2 options : Linen, Wool — hex_code vide partout"],
                ["invalid_material.csv","material (select simple)",  "3 erreurs deliberees — validation pour attribut non-echantillon"],
            ],
            col_widths=[5*cm, 4.5*cm, 7.5*cm]
        ),
        space(),

        h2("Test 1 — Installation"),
        code(
"""bin/magento module:enable Aichouchm_AttributeImport
bin/magento setup:upgrade
bin/magento cache:flush"""),
        p("Attendu : aucune erreur. Le module apparait dans <b>bin/magento module:status</b> comme active."),
        space(),

        h2("Test 2 — Navigation et interface"),
        p("Aller dans <b>Stores → Attributes → Import Attributes</b>."),
        simple_table(
            ["Ce qu'il faut verifier", "Attendu"],
            [
                ["Entree de menu",       "\"Import Attributes\" apparait sous Stores → Attributes"],
                ["Liste deroulante",     "Affiche uniquement les attributs select/multiselect definis par l'utilisateur — pas les attributs systeme"],
                ["Upload de fichier",    "Accepte les fichiers .csv"],
                ["Bouton Verifier",      "Present et cliquable"],
                ["Bouton Importer",      "Present — active uniquement apres une verification reussie"],
                ["Bouton Voir le journal","Present — redirige vers la page du journal"],
            ],
            col_widths=[5*cm, 12*cm]
        ),
        space(),

        h2("Test 3 — Color : Erreurs de validation  (invalid_color.csv)"),
        p("Selectionner <b>color</b>. Uploader <b>invalid_color.csv</b>. Cliquer sur <b>Verifier les donnees</b>."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
color,default,Coral,#FF6B6B,abc,1    <- Ligne 2 : sort_order non numerique
color,fr,Corail,#FF6B6B,1,1
color,default,Teal,notahex,2,1       <- Ligne 4 : hex invalide + is_default=1 en double
color,fr,Sarcelle,#008080,2,0
color,default,Coral,#FF6B6B,3,0      <- Ligne 6 : "Coral" en double (meme que ligne 2)
color,fr,Corail,#FF6B6B,3,0"""),
        simple_table(
            ["Ligne", "Erreur attendue"],
            [
                ["2", "sort_order must be a number, got \"abc\""],
                ["4", "is_default=1 is already set for another option"],
                ["4", "hex_code \"notahex\" is not a valid hex colour (expected #RRGGBB)"],
                ["6", "Duplicate option value \"Coral\" within the CSV (admin store)"],
            ],
            col_widths=[2*cm, 15*cm]
        ),
        callout("warn", "4 erreurs affichees. Le bouton Importer reste bloque. Rien n'est ecrit en DB."),
        space(),

        h2("Test 4 — Color : Chemin nominal  (valid_color.csv)"),
        p("Selectionner <b>color</b>. Uploader <b>valid_color.csv</b>. Cliquer sur <b>Verifier les donnees</b>."),
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
            ["Etape", "Attendu"],
            [
                ["Verifier", "Apercu affiche les 9 lignes. 0 erreur. Bouton Importer active."],
                ["Importer", "\"Import complete. Imported: 3, Skipped (already exist): 0\""],
                ["Verifier", "Stores → Attributes → Product → color → Manage Options : Coral, Teal, Indigo avec libelles fr/en et echantillons hex"],
            ],
            col_widths=[3*cm, 14*cm]
        ),
        space(),

        h2("Test 5 — Color : Ignorement des doublons  (duplicate_color.csv)"),
        p("Executer APRES le test 4. Selectionner <b>color</b>. Uploader <b>duplicate_color.csv</b>."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
color,default,Coral,#FF6B6B,1,1      <- deja en DB depuis le test 4
color,fr,Corail,#FF6B6B,1,1
color,en,Coral,#FF6B6B,1,1
color,default,Teal,#008080,2,0       <- deja en DB depuis le test 4
color,fr,Sarcelle,#008080,2,0
color,en,Teal,#008080,2,0
color,default,Navy,#001F5B,5,0       <- nouvelle option (pas encore en DB)
color,fr,Marine,#001F5B,5,0
color,en,Navy,#001F5B,5,0"""),
        simple_table(
            ["Etape", "Attendu"],
            [
                ["Verifier", "0 erreurs de validation — les doublons sont une verification DB, pas CSV."],
                ["Importer", "\"Imported: 1, Skipped (already exist): 2\" — seulement Navy cree."],
                ["Verifier", "L'attribut color a maintenant Coral, Teal, Indigo (du test 4) + Navy."],
            ],
            col_widths=[3*cm, 14*cm]
        ),
        callout("info", "Selon la regle 5 du cahier des charges : les doublons sont journalises "
                "comme avertissements et ignores — jamais ecrases."),
        space(),

        h2("Test 6 — Material : Erreurs de validation  (invalid_material.csv)"),
        p("Selectionner <b>material</b>. Uploader <b>invalid_material.csv</b>. Cliquer sur <b>Verifier les donnees</b>."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
material,default,Linen,,abc,1        <- Ligne 2 : sort_order non numerique
material,fr,Lin,,1,1
material,default,Wool,,2,2           <- Ligne 4 : is_default doit etre 0 ou 1, recu "2"
material,fr,Laine,,2,0
material,default,Linen,,3,0          <- Ligne 6 : "Linen" en double
material,fr,Lin,,3,0"""),
        simple_table(
            ["Ligne", "Erreur attendue"],
            [
                ["2", "sort_order must be a number, got \"abc\""],
                ["4", "is_default must be 0 or 1, got \"2\""],
                ["6", "Duplicate option value \"Linen\" within the CSV (admin store)"],
            ],
            col_widths=[2*cm, 15*cm]
        ),
        callout("warn", "3 erreurs affichees. hex_code est vide partout — pas d'erreurs d'echantillon "
                "car material est un select simple."),
        space(),

        h2("Test 7 — Material : Chemin nominal  (valid_material.csv)"),
        p("Selectionner <b>material</b>. Uploader <b>valid_material.csv</b>. "
          "La colonne hex_code est vide — le module ne doit pas generer d'erreur."),
        code(
"""attribute_code,store_view,value,hex_code,sort_order,is_default
material,default,Linen,,1,1
material,fr,Lin,,1,1
material,en,Linen,,1,1
material,default,Wool,,2,0
material,fr,Laine,,2,0
material,en,Wool,,2,0"""),
        simple_table(
            ["Etape", "Attendu"],
            [
                ["Verifier", "0 erreur. Cellules hex_code vides ignorees — material n'est pas un echantillon visuel."],
                ["Importer", "\"Imported: 2, Skipped (already exist): 0\""],
                ["Verifier", "L'attribut material a Linen + Wool avec libelles fr/en."],
            ],
            col_widths=[3*cm, 14*cm]
        ),
        space(),

        h2("Test 8 — Visualiseur de journal"),
        p("Naviguer vers <b>Stores → Attributes → Import Attributes → Voir le journal</b>."),
        simple_table(
            ["Ce qu'il faut verifier", "Attendu"],
            [
                ["Entrees INFO",    "\"Import started\" + \"Import complete\" pour chaque import"],
                ["Entrees WARNING", "\"Skipped: Coral already exists\" et \"Skipped: Teal already exists\" du test 5"],
                ["Entrees ERROR",   "Messages d'erreur de validation des tests 3 et 6"],
                ["Codage couleur",  "INFO=vert, WARNING=ambre, ERROR=rouge"],
                ["Horodatages",     "Chaque ligne a un prefixe date + heure"],
            ],
            col_widths=[5*cm, 12*cm]
        ),
        space(),

        h2("Test 9 — ACL / Permissions"),
        p("Aller dans <b>Systeme → Permissions → Roles utilisateurs</b>. Modifier un role."),
        simple_table(
            ["Ce qu'il faut verifier", "Attendu"],
            [
                ["Arbre des ressources", "Stores → Stores Attributes → Import Attributes est une ressource accordable"],
                ["Refuser l'acces",      "Un role sans ressource ne voit pas l'entree de menu et obtient 403 sur l'URL directe"],
            ],
            col_widths=[4*cm, 13*cm]
        ),
        space(),
        hr(),
        space(0.5),
        Paragraph(
            "Aichouchm_AttributeImport  |  Licence MIT  |  Mehdi Aichouch",
            S("foot", fontSize=8, textColor=GREY, alignment=TA_CENTER)
        ),
    ]

    # Aplatir : code() peut retourner une liste si un bloc est trop grand pour une page
    flat = []
    for item in story:
        if isinstance(item, list):
            flat.extend(item)
        else:
            flat.append(item)
    return flat

# ── Generer le PDF ────────────────────────────────────────────────────────────
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
