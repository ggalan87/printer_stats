#!/usr/bin/env python3
# coding: utf-8

"""
A tool to parse status page of printers in purpose of keeping stats. Main file.

Copyright (C) 2018 George Galanakis <galan87@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import configparser
import os
import re
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup


class PrinterInfo:
    def __init__(self, name):
        self.name = name


def parse_status_P1606dn(name, url, out_dir):
    with urllib.request.urlopen(url) as response:
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, "lxml")

        # Toner level
        toner_level = soup.find(text=re.compile('Black Cartridge')).parent.parent.findAll('td')[2].string

        # Pages printed
        print_counter = soup.find(text=re.compile('Pages printed with this supply*')).parent.parent.findAll('td')[1].string

        today = datetime.now()
        date_string = today.strftime('%d/%m/%Y,%H:%M')

        out_string = date_string + '|' + toner_level.strip() + '|' + print_counter.strip()
        print(out_string)

        file_path = os.path.join(out_dir, printer_name + '.txt')
        with open(file_path,'a+') as of:
            of.write(out_string + '\n')


if __name__ == "__main__":
    print('Printing Monitor Started')

    # Read the configuration
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    printer_name = config.get('Settings', 'PrinterName')
    printer_url = config.get('Settings', 'PrinterURL')
    out_dir = config.get('Settings', 'OutputDirectory')

    out_dir += '/'

    if not os.path.exists(out_dir):
        raise FileNotFoundError("The output directory does not exist")

    parse_status_P1606dn(printer_name, printer_url, out_dir)

    print('Printing Monitor Quited')
