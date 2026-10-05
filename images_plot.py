import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

PIX = 0.396                      # arcsec/px
ZP = 23.7458                     # = -ZCAL (siehe Hinweis unten)
x0, y0 = 190.12, 155.40          # Zentrum (Imfit minus 1)

data = fits.getdata("source/NGC0237_i.fits")
model = fits.getdata("Resultados_sersic_exp/model_sersic_exp.fits")
mask = fits.getdata("source/NGC0237_mask2D_new.fits") > 0

def mu(I):
    I = np.where(I > 0, I, np.nan)            # Pixel mit ≤ 0 lassen sich nicht umrechnen
    return -2.5 * np.log10(I) + ZP

mu_d, mu_m = mu(data), mu(model)
dmu = mu_d - mu_m                              # Residuum in mag/arcsec²

# Ausschnitt auf das Fitfenster
ys, xs = np.where(~mask)
sl = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
extent = [(xs.min() - 0.5 - x0) * PIX, (xs.max() + 0.5 - x0) * PIX,
          (ys.min() - 0.5 - y0) * PIX, (ys.max() + 0.5 - y0) * PIX]

# Grenzen der Skala: hell = kleine Zahl
vmin = mu(np.percentile(data[~mask], 99.9))
vmax = mu(np.percentile(data[~mask & (data > 0)], 10))

cm = plt.get_cmap("inferno_r").copy()
cm.set_bad("black")

fig, ax = plt.subplots(1, 3, figsize=(16, 4.5), sharex=True, sharey=True)
for a, img, t in zip(ax[:2], [mu_d, mu_m], ["Galaxia", "Modelo"]):
    im = a.imshow(img[sl], origin="lower", cmap=cm, vmin=vmin, vmax=vmax, extent=extent)
    a.set_title(t)
cb = fig.colorbar(im, ax=ax[:2], label="μ$_r$ [mag/arcsec²]", shrink=0.85)
cb.ax.invert_yaxis()                            # hell (kleine μ) oben

lim = 0.5
im2 = ax[2].imshow(dmu[sl], origin="lower", cmap="seismic_r",
                   vmin=-lim, vmax=lim, extent=extent)
ax[2].set_title("Residuo")
fig.colorbar(im2, ax=ax[2], label="μ$_r$ [mag/arcsec²]", shrink=0.85)

for a in ax:
    a.set_xlabel("x [arcsec]")
ax[0].set_ylabel("y [arcsec]")
plt.savefig("fit_2d.png", dpi=200, bbox_inches="tight")
plt.show()