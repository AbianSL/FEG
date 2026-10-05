from astropy.io import fits
import subprocess
import matplotlib.pyplot as plt
from photutils.isophote import EllipseGeometry, Ellipse
import numpy as np

def show_table(data) -> None:
    pass

R_E = 5      # aus dem Plot abgelesen
R_B = 100    # aus dem Plot abgelesen


def mean_pa(pa_deg):
    # Mittelwert für Achsenwinkel (Periode 180°), damit 2° und 178° nicht zu 90° werden
    a = np.radians(pa_deg) * 2
    m = np.arctan2(np.sin(a).mean(), np.cos(a).mean())
    return (np.degrees(m) / 2) % 180


def start_values(isolist, r_e, r_b):
    sma, I, eps = isolist.sma, isolist.intens, isolist.eps
    pa = (np.degrees(isolist.pa) - 90) % 180          # Imfit-Konvention
    good = np.isfinite(I) & (I > 0)

    bulge = good & (sma < r_b)
    disk = good & (sma > r_b)
    inner = good & (sma < r_e)
    mid = good & (sma > r_e) & (sma < r_b)

    slope, icpt = np.polyfit(sma[mid], np.log(I[mid]), 1)   # ln(I) = ln(I0) - R/h

    bulge_p = dict(pa=mean_pa(pa[bulge]), eps=eps[bulge].mean(),
                n=2.0, I_e=I[inner].mean(), r_e=r_e)
    disk_p = dict(pa=mean_pa(pa[disk]), eps=eps[disk].mean(),
                I_0=np.exp(icpt), h=-1 / slope)
    return bulge_p, disk_p


def write_config(path, x0, y0, b, d=None):
    with open(path, "w") as f:
        f.write(f"X0 {x0:.2f} {x0-20:.2f},{x0+20:.2f}\n")
        f.write(f"Y0 {y0:.2f} {y0-20:.2f},{y0+20:.2f}\n")
        f.write("FUNCTION Sersic\n")
        f.write(f"PA {b['pa']:.1f} 0,180\n")
        f.write(f"ell {b['eps']:.3f} 0,1\n")
        f.write(f"n {b['n']:.2f} 0.5,6\n")
        f.write(f"I_e {b['I_e']:.2f} {b['I_e']/10:.2f},{b['I_e']*10:.2f}\n")
        f.write(f"r_e {b['r_e']:.2f} 1,{max(3*b['r_e'], 20):.0f}\n")
        if d:
            f.write("FUNCTION Exponential\n")
            f.write(f"PA {d['pa']:.1f} 0,180\n")
            f.write(f"ell {d['eps']:.3f} 0,1\n")
            f.write(f"I_0 {d['I_0']:.2f} {d['I_0']/10:.2f},{d['I_0']*10:.2f}\n")
            f.write(f"h {d['h']:.2f} {d['h']/3:.2f},{d['h']*3:.2f}\n")  


def main():

    with fits.open("source/NGC0237_i.fits") as f:
        data = f[0].data
    with fits.open("source/NGC0237_mask2D_new.fits") as f:
        mask = f[0].data > 0          # True = Stern/Hintergrundgalaxie, wird ignoriert

    img = np.ma.masked_array(data, mask=mask)

    # Startwerte aus dem Bericht (DS9): Zentrum x0=191, y0=157
    geom = EllipseGeometry(x0=191, y0=157, sma=10, eps=0.3, pa=0.0)
    isolist = Ellipse(img, geom).fit_image(maxsma=160)

    sma = isolist.sma
    pa_imfit = (np.degrees(isolist.pa) - 90) % 180   # Imfit-Konvention

    fig, ax = plt.subplots(3, 1, figsize=(5, 10))
    ax[0].scatter(sma, isolist.intens, s=8)
    ax[0].set_yscale("log")
    ax[0].set_ylabel("Intensität [ADU]")
    #ax[0].set_xlim(0,20)
    #ax[0].set_ylim(200,2000)
    ax[0].set_xlabel("SMA [px]")
    ax[1].scatter(sma, isolist.eps, s=8)
    ax[1].set_ylabel("ε")
    ax[2].scatter(sma, pa_imfit, s=8)
    ax[2].set_ylabel("PA [°] (Imfit)")
    ax[2].set_xlabel("SMA [px]")
    ax[2].set_ylim(70,140)
    ax[2].set_xlim(0,160)
    plt.savefig("isophoten.png", dpi=150)
    plt.show()

    x0 = np.median(isolist.x0[isolist.sma < 10]) + 1    # +1: Imfit zählt ab 1
    y0 = np.median(isolist.y0[isolist.sma < 10]) + 1

    bulge_p, disk_p = start_values(isolist, R_E, R_B)
    print("Bulbus:", bulge_p)
    print("Scheibe:", disk_p)

    write_config("configs/config_auto_sersic.dat", x0, y0, bulge_p)
    write_config("configs/config_auto_sersic_exp.dat", x0, y0, bulge_p, disk_p)

    
    DEFAULT_FILE = "source/NGC0237_i.fits"
    with fits.open(DEFAULT_FILE) as file:
        header = file[0].header
        data = file[0].data
        SKY = 264.45304
        ZCAL = -23.7458
        GAIN = 4.87
        READ_NOISE = 4.6225
        FWGN_I = 0,8316
        BETA_I = 3.8
        
        #print(header.keys)

        subprocess.run(["./run.sh", f"--sky={SKY}", f"--gain={GAIN}", f"--readnoise={READ_NOISE}", "-s", "-m", "-p"])

if __name__ == "__main__":
    main()
