import subprocess
import sys
import os
from glob import glob
import argparse
import pathlib

parser = argparse.ArgumentParser(
    description='Convert (multi-page) pdf to svg(s).')

parser.add_argument('-k', '--keep-pdf-pages', action='store_true')
parser.add_argument('filepath', type=pathlib.Path)

args = parser.parse_args(sys.argv[1:])

args.filepath = args.filepath.resolve(strict=True)

if not args.filepath.suffix == '.pdf':
    raise ValueError('Input file is not a pdf.')


gs_cmd = ['gswin64c', '-sDEVICE=pdfwrite', '-dSAFER', '-dNoOutputFonts', '-q',
          '-o', '{}'.format(args.filepath.parent.joinpath(args.filepath.stem
                            + '-%03d.pdf')), '{}'.format(args.filepath)]

gs_proc = subprocess.run(gs_cmd)

pdf_pages = glob('{}'.format(args.filepath.parent.joinpath(args.filepath.stem
                             + '-[0-9][0-9][0-9].pdf')))

ink_cmd = ['inkscape', '--export-plain-svg', '--export-type=svg']

if len(pdf_pages) == 1:

    ink_cmd += [pdf_pages[0], '--export-filename={}'.format(
        args.filepath.parent.joinpath(args.filepath.stem + '.svg'))]

    ink_proc = subprocess.run(ink_cmd)

    os.remove(pdf_pages[0])

else:

    ink_cmd += pdf_pages

    ink_proc = subprocess.run(ink_cmd)

    if not args.keep_pdf_pages:
        for page in pdf_pages:
            os.remove(page)
