# -*- coding: utf-8 -*-
"""
Build a professional, submission-ready A4 PDF for:
  NPC - Unit 3 : Configure a DNS Server and Web Server Using Cisco Packet Tracer
Student: Vivek Borse (PRN 2125UCSM1082)

Embeds the student's real Cisco Packet Tracer screenshots.
Output: NPC_Unit_3_Vivek_Borse.pdf
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, Preformatted, KeepTogether,
)
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "NPC_Unit_3_Vivek_Borse.pdf")

# ---------------------------------------------------------------- palette
NAVY = HexColor(0x1F3864)       # dark blue headings
BLUE = HexColor(0x2E5496)       # medium blue
GREY = HexColor(0x595959)       # body grey accents
LGREY = HexColor(0xD9D9D9)      # light grey rules
HDRBG = HexColor(0x1F3864)      # table header background
ROWBG = HexColor(0xEEF2F9)      # light row shading
CODEBG = HexColor(0xF4F6F8)     # code box background
BLACK = HexColor(0x222222)

CONTENT_W = A4[0] - 4 * cm

# ---------------------------------------------------------------- styles
def P(name, **kw):
    base = dict(fontName="Helvetica", fontSize=10.5, leading=15, textColor=BLACK)
    base.update(kw)
    return ParagraphStyle(name, **base)

st_body   = P("body", alignment=TA_JUSTIFY, spaceAfter=6)
st_h1      = P("h1", fontName="Helvetica-Bold", fontSize=15, textColor=NAVY,
               spaceBefore=2, spaceAfter=6, leading=18)
st_h2      = P("h2", fontName="Helvetica-Bold", fontSize=12, textColor=BLUE,
               spaceBefore=8, spaceAfter=4, leading=15)
st_list    = P("list", alignment=TA_LEFT, leftIndent=16, firstLineIndent=-12,
               spaceAfter=3)
st_cap     = P("cap", fontName="Helvetica-Oblique", fontSize=8.5, textColor=GREY,
               alignment=TA_CENTER, spaceBefore=3, spaceAfter=10)
st_code    = P("code", fontName="Courier", fontSize=9, leading=12.5, textColor=BLACK)
st_cell    = P("cell", fontSize=10, leading=13)
st_cellb   = P("cellb", fontName="Helvetica-Bold", fontSize=10, leading=13,
               textColor=white)

# cover styles
st_cv_small = P("cvs", alignment=TA_CENTER, fontSize=12, textColor=GREY, leading=16)
st_cv_tag   = P("cvt", alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=13,
                textColor=BLUE, leading=18)
st_cv_title = P("cvtitle", alignment=TA_CENTER, fontName="Helvetica-Bold",
                fontSize=22, textColor=NAVY, leading=27)
st_cv_sub   = P("cvsub", alignment=TA_CENTER, fontName="Helvetica-Bold",
                fontSize=14, textColor=BLACK, leading=19)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- helpers
def heading(text):
    return [Paragraph(text, st_h1),
            HRFlowable(width="100%", thickness=1.1, color=NAVY,
                       spaceBefore=1, spaceAfter=8)]


def sub(text):
    return Paragraph(text, st_h2)


def body(text):
    return Paragraph(text, st_body)


def numbered(items):
    return [Paragraph(f"{i}.&nbsp;&nbsp;{esc(t)}", st_list)
            for i, t in enumerate(items, 1)]


def bullets(items):
    return [Paragraph(f"&bull;&nbsp;&nbsp;{t}", st_list) for t in items]


def code_box(text, escape=True):
    # Preformatted renders text verbatim (it handles special characters itself),
    # so pass the raw text to avoid double-escaping of < > &.
    pre = Preformatted(text, st_code)
    t = Table([[pre]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODEBG),
        ("BOX", (0, 0), (-1, -1), 0.6, LGREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def figure(path, caption, max_w=CONTENT_W, max_h=20 * cm):
    ir = ImageReader(path)
    iw, ih = ir.getSize()
    scale = min(max_w / iw, max_h / ih)
    img = Image(path, width=iw * scale, height=ih * scale)
    img.hAlign = "CENTER"
    box = Table([[img]], colWidths=[iw * scale])
    box.hAlign = "CENTER"
    box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.8, LGREY),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return KeepTogether([box, Paragraph(caption, st_cap)])


def info_table(rows):
    data = [[Paragraph(k, P("k", fontName="Helvetica-Bold", fontSize=10.5)),
             Paragraph(v, st_cell)] for k, v in rows]
    t = Table(data, colWidths=[5 * cm, CONTENT_W - 5 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), ROWBG),
        ("GRID", (0, 0), (-1, -1), 0.5, LGREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def data_table(header, rows, widths):
    data = [[Paragraph(h, st_cellb) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), st_cell) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HDRBG),
        ("GRID", (0, 0), (-1, -1), 0.5, LGREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWBG))
    t.setStyle(TableStyle(style))
    return t


# ---------------------------------------------------------------- diagram
def draw_logical_topology(path):
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    def box(cx, cy, w, h, label, sub_, face, edge):
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=1.8, facecolor=face, edgecolor=edge, zorder=3))
        ax.text(cx, cy + 0.16, label, ha="center", va="center",
                fontsize=11, fontweight="bold", zorder=4)
        ax.text(cx, cy - 0.24, sub_, ha="center", va="center",
                fontsize=8.5, color="#333333", zorder=4)

    sw = (5.0, 3.1)
    box(sw[0], sw[1], 2.7, 0.9, "Switch0 (2960)", "Layer-2  |  no IP", "#fde9c8", "#e08e0b")

    pc_f, pc_e = "#d7e9fb", "#2f6fb0"
    sv_f, sv_e = "#dcf3df", "#2e8b45"
    nodes = {
        "DNS Server": (1.6, 5.0, sv_f, sv_e, "Fa0/1", "192.168.1.2"),
        "Web Server": (1.6, 1.2, sv_f, sv_e, "Fa0/2", "192.168.1.3"),
        "PC0":        (8.4, 5.0, pc_f, pc_e, "Fa0/3", "192.168.1.10"),
        "PC1":        (8.4, 1.2, pc_f, pc_e, "Fa0/4", "192.168.1.11"),
    }
    for name, (x, y, _, _, port, _ip) in nodes.items():
        ax.plot([x, sw[0]], [y, sw[1]], color="#7a7a7a", linewidth=1.6, zorder=1)
        mx, my = (x + sw[0]) / 2, (y + sw[1]) / 2
        ax.text(mx, my + 0.12, port, ha="center", va="center", fontsize=7.5,
                color="#555555", style="italic", zorder=2,
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    for name, (x, y, fc, ec, port, ip) in nodes.items():
        box(x, y, 2.1, 0.9, name, ip, fc, ec)

    ax.text(5.0, 5.95, "Logical Network Topology  -  192.168.1.0/24",
            ha="center", va="center", fontsize=12.5, fontweight="bold")
    ax.text(5.0, 0.2, "Domain www.npcunit3.com  ->  192.168.1.3        DNS Server  192.168.1.2",
            ha="center", va="center", fontsize=9, color="#444444")
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- footer / page numbers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        n = len(self._saved)
        for state in self._saved:
            self.__dict__.update(state)
            self._footer(n)
            super().showPage()
        super().save()

    def _footer(self, total):
        self.setStrokeColor(LGREY)
        self.setLineWidth(0.5)
        self.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
        self.setFont("Helvetica", 8)
        self.setFillColor(GREY)
        self.drawString(2 * cm, 1.05 * cm,
                        "NPC \u2013 Unit 3  |  Vivek Borse  |  PRN 2125UCSM1082")
        self.drawRightString(A4[0] - 2 * cm, 1.05 * cm,
                             "Page %d of %d" % (self._pageNumber, total))


# ---------------------------------------------------------------- cover page
def cover(story):
    story.append(Spacer(1, 1.4 * cm))
    story.append(HRFlowable(width="100%", thickness=2.5, color=NAVY, spaceAfter=14))
    story.append(Paragraph("PRACTICAL ASSIGNMENT REPORT", st_cv_tag))
    story.append(Paragraph("NPC \u2013 UNIT 3", st_cv_small))
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("CONFIGURE A DNS SERVER AND WEB SERVER", st_cv_title))
    story.append(Paragraph("USING CISCO PACKET TRACER", st_cv_title))
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="100%", thickness=2.5, color=NAVY, spaceBefore=6))
    story.append(Spacer(1, 1.5 * cm))

    story.append(Paragraph("Submitted By", st_cv_sub))
    story.append(Spacer(1, 0.5 * cm))

    rows = [
        ("Student Name", "Vivek Borse"),
        ("PRN", "2125UCSM1082"),
        ("Department", "Cyber Security"),
        ("Semester", "3rd Semester"),
        ("Year", "Second Year"),
        ("Subject", "NPC"),
        ("College / University", "Sanjivani University, Kopargaon"),
    ]
    data = [[Paragraph(k, P("ck", fontName="Helvetica-Bold", fontSize=11,
                            textColor=NAVY)),
             Paragraph(v, P("cv", fontSize=11))] for k, v in rows]
    t = Table(data, colWidths=[6 * cm, 8.5 * cm])
    t.hAlign = "CENTER"
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), ROWBG),
        ("GRID", (0, 0), (-1, -1), 0.5, LGREY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.8 * cm))
    story.append(Paragraph(
        'GitHub Repository:&nbsp; '
        '<link href="https://github.com/vivekborse99/Unit_3_DNS_Web_Server" '
        'color="#2E5496"><u>github.com/vivekborse99/Unit_3_DNS_Web_Server</u></link>',
        P("cvrepo", alignment=TA_CENTER, fontSize=10.5, textColor=GREY, leading=15)))
    story.append(Spacer(1, 1.1 * cm))
    story.append(Paragraph(
        "A practical report submitted towards the Networking Protocols &amp; "
        "Communication (NPC) course, demonstrating the configuration and testing of "
        "DNS name resolution and HTTP web access within a local area network built in "
        "Cisco Packet Tracer.",
        P("cvnote", alignment=TA_CENTER, fontSize=10, textColor=GREY, leading=15)))
    story.append(PageBreak())


# ---------------------------------------------------------------- content
def content(story, topo_png):
    # ---- 2. AIM & OBJECTIVES ----
    story += heading("1.  Aim and Objectives")
    story.append(sub("Aim"))
    story.append(body(
        "To configure a DNS Server and a Web Server using Cisco Packet Tracer and to "
        "access a website through its domain name instead of its IP address."))
    story.append(sub("Objectives"))
    story += numbered([
        "Create a network topology using PCs, a switch, a DNS Server and a Web Server.",
        "Assign appropriate IP addresses to all devices.",
        "Configure and enable the HTTP service on the Web Server.",
        "Configure the DNS service and create an A (Address) record.",
        "Configure the PCs to use the DNS Server for name resolution.",
        "Verify connectivity between devices using ping commands.",
        "Access the hosted website using its domain name from a client PC.",
    ])
    story.append(PageBreak())

    # ---- 3. REQUIREMENTS ----
    story += heading("2.  Requirements")
    story.append(body("The following devices and software were used to carry out this "
                      "practical. The role of each component is described briefly."))
    story += bullets([
        "<b>Cisco Packet Tracer</b> &ndash; network simulation software used to design, "
        "configure and test the topology virtually.",
        "<b>PC0 and PC1 (PC-PT)</b> &ndash; client end devices that send DNS queries and "
        "request web pages from the server.",
        "<b>Cisco 2960 Switch (Switch0)</b> &ndash; a Layer-2 device that connects all "
        "end devices within the same LAN and forwards frames based on MAC addresses.",
        "<b>DNS Server (Server-PT)</b> &ndash; resolves the domain name to the Web "
        "Server's IP address by hosting the DNS A record.",
        "<b>Web Server (Server-PT)</b> &ndash; hosts the website and serves the web page "
        "to clients over the HTTP protocol.",
        "<b>Copper Straight-Through cables</b> &ndash; connect the end devices and servers "
        "to the switch (used between devices of different types).",
    ])
    story.append(PageBreak())

    # ---- 4. TOPOLOGY ----
    story += heading("3.  Network Topology")
    story.append(body(
        "The network is a single local area network (LAN) belonging to the subnet "
        "192.168.1.0/24. The DNS Server, Web Server, PC0 and PC1 are each connected to "
        "the central switch, Switch0, using Copper Straight-Through cables. Because every "
        "device is in the same subnet, communication takes place through the switch "
        "without the need for a router."))
    story.append(sub("Logical layout"))
    story.append(code_box(
        "DNS Server --+\n"
        "Web Server --+\n"
        "PC0 ---------+--- Switch0\n"
        "PC1 ---------+", escape=True))
    story.append(Spacer(1, 6))
    story.append(figure(topo_png, "Figure 3.1: Logical network topology (reference design)",
                        max_h=10.5 * cm))
    story.append(figure("screenshots/01_topology.png",
                        "Figure 3.2: Topology as implemented in Cisco Packet Tracer",
                        max_h=10 * cm))
    story.append(PageBreak())

    # ---- 5. IP ADDRESSING ----
    story += heading("4.  IP Addressing Table")
    story.append(body("Static IP addressing was used for all devices. The addressing "
                      "scheme is shown in the table below."))
    story.append(data_table(
        ["Device", "IP Address", "Subnet Mask"],
        [["DNS Server", "192.168.1.2", "255.255.255.0"],
         ["Web Server", "192.168.1.3", "255.255.255.0"],
         ["PC0", "192.168.1.10", "255.255.255.0"],
         ["PC1", "192.168.1.11", "255.255.255.0"]],
        widths=[CONTENT_W * 0.34, CONTENT_W * 0.33, CONTENT_W * 0.33]))
    story.append(Spacer(1, 10))
    story.append(info_table([
        ("DNS Server address configured on the PCs", "192.168.1.2"),
        ("Default gateway", "Not required for communication within this single subnet."),
    ]))
    story.append(PageBreak())

    # ---- 6. DNS SERVER CONFIG ----
    story += heading("5.  DNS Server Configuration")
    story += numbered([
        "Open the DNS Server.",
        "Navigate to Desktop > IP Configuration.",
        "Assign the IP address 192.168.1.2.",
        "Set the subnet mask to 255.255.255.0.",
        "Navigate to Services > DNS.",
        "Turn the DNS service ON.",
        "Create the DNS resource record shown below.",
    ])
    story.append(Spacer(1, 6))
    story.append(data_table(
        ["Name", "Type", "Address"],
        [["www.npcunit3.com", "A Record", "192.168.1.3"]],
        widths=[CONTENT_W * 0.45, CONTENT_W * 0.25, CONTENT_W * 0.30]))
    story.append(Spacer(1, 8))
    story.append(body(
        "The DNS A (Address) record maps the human-readable domain name "
        "<b>www.npcunit3.com</b> to the Web Server's IPv4 address <b>192.168.1.3</b>. "
        "When a PC requests the domain name, the DNS Server returns this address so the "
        "browser can reach the Web Server."))
    story.append(PageBreak())

    # ---- 7. WEB SERVER CONFIG ----
    story += heading("6.  Web Server Configuration")
    story += numbered([
        "Open the Web Server.",
        "Navigate to Desktop > IP Configuration.",
        "Assign the IP address 192.168.1.3.",
        "Set the subnet mask to 255.255.255.0.",
        "Navigate to Services > HTTP.",
        "Enable the HTTP service.",
        "Edit index.html to display a simple welcome page.",
    ])
    story.append(Spacer(1, 6))
    story.append(sub("index.html"))
    html = ("<html>\n"
            "<head>\n"
            "    <title>NPC Unit 3</title>\n"
            "</head>\n"
            "<body>\n"
            "    <h1>Welcome to My Web Server!</h1>\n"
            "    <p>DNS and Web Server Configuration Successful.</p>\n"
            "</body>\n"
            "</html>")
    story.append(code_box(html, escape=True))
    story.append(Spacer(1, 6))
    story.append(body(
        "The HTML page is stored on the Web Server and delivered to the client through "
        "the HTTP service whenever the website is requested."))
    story.append(PageBreak())

    # ---- 8. PC CONFIG ----
    story += heading("7.  PC Configuration")
    story.append(body("PC0 and PC1 were configured with static IP addresses through "
                      "Desktop > IP Configuration. The DNS Server field on each PC points "
                      "to the DNS Server at 192.168.1.2."))
    story.append(sub("PC0"))
    story.append(info_table([
        ("IP Address", "192.168.1.10"),
        ("Subnet Mask", "255.255.255.0"),
        ("DNS Server", "192.168.1.2"),
    ]))
    story.append(Spacer(1, 8))
    story.append(sub("PC1"))
    story.append(info_table([
        ("IP Address", "192.168.1.11"),
        ("Subnet Mask", "255.255.255.0"),
        ("DNS Server", "192.168.1.2"),
    ]))
    story.append(Spacer(1, 8))
    story.append(body("Static addressing was used throughout this practical so that the "
                      "addresses remain fixed and predictable."))
    story.append(PageBreak())

    # ---- 9. CONNECTIVITY TESTING ----
    story += heading("8.  Connectivity Testing")
    story.append(body("Connectivity was verified from PC0 using the ping command. The "
                      "following commands were executed in Desktop > Command Prompt:"))
    story.append(code_box("C:\\>ping 192.168.1.2      (DNS Server)\n"
                         "C:\\>ping 192.168.1.3      (Web Server)", escape=True))
    story.append(Spacer(1, 6))
    story.append(body(
        "<b>Observed result:</b> both ping tests returned 4 of 4 replies with 0% packet "
        "loss (time &lt; 1 ms, TTL = 128), which confirms successful IP connectivity "
        "between PC0 and both servers. The screenshot below shows the actual output."))
    story.append(figure("screenshots/02_ping_test.png",
                        "Figure 8.1: Ping test to the DNS Server (192.168.1.2) and Web "
                        "Server (192.168.1.3) from PC0", max_h=12 * cm))
    story.append(PageBreak())

    # ---- 10. WEBSITE ACCESS ----
    story += heading("9.  Website Access and Result")
    story.append(body("The website was accessed from a client PC using its domain name:"))
    story += numbered([
        "Open PC0.",
        "Navigate to Desktop > Web Browser.",
        "Enter the URL http://www.npcunit3.com",
        "Click Go.",
    ])
    story.append(Spacer(1, 4))
    story.append(body("<b>Expected / observed web page output:</b>"))
    story.append(code_box("Welcome to My Web Server!\n"
                         "DNS and Web Server Configuration Successful.", escape=True))
    story.append(Spacer(1, 6))
    story.append(figure("screenshots/03_website_browser.png",
                        "Figure 9.1: Website opened on PC0 through the domain name "
                        "http://www.npcunit3.com", max_h=8.5 * cm))
    story.append(figure("screenshots/04_full_simulation.png",
                        "Figure 9.2: Complete Packet Tracer workspace with the website "
                        "served to PC0", max_h=9 * cm))
    story.append(body(
        "Successful access to the website through the domain name demonstrates that DNS "
        "name resolution and HTTP web access are both working correctly: the domain name "
        "was resolved to 192.168.1.3 by the DNS Server, and the page was then served by "
        "the Web Server over HTTP."))
    story.append(PageBreak())

    # ---- 11. TROUBLESHOOTING ----
    story += heading("10.  Troubleshooting")
    story.append(body("Common problems that may occur during this practical and their "
                      "solutions are listed below."))
    story.append(data_table(
        ["Problem", "Solution"],
        [["Website domain does not resolve",
          "Check that the DNS service is ON and the A record for www.npcunit3.com "
          "(192.168.1.3) exists."],
         ["Website cannot be accessed",
          "Check that the HTTP service is enabled and the Web Server IP (192.168.1.3) "
          "is configured correctly."],
         ["Ping fails",
          "Verify IP addresses, subnet masks, cables and switch connections (link "
          "lights green)."],
         ["Incorrect DNS server address",
          "Configure 192.168.1.2 in the DNS Server field of each PC."],
         ["Incorrect domain name",
          "Ensure the browser URL exactly matches the DNS record (www.npcunit3.com)."]],
        widths=[CONTENT_W * 0.34, CONTENT_W * 0.66]))
    story.append(PageBreak())

    # ---- 12. CONCLUSION ----
    story += heading("11.  Conclusion")
    story.append(body(
        "In this practical, a local area network was successfully designed and configured "
        "in Cisco Packet Tracer using two PCs, a switch, a DNS Server and a Web Server, "
        "all addressed within the 192.168.1.0/24 subnet. The HTTP service was enabled on "
        "the Web Server to host a simple web page, and a DNS A record was created so that "
        "the domain name <b>www.npcunit3.com</b> maps to the Web Server's IP address "
        "<b>192.168.1.3</b>."))
    story.append(body(
        "Connectivity was verified with the ping command, and the website was accessed "
        "from PC0 through its domain name rather than its IP address. This confirms that "
        "DNS name resolution and HTTP website access function correctly within the local "
        "network, demonstrating how clients, a DNS Server and a Web Server interact in a "
        "TCP/IP network."))


# ---------------------------------------------------------------- build
def build():
    topo = os.path.join(HERE, "logical_topology.png")
    draw_logical_topology(topo)

    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="NPC Unit 3 - DNS and Web Server (Vivek Borse)",
        author="Vivek Borse",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame])])

    story = []
    cover(story)
    content(story, topo)
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Created:", OUT)


if __name__ == "__main__":
    build()
