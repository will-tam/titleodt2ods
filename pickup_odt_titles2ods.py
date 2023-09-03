#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library import.
import sys
import os
import glob

# Third-part library import.
import odfdo

# Project library import.


######################

ODS_FILENAME = '00-Sommaire-pickup_odt_title2ods.ods'
TOC_TABLE_TITLE = 'Sommaire'

HEADERS_NAME = ['Fichiers', 'Titre']

def help(appli, why=None):
    """
    Print if need help.
    """
    print("\n")
    if why:
        print(f"ERROR : {why}\n\n")
    print(f"Utilisation : {appli} [-h | --help] [/ce/chemin/]fichier.odt | /ce/chemin/")
    print("\n")

def check_old_ods_file():
    """
    Check if ods ODS_FILENAME file exists.
    If 'yes', ask to overwrite it.
    If overwriting is accepted, return True, everelse False
    """
    rc = True

    if os.path.exists(ODS_FILENAME):
        answ = ""
        print(f"\n{ODS_FILENAME} already exists. Overwrite it (y/n) ?")
        while answ not in ['y', 'n']:
            answ = input().lower()

        if answ == 'n':
            rc = False

    return rc

def extract_titles(odtfile):
    """
    Extract titles from odt odtfile file.
    """
    body = odfdo.Document(odtfile).body
    found_titles = [paragraph.text_recursive for paragraph in body.get_paragraphs() if paragraph.get_attribute('text:style-name') in ['Title', 'Heading']]

    return (odtfile, found_titles)

def create_ods(odsfile, datas):
    """
    Create a new .ods odsfile file according given datas.
    Old ods file will be cheched.
    """

    if not check_old_ods_file():
        print(f"\nNo new {ODS_FILENAME} created !\n")
        return False

    bold_cell = odfdo.Element.from_tag(
    '''
    <style:style style:name="ce1" style:family="table-cell" style:parent-style-name="Default">
    <style:text-properties fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/>
    </style:style>
    '''
    )

    document = odfdo.Document('spreadsheet')
    body = document.body
    table = odfdo.Table(TOC_TABLE_TITLE, width=2, height=1)
    body.clear()
    body.append(table)

    headers_bold = document.insert_style(bold_cell,  automatic=True)

    table.set_row_values(y=0, values=HEADERS_NAME, style=headers_bold)

    for r, data in enumerate(datas):
        r += 1
        table.set_row_values(y=r, values=[data[0]] + data[1])

    print("\ntable size:", table.size)
    table.rstrip()
    print("table size after strip:", table.size)
    print(f"Content :\n{table.to_csv()}")

    document.save(target=odsfile, pretty=True)

    return True

def main(args):
    """
    Main function.
    @parameters : some arguments, in case of use.
    @return : 0 = all was good.
              ... = some problem occures.
    """
    if len(args) == 1 or args[1] in ['-h', '--help'] :
        help(args[0])
        return 1

    odtfile = args[1]

    if args[1][-4:].find(".odt") != -1 :
        odtfiles = [args[1]]
    elif os.path.isdir(odtfile):
        odtfiles = glob.glob(os.path.join(odtfile, '*.odt'))
    else:
        help(args[0], "quel fichier(s) odt dois-je traiter ?")
        return 2

    if len(odtfiles) == 0:
        help(args[0], f"Pas de fichiers odt trouvés dans le repertoire {odtfile}")
        return 3

    if len(odtfiles) == 1 and not os.path.exists(odtfile):
        help(args[0], f"fichier {odtfiles[0]} : innexistant !")
        return 4

    titles = [extract_titles(odtfile) for odtfile in odtfiles]

    if not create_ods(ODS_FILENAME, titles):
        return 5

    return 0

######################

if __name__ == "__main__":
    ret_code = main(sys.argv)      # Keep only the argus after the script name.
    sys.exit(ret_code)
