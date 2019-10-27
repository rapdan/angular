# -*- coding: utf-8 -*-

import os
import sys
import re
from google.cloud import translate

# Create your own account in Google Cloud Platform and generate a file .json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'your_token.json'
target = 'pl'   # you can change to another language


def save_line(line, plik='nowy.srt'):
    ''' Funkcja dopisuje kolejną linię do zadanego pliku (domyślnie nowy.src)'''
    with open(plik, 'a') as f:
        f.write(line)


def clear_file(plik_dest):
    ''' Funkcja czysci zadany plik z informacji zapisanych wczesniej'''
    try:
        with open(plik_dest, 'w') as f:
            f.write('')
    except IOError as err:
        print('Cos poszło nie tak jak powinno z plikiem..', err)
        er = sys.exc_info()
        for e in er:
            print(e)
    return print('Rozpoczynam tłumaczenie...')


def file_name_input():
    ''' Prosi o wprowadzenie nazwy pliku i sprawdza czy istnieje z 
        rozszerzeniem .srt lub bez rozszerzenia
        zwraca nazwe pliku do tłumaczenia z rozszerzeniem .src'''
    while True:
        try:
            plik_source = input('Podaj nazwę pliku .srt do tłumaczenia: ')
            if os.path.exists(plik_source):  # sprawdzenie czy istnieje plik
                return plik_source
            # sprawdzenie czy istnieje plik bez .srt
            elif os.path.exists(plik_source + '.srt'):
                return plik_source + '.srt'
            # sprawdzenie czy istnieje plik bez .en.srt
            elif os.path.exists(plik_source + '.en.srt'):
                return plik_source + '.en.srt'
            else:
                continue
        except IOError as err:
            print('Problem z plikiem..', err)
            er = sys.exc_info()
            for e in er:
                print(e)
        continue


def name_dest(plik_source):
    ''' Tworzy nazwe pliku do ktorego zostaną zapisane rezultaty tłumaczenia.
        zmienia koncówkę .en.src na .pl.src i zwraca plik_dest'''
    try:
        plik_dest = re.sub(r'.en.srt|.srt', r'.pl.srt', plik_source)
        return plik_dest
    except IOError as err:
        print('Nie można utworzyć nazwy pliku z koncówką .pl.srt', err)
        er = sys.exc_info()
        for e in er:
            print(e)

# def change_lang_name():
#     pass


# def translate_text(text, target='pl'):
#     ''' Moduł tłumaczacy wybraną frazę '''
#     #tr = translate.Client()
#     translation = tr.translate(text, target)
#     return translation


def main():
    plik_source = file_name_input()
    print('Plik źródłowy: {}'.format(plik_source))
    plik_dest = name_dest(plik_source)
    print('Plik wynikowy: {}'.format(plik_dest))

    clear_file(plik_dest)  # wyczyszczenie pliku jeżeli był wcześniej zapisany

    # regular expresion to search text to translate in file .srt
    regex = (r'\d+\n')  # only number in line
    regex2 = (r'\d+:\d+:\d+.\d+ -->')  # only time and --> in line
    translate_client = translate.Client()  # utworzenie klasy translatora

    with open(plik_source) as f:
        for line in f:
            if line == '':
                save_line('\n', plik_dest)
                continue
            elif re.match(regex, line):
                save_line(line, plik_dest)
                continue
            elif re.match(regex2, line):
                save_line(line, plik_dest)
                continue
            else:
                translation = translate_client.translate(
                    line, target_language=target)
                line_pl = translation['translatedText'] + '\n'
                print(line_pl)
                save_line(line_pl, plik_dest)


if __name__ == "__main__":
    main()
