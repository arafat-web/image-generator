
# Image Generator (Portfolio Hero)

Generate a flat-style PNG hero image for your portfolio, customized with your name, role, and tagline.

## Quick start

```bash
pip install -r requirements.txt
python generate_portfolio_hero.py
```

This writes `portfolio_hero.png` (1024x1024) with your info.

## Customize

Edit the top of `generate_portfolio_hero.py` or override via environment variables:

- `PORTFOLIO_NAME` (default: "Arafat Hossain Ar")
- `PORTFOLIO_ROLE` (default: "Full Stack Software Developer")
- `PORTFOLIO_TAGLINE` (default: "PHP, Java, JavaScript, and SQL — Laravel, CodeIgniter, JSP.")
- `PORTFOLIO_WIDTH` (default: 1024)
- `PORTFOLIO_HEIGHT` (default: 1024)
- `PORTFOLIO_OUTPUT` (default: "portfolio_hero.png")

Example:

```bash
PORTFOLIO_NAME="Arafat Hossain Ar" \
PORTFOLIO_ROLE="Full Stack Software Developer" \
PORTFOLIO_TAGLINE="PHP, Java, JavaScript, and SQL — Laravel, CodeIgniter, JSP." \
python generate_portfolio_hero.py
```

## GitHub Actions

Trigger the workflow manually in the Actions tab and optionally provide inputs (name, role, tagline, width, height). If inputs are blank, the script keeps its defaults.
