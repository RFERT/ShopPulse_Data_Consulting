"""Build the defense slide deck (docs/slides/shoppulse_soutenance.pptx).

Usage: python docs/slides/build_deck.py
Requires python-pptx (pip install python-pptx).
"""

from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("shoppulse_soutenance.pptx")
DASHBOARD = ROOT / "dashboards" / "apercu_dashboard.png"

NAVY = RGBColor(0x0F, 0x17, 0x2A)
TEAL = RGBColor(0x14, 0xB8, 0xA6)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)
RED = RGBColor(0xE5, 0x57, 0x5A)
LIGHT = RGBColor(0xF1, 0xF5, 0xF9)
GREY = RGBColor(0x64, 0x74, 0x8B)
SOFT = RGBColor(0x94, 0xA3, 0xB8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x1E, 0x29, 0x3B)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
TOTAL = 10


def text(slide, x, y, w, h, content, size=18, bold=False, color=INK, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, font="Calibri"):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = anchor
    lines = content if isinstance(content, list) else [content]
    for i, line in enumerate(lines):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        para.alignment = align
        para.space_after = Pt(6)
        run = para.add_run()
        run.text = line
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = font
    return box


def rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=None):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
    shp.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp.adjustments[0] = 0.08
    return shp


def card(slide, x, y, w, h, title, body, accent=TEAL, body_size=15):
    rect(slide, x, y, w, h, LIGHT)
    rect(slide, x, y, 0.09, h, accent, shape=MSO_SHAPE.RECTANGLE)
    text(slide, x + 0.25, y + 0.12, w - 0.4, 0.5, title, size=19, bold=True, color=NAVY)
    text(slide, x + 0.25, y + 0.7, w - 0.4, h - 0.8, body, size=body_size)


def base(title, subtitle, notes):
    slide = prs.slides.add_slide(BLANK)
    rect(slide, 0, 0, 13.333, 1.15, NAVY, shape=MSO_SHAPE.RECTANGLE)
    rect(slide, 0, 1.15, 13.333, 0.06, TEAL, shape=MSO_SHAPE.RECTANGLE)
    text(slide, 0.6, 0.12, 12.2, 0.6, title, size=28, bold=True, color=WHITE)
    text(slide, 0.6, 0.7, 12.2, 0.4, subtitle, size=15, color=SOFT)
    slide.notes_slide.notes_text_frame.text = notes
    return slide


def footer(slide, n):
    text(slide, 0.6, 7.05, 8, 0.3, "ShopPulse · Audit Data & IA · RFERT", size=11, color=GREY)
    text(slide, 11.7, 7.05, 1.1, 0.3, f"{n}/{TOTAL}", size=11, color=GREY, align=PP_ALIGN.RIGHT)


def banner(slide, y, h, content, size=18):
    rect(slide, 0.6, y, 12.14, h, NAVY)
    text(slide, 0.9, y, 11.6, h, content, size=size, bold=True, color=WHITE,
         anchor=MSO_ANCHOR.MIDDLE)


# 1. Title -------------------------------------------------------------------
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY, shape=MSO_SHAPE.RECTANGLE)
text(s, 0.8, 1.2, 11.5, 1.3, "ShopPulse", size=66, bold=True, color=WHITE)
rect(s, 0.8, 2.55, 1.2, 0.07, TEAL, shape=MSO_SHAPE.RECTANGLE)
text(s, 0.8, 2.8, 11.5, 0.9, "De la donnée brute à la décision métier", size=32, color=TEAL)
text(s, 0.8, 3.7, 11.5, 0.6,
     "Plateforme Data & IA · dataset Olist · Mission Flash (rattrapage HETIC)",
     size=18, color=SOFT)
rect(s, 0.8, 4.9, 11.7, 1.3, INK)
text(s, 1.1, 4.9, 11.2, 1.3,
     ["98 199 commandes. 8,1 % arrivent en retard.",
      "Et un retard coûte 1,7 point de note au client (2,57 contre 4,29)."],
     size=22, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.8, 6.7, 11, 0.4, "RFERT · github.com/RFERT/ShopPulse_Data_Consulting", size=14,
     color=SOFT)
s.notes_slide.notes_text_frame.text = (
    "Accroche (15 s) : partir du chiffre choc, puis annoncer le plan en une phrase."
)

# 2. Problem -----------------------------------------------------------------
s = base("Le problème et la valeur apportée", "Trois irritants, trois leviers",
         "Section 1 du script (1 min). Insister sur le lien retard -> note.")
card(s, 0.6, 1.7, 4.0, 3.4, "Direction",
     ["Irritant : pas de vue unique sur l'activité.",
      "Levier : dashboard de 5 KPI, alimenté par une base consolidée."], accent=TEAL)
card(s, 4.67, 1.7, 4.0, 3.4, "Marketing",
     ["Irritant : clients jamais segmentés, peu de réachat.",
      "Levier : segmentation RFM, 3 personas, 3 campagnes chiffrées."], accent=AMBER)
card(s, 8.74, 1.7, 4.0, 3.4, "Logistique & SAV",
     ["Irritant : retards et avis négatifs subis.",
      "Levier : prédiction du retard et analyse de sentiment, exposées en API."], accent=RED)
banner(s, 5.5, 1.2,
       ["Test de Mann-Whitney : note 2,57 (retard) contre 4,29 (à l'heure), p ≈ 0.",
        "Le retard est le premier levier de satisfaction."])
footer(s, 2)

# 3. Architecture ------------------------------------------------------------
s = base("Architecture cible", "Du fichier source à la décision, entièrement conteneurisé",
         "Section 2 (1 min 30). Suivre le flux de gauche à droite, puis citer Docker et la CI.")
cols = [
    ("Sources", ["Olist", "9 fichiers CSV"], GREY),
    ("ETL · Airflow", ["Extract", "Contrôles qualité", "Nettoyage tracé",
                       "Chargement idempotent"], TEAL),
    ("Stockage", ["PostgreSQL", "9 tables, clés, index"], NAVY),
    ("Analyse & ML", ["EDA + statistiques", "RFM + clustering", "Modèle retard",
                      "Modèle sentiment"], AMBER),
    ("Restitution", ["API FastAPI", "Dashboard Streamlit"], RED),
]
col_w, gap, x0, y0 = 2.2, 0.285, 0.6, 1.6
for i, (name, items, colr) in enumerate(cols):
    x = x0 + i * (col_w + gap)
    rect(s, x, y0, col_w, 0.6, colr)
    text(s, x, y0, col_w, 0.6, name, size=16, bold=True, color=WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    for j, item in enumerate(items):
        yy = y0 + 0.8 + j * 0.72
        rect(s, x, yy, col_w, 0.6, LIGHT, line=colr)
        text(s, x, yy, col_w, 0.6, item, size=13, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    if i < len(cols) - 1:
        arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + col_w + 0.02),
                                   Inches(y0 + 0.12), Inches(gap - 0.04), Inches(0.36))
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = GREY
        arrow.line.fill.background()
rect(s, 0.6, 5.4, 12.14, 0.6, NAVY)
text(s, 0.6, 5.4, 12.14, 0.6, "Utilisateurs : Direction · Marketing · Logistique · Service client",
     size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.6, 6.2, 12.14, 0.6, LIGHT, line=TEAL)
text(s, 0.6, 6.2, 12.14, 0.6,
     "Industrialisation : Docker / docker-compose · GitHub Actions (ruff, pytest, build)",
     size=15, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
footer(s, 3)

# 4. Tech choices ------------------------------------------------------------
s = base("Arbitrages techniques", "Coût · délai · adéquation · pérennité",
         "Section 2. Deux arbitrages détaillés, le troisième en une phrase.")
rows = [
    ("Besoin", "Choix retenu", "Alternative écartée", "Pourquoi"),
    ("Orchestration ETL", "Airflow", "Prefect",
     "Standard industriel, UI de supervision, compétence transférable"),
    ("Restitution", "Streamlit", "Metabase",
     "100 % Python, 5 KPI sur mesure, une seule stack à maintenir"),
    ("Avis en portugais", "Entraînement direct", "Traduction",
     "Pas de coût ni de perte d'information, pipeline simple"),
    ("API", "FastAPI", "Flask", "Validation Pydantic et OpenAPI natives"),
]
table = s.shapes.add_table(len(rows), 4, Inches(0.6), Inches(1.7), Inches(12.14),
                           Inches(3.9)).table
for c, w in enumerate([2.6, 2.6, 2.6, 4.34]):
    table.columns[c].width = Inches(w)
for r, row in enumerate(rows):
    for c, val in enumerate(row):
        cell = table.cell(r, c)
        cell.text = val
        run = cell.text_frame.paragraphs[0].runs[0]
        run.font.size = Pt(16)
        run.font.bold = r == 0 or c == 1
        run.font.color.rgb = WHITE if r == 0 else INK
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if r == 0 else (LIGHT if r % 2 else WHITE)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
text(s, 0.6, 5.9, 12.14, 0.9,
     "Le pipeline reste découplé d'Airflow (exécutable en CLI) : réversibilité préservée.",
     size=17, bold=True, color=NAVY)
footer(s, 4)

# 5. Data & quality ----------------------------------------------------------
s = base("Les données : pipeline et qualité", "Rejouable, traçable, idempotent",
         "Section 3 (1 min 30). Montrer le rapport avant/après si le temps le permet.")
for i, step in enumerate(["Extract", "Contrôles qualité", "Nettoyage tracé",
                          "Chargement idempotent"]):
    shp = s.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(0.6 + i * 3.08), Inches(1.6),
                             Inches(3.0), Inches(0.9))
    shp.fill.solid()
    shp.fill.fore_color.rgb = TEAL if i % 2 == 0 else NAVY
    shp.line.fill.background()
    shp.text_frame.text = step
    run = shp.text_frame.paragraphs[0].runs[0]
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = WHITE
for i, (big, label, colr) in enumerate([
    ("9", "tables reliées par clés étrangères", TEAL),
    ("≈ 1,55 M", "lignes chargées dans PostgreSQL", AMBER),
    ("0", "ligne supprimée au nettoyage", RED),
]):
    x = 0.6 + i * 4.1
    rect(s, x, 2.85, 3.95, 1.7, LIGHT)
    text(s, x, 2.9, 3.95, 0.9, big, size=44, bold=True, color=colr, align=PP_ALIGN.CENTER)
    text(s, x, 3.8, 3.95, 0.7, label, size=15, align=PP_ALIGN.CENTER)
text(s, 0.6, 4.9, 12.14, 1.9, [
    "• Rapport de qualité avant / après généré automatiquement (lignes, nulls, doublons).",
    "• Règles de nettoyage tracées : ex. 13 catégories produit inconnues mises à NULL.",
    "• 261 831 doublons de géolocalisation repérés et documentés.",
    "• Rejouer le pipeline produit exactement le même état.",
], size=17)
footer(s, 5)

# 6. Dashboard ---------------------------------------------------------------
s = base("Réponse métier n°1 : le tableau de bord Direction", "5 KPI, une seule page",
         "Section 4. Ouvrir le dashboard en direct si possible (localhost:8501).")
s.shapes.add_picture(str(DASHBOARD), Inches(0.5), Inches(1.5), width=Inches(7.9))
kpis = [("R$ 13,49 M", "Chiffre d'affaires"), ("98 199", "Commandes"),
        ("R$ 137,42", "Panier moyen"), ("4,09 / 5", "Note moyenne"),
        ("8,1 %", "Taux de retard")]
for i, (val, lab) in enumerate(kpis):
    y = 1.6 + i * 1.04
    rect(s, 9.0, y, 3.75, 0.92, LIGHT)
    rect(s, 9.0, y, 0.09, 0.92, [TEAL, AMBER, TEAL, AMBER, RED][i], shape=MSO_SHAPE.RECTANGLE)
    text(s, 9.25, y + 0.02, 3.4, 0.5, val, size=22, bold=True, color=NAVY)
    text(s, 9.25, y + 0.52, 3.4, 0.35, lab, size=13, color=GREY)
text(s, 0.6, 6.3, 8.1, 0.6,
     "São Paulo concentre l'essentiel des commandes ; un retard de 8,1 % pèse sur la note.",
     size=14, color=GREY)
footer(s, 6)

# 7. Segmentation ------------------------------------------------------------
s = base("Réponse métier n°2 : segmentation RFM et recommandations",
         "Clustering sur Récence, Fréquence, Montant · ~95 000 clients",
         "Section 4. Une phrase par persona, puis le total.")
personas = [
    ("Victor · 35 %", "Nouvel acheteur à fort potentiel",
     ["~33 200 clients, panier R$ 251, un seul achat.",
      "Relance cross-sell J+30 (5 % de réachat)."], "~R$ 417 000", TEAL),
    ("Lucia · 29 %", "Cliente dormante",
     ["~27 500 clients, dernier achat il y a ~476 jours.",
      "Win-back à -15 % (3 % de réactivation)."], "~R$ 90 000", AMBER),
    ("Marco · 3 %", "Fidèle premium",
     ["~2 900 clients, 2,1 commandes, R$ 260.",
      "Programme VIP (+0,3 commande par an)."], "~R$ 226 000", RED),
]
for i, (name, role, body, gain, colr) in enumerate(personas):
    x = 0.6 + i * 4.095
    rect(s, x, 1.7, 3.95, 3.7, LIGHT)
    rect(s, x, 1.7, 3.95, 0.09, colr, shape=MSO_SHAPE.RECTANGLE)
    text(s, x + 0.2, 1.9, 3.6, 0.5, name, size=22, bold=True, color=NAVY)
    text(s, x + 0.2, 2.4, 3.6, 0.4, role, size=15, color=GREY)
    text(s, x + 0.2, 2.9, 3.6, 1.6, body, size=14)
    text(s, x + 0.2, 4.6, 3.6, 0.7, gain, size=28, bold=True, color=colr)
banner(s, 5.7, 1.1,
       "≈ R$ 733 000 de CA incrémental estimé (hypothèses prudentes, voir docs/marketing.md)",
       size=20)
footer(s, 7)

# 8. Models ------------------------------------------------------------------
s = base("Les modèles : performances, limites et biais",
         "Validation croisée 5 plis, comparaison à une baseline",
         "Section 5 (2 min). Humilité : le TF-IDF bat le réseau de neurones.")


def bar_chart(slide, x, y, w, h, title, cats, values, colors):
    data = CategoryChartData()
    data.categories = cats
    data.add_series(title, values)
    chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y),
                                   Inches(w), Inches(h), data).chart
    chart.has_legend = False
    chart.has_title = True
    chart.chart_title.text_frame.text = title
    title_run = chart.chart_title.text_frame.paragraphs[0].runs[0]
    title_run.font.size = Pt(15)
    title_run.font.bold = True
    chart.value_axis.maximum_scale = 1.0
    chart.value_axis.minimum_scale = 0
    chart.value_axis.has_major_gridlines = False
    chart.value_axis.tick_labels.font.size = Pt(11)
    chart.category_axis.tick_labels.font.size = Pt(12)
    plot = chart.plots[0]
    plot.gap_width = 70
    plot.has_data_labels = True
    plot.data_labels.number_format = "0.00"
    plot.data_labels.number_format_is_linked = False
    plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    plot.data_labels.font.size = Pt(13)
    plot.data_labels.font.bold = True
    for idx, colr in enumerate(colors):
        point = plot.series[0].points[idx]
        point.format.fill.solid()
        point.format.fill.fore_color.rgb = colr


bar_chart(s, 0.5, 1.45, 4.3, 3.8, "Retard · ROC-AUC", ["Baseline", "Rég. log.", "Random Forest"],
          [0.50, 0.69, 0.72], [GREY, AMBER, TEAL])
bar_chart(s, 4.85, 1.45, 3.6, 3.8, "Sentiment · F1", ["TF-IDF", "PyTorch"], [0.91, 0.90],
          [TEAL, AMBER])
card(s, 8.65, 1.6, 4.1, 3.65, "Limites et biais", [
    "• Rappel faible à 0,5 : l'API expose la probabilité, seuil métier 0,30.",
    "• Audit d'équité par région : écart de rappel 0,86 (élevé à Rio, bas dans le RS).",
    "• Corrections prévues : seuils par région, calibration.",
], accent=RED, body_size=14)
banner(s, 5.5, 1.3, [
    "Le retard reste difficile à prédire : le modèle sert à prioriser, pas à décider seul.",
    "Le deep learning est battu par une régression logistique : la baseline reste le juge de paix.",
], size=16)
footer(s, 8)

# 9. API demo ----------------------------------------------------------------
s = base("Démonstration : l'API conteneurisée", "En direct : docker compose up, puis deux appels",
         "Section 6 (1 min). Passer en direct sur le terminal et sur localhost:8000/docs.")
rect(s, 0.6, 1.7, 7.4, 4.9, RGBColor(0x0B, 0x12, 0x20))
code = [
    "$ docker compose -f infra/docker-compose.yml up -d",
    "",
    "$ curl -X POST localhost:8000/predict/sentiment \\",
    "    -d '{\"texte\": \"Produto ótimo, chegou rápido!\"}'",
    "{\"sentiment\":\"positif\",\"probabilite_positif\":0.97}",
    "",
    "$ curl -X POST localhost:8000/predict/retard \\",
    "    -d '{... commande SP -> RJ ...}'",
    "{\"probabilite_retard\":0.73,",
    " \"risque_eleve\":true,\"seuil\":0.3}",
]
text(s, 0.85, 1.85, 7.0, 4.6, code, size=14, color=RGBColor(0x86, 0xEF, 0xAC),
     font="Consolas")
card(s, 8.3, 1.7, 4.45, 2.3, "Pourquoi une API ?", [
    "Un endpoint par modèle, entrées validées (Pydantic), documentation OpenAPI sur /docs.",
], accent=TEAL)
card(s, 8.3, 4.3, 4.45, 2.3, "Prêt à tourner", [
    "Image Docker unique, configuration par variables d'environnement, ports modifiables.",
], accent=AMBER)
footer(s, 9)

# 10. Wrap-up ----------------------------------------------------------------
s = base("Bilan : écarts, bonus et suite", "Ce qui est livré, et ce que je referais",
         "Section 7 (30 s). Conclure sur la transparence IA et la punchline.")
card(s, 0.6, 1.7, 6.0, 2.55, "Bonus réalisés", [
    "• MLflow : suivi des expériences",
    "• ELK : logs JSON et supervision",
    "• Spark : analyse du clickstream REES46",
    "• AWS : plan ECS Fargate + RDS, ~50 USD/mois (non déployé)",
], accent=TEAL)
card(s, 6.75, 1.7, 6.0, 2.55, "Qualité", [
    "• 34 tests, couverture 76,8 %",
    "• ruff + GitHub Actions : intégration continue verte",
    "• Un tiers clone et lance en moins de 30 minutes",
], accent=AMBER)
card(s, 0.6, 4.45, 6.0, 2.2, "Ce que je referais", [
    "• Meilleur rappel sur le retard, seuils par région",
    "• Contrôles de données (Great Expectations), suivi de dérive",
], accent=RED)
card(s, 6.75, 4.45, 6.0, 2.2, "Transparence", [
    "• L'IA a été utilisée comme assistant de développement.",
    "• Usage détaillé dans le README (section « Usage de l'IA »).",
], accent=GREY)
footer(s, 10)

prs.save(OUT)
print(f"saved {OUT} ({len(prs.slides)} slides)")
