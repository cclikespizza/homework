# -*- coding=utf-8 -*-

__author__ = 'elmira'

import codecs
import re
from lxml.html import parse


class Struct:
    def __init__(self, **values):
        vars(self).update(values)


def show(prof):
    prof1 = u''
    prof1 += ' '.join([u'Преподаватель:', prof.surname, prof.first_name, prof.fathers_name, u'\r\n'])
    prof1 += ' '.join([u'Телефон(ы):', ''.join(prof.phone), u'\r\n'])
    prof1 += ' '.join([u'Е-мейл(ы):', ', '.join(prof.email), u'\r\n'])
    prof1 += ' '.join([u'Адрес:', prof.address, u'\r\n'])
    prof1 += ' '.join([u'Подразделения:', ', '.join(prof.places), u'\r\n'])
    prof1 += u'Подразделение и должность:' + u'\r\n'
    for department in prof.faculty:
        prof1 += '    ' + department + u': ' + prof.faculty[department] + u'\r\n'
    prof1 += u'\r\n'
    return prof1


def split_name(name):
    fathers_name = ''
    name = name.split()
    surname, first_name = name[0], name[1]
    if len(name) == 3:
        fathers_name = name[2]
    return surname, first_name, fathers_name


def process_fac(depts):
    dic = {}  # this is a dictionary {workplace : position}
    all_depts = set()  # this is a set of all departments that a person belongs to
    if depts:
        places = depts.split('|')
        for place in places:
            place = place.strip()
            if ':' in place:
                place, job = place.split(':')[0], place.split(':')[1]
                dic[place.strip()] = job.strip()
            all_depts.add(place.strip())
    return dic, all_depts


def process_email(line):
    line = re.search(u'document.write\\((.*?)\\)', line, flags=re.U | re.DOTALL)
    email = line.group(1).replace(u"'+'", '').replace(u"<wbr/>", '')[1:-1].split(' ')
    email = [adr.strip(',:;') for adr in email if adr.strip(',:;') != '' and '@' in adr and len(adr) > 1]
    return email


def create_prep(tree):
    # Honestly, this one should be much shorter. But... well, it works and I let it go


    surname, first_name, fathers_name = split_name(tree.findall('.//*[@class="emp-fio"]/*')[0].text)

    faculty = ''.join(tree.findall('.//*[@class="emp-description"]/*[@class="details"]')[0].itertext())
    faculty, places = process_fac(faculty)

    address = tree.findall('.//*[@class="emp-description"]/*[@class="addr"]')
    if address:
        address = ''.join(address[0].itertext()).replace(u'Адрес: ', '')

    phone = tree.findall('.//*[@class="emp-description"]/*[@class="tel"]')
    if phone:
        phone = ''.join(phone[0].itertext()).replace(u'Телефон: ', '')

    email = tree.findall('.//*[@class="emp-description"]/script')
    if email:
        email = process_email(''.join(email[0].itertext()))
    return Struct(surname=surname, first_name=first_name, fathers_name=fathers_name,
                  faculty=faculty, places=places, address=address, phone=phone, email=email)

if __name__ == "__main__":

    text = codecs.open(u'pros.html', 'r', 'utf-8')
    data = parse(text)
    text.close()
    emps = data.findall('//*[@class="emp-item"]')
    db = []
    for emp in emps:
        db.append(create_prep(emp))
    for i in [337, 338]:
        print show(db[i])
