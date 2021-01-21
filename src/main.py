import rarfile
import threading
from tqdm import tqdm
import time
from argparse import ArgumentParser
import zipfile
import shutil
import os
import pikepdf

version = 1.0

logo = r"""
######################################################################
#  ____  _   _    ____  __   ___    _____   ____    ___   __      _  #
# |  __|| || |   |  __||  \ | _ \  |  _  | / ___|  /   \ |  \    | | #
# | |__ | || |   | |__ | _ |||_| | | |_| || /     |  _  || |\\   | | #
# |  __|| || |   |  __||| |||   /  |  _  || |  __ | | | || | \\  | | #
# | |   | || |   | |   ||_|||   \  | | | || | |_ || |_| || |  \\ | | #
# | |   | || |__ | |__ |   || |\ \ | | | || \_/  ||     || |   \\| | #
# |_|   |_||____||____||__/ |_| \_\|_| |_| \___/|| \___/ |_|    \__| #
#                                                by Frederik Kursawe #
#                                                               v{} #
#                                                                    #
######################################################################""".format(version)



def crack_rar(pwd, file):
    try:
        r = rarfile.RarFile(file)
        r.extractall(pwd=pwd)
        print("[+] Password found: ", pwd)
        exit(0)
    except:
        pass

def crack_zip(pwd, file):
    try:
        zip_file = zipfile.ZipFile(file)
        zip_file.extractall(pwd=pwd.encode())
        print("[+] Password found: ", pwd)
        exit(0)
    except:
        pass

def crack_pdf(pwd, file):
    try:

        with pikepdf.open(file, password=pwd):
            print("[+] Password found: ", pwd)
    except pikepdf._qpdf.PasswordError:
        pass

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-w', '--wordlist', dest="wordlist", nargs=1, required=True, help="The wordlist")
    parser.add_argument('-f', '--file', dest="file", nargs=1, required=True, help='The zip file.')

    args = parser.parse_args()
    # the password list path you want to use
    wordlist = args.wordlist[0]
    # the zip file you want to crack its password
    file = args.file[0]
    print(logo)
    print("\n[*] Starting filegragon")
    ts = time.time()
    with open(wordlist) as w:
        if rarfile.is_rarfile(file):
            print("[*] Beginn cracking...\n")
            for p in w.readlines():
                t = threading.Thread(target=crack_rar, args=(p.strip("\n"), file))
                t.start()

        elif zipfile.is_zipfile(file):
            print("[*] Beginn cracking...\n")
            for p in w.readlines():
                t = threading.Thread(target=crack_zip, args=(p.strip("\n"), file))
                t.start()
        elif file.endswith(".pdf"):
            print("[*] Beginn cracking...\n")
            for p in w.readlines():
                t = threading.Thread(target=crack_pdf, args=(p.strip("\n"), file))
                t.start()
        else:
            print("[!] Invalid file name!!")


td = time.time() - ts
print("Done in " + str(td) + " sec.")