import kindlecomicconverter.comic2ebook as c2e
from multiprocessing import freeze_support, set_start_method
import os
import sys
import subprocess

path = '/Users/nicholasharman/Documents/Manga_to_try/To_Convert'
dir_list = next(os.walk('/Users/nicholasharman/Documents/Manga_to_try/To_Convert'))
place = 0

if __name__ == '__main__':
    set_start_method('spawn')
    freeze_support()
    for a in dir_list[1]:
        place += 1
        print(str(place) + " of " + str(len(dir_list[1])) + " " + a)
        c2e.main(["--profile=KV", "--upscale","--splitter=0" ,path + "/" + a])
#print("Done")

"""
**if no path given it will write in the place its executed. i dont think the path thing at the end does anything**

Usage: kcc-c2e [options] comic_file|comic_folder

Options:
  MAIN:
    -p PROFILE, --profile=PROFILE
                        Device profile (Available options: K1, K2, K34, K578,
                        KDX, KPW, KV, KO, KoMT, KoG, KoGHD, KoA, KoAHD, KoAH2O,
                        KoAO, KoF) [Default=KV]
    -m, --manga-style   Manga style (right-to-left reading and splitting)
    -q, --hq            Try to increase the quality of magnification
    -2, --two-panel     Display two not four panels in Panel View mode
    -w, --webtoon       Webtoon processing mode

  OUTPUT SETTINGS:
    -o OUTPUT, --output=OUTPUT
                        Output generated file to specified directory or file
    -t TITLE, --title=TITLE
                        Comic title [Default=filename or directory name]
    -f FORMAT, --format=FORMAT
                        Output format (Available options: Auto, MOBI, EPUB,
                        CBZ, KFX) [Default=Auto]
    -b BATCHSPLIT, --batchsplit=BATCHSPLIT
                        Split output into multiple files. 0: Don't split 1:
                        Automatic mode 2: Consider every subdirectory as
                        separate volume [Default=0]

  PROCESSING:
    -u, --upscale       Resize images smaller than device's resolution
    -s, --stretch       Stretch images to device's resolution
    -r SPLITTER, --splitter=SPLITTER
                        Double page parsing mode. 0: Split 1: Rotate 2: Both
                        [Default=0]
    -g GAMMA, --gamma=GAMMA
                        Apply gamma correction to linearize the image
                        [Default=Auto]
    -c CROPPING, --cropping=CROPPING
                        Set cropping mode. 0: Disabled 1: Margins 2: Margins +
                        page numbers [Default=2]
    --cp=CROPPINGP, --croppingpower=CROPPINGP
                        Set cropping power [Default=1.0]
    --blackborders      Disable autodetection and force black borders
    --whiteborders      Disable autodetection and force white borders
    --forcecolor        Don't convert images to grayscale
    --forcepng          Create PNG files instead JPEG

  CUSTOM PROFILE:
    --customwidth=CUSTOMWIDTH
                        Replace screen width provided by device profile
    --customheight=CUSTOMHEIGHT
                        Replace screen height provided by device profile

  OTHER:
    -h, --help          Show this help message and exit


Links
https://github.com/ciromattia/kcc/wiki/Profiles#current-devices
https://github.com/ciromattia/kcc/blob/master/README.md
https://hub.docker.com/r/wesleympg/kindle-comic-converter-cli
"""
