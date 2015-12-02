__author__ = 'elmira'

import subprocess
import os
import codecs, uuid

PATH_TO_MYSTEM = 'C:\\Users\\Admin\\OneDrive\\PycharmProjects\\prog_homework\\seminar10\\mystem.exe'

def mystem(fname):
    with open('corpus/'+fname, encoding='utf-8') as f1:
        fname2 = 'temp' + str(uuid.uuid4()) + '.txt'
        f = codecs.open(fname2, 'w', 'utf-8')
        f.write(f1.read())
        f.close()
    args = [PATH_TO_MYSTEM, '-cnisd', '--format', 'xml', '--eng-gr', fname2]

    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    output = p.stdout.read()  # this is mystem xml
    os.remove(fname2)
    with open('xml/'+fname.replace('txt', 'xml'), 'wb') as f:
        f.write(output)

for fname in os.listdir('corpus'):
    mystem(fname)