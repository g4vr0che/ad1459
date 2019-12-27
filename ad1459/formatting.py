#!/usr/bin/env python3

""" AD1459, an IRC Client

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  A parser for IRC style tags.
"""

import logging

class Parser:

    formatting = {
        '\x02': ['b', '*'],
        #'\u0003': 'color',
        #'\u000F': 'clear',
        '\x1D': ['i', '_'],
        '\x1F': ['u', '-']
    }

    def __init__(self):
        self.log = logging.getLogger('ad1459.formatting')
    
    def format_text(self, text):
        for i in self.formatting:
            # text = text.replace(f'/{self.formatting[i][0]}', i)
            text = text.replace(f'/{self.formatting[i][1]}', i)
        return text

    def parse_text(self, text):
        # text = text.replace('\u0002', '') # bold
        # text = text.replace('\u0003', '') # colour
        # text = text.replace('\u000F', '') # cancel all
        # text = text.replace('\u001D', '') # italic
        # text = text.replace('\u001F', '') # underline
        
        # \u0002 bold
        # \u0003 colour
        # \u000F cancel all
        # \u001D italic
        # \u001F underline
        text = self.fix_markedup_tags(text)
        f_text = ''
        current_tags = []

        for char in text:
            if char in self.formatting:
                print(self.formatting[char])

                if not char in current_tags:
                    for tag in reversed(current_tags):
                        f_text = f'{f_text}</{self.formatting[tag][0]}>'

                    current_tags.append(char)
                    print(current_tags)
                    for tag in current_tags:
                        f_text = f'{f_text}<{self.formatting[tag][0]}>'

                else:
                    for tag in reversed(current_tags):
                        f_text = f'{f_text}</{self.formatting[tag][0]}>'

                    current_tags.pop()
                    print(current_tags)
                    for tag in current_tags:
                        f_text = f'{f_text}<{self.formatting[tag][0]}>'

            else: 
                f_text = f'{f_text}{char}'
        
        for tag in reversed(current_tags):
            f_text = f'{f_text}</{self.formatting[tag][0]}>'

        return f_text
    
    def fix_markedup_tags(self, text):
        mu_formatting = {
            '&#x2;': '\x02',
            #'\u0003': #'\u0003',
            #'\u000F': #'\u000F',
            '&#x1d;': '\x1D',
            '&#x1f;': '\x1F'
        }

        for i in mu_formatting:
            text = text.replace(i, mu_formatting[i])
        
        return text