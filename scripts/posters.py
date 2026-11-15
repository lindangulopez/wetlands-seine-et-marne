"""Four Art Nouveau seasonal posters (after the composition of Mucha's The Seasons, 1896),
each with a Black woman and the species of the matching wetland story. Writes SVG files.
Usage: python posters.py OUT_DIR
"""
import math, sys, os
OUT = sys.argv[1]
W, H = 800, 1600

def P(d, fill="none", stroke="none", sw=0, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def circle(cx, cy, r, fill, stroke="none", sw=0, extra=""):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def ellipse(cx, cy, rx, ry, fill, rot=0, stroke="none", sw=0):
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})"/>'

def leaf(x, y, L, ang, fill, vein):
    # pointed leaf from base (x,y), length L, angle in degrees
    a = math.radians(ang); dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx; w = L * 0.28
    tip = (x + dx * L, y + dy * L); c1 = (x + dx * L * .45 + nx * w, y + dy * L * .45 + ny * w); c2 = (x + dx * L * .45 - nx * w, y + dy * L * .45 - ny * w)
    d = f"M{x:.1f},{y:.1f} Q{c1[0]:.1f},{c1[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} Q{c2[0]:.1f},{c2[1]:.1f} {x:.1f},{y:.1f}Z"
    return P(d, fill, "#2B1A10", 1.6) + P(f"M{x:.1f},{y:.1f} L{tip[0]:.1f},{tip[1]:.1f}", "none", vein, 1.2)

def whiplash(x0, y0, x1, y1, bend, color, sw):
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2
    return P(f"M{x0},{y0} C{x0 + bend * 0.2},{my} {mx},{y1 + 60} {x1},{y1}", "none", color, sw)

# ---------- motifs ----------
def marigold(cx, cy, r):
    s = ""
    for k in range(5):
        a = math.radians(k * 72 - 90)
        s += ellipse(cx + math.cos(a) * r * .55, cy + math.sin(a) * r * .55, r * .5, r * .34, "#F4C430", math.degrees(a), "#7A4A00", 1.4)
    return s + circle(cx, cy, r * .28, "#E08E0B", "#7A4A00", 1.2)

def loosestrife(x, y, h):
    s = P(f"M{x},{y} L{x},{y - h}", "none", "#4E6B2F", 3)
    for i in range(int(h / 12)):
        yy = y - h + i * 12; ww = 9 * (1 - i / (h / 12)) + 4
        s += ellipse(x - ww * .6, yy, ww * .55, 5, "#9B3FA0", -20, "#4A1F4F", .8) + ellipse(x + ww * .6, yy + 4, ww * .55, 5, "#B65DB8", 20, "#4A1F4F", .8)
    return s

def reed(x, y, h, lean=0.0, plume="#C9B79C"):
    tx = x + lean * h; ty = y - h
    s = P(f"M{x},{y} Q{x + lean * h * .3},{y - h * .6} {tx},{ty}", "none", "#8C7A55", 3)
    pts = " ".join(f"{tx + math.sin(i) * 8:.1f},{ty - i * 6:.1f}" for i in range(8))
    s += ellipse(tx + 6, ty - 26, 12, 34, plume, 15 + lean * 30, "#7A6A4A", 1)
    return s

def alder_cone(cx, cy, r=10):
    s = ellipse(cx, cy, r * .7, r, "#5A3A22", 0, "#2B1A10", 1.2)
    for k in range(3):
        s += P(f"M{cx - r * .6},{cy - r * .5 + k * r * .5} Q{cx},{cy - r * .3 + k * r * .5} {cx + r * .6},{cy - r * .5 + k * r * .5}", "none", "#8B5E3C", 1)
    return s

def mushroom(cx, cy, r, cap, stem="#EFE3C8", gills=True):
    s = P(f"M{cx - r * .18},{cy} L{cx - r * .14},{cy - r * .9} L{cx + r * .14},{cy - r * .9} L{cx + r * .18},{cy}Z", stem, "#2B1A10", 1.2)
    s += P(f"M{cx - r},{cy - r * .85} Q{cx},{cy - r * 1.9} {cx + r},{cy - r * .85} Q{cx},{cy - r * .6} {cx - r},{cy - r * .85}Z", cap, "#2B1A10", 1.4)
    return s

def cup_fungus(cx, cy, r):
    return P(f"M{cx - r},{cy - r * .6} Q{cx},{cy + r * .9} {cx + r},{cy - r * .6} Q{cx},{cy - r * .1} {cx - r},{cy - r * .6}Z", "#D7263D", "#5B0A14", 1.4) + ellipse(cx, cy - r * .55, r * .95, r * .22, "#9E0F22")

def bracket(cx, cy, r, col="#B07A4A"):
    s = ""
    for k in range(3):
        s += P(f"M{cx - r + k * 4},{cy + k * r * .45} Q{cx},{cy - r * .5 + k * r * .45} {cx + r - k * 4},{cy + k * r * .45} Q{cx},{cy + r * .25 + k * r * .45} {cx - r + k * 4},{cy + k * r * .45}Z", col, "#2B1A10", 1.2)
    return s

def dragonfly(cx, cy, s=1.0, body="#3C7DC4", rot=0):
    g = f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s})">'
    for dx, dy, a in [(-4, -6, -25), (4, -6, 25), (-4, 4, -10), (4, 4, 10)]:
        g += ellipse(dx * 6, dy, 26, 7, "#E8F1F8AA", a + (180 if dx < 0 else 0), "#5A6B7A", .8)
    g += P("M0,-14 L0,48", "none", body, 5) + circle(0, -16, 5, body)
    return g + "</g>"

def bird(cx, cy, s, col, rot=0, kind="small"):
    g = f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s})">'
    if kind == "heron":
        g += P("M0,0 Q-6,-40 4,-70 Q10,-90 30,-96 L44,-100 L30,-90 Q20,-80 18,-60 Q30,-30 20,0 Q10,30 -10,40 L-30,90 M-8,40 L-10,92 M-30,90 L-38,92", col, "#2B1A10", 1.6)
    else:
        g += P("M-30,0 Q-10,-24 18,-14 L34,-18 L24,-8 Q22,12 -4,14 Q-20,14 -30,0Z M-30,0 L-46,8 L-40,-4Z", col, "#2B1A10", 1.4) + circle(16, -12, 2.2, "#111")
    return g + "</g>"

def snowflake(cx, cy, r):
    s = ""
    for k in range(6):
        a = math.radians(k * 60)
        s += P(f"M{cx},{cy} L{cx + math.cos(a) * r:.1f},{cy + math.sin(a) * r:.1f}", "none", "#FFFFFF", 1.6)
    return s

def toad(cx, cy, s=1):
    return f'<g transform="translate({cx},{cy}) scale({s})">' + ellipse(0, 0, 26, 16, "#8A6A3A", 0, "#2B1A10", 1.4) + circle(-14, -12, 6, "#8A6A3A", "#2B1A10", 1.2) + circle(14, -12, 6, "#8A6A3A", "#2B1A10", 1.2) + circle(-14, -13, 2.5, "#C98A1B") + circle(14, -13, 2.5, "#C98A1B") + "</g>"

def snake(x, y, col="#5C6B3C"):
    return P(f"M{x},{y} C{x + 40},{y - 40} {x - 40},{y - 70} {x},{y - 110} S{x + 50},{y - 170} {x + 10},{y - 210}", "none", "#2B1A10", 15) + P(f"M{x},{y} C{x + 40},{y - 40} {x - 40},{y - 70} {x},{y - 110} S{x + 50},{y - 170} {x + 10},{y - 210}", "none", col, 11) + circle(x + 10, y - 212, 8, col, "#2B1A10", 1.4)

def bat(cx, cy, s=1):
    return f'<g transform="translate({cx},{cy}) scale({s})">' + P("M0,0 Q-12,-10 -24,-4 Q-34,-14 -48,-6 Q-40,2 -44,12 Q-30,6 -18,12 Q-8,4 0,8 Q8,4 18,12 Q30,6 44,12 Q40,2 48,-6 Q34,-14 24,-4 Q12,-10 0,0Z", "#3B2A2A", "#111", 1) + "</g>"

def mouse(cx, cy, s=1):
    return f'<g transform="translate({cx},{cy}) scale({s})">' + ellipse(0, 0, 18, 11, "#C07A3E", 0, "#2B1A10", 1.2) + circle(14, -6, 8, "#C07A3E", "#2B1A10", 1.2) + circle(12, -14, 4, "#D99A6A", "#2B1A10", 1) + circle(19, -6, 1.6, "#111") + P("M-18,2 Q-34,10 -30,26 Q-28,34 -20,30", "none", "#8A5A2E", 2) + "</g>"

# ---------- figure ----------
SKIN = {"spring": ("#5C3A24", "#7A4E33", "#3E2617"), "summer": ("#4A2C1C", "#6B412B", "#2E1A10"),
        "autumn": ("#6B4329", "#8A5A3B", "#432816"), "winter": ("#3F2618", "#5E3B27", "#24150C")}

def face(cx, cy, sk):
    base, hi, dark = sk
    s = P(f"M{cx - 58},{cy - 10} Q{cx - 60},{cy + 60} {cx},{cy + 88} Q{cx + 60},{cy + 60} {cx + 58},{cy - 10} Q{cx + 54},{cy - 82} {cx},{cy - 84} Q{cx - 54},{cy - 82} {cx - 58},{cy - 10}Z", base, dark, 2)
    s += ellipse(cx - 30, cy + 30, 16, 10, hi + "66") + ellipse(cx + 30, cy + 30, 16, 10, hi + "66")
    # closed eyes, brows
    for sx in (-1, 1):
        ex = cx + sx * 24
        s += P(f"M{ex - 14},{cy} Q{ex},{cy + 9} {ex + 14},{cy}", "none", "#1A0E08", 2.6)
        s += P(f"M{ex - 13},{cy + 2} l-3,4 M{ex - 5},{cy + 6} l-1,5 M{ex + 5},{cy + 6} l1,5", "none", "#1A0E08", 1.4)
        s += P(f"M{ex - 17},{cy - 18} Q{ex},{cy - 27} {ex + 17},{cy - 17}", "none", "#1A0E08", 3)
    # nose
    s += P(f"M{cx - 3},{cy + 8} Q{cx - 6},{cy + 30} {cx - 14},{cy + 38} Q{cx},{cy + 46} {cx + 14},{cy + 38} Q{cx + 6},{cy + 30} {cx + 3},{cy + 8}", "none", dark, 2)
    # lips
    s += P(f"M{cx - 20},{cy + 58} Q{cx - 9},{cy + 49} {cx},{cy + 54} Q{cx + 9},{cy + 49} {cx + 20},{cy + 58} Q{cx},{cy + 64} {cx - 20},{cy + 58}Z", "#7E3A34", "#3A1410", 1.4)
    s += P(f"M{cx - 20},{cy + 58} Q{cx},{cy + 76} {cx + 20},{cy + 58} Q{cx},{cy + 64} {cx - 20},{cy + 58}Z", "#93463E", "#3A1410", 1.4)
    # earrings
    s += circle(cx - 60, cy + 30, 7, "none", "#D4A84B", 3) + circle(cx + 60, cy + 30, 7, "none", "#D4A84B", 3)
    return s

def body(cx, top, sk, dress, dress2, trim):
    base, hi, dark = sk
    s = P(f"M{cx - 26},{top - 10} L{cx - 30},{top + 60} L{cx + 30},{top + 60} L{cx + 26},{top - 10}Z", base, dark, 2)  # neck
    s += P(f"M{cx - 30},{top + 50} Q{cx - 110},{top + 70} {cx - 160},{top + 120} L{cx + 160},{top + 120} Q{cx + 110},{top + 70} {cx + 30},{top + 50}Z", base, dark, 2)  # shoulders
    # dress, flowing
    s += P(f"M{cx - 150},{top + 112} Q{cx - 120},{top + 330} {cx - 120},{top + 420} Q{cx - 150},{top + 640} {cx - 190},{top + 860} Q{cx - 100},{top + 895} {cx},{top + 878} Q{cx + 100},{top + 900} {cx + 195},{top + 860} Q{cx + 150},{top + 640} {cx + 120},{top + 420} Q{cx + 120},{top + 330} {cx + 150},{top + 112} Q{cx},{top + 160} {cx - 150},{top + 112}Z", dress, "#2B1A10", 2.4)
    for k in range(-3, 4):
        x0 = cx + k * 28
        s += P(f"M{x0},{top + 430} Q{x0 + k * 10},{top + 650} {x0 + k * 24},{top + 872}", "none", dress2, 3)
    s += P(f"M{cx - 122},{top + 400} Q{cx},{top + 440} {cx + 122},{top + 400} L{cx + 124},{top + 432} Q{cx},{top + 470} {cx - 124},{top + 432}Z", trim, "#2B1A10", 1.8)
    s += P(f"M{cx + 40},{top + 446} Q{cx + 70},{top + 560} {cx + 30},{top + 660} M{cx + 56},{top + 444} Q{cx + 96},{top + 540} {cx + 70},{top + 640}", "none", trim, 7)
    s += P(f"M{cx - 182},{top + 830} Q{cx - 100},{top + 862} {cx},{top + 846} Q{cx + 100},{top + 866} {cx + 188},{top + 830}", "none", trim, 10)
    for k in range(-8, 9):
        s += circle(cx + k * 21, top + 846 + abs(k) * 0.4 - 18, 4, trim, "#2B1A10", 1)
    s += P(f"M{cx - 150},{top + 116} Q{cx},{top + 166} {cx + 150},{top + 116}", "none", trim, 10)
    # necklace
    s += P(f"M{cx - 44},{top + 66} Q{cx},{top + 110} {cx + 44},{top + 66}", "none", "#D4A84B", 4)
    for k in range(-3, 4):
        s += circle(cx + k * 11, top + 92 - abs(k) * 4, 4, "#D4A84B")
    return s

def arms(cx, top, sk, hold_y):
    base, hi, dark = sk
    s = ""
    for sx in (-1, 1):
        d = f"M{cx + sx * 150},{top + 130} Q{cx + sx * 175},{top + 300} {cx + sx * 70},{hold_y}"
        s += P(d, "none", dark, 40) + P(d, "none", base, 34)
        s += ellipse(cx + sx * 52, hold_y - 4, 24, 16, base, sx * 20, dark, 2)
    return s

# ---------- hair ----------
def hair_spring(cx, cy):
    s = ""
    for k in range(26):
        a = math.radians(-200 + k * 9.2)
        s += circle(cx + math.cos(a) * 105, cy - 30 + math.sin(a) * 105, 46, "#1B1110")
    s += circle(cx, cy - 40, 100, "#1B1110")
    for k, a in enumerate(range(-160, -10, 30)):
        r = math.radians(a)
        s += marigold(cx + math.cos(r) * 128, cy - 30 + math.sin(r) * 128, 22)
    return s

def hair_summer(cx, cy):
    s = P(f"M{cx - 66},{cy - 20} Q{cx - 70},{cy - 110} {cx},{cy - 116} Q{cx + 70},{cy - 110} {cx + 66},{cy - 20} Q{cx + 40},{cy - 80} {cx},{cy - 82} Q{cx - 40},{cy - 80} {cx - 66},{cy - 20}Z", "#1B1110")
    for sx in (-1, 1):
        for k in range(4):
            x0 = cx + sx * (52 + k * 13)
            d = f"M{x0},{cy - 30} C{x0 + sx * 40},{cy + 120} {x0 - sx * 30},{cy + 260} {x0 + sx * 20},{cy + 420}"
            s += P(d, "none", "#1B1110", 13) + P(d, "none", "#3A2620", 3, 'stroke-dasharray="6 7"')
        s += circle(cx + sx * 70, cy + 420, 7, "#D4A84B")
    for k in range(5):
        s += loosestrife(cx - 95 + k * 10, cy - 70 - k * 4, 60) if k < 2 else ""
    s += loosestrife(cx + 92, cy - 64, 64) + loosestrife(cx + 104, cy - 50, 50)
    return s

def hair_autumn(cx, cy):
    s = P(f"M{cx - 70},{cy - 10} Q{cx - 110},{cy - 150} {cx},{cy - 190} Q{cx + 130},{cy - 170} {cx + 80},{cy - 20} Q{cx + 40},{cy - 90} {cx},{cy - 92} Q{cx - 40},{cy - 90} {cx - 70},{cy - 10}Z", "#A3471E", "#2B1A10", 2.4)
    s += P(f"M{cx - 80},{cy - 70} Q{cx},{cy - 120} {cx + 90},{cy - 80}", "none", "#D9822B", 9)
    s += P(f"M{cx - 60},{cy - 130} Q{cx + 10},{cy - 170} {cx + 70},{cy - 140}", "none", "#D9822B", 7)
    s += P(f"M{cx + 60},{cy - 180} Q{cx + 120},{cy - 220} {cx + 90},{cy - 150} Q{cx + 140},{cy - 190} {cx + 110},{cy - 130}", "#C2601F", "#2B1A10", 2)
    for k in range(5):
        s += alder_cone(cx - 70 + k * 30, cy - 172 + abs(k - 2) * 8, 9)
    return s

def hair_winter(cx, cy):
    s = P(f"M{cx - 120},{cy + 140} Q{cx - 140},{cy - 140} {cx},{cy - 160} Q{cx + 140},{cy - 140} {cx + 120},{cy + 140} Q{cx + 80},{cy - 30} {cx},{cy - 108} Q{cx - 80},{cy - 30} {cx - 120},{cy + 140}Z", "#2F4A6B", "#14243A", 2.4)
    s += P(f"M{cx - 62},{cy - 30} Q{cx - 60},{cy - 100} {cx},{cy - 104} Q{cx + 60},{cy - 100} {cx + 62},{cy - 30} Q{cx + 30},{cy - 70} {cx},{cy - 72} Q{cx - 30},{cy - 70} {cx - 62},{cy - 30}Z", "#1B1110")
    s += P(f"M{cx - 120},{cy + 140} Q{cx - 140},{cy - 140} {cx},{cy - 160} Q{cx + 140},{cy - 140} {cx + 120},{cy + 140}", "none", "#E9EEF3", 8)
    for k in range(-2, 3):
        s += reed(cx + k * 28, cy - 150, 60, k * .12, "#E3D9C6")
    return s

HAIR = {"spring": hair_spring, "summer": hair_summer, "autumn": hair_autumn, "winter": hair_winter}

# ---------- seasons ----------
S = {
 "spring": dict(fr="PRINTEMPS", en="SPRING", bg=("#F4EFC9", "#CFE3B4"), halo="#E9D88A", halo2="#B9C97A", dress="#7FA35A", dress2="#5E7F3E", trim="#F4C430", frame="#5E7F3E", ink="#2F3A1E",
             species="Populage des marais · Rousserolle effarvatte · Agrion jouvencelle · Crapaud commun · Polypore écailleux · Brochet"),
 "summer": dict(fr="ÉTÉ", en="SUMMER", bg=("#FBE6C4", "#E9B98A"), halo="#F2C46B", halo2="#D9874A", dress="#7A3F8F", dress2="#5A2A6B", trim="#E08E0B", frame="#7A3F8F", ink="#3B1E3F",
             species="Salicaire · Martin-pêcheur · Caloptéryx éclatant · Couleuvre helvétique · Lactaire des flaques · Étiage d'août"),
 "autumn": dict(fr="AUTOMNE", en="AUTUMN", bg=("#F2DDB8", "#D8A46A"), halo="#E3A04B", halo2="#B8652A", dress="#8B4A23", dress2="#6A3418", trim="#D9822B", frame="#7A3A18", ink="#3A1E0E",
             species="Aulne glutineux · Bécassine des marais · Sympétrum sanguin · Rat des moissons · Pholiote changeante · Chute des feuilles"),
 "winter": dict(fr="HIVER", en="WINTER", bg=("#E6EDF2", "#B8CAD8"), halo="#D6E2EC", halo2="#8FA9C0", dress="#3E5C7E", dress2="#2C4561", trim="#E9EEF3", frame="#2C4561", ink="#16263A",
             species="Roseau commun · Butor étoilé · Dytique bordé · Murin de Daubenton · Pézize écarlate · Crues d'hiver"),
}

def border_plants(season):
    s = ""
    if season == "spring":
        for x in (95, 705):
            sx = 1 if x < 400 else -1
            s += whiplash(x, 1270, x + sx * 30, 640, sx * 60, "#4E6B2F", 5)
            for k in range(6):
                y = 1220 - k * 100; s += leaf(x + sx * 10, y, 60, -90 + sx * 50, "#7FA35A", "#4E6B2F")
                if k % 2 == 0: s += marigold(x + sx * 40, y - 30, 20)
        s += bird(140, 760, 1.1, "#A88B5C") + dragonfly(650, 820, 1.2, "#3C7DC4", 20) + toad(170, 1230, 1.3)
        s += mushroom(640, 1240, 26, "#A0703A") + bracket(660, 1180, 26)
        s += P("M120,1290 Q200,1260 260,1290 Q320,1320 380,1290", "none", "#5B8DB8", 4) + f'<path d="M240,1280 q30,-14 60,0 q-30,10 -60,0z M300,1280 l14,-8 l0,16z" fill="#6B7A5A" stroke="#2B1A10" stroke-width="1.2"/>'
    if season == "summer":
        for k in range(6):
            s += loosestrife(90 + k * 18, 1280 - (k % 2) * 30, 200 + (k % 3) * 40) + loosestrife(710 - k * 18, 1280 - (k % 2) * 30, 190 + (k % 3) * 40)
        s += bird(660, 760, 1.2, "#2E86C1") + f'<g transform="translate(660,760)">{ellipse(6,0,10,8,"#E07B39")}</g>' + dragonfly(150, 800, 1.2, "#1F4E9C", -20)
        s += snake(150, 1240) + mushroom(620, 1250, 24, "#E08E3A") + mushroom(660, 1260, 16, "#E8A04A")
    if season == "autumn":
        for x in (95, 705):
            sx = 1 if x < 400 else -1
            s += whiplash(x, 1270, x + sx * 20, 620, sx * 70, "#5A3A22", 7)
            for k in range(6):
                y = 1220 - k * 105; s += leaf(x + sx * 12, y, 56, -90 + sx * 55, ["#C2601F", "#D9822B", "#A3471E"][k % 3], "#5A3A22")
                s += alder_cone(x + sx * 46, y - 20, 9)
        s += bird(160, 780, 1.1, "#8A6A45", -10) + dragonfly(640, 800, 1.2, "#C0262D", 15) + mouse(640, 1180, 1.4)
        s += mushroom(150, 1250, 26, "#D9A441") + mushroom(190, 1258, 18, "#C98A2E") + mushroom(110, 1260, 14, "#D9A441")
        for k in range(10): s += leaf(220 + k * 38, 1300 - (k % 2) * 10, 26, -30 + k * 23, ["#C2601F", "#D9822B"][k % 2], "#5A3A22")
    if season == "winter":
        for k in range(7):
            s += reed(90 + k * 16, 1290, 380 + (k % 3) * 60, .05 * (k - 3)) + reed(710 - k * 16, 1290, 360 + (k % 3) * 60, -.05 * (k - 3))
        s += bird(118, 1150, 0.95, "#A88B5C", 0, "heron") + bat(650, 760, 1.4) + cup_fungus(672, 1250, 20) + cup_fungus(706, 1262, 13)
        s += f'<g transform="translate(680,1185)">{ellipse(0,0,18,11,"#3A2A1A",0,"#111",1.2)}{P("M-14,0 L14,0","none","#C9A13B",1.6)}</g>'
        for (x, y) in [(120, 700), (690, 690), (200, 640), (610, 650), (130, 980), (680, 1010), (400, 60), (250, 120), (560, 110)]:
            s += snowflake(x, y, 9)
        s += P("M110,1300 Q260,1270 400,1300 Q540,1330 690,1300", "none", "#8FB3D1", 6)
    return s

def poster(season):
    c = S[season]; sk = SKIN[season]; cx = 400; cy = 470
    defs = f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['bg'][0]}"/><stop offset="1" stop-color="{c['bg'][1]}"/></linearGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5"><stop offset="0.55" stop-color="{c['halo']}"/><stop offset="1" stop-color="{c['halo2']}"/></radialGradient>
</defs>'''
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">' + defs
    s += f'<rect width="{W}" height="{H}" fill="{c["bg"][0]}"/>'
    # frame
    s += f'<rect x="28" y="28" width="{W - 56}" height="{H - 56}" rx="18" fill="url(#bg)" stroke="{c["frame"]}" stroke-width="8"/>'
    s += f'<rect x="44" y="44" width="{W - 88}" height="{H - 88}" rx="12" fill="none" stroke="{c["frame"]}" stroke-width="2"/>'
    # arch top
    s += P(f"M70,{cy + 40} L70,{cy - 120} Q70,{70} {cx},{70} Q{W - 70},{70} {W - 70},{cy - 120} L{W - 70},{cy + 40}", "none", c["frame"], 4)
    # halo with segments
    s += circle(cx, cy - 20, 250, "url(#halo)", c["frame"], 4)
    for k in range(48):
        a = math.radians(k * 7.5)
        s += P(f"M{cx + math.cos(a) * 200:.1f},{cy - 20 + math.sin(a) * 200:.1f} L{cx + math.cos(a) * 248:.1f},{cy - 20 + math.sin(a) * 248:.1f}", "none", c["frame"] + "88", 2)
    s += circle(cx, cy - 20, 200, "none", c["frame"], 3)
    for k in range(24):
        a = math.radians(k * 15 + 7.5)
        s += circle(cx + math.cos(a) * 224, cy - 20 + math.sin(a) * 224, 6, c["trim"], c["frame"], 1.5)
    # border plants behind figure
    s += border_plants(season)
    # figure
    if season == "summer": s += HAIR[season](cx, cy)  # braids behind
    elif season != "winter": s += HAIR[season](cx, cy) if season == "spring" else ""
    if season == "winter": s += P(f"M{cx - 120},{cy + 140} Q{cx - 215},{cy + 700} {cx - 205},{cy + 830} L{cx + 205},{cy + 830} Q{cx + 215},{cy + 700} {cx + 120},{cy + 140}Z", "#2F4A6B", "#14243A", 2.4)  # cloak
    s += body(cx, cy + 80, sk, c["dress"], c["dress2"], c["trim"])
    s += face(cx, cy, sk)
    if season in ("autumn", "winter"): s += HAIR[season](cx, cy)
    # bouquet held at the waist
    hold_y = cy + 470
    bq = {"spring": lambda: "".join(marigold(cx - 40 + k * 26, hold_y - 40 - (k % 2) * 22, 18) for k in range(4)),
          "summer": lambda: "".join(loosestrife(cx - 30 + k * 20, hold_y - 10, 110 + (k % 2) * 30) for k in range(4)),
          "autumn": lambda: "".join(leaf(cx, hold_y, 70, -60 - k * 22, ["#C2601F", "#D9822B", "#A3471E"][k % 3], "#5A3A22") for k in range(5)) + alder_cone(cx - 12, hold_y - 30, 10) + alder_cone(cx + 14, hold_y - 40, 10),
          "winter": lambda: "".join(reed(cx - 30 + k * 15, hold_y + 10, 150, (k - 2) * .08, "#E3D9C6") for k in range(5))}
    s += bq[season]()
    s += arms(cx, cy + 80, sk, hold_y)
    # lettering panel
    py = 1330
    s += P(f"M70,{py} Q{cx},{py - 40} {W - 70},{py} L{W - 70},{H - 70} L70,{H - 70}Z", c["bg"][0], c["frame"], 4)
    s += f'<text x="{cx}" y="{py + 70}" text-anchor="middle" font-family="Federo, \'Cinzel\', Georgia, serif" font-size="78" letter-spacing="10" fill="{c["ink"]}">{c["fr"]}</text>'
    s += f'<text x="{cx}" y="{py + 112}" text-anchor="middle" font-family="Federo, \'Cinzel\', Georgia, serif" font-size="19" letter-spacing="5" fill="{c["frame"]}">{c["en"]} · ZONES HUMIDES DE SEINE-ET-MARNE</text>'
    sp = c["species"].split(" · "); l1 = " · ".join(sp[:3]); l2 = " · ".join(sp[3:])
    s += f'<text x="{cx}" y="{py + 144}" text-anchor="middle" font-family="\'Cormorant Garamond\', Georgia, serif" font-style="italic" font-size="20" fill="{c["ink"]}">{l1}</text>'
    s += f'<text x="{cx}" y="{py + 168}" text-anchor="middle" font-family="\'Cormorant Garamond\', Georgia, serif" font-style="italic" font-size="20" fill="{c["ink"]}">{l2}</text>'
    s += f'<text x="{cx}" y="{py + 192}" text-anchor="middle" font-family="\'Cormorant Garamond\', Georgia, serif" font-size="13" fill="{c["frame"]}">Linda Angulo López · d\'après Alphonse Mucha, Les Saisons (1896) · lindangulopez.github.io/wetlands-seine-et-marne</text>'
    # corner ornaments
    for (x, y, rx, ry) in [(70, 70, 1, 1), (W - 70, 70, -1, 1), (70, H - 70, 1, -1), (W - 70, H - 70, -1, -1)]:
        s += P(f"M{x},{y + ry * 60} Q{x},{y} {x + rx * 60},{y} M{x + rx * 14},{y + ry * 40} Q{x + rx * 14},{y + ry * 14} {x + rx * 40},{y + ry * 14}", "none", c["frame"], 3) + circle(x + rx * 14, y + ry * 14, 5, c["trim"], c["frame"], 1.5)
    return s + "</svg>"

os.makedirs(OUT, exist_ok=True)
for season in S:
    open(f"{OUT}/poster-{season}.svg", "w").write(poster(season)); print("wrote", season)
