import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.isophote import EllipseGeometry, Ellipse

PIX = 0.396          # arcsec/px
ZP = 23.7458         # = -ZCAL, siehe Hinweis unten

def profile(img, mask, x0, y0, eps, pa_imfit, rmax=160, dr=1.0):
    yy, xx = np.indices(img.shape)
    th = np.radians(pa_imfit + 90)                 # wie im Bericht: θ = PA + 90°
    dx, dy = xx - x0, yy - y0
    xp = dx * np.cos(th) + dy * np.sin(th)
    yp = -dx * np.sin(th) + dy * np.cos(th)
    a = np.hypot(xp, yp / (1 - eps))               # große Halbachse durch jeden Pixel

    edges = np.arange(0, rmax + dr, dr)
    r, I = [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = (a >= lo) & (a < hi) & ~mask
        if sel.sum() > 10:
            r.append(0.5 * (lo + hi))
            I.append(img[sel].mean())
    r, I = np.array(r), np.array(I)
    ok = I > 0
    return r[ok] * PIX, -2.5 * np.log10(I[ok]) + ZP

data = fits.getdata("source/NGC0237_i.fits")
model = fits.getdata("Resultados_sersic_exp/model_sersic_exp.fits")
mask = fits.getdata("source/NGC0237_mask2D_new.fits") > 0

x0, y0 = 190.12, 155.40      # Imfit-Zentrum (191,12 / 156,40) minus 1 für Python
r_d, mu_d = profile(data, mask, x0, y0, eps=0.40, pa_imfit=87.7)
r_m, mu_m = profile(model, mask, x0, y0, eps=0.40, pa_imfit=87.7)

# Komponenten aus den Imfit-Parametern (entlang der jeweiligen großen Achse)
n, I_e, r_e = 1.545, 214.124, 9.936
I_0, h = 657.853, 23.486
b = 1.9992 * n - 0.3271
r = np.linspace(0.5, 160, 300)                       # Pixel
I_b = I_e * np.exp(-b * ((r / r_e) ** (1 / n) - 1))
I_d = I_0 * np.exp(-r / h)
mu = lambda I: -2.5 * np.log10(I) + ZP

plt.plot(r_d, mu_d, "k.", label="Galaxia")
plt.plot(r_m, mu_m, "r-", label="Sérsic + Exponencial")
plt.plot(r * PIX, mu(I_b), "b--", label="Sérsic")
plt.plot(r * PIX, mu(I_d), "g--", label="Exponencial")
plt.gca().invert_yaxis()
plt.xlabel("R [arcsec]")
plt.ylabel("μ$_r$ [mag/arcsec²]")
plt.legend()
plt.savefig("profil_1d.png", dpi=150)
plt.show()