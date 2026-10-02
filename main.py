from astropy.io import fits
import subprocess

def main():
    DEFAULT_FILE = "source/NGC0237_i.fits"
    with fits.open(DEFAULT_FILE) as file:
        header = file[0].header
        data = file[0].data
        SKY = 264.45304
        ZCAL = -23.7458
        GAIN = 4.87
        READ_NOISE = 4.6225
        
        subprocess.run(["./run.sh", f"--sky={SKY}", f"--gain={GAIN}", f"readnoise={READ_NOISE}", "-s"])

if __name__ == "__main__":
    main()
