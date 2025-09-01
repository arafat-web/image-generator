from PIL import Image, ImageDraw, ImageFont
import os

# Defaults (edit these to customize)
WIDTH, HEIGHT = 1024, 1024  # flat, 1024x1024
OUTPUT = "portfolio_hero.png"
NAME = "Arafat Hossain Ar"
ROLE = "Full Stack Software Developer"
TAGLINE = "PHP, Java, JavaScript, and SQL — Laravel, CodeIgniter, JSP."

# Color palette (flat)
COLORS = {
    "bg": (15, 23, 42),          # slate-900
    "primary": (99, 102, 241),   # indigo-500
    "accent": (14, 165, 233),    # sky-500
    "accent2": (56, 189, 248),   # sky-400
    "muted": (148, 163, 184),    # slate-400
    "white": (255, 255, 255)
}

def load_font(size, bold=False):
    # Try common fonts, fall back to default
    candidates = [
        ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
        ("Arial Bold.ttf" if bold else "Arial.ttf"),
        ("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"),
        ("Inter-Bold.ttf" if bold else "Inter-Regular.ttf"),
        ("Poppins-Bold.ttf" if bold else "Poppins-Regular.ttf"),
        ("Montserrat-Bold.ttf" if bold else "Montserrat-Regular.ttf"),
    ]
    for fname in candidates:
        try:
            return ImageFont.truetype(fname, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_accent_shapes(base):
    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Large soft circle off-canvas (top-right)
    r = int(w * 0.85)
    bbox = (int(w - r * 0.65), int(-r * 0.35), int(w + r * 0.35), int(r * 0.65))
    d.ellipse(bbox, fill=COLORS["primary"] + (60,))

    # Medium circle (bottom-left)
    r2 = int(w * 0.5)
    bbox2 = (int(-r2 * 0.3), int(h - r2 * 0.9), int(r2 * 0.7), int(h + r2 * 0.1))
    d.ellipse(bbox2, fill=COLORS["accent"] + (70,))

    # Rounded rectangle as abstract layer
    card = Image.new("RGBA", (int(w * 0.55), int(h * 0.22)), (0, 0, 0, 0))
    dc = ImageDraw.Draw(card)
    dc.rounded_rectangle(
        (0, 0, card.size[0], card.size[1]),
        radius=int(card.size[1] * 0.25),
        fill=COLORS["accent2"] + (55,),
    )
    card = card.rotate(345, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(card, (int(w * 0.38), int(h * 0.64)))

    # Subtle radial highlight
    rad = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(rad)
    center = (int(w * 0.35), int(h * 0.25))
    max_r = int(w * 0.6)
    for rr in range(max_r, 0, -4):
        alpha = int(20 * (1 - rr / max_r))
        bbox = (center[0] - rr, center[1] - rr, center[0] + rr, center[1] + rr)
        dr.ellipse(bbox, fill=alpha)
    glow = Image.new("RGBA", (w, h), COLORS["white"] + (0,))
    base.alpha_composite(glow, (0, 0), rad)
    base.alpha_composite(overlay)

def fit_text(draw, text, max_width, base_size, bold=False):
    size = base_size
    while size > max(10, int(base_size * 0.4)):
        font = load_font(size, bold=bold)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 1
    return load_font(max(10, int(base_size * 0.4)), bold=bold)

def draw_avatar(base, cx, cy, radius, initials="AH"):
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Outer circle
    d.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=COLORS["primary"] + (255,))
    # Inner circle offset for depth
    inner_r = int(radius * 0.86)
    d.ellipse((cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r), fill=COLORS["accent"] + (255,))

    # Initials
    font = load_font(int(radius * 0.75), bold=True)
    tb = d.textbbox((0, 0), initials, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    d.text((cx - tw / 2, cy - th / 2 - 4), initials, font=font, fill=COLORS["white"])

    base.alpha_composite(overlay)

def draw_button(draw, x, y, w, h, text, filled=True):
    radius = int(h * 0.45)
    rect = (x, y, x + w, y + h)
    if filled:
        draw.rounded_rectangle(rect, radius=radius, fill=COLORS["primary"])
        txt_color = COLORS["white"]
    else:
        draw.rounded_rectangle(rect, radius=radius, outline=COLORS["white"], width=3)
        txt_color = COLORS["white"]

    font = load_font(int(h * 0.45), bold=True)
    tb = draw.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    tx = x + (w - tw) / 2
    ty = y + (h - th) / 2 - 2
    draw.text((tx, ty), text, font=font, fill=txt_color)

def main():
    w, h = WIDTH, HEIGHT

    # Base canvas
    img = Image.new("RGBA", (w, h), COLORS["bg"] + (255,))
    draw = ImageDraw.Draw(img)

    # Decor
    draw_accent_shapes(img)

    # Layout
    margin = int(w * 0.08)
    col_w = int(w * 0.52)
    x = margin
    y = int(h * 0.22)

    # Headline
    title_font = fit_text(draw, NAME, max_width=col_w, base_size=int(w * 0.11), bold=True)
    tb = draw.textbbox((0, 0), NAME, font=title_font)
    draw.text((x, y), NAME, font=title_font, fill=COLORS["white"])
    y += (tb[3] - tb[1]) + int(h * 0.02)

    # Role
    role_font = fit_text(draw, ROLE, max_width=col_w, base_size=int(w * 0.05), bold=True)
    tb = draw.textbbox((0, 0), ROLE, font=role_font)
    draw.text((x, y), ROLE, font=role_font, fill=COLORS["accent2"])
    y += (tb[3] - tb[1]) + int(h * 0.025)

    # Tagline (wrap simple)
    paragraph_font = load_font(int(w * 0.032))
    words = TAGLINE.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        tw = draw.textbbox((0, 0), test, font=paragraph_font)[2]
        if tw <= col_w:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    for line in lines[:3]:
        draw.text((x, y), line, font=paragraph_font, fill=COLORS["muted"])
        y += draw.textbbox((0, 0), line, font=paragraph_font)[3] - draw.textbbox((0, 0), line, font=paragraph_font)[1] + int(h * 0.012)

    # Buttons
    btn_w = int(w * 0.26)
    btn_h = int(h * 0.07)
    spacing = int(w * 0.03)
    btn_y = y + int(h * 0.02)
    draw_button(draw, x, btn_y, btn_w, btn_h, "View Projects", filled=True)
    draw_button(draw, x + btn_w + spacing, btn_y, btn_w, btn_h, "Contact Me", filled=False)

    # Avatar placeholder on right
    cx = int(w * 0.74)
    cy = int(h * 0.45)
    r = int(min(w, h) * 0.18)
    initials = "".join([p[0] for p in NAME.split()[:2]]).upper() if NAME.strip() else "AH"
    draw_avatar(img, cx, cy, r, initials=initials)

    # Save
    out = img.convert("RGB")  # PNG without alpha if needed by some hosts
    out.save(OUTPUT, "PNG")
    print(f"Wrote {OUTPUT} ({w}x{h}, flat style)")

if __name__ == "__main__":
    # Allow quick env overrides if desired; fall back to defaults if empty
    env_name = os.getenv("PORTFOLIO_NAME")
    env_role = os.getenv("PORTFOLIO_ROLE")
    env_tagline = os.getenv("PORTFOLIO_TAGLINE")
    env_output = os.getenv("PORTFOLIO_OUTPUT")
    env_width = os.getenv("PORTFOLIO_WIDTH")
    env_height = os.getenv("PORTFOLIO_HEIGHT")

    NAME = env_name or NAME
    ROLE = env_role or ROLE
    TAGLINE = env_tagline or TAGLINE
    OUTPUT = env_output or OUTPUT
    try:
        WIDTH = int(env_width) if env_width else WIDTH
        HEIGHT = int(env_height) if env_height else HEIGHT
    except Exception:
        pass
    main()