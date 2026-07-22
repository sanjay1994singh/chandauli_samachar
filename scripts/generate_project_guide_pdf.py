from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "chandauli_samachar_complete_upload_guide.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

FONT = r"C:\Windows\Fonts\Nirmala.ttc"
pdfmetrics.registerFont(TTFont("Nirmala", FONT, subfontIndex=0, shapable=True))
pdfmetrics.registerFont(TTFont("NirmalaBold", FONT, subfontIndex=0, shapable=True))

RED = colors.HexColor("#D71920")
NAVY = colors.HexColor("#101D32")
INK = colors.HexColor("#17243A")
MUTED = colors.HexColor("#667085")
LIGHT = colors.HexColor("#F3F6FA")
LINE = colors.HexColor("#DDE3EB")
GREEN = colors.HexColor("#157347")
ORANGE = colors.HexColor("#B45309")
BASE = "https://chandaulisamacharexpress.in"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Hindi", fontName="Nirmala", fontSize=10.5, leading=16, textColor=INK))
styles.add(ParagraphStyle(name="SmallHindi", fontName="Nirmala", fontSize=8.4, leading=12.5, textColor=MUTED))
styles.add(ParagraphStyle(name="TitleHindi", fontName="NirmalaBold", fontSize=27, leading=34, textColor=NAVY, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="SubTitleHindi", fontName="Nirmala", fontSize=12, leading=18, textColor=MUTED, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="H1Hindi", fontName="NirmalaBold", fontSize=20, leading=27, textColor=NAVY, spaceAfter=8))
styles.add(ParagraphStyle(name="H2Hindi", fontName="NirmalaBold", fontSize=14, leading=20, textColor=RED, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name="H3Hindi", fontName="NirmalaBold", fontSize=11, leading=16, textColor=NAVY, spaceBefore=5, spaceAfter=3))
styles.add(ParagraphStyle(name="WhiteHindi", fontName="NirmalaBold", fontSize=11, leading=15, textColor=colors.white))
styles.add(ParagraphStyle(name="CellHindi", fontName="Nirmala", fontSize=8.8, leading=12.5, textColor=INK))
styles.add(ParagraphStyle(name="CellHead", fontName="NirmalaBold", fontSize=8.8, leading=12, textColor=colors.white, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Callout", fontName="Nirmala", fontSize=9.2, leading=14, textColor=INK, backColor=colors.HexColor("#FFF8E7"), borderColor=colors.HexColor("#F4D48A"), borderWidth=0.7, borderPadding=8))


def p(text, style="Hindi"):
    return Paragraph(text, styles[style])


def link(label, url):
    return f'<link href="{url}" color="#D71920"><u>{label}</u></link>'


def bullets(items):
    return [p("• " + item) for item in items]


def page_header_footer(c: canvas.Canvas, doc):
    c.saveState()
    w, h = A4
    if doc.page > 1:
        c.setFillColor(NAVY)
        c.rect(0, h - 13 * mm, w, 13 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("NirmalaBold", 8.5)
        c.drawString(16 * mm, h - 8.5 * mm, "चंदौली समाचार एक्सप्रेस - प्रोजेक्ट एवं अपलोड गाइड")
    c.setStrokeColor(LINE)
    c.line(15 * mm, 13 * mm, w - 15 * mm, 13 * mm)
    c.setFillColor(MUTED)
    c.setFont("Nirmala", 7.5)
    c.drawString(15 * mm, 8.5 * mm, "तैयार: 19 जुलाई 2026 | स्रोत: Django प्रोजेक्ट + लाइव साइट")
    c.drawRightString(w - 15 * mm, 8.5 * mm, f"पृष्ठ {doc.page}")
    c.restoreState()


class BrowserMock(Flowable):
    def __init__(self, title, url, kind="home", height=112 * mm):
        super().__init__()
        self.title, self.url, self.kind, self.height = title, url, kind, height
        self.width = 178 * mm

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.setStrokeColor(LINE)
        c.setFillColor(colors.white)
        c.roundRect(0, 0, w, h, 4 * mm, fill=1, stroke=1)
        c.setFillColor(colors.HexColor("#E9EEF5"))
        c.roundRect(0, h - 12 * mm, w, 12 * mm, 4 * mm, fill=1, stroke=0)
        for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
            c.setFillColor(colors.HexColor(col))
            c.circle(6 * mm + i * 5 * mm, h - 6 * mm, 1.5 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.roundRect(24 * mm, h - 9 * mm, 145 * mm, 6 * mm, 2 * mm, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont("Nirmala", 6.8)
        c.drawString(28 * mm, h - 7.2 * mm, self.url)

        if self.kind == "home":
            self._home(c, w, h - 12 * mm)
        elif self.kind == "admin":
            self._admin(c, w, h - 12 * mm)
        elif self.kind == "article":
            self._article_form(c, w, h - 12 * mm)
        elif self.kind == "ad":
            self._ad_form(c, w, h - 12 * mm)

    def _label(self, c, x, y, text, bg=RED, width=28 * mm):
        c.setFillColor(bg)
        c.roundRect(x, y, width, 7 * mm, 2 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("NirmalaBold", 6.8)
        c.drawCentredString(x + width / 2, y + 2.2 * mm, text)

    def _home(self, c, w, h):
        c.setFillColor(NAVY)
        c.rect(0, h - 8 * mm, w, 8 * mm, fill=1, stroke=0)
        c.setFillColor(RED)
        c.roundRect(7 * mm, h - 24 * mm, 12 * mm, 12 * mm, 3 * mm, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("NirmalaBold", 13)
        c.drawString(23 * mm, h - 19 * mm, "चंदौली समाचार एक्सप्रेस")
        c.setFillColor(LIGHT)
        c.rect(0, h - 36 * mm, w, 8 * mm, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("NirmalaBold", 7)
        c.drawString(7 * mm, h - 33.5 * mm, "होम  |  स्थानीय  |  राजनीति  |  शिक्षा  |  अपराध  |  संपर्क")
        c.setFillColor(colors.HexColor("#30445F"))
        c.roundRect(7 * mm, h - 92 * mm, 112 * mm, 50 * mm, 3 * mm, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#7E92AA"))
        c.rect(7 * mm, h - 68 * mm, 112 * mm, 26 * mm, fill=1, stroke=0)
        self._label(c, 11 * mm, h - 87 * mm, "Featured खबर", width=30 * mm)
        c.setFillColor(colors.white)
        c.setFont("NirmalaBold", 11)
        c.drawString(11 * mm, h - 76 * mm, "मुख्य समाचार का शीर्षक यहाँ दिखाई देगा")
        c.setFillColor(colors.HexColor("#E6F0FA"))
        c.roundRect(124 * mm, h - 65 * mm, 47 * mm, 23 * mm, 3 * mm, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#FFF2CC"))
        c.roundRect(124 * mm, h - 92 * mm, 47 * mm, 23 * mm, 3 * mm, fill=1, stroke=0)
        self._label(c, 130 * mm, h - 88 * mm, "होम विज्ञापन", bg=ORANGE, width=34 * mm)
        c.setFillColor(NAVY)
        c.setFont("NirmalaBold", 10)
        c.drawString(7 * mm, h - 103 * mm, "ताज़ा खबरें")
        for i in range(3):
            x = 7 * mm + i * 56 * mm
            c.setFillColor(LIGHT)
            c.roundRect(x, h - 140 * mm, 51 * mm, 31 * mm, 2 * mm, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#CBD5E1"))
            c.rect(x, h - 124 * mm, 51 * mm, 15 * mm, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont("NirmalaBold", 6.8)
            c.drawString(x + 3 * mm, h - 130 * mm, "खबर कार्ड: फोटो + शीर्षक")

    def _admin(self, c, w, h):
        c.setFillColor(colors.HexColor("#417690"))
        c.rect(0, h - 13 * mm, w, 13 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("NirmalaBold", 11)
        c.drawString(7 * mm, h - 8.5 * mm, "Django administration")
        c.setFillColor(LIGHT)
        c.rect(0, 0, 37 * mm, h - 13 * mm, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("NirmalaBold", 8)
        c.drawString(5 * mm, h - 24 * mm, "साइट प्रबंधन")
        modules = ["Articles", "Advertisements", "Categories", "States / Cities", "Users", "Contact messages"]
        y = h - 37 * mm
        for m in modules:
            c.setFillColor(colors.white)
            c.roundRect(43 * mm, y, 123 * mm, 11 * mm, 2 * mm, fill=1, stroke=0)
            c.setFillColor(INK)
            c.setFont("NirmalaBold", 8)
            c.drawString(48 * mm, y + 3.7 * mm, m)
            self._label(c, 142 * mm, y + 2 * mm, "+ Add", bg=GREEN, width=19 * mm)
            y -= 15 * mm

    def _fields(self, c, fields, start_y, action):
        y = start_y
        for label, hint in fields:
            c.setFillColor(INK)
            c.setFont("NirmalaBold", 7.2)
            c.drawString(8 * mm, y + 3.3 * mm, label)
            c.setStrokeColor(LINE)
            c.setFillColor(colors.white)
            c.roundRect(43 * mm, y, 124 * mm, 8 * mm, 1.5 * mm, fill=1, stroke=1)
            c.setFillColor(MUTED)
            c.setFont("Nirmala", 6.2)
            c.drawString(47 * mm, y + 2.6 * mm, hint)
            y -= 11 * mm
        self._label(c, 128 * mm, max(4 * mm, y - 1 * mm), action, bg=GREEN, width=39 * mm)

    def _article_form(self, c, w, h):
        c.setFillColor(colors.HexColor("#417690"))
        c.rect(0, h - 13 * mm, w, 13 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("NirmalaBold", 11)
        c.drawString(7 * mm, h - 8.5 * mm, "Add article / खबर जोड़ें")
        fields = [
            ("Title", "खबर का पूरा शीर्षक"),
            ("Slug", "URL के लिए english-small-words"),
            ("Summary", "2-3 पंक्ति का सार"),
            ("Content", "पूरी खबर"),
            ("Featured image", "कंप्यूटर से JPG/PNG चुनें"),
            ("Category", "श्रेणी चुनें"),
            ("State / City", "स्थान चुनें"),
            ("Status", "Published"),
            ("Featured / Breaking", "जरूरत के अनुसार टिक करें"),
            ("Published at", "तारीख और समय"),
        ]
        self._fields(c, fields, h - 25 * mm, "Save and continue")

    def _ad_form(self, c, w, h):
        c.setFillColor(colors.HexColor("#417690"))
        c.rect(0, h - 13 * mm, w, 13 * mm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("NirmalaBold", 11)
        c.drawString(7 * mm, h - 8.5 * mm, "Add advertisement / विज्ञापन जोड़ें")
        fields = [
            ("Internal name", "पहचान के लिए नाम"),
            ("Advertiser", "विज्ञापनदाता"),
            ("Headline", "मुख्य लाइन"),
            ("Subheadline", "दूसरी लाइन"),
            ("Image", "Square banner JPG/PNG"),
            ("Style", "Image banner या Text creative"),
            ("WhatsApp / Contact", "क्लिक करने पर action"),
            ("Destination URL", "https://..."),
            ("Placement", "home_sidebar"),
            ("Priority", "बड़ी संख्या पहले"),
            ("Start / End", "विज्ञापन की अवधि"),
            ("Active", "टिक होना चाहिए"),
        ]
        self._fields(c, fields, h - 23 * mm, "Save")


def make_table(rows, widths):
    t = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "NirmalaBold"),
        ("FONTNAME", (0, 1), (-1, -1), "Nirmala"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.4),
        ("LEADING", (0, 0), (-1, -1), 12),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


story = []

# Cover
story += [
    Spacer(1, 28 * mm),
    p("चंदौली समाचार एक्सप्रेस", "TitleHindi"),
    p("पूरा प्रोजेक्ट समझें एवं कंटेंट अपलोड गाइड", "SubTitleHindi"),
    Spacer(1, 14 * mm),
    BrowserMock("Homepage", BASE + "/", "home", 102 * mm),
    Spacer(1, 9 * mm),
    p("यह गाइड बताती है कि वेबसाइट में कौन-सा हिस्सा क्या करता है, एडमिन में कहाँ क्या अपलोड करना है, और सेव करने के बाद वह लाइव साइट पर कहाँ दिखाई देगा।", "Callout"),
    Spacer(1, 8 * mm),
    p("<b>लाइव वेबसाइट:</b> " + link(BASE, BASE + "/")),
    p("<b>एडमिन लॉगिन:</b> " + link(BASE + "/admin/", BASE + "/admin/")),
    PageBreak(),
]

# Overview
story += [
    p("1. प्रोजेक्ट का आसान नक्शा", "H1Hindi"),
    p("यह Django आधारित हिंदी लोकल-न्यूज़ वेबसाइट है। एडमिन पैनल में डाला गया डेटा database में सेव होता है; templates उसे homepage, category list और detail page पर दिखाते हैं।"),
]
overview = [
    [p("भाग", "CellHead"), p("क्या संभालता है", "CellHead"), p("कहाँ दिखता है", "CellHead")],
    [p("News / Article", "CellHindi"), p("शीर्षक, सार, पूरी खबर, फोटो, category, city, author, publish status", "CellHindi"), p("Homepage, category page, search और news detail", "CellHindi")],
    [p("Category", "CellHindi"), p("स्थानीय, राजनीति, शिक्षा जैसी श्रेणियाँ और navigation order", "CellHindi"), p("ऊपरी menu तथा category URL", "CellHindi")],
    [p("State / City", "CellHindi"), p("राज्य और शहर; article के स्थान के लिए", "CellHindi"), p("News card पर city नाम", "CellHindi")],
    [p("Advertisement", "CellHindi"), p("Banner/text ad, click link, WhatsApp/phone, placement, priority और date", "CellHindi"), p("अभी homepage sidebar", "CellHindi")],
    [p("Accounts / User", "CellHindi"), p("Admin, staff, reporter profile, phone, photo, bio और city", "CellHindi"), p("Article author/desk नाम", "CellHindi")],
    [p("Contact Message", "CellHindi"), p("Contact form से आए संदेश और resolved status", "CellHindi"), p("केवल admin में; public को धन्यवाद संदेश", "CellHindi")],
]
story += [Spacer(1, 3 * mm), make_table(overview, [31 * mm, 79 * mm, 65 * mm]), Spacer(1, 7 * mm)]
story += bullets([
    "<b>मुख्य URL:</b> " + link("Homepage", BASE + "/"),
    "<b>Search:</b> " + link(BASE + "/search/?q=चंदौली", BASE + "/search/?q=%E0%A4%9A%E0%A4%82%E0%A4%A6%E0%A5%8C%E0%A4%B2%E0%A5%80"),
    "<b>News detail pattern:</b> <font color='#D71920'>/news/&lt;slug&gt;/</font>",
    "<b>Category pattern:</b> <font color='#D71920'>/category/&lt;slug&gt;/</font>",
    "<b>Contact:</b> " + link(BASE + "/contact-us/", BASE + "/contact-us/"),
])
story += [p("महत्वपूर्ण: केवल <b>Status = Published</b> वाली खबर public site पर दिखाई जाती है। Draft खबर database में रहेगी, लेकिन visitor को नहीं दिखेगी।", "Callout"), PageBreak()]

# Admin
story += [
    p("2. एडमिन पैनल में प्रवेश", "H1Hindi"),
    BrowserMock("Admin", BASE + "/admin/", "admin", 103 * mm),
    Spacer(1, 6 * mm),
    p("<b>कदम:</b> ब्राउज़र में " + link(BASE + "/admin/", BASE + "/admin/") + " खोलें → admin username/password डालें → Log in करें।"),
    p("Login के बाद Articles, Advertisements, Categories, States, Cities, Users और Contact messages दिखाई देंगे। जिस सेक्शन में नया डेटा जोड़ना हो, उसके सामने <b>+ Add</b> दबाएँ।"),
    p("सुरक्षा: admin password किसी reporter या बाहरी व्यक्ति से साझा न करें। Reporter के लिए अलग staff user बनाकर केवल जरूरी permissions दें।", "Callout"),
    PageBreak(),
]

# Article upload
story += [
    p("3. नई खबर कैसे अपलोड करें", "H1Hindi"),
    p("<b>पथ:</b> Admin → News → Articles → Add article"),
    BrowserMock("Article form", BASE + "/admin/news/article/add/", "article", 137 * mm),
    Spacer(1, 5 * mm),
    p("फोटो के लिए JPG/PNG/WebP रखें; landscape image बेहतर दिखती है। सुझाया आकार 1200 × 675 px, साफ़ फोटो, और बहुत भारी file से बचें।"),
    PageBreak(),
]

article_fields = [
    [p("Field", "CellHead"), p("क्या भरें", "CellHead"), p("नतीजा", "CellHead")],
    [p("Title", "CellHindi"), p("साफ़ और पूरा हिंदी headline", "CellHindi"), p("Homepage card और detail page का बड़ा शीर्षक", "CellHindi")],
    [p("Slug", "CellHindi"), p("English lower-case: chandauli-road-news", "CellHindi"), p(BASE + "/news/chandauli-road-news/", "CellHindi")],
    [p("Summary", "CellHindi"), p("2-3 लाइन में खबर का सार", "CellHindi"), p("Lead story और cards पर preview", "CellHindi")],
    [p("Content", "CellHindi"), p("पूरी खबर; paragraph के बीच नई लाइन", "CellHindi"), p("Detail page का मुख्य लेख", "CellHindi")],
    [p("Featured image", "CellHindi"), p("अपने कंप्यूटर से फोटो चुनें", "CellHindi"), p("media/articles/YYYY/MM/ में upload; card + detail में दिखेगी", "CellHindi")],
    [p("Image URL", "CellHindi"), p("केवल external/demo image; upload photo हो तो खाली छोड़ें", "CellHindi"), p("Featured image न होने पर fallback", "CellHindi")],
    [p("Category", "CellHindi"), p("सही श्रेणी चुनें", "CellHindi"), p("Menu/category page और related news तय करेगा", "CellHindi")],
    [p("State / City", "CellHindi"), p("खबर का स्थान", "CellHindi"), p("Card पर city नाम", "CellHindi")],
    [p("Author", "CellHindi"), p("Reporter/user चुनें", "CellHindi"), p("Detail page meta में नाम", "CellHindi")],
    [p("Status", "CellHindi"), p("<b>Published</b>", "CellHindi"), p("तभी public site पर दिखाई देगी", "CellHindi")],
    [p("Breaking", "CellHindi"), p("तुरंत जरूरी खबर पर tick", "CellHindi"), p("Homepage के लाल breaking ticker में", "CellHindi")],
    [p("Featured", "CellHindi"), p("दिन की मुख्य खबर पर tick", "CellHindi"), p("Homepage के बड़े hero area में", "CellHindi")],
    [p("Published at", "CellHindi"), p("वास्तविक प्रकाशन date/time", "CellHindi"), p("Ordering और article date", "CellHindi")],
]
story += [
    p("4. Article field-by-field समझें", "H1Hindi"),
    make_table(article_fields, [32 * mm, 72 * mm, 71 * mm]),
    Spacer(1, 6 * mm),
    p("<b>Save के बाद जांच:</b> homepage refresh करें। अगर featured tick है तो बड़ी खबर; breaking tick है तो ticker; सामान्य published खबर ताज़ा खबरों के grid में दिखेगी। Article title पर click करके detail URL खोलें।", "Callout"),
    PageBreak(),
]

# Where news appears
story += [
    p("5. अपलोड की गई खबर कहाँ दिखाई देगी", "H1Hindi"),
    BrowserMock("Homepage mapping", BASE + "/", "home", 105 * mm),
    Spacer(1, 5 * mm),
]
where_rows = [
    [p("आपने क्या चुना", "CellHead"), p("लाइव साइट पर स्थान", "CellHead"), p("शर्त", "CellHead")],
    [p("Status = Published", "CellHindi"), p("ताज़ा खबरें grid और search", "CellHindi"), p("Published at सही हो", "CellHindi")],
    [p("Is Featured = Yes", "CellHindi"), p("Homepage का बड़ा hero/banner", "CellHindi"), p("Published; सबसे नया featured पहले", "CellHindi")],
    [p("Is Breaking = Yes", "CellHindi"), p("Homepage का breaking ticker", "CellHindi"), p("Published; अधिकतम 6", "CellHindi")],
    [p("Category", "CellHindi"), p("/category/slug/ सूची और menu", "CellHindi"), p("Category active हो", "CellHindi")],
    [p("Featured image", "CellHindi"), p("Hero, news card और detail page", "CellHindi"), p("File server पर media URL उपलब्ध हो", "CellHindi")],
    [p("City", "CellHindi"), p("News card की तारीख के पास", "CellHindi"), p("City selected हो", "CellHindi")],
    [p("Author", "CellHindi"), p("Detail page meta line", "CellHindi"), p("User selected हो", "CellHindi")],
]
story += [make_table(where_rows, [52 * mm, 72 * mm, 51 * mm]), Spacer(1, 5 * mm), p("View count detail page खुलने पर अपने-आप 1 बढ़ता है। उसी category की अधिकतम 4 related खबरें detail page के sidebar में आती हैं।", "Callout"), PageBreak()]

# Category and location
story += [
    p("6. Category, State और City पहले कैसे बनाएँ", "H1Hindi"),
    p("यदि dropdown में सही category/city नहीं है तो article बनाने से पहले master data बनाएँ।"),
    p("Category", "H2Hindi"),
]
story += bullets([
    "Admin → Categories → Add category.",
    "<b>Name:</b> हिंदी नाम, जैसे स्थानीय / शिक्षा / राजनीति.",
    "<b>Slug:</b> English lower-case, जैसे local / education / politics.",
    "<b>Order:</b> छोटी संख्या menu में पहले.",
    "<b>Is active:</b> tick; तभी navigation menu में आएगी.",
])
story += [p("State और City", "H2Hindi")]
story += bullets([
    "पहले Admin → States → Add state: नाम और slug.",
    "फिर Admin → Cities → Add city: state चुनें, city name और slug भरें.",
    "इसके बाद Article form में वही city चुनी जा सकेगी.",
])
story += [
    p("Category slug बदलने पर पुराना category URL टूट सकता है। Published category के slug को बिना redirect plan के न बदलें।", "Callout"),
    Spacer(1, 5 * mm),
    p("उदाहरण URL: <font color='#D71920'>https://chandaulisamacharexpress.in/category/local/</font>"),
    PageBreak(),
]

# Ads
story += [
    p("7. विज्ञापन कहाँ और कैसे अपलोड करें", "H1Hindi"),
    p("<b>पथ:</b> Admin → Advertisements → Add advertisement"),
    BrowserMock("Advertisement form", BASE + "/admin/advertisements/advertisement/add/", "ad", 145 * mm),
    PageBreak(),
]
ad_rows = [
    [p("Field", "CellHead"), p("क्या भरें", "CellHead"), p("व्यवहार", "CellHead")],
    [p("Internal name", "CellHindi"), p("केवल admin पहचान, जैसे July Clinic Ad", "CellHindi"), p("Public banner पर जरूरी नहीं दिखता", "CellHindi")],
    [p("Style", "CellHindi"), p("Image banner", "CellHindi"), p("Uploaded image पूरा ad बनेगा", "CellHindi")],
    [p("Image", "CellHindi"), p("Square 1080 × 1080 px सुझाया", "CellHindi"), p("media/advertisements/YYYY/MM/ में upload", "CellHindi")],
    [p("Destination URL", "CellHindi"), p("https:// से पूरा link", "CellHindi"), p("Ad click होने पर नया tab", "CellHindi")],
    [p("WhatsApp", "CellHindi"), p("10 digit mobile", "CellHindi"), p("URL खाली हो तो WhatsApp chat खुलेगी", "CellHindi")],
    [p("Contact", "CellHindi"), p("Phone number", "CellHindi"), p("URL/WhatsApp खाली हो तो call link", "CellHindi")],
    [p("Placement", "CellHindi"), p("<b>home_sidebar</b>", "CellHindi"), p("वर्तमान template में homepage के दाईं तरफ", "CellHindi")],
    [p("Priority", "CellHindi"), p("उच्च संख्या", "CellHindi"), p("पहले चुना जाएगा; बराबर priority पर random", "CellHindi")],
    [p("Starts / Ends", "CellHindi"), p("Campaign date/time या खाली", "CellHindi"), p("अवधि के बाहर ad नहीं दिखेगा", "CellHindi")],
    [p("Is active", "CellHindi"), p("Tick", "CellHindi"), p("Untick होने पर तुरंत बंद", "CellHindi")],
]
story += [
    p("8. Advertisement field-by-field", "H1Hindi"),
    make_table(ad_rows, [33 * mm, 70 * mm, 72 * mm]),
    Spacer(1, 6 * mm),
    p("वर्तमान code में केवल <b>home_sidebar</b> placement template में इस्तेमाल हो रहा है। Model में home_wide, article_sidebar और article_inline options हैं, लेकिन उन्हें दिखाने के लिए संबंधित templates में ad tag जोड़ना पड़ेगा।", "Callout"),
    PageBreak(),
]

# users/contact/static
story += [
    p("9. Reporter/User, Contact और Static pages", "H1Hindi"),
    p("Reporter/User", "H2Hindi"),
]
story += bullets([
    "Admin → Users → Add user; username और strong password बनाएँ.",
    "Profile में phone, profile image, bio, city और Is reporter भरें.",
    "Admin access देना हो तो Staff status और केवल जरूरी permissions दें.",
    "Article में Author चुनने पर detail page पर reporter का नाम आता है.",
])
story += [p("Contact messages", "H2Hindi")]
story += bullets([
    "Visitor " + link("Contact page", BASE + "/contact-us/") + " पर form भरता है.",
    "Message database में Contact messages में आता है.",
    "Admin पढ़कर follow-up करे और Is resolved tick कर दे.",
])
story += [p("Public information pages", "H2Hindi")]
pages_rows = [
    [p("Page", "CellHead"), p("URL", "CellHead")],
    [p("हमारे बारे में", "CellHindi"), p(link(BASE + "/about-us/", BASE + "/about-us/"), "CellHindi")],
    [p("Privacy Policy", "CellHindi"), p(link(BASE + "/privacy-policy/", BASE + "/privacy-policy/"), "CellHindi")],
    [p("Disclaimer", "CellHindi"), p(link(BASE + "/disclaimer/", BASE + "/disclaimer/"), "CellHindi")],
    [p("Terms", "CellHindi"), p(link(BASE + "/terms-and-conditions/", BASE + "/terms-and-conditions/"), "CellHindi")],
    [p("Editorial Policy", "CellHindi"), p(link(BASE + "/editorial-policy/", BASE + "/editorial-policy/"), "CellHindi")],
    [p("Correction Policy", "CellHindi"), p(link(BASE + "/correction-policy/", BASE + "/correction-policy/"), "CellHindi")],
]
story += [
    make_table(pages_rows, [50 * mm, 125 * mm]),
    Spacer(1, 6 * mm),
    p("ये static pages अभी template files में लिखे हुए हैं; admin से edit नहीं होते। Text बदलने के लिए developer को templates/pages/ की file update करके server पर deploy करना होगा।", "Callout"),
    PageBreak(),
]

# media/deploy
story += [
    p("10. File वास्तव में server पर कहाँ जाती है", "H1Hindi"),
]
media_rows = [
    [p("Upload", "CellHead"), p("Code path", "CellHead"), p("Public URL pattern", "CellHead")],
    [p("Article photo", "CellHindi"), p("media/articles/YYYY/MM/", "CellHindi"), p("/media/articles/YYYY/MM/file.jpg", "CellHindi")],
    [p("Advertisement", "CellHindi"), p("media/advertisements/YYYY/MM/", "CellHindi"), p("/media/advertisements/YYYY/MM/file.jpg", "CellHindi")],
    [p("User profile", "CellHindi"), p("media/profiles/", "CellHindi"), p("/media/profiles/file.jpg", "CellHindi")],
    [p("CSS", "CellHindi"), p("static/css/", "CellHindi"), p("/static/css/file.css", "CellHindi")],
]
story += [
    make_table(media_rows, [43 * mm, 66 * mm, 66 * mm]),
    Spacer(1, 7 * mm),
    p("Production server पर Django DEBUG=False होने पर media files को Django खुद serve नहीं करता। Hosting/Nginx/Apache में <b>/media/ → MEDIA_ROOT</b> और <b>/static/ → STATIC_ROOT</b> mapping सही होनी चाहिए। वरना admin upload सफल दिखेगा लेकिन public page पर image broken होगी।", "Callout"),
    p("Database में image का path सेव होता है; actual file media folder/storage में रहती है। Database backup और media backup दोनों जरूरी हैं।"),
    p("Code/config में MySQL production default है; local testing में DB_ENGINE=sqlite इस्तेमाल किया जा सकता है।"),
    PageBreak(),
]

# checklist troubleshooting
story += [
    p("11. Publish checklist और समस्या समाधान", "H1Hindi"),
    p("हर खबर publish करने से पहले", "H2Hindi"),
]
story += bullets([
    "Headline, spelling, नाम, स्थान और तारीख दोबारा पढ़ें.",
    "Slug unique और English lower-case रखें.",
    "सही category, city और author चुनें.",
    "Photo ownership/permission सुनिश्चित करें; गलत या भ्रामक photo न लगाएँ.",
    "Summary संक्षिप्त और content पूरा रखें.",
    "Status Published, Published at सही; Featured/Breaking केवल जरूरत पर.",
    "Save के बाद desktop और mobile दोनों पर live URL खोलकर जाँचें.",
])
trouble = [
    [p("समस्या", "CellHead"), p("सबसे संभावित कारण", "CellHead"), p("क्या करें", "CellHead")],
    [p("खबर नहीं दिख रही", "CellHindi"), p("Draft status / समय / गलत URL", "CellHindi"), p("Published करें; Published at जाँचें; homepage refresh", "CellHindi")],
    [p("फोटो broken", "CellHindi"), p("Media server mapping या file missing", "CellHindi"), p("/media/... URL खोलें; hosting media config जाँचें", "CellHindi")],
    [p("Category menu में नहीं", "CellHindi"), p("Is active off या order सीमा", "CellHindi"), p("Category active करें; homepage reload", "CellHindi")],
    [p("Ad नहीं दिख रहा", "CellHindi"), p("Inactive/date/placement/image style", "CellHindi"), p("Active, dates और home_sidebar जाँचें", "CellHindi")],
    [p("Ad click गलत", "CellHindi"), p("Destination URL priority", "CellHindi"), p("पूरा https:// URL सुधारें; URL WhatsApp/phone से पहले चुना जाता है", "CellHindi")],
    [p("Hindi text अजीब", "CellHindi"), p("Source encoding mojibake", "CellHindi"), p("Files UTF-8 में ठीक करें; deploy से पहले visual check", "CellHindi")],
]
story += [Spacer(1, 5 * mm), make_table(trouble, [45 * mm, 62 * mm, 68 * mm]), PageBreak()]

# Architecture + findings
story += [
    p("12. Developer के लिए महत्वपूर्ण निष्कर्ष", "H1Hindi"),
]
dev_rows = [
    [p("Area", "CellHead"), p("वर्तमान स्थिति", "CellHead"), p("सुझाव", "CellHead")],
    [p("Admin upload", "CellHindi"), p("Article, ad, category, city, user, message उपलब्ध", "CellHindi"), p("Reporter permissions सीमित रखें", "CellHindi")],
    [p("Ad placements", "CellHindi"), p("Model में 4; template में केवल home_sidebar", "CellHindi"), p("बाकी placements के template slots जोड़ें", "CellHindi")],
    [p("Media production", "CellHindi"), p("DEBUG में Django serve करता है", "CellHindi"), p("Nginx/hosting media mapping verify करें", "CellHindi")],
    [p("Hindi encoding", "CellHindi"), p("कई source labels mojibake रूप में दिखाई दे रहे हैं", "CellHindi"), p("UTF-8 cleanup करके regression test करें", "CellHindi")],
    [p("Weather", "CellHindi"), p("Homepage पर hard-coded 32° / साफ़ मौसम", "CellHindi"), p("Live weather API या text हटाएँ/अपडेट करें", "CellHindi")],
    [p("SEO", "CellHindi"), p("Basic title/description", "CellHindi"), p("Per-article meta, OG image, sitemap और robots जोड़ें", "CellHindi")],
    [p("Backups", "CellHindi"), p("Project में policy नहीं दिखी", "CellHindi"), p("Daily database + media backup और restore test", "CellHindi")],
]
story += [
    make_table(dev_rows, [36 * mm, 76 * mm, 63 * mm]),
    Spacer(1, 7 * mm),
    p("Project verification: Django system check सफल; local SQLite data में 6 published articles, 7 categories, 1 advertisement, 1 state और 3 cities मिले।", "Callout"),
    p("यह manual वर्तमान repository structure और live domain के आधार पर बनाया गया है। Hosting dashboard की credentials/config repository में उपलब्ध न होने के कारण server-provider-specific upload/deploy buttons इस गाइड में शामिल नहीं हैं।"),
    Spacer(1, 8 * mm),
    p("<b>मुख्य लिंक</b>", "H2Hindi"),
    p(link("लाइव Homepage", BASE + "/") + " &nbsp;&nbsp;|&nbsp;&nbsp; " + link("Admin Login", BASE + "/admin/") + " &nbsp;&nbsp;|&nbsp;&nbsp; " + link("Contact", BASE + "/contact-us/")),
]

doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    rightMargin=16 * mm,
    leftMargin=16 * mm,
    topMargin=19 * mm,
    bottomMargin=18 * mm,
    title="चंदौली समाचार एक्सप्रेस - पूरा प्रोजेक्ट एवं अपलोड गाइड",
    author="OpenAI Codex",
    subject="Django news website content upload and display guide",
)
doc.build(story, onFirstPage=page_header_footer, onLaterPages=page_header_footer)
print(OUT)
