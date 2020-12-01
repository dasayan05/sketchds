import os
import wget, shutil
from csv import reader

def main(args):
    curdir = os.path.dirname(os.path.abspath(__file__))
    url_file = os.path.join(curdir, 'glyphazzn_urls.txt')

    # There are 3 types of extension - TTF/OTF/PFB
    os.makedirs(os.path.join(args.outdir, 'ttf'), exist_ok=True)
    os.makedirs(os.path.join(args.outdir, 'otf'), exist_ok=True)
    os.makedirs(os.path.join(args.outdir, 'pfb'), exist_ok=True)
    os.makedirs(os.path.join(args.outdir, 'others'), exist_ok=True)

    with open(url_file, 'r') as read_obj:
        csv_reader = reader(read_obj)

        for row in csv_reader:
            link = row[-1].strip()
            try:
                filepath = wget.download(link, out=args.outdir)
                filename = os.path.basename(filepath)
            except Exception as e:
                print('[error]', e.__class__, link)
                continue
            print(filename, 'downloaded successfully')

            # Put the downloaded files into proper folder
            fname_split_parts = filename.split('.')
            ext = fname_split_parts[-1]
            # breakpoint()

            if ext.lower() == 'ttf':
                shutil.move(filepath, f'{args.outdir}/ttf/{filename}')
            elif ext.lower() == 'otf':
                shutil.move(filepath, f'{args.outdir}/otf/{filename}')
            elif ext.lower() == 'pfb':
                shutil.move(filepath, f'{args.outdir}/pfb/{filename}')
            else:
                # some junk; can be deleted
                shutil.move(filepath, f'{args.outdir}/others/{filename}')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Downloading GlyphAZZN raw font files')
    parser.add_argument('--outdir', type=str, required=True, help='path to an empty folder')
    args = parser.parse_args()

    main(args)
