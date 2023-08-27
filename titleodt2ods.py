#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Standard library import.
import sys
import os
import glob
import zipfile
import re
import csv

# Third-part library import.

# Project library import.

######################

CONTENT_XML_NAME = 'content.xml'
CSV_FILE_NAME = '00-Sommaire.csv'

HEADERS_NAME = ['Fichiers', 'Titre']

re_Titre = re.compile(r'<text:p text:style-name="Title">(.*?)</text:p>')
re_Heading = re.compile(r'<text:p text:style-name="Heading">(.*?)</text:p>')
re_sub = re.compile(r'<.*?>')

def help(appli, why=None):
    """
    Print if need help.
    """
    print("\n")
    if why:
        print(f"ERROR : {why}\n\n")
    print(f"Utilisation : {appli} [-h | --help] [/ce/chemin/]fichier.odt | /ce/chemin/")
    print("\n")

def extract_content_xml(odtfile):
    """
    Return CONTENT_XML file content, or None if something wrong.
    """
    try:
        with zipfile.ZipFile(odtfile) as zipf:
            with zipf.open(CONTENT_XML_NAME) as content_xmlfile:
                return content_xmlfile.read().decode(encoding='utf-8')
    except:
        return None

def extract_Titre(content_xml):
    """
    Return found title beetween Title or Heading tags.
    Cleanup some other unwanted tags inside result.
    """
    titles = []

    titre = re_Titre.search(content_xml)
    heading = re_Heading.search(content_xml)

    if titre:
        titles.append(titre.group(1))

    if heading:
        titles.append(heading.group(1))

    titles = [re_sub.sub('', title) for title in titles]

    return titles

def create_csv(csv_file_name, what):
    """
    Create a CSV file.
    """
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, HEADERS_NAME, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(HEADERS_NAME)
        for file_name, titles in what.items():
            csv_writer.writerow([file_name] + titles)

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

    files_titles = {}
    for odtfile in odtfiles:
        print("")
        print(f"Traitement de {odtfile}")
        content_xml = extract_content_xml(odtfile)
        if content_xml:
            titles = extract_Titre(content_xml)
        else:
            print(f"Pas de fichier {CONTENT_XML_NAME} ou problème dans {odtfile}")
            return 5

        files_titles.update({odtfile : titles})

#    print(f"\n{files_titles}")

    print(f"\nEcriture de {CSV_FILE_NAME} ... \n")
    create_csv(CSV_FILE_NAME, files_titles)

    return 0

######################

if __name__ == "__main__":
    ret_code = main(sys.argv)      # Keep only the argus after the script name.
    sys.exit(ret_code)
