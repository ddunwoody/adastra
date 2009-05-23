from lxml import etree
import re

class SvgLoader(object):
    def __init__(self, path):
        svg = etree.parse(path)
        find = etree.ETXPath('//path')
        self.paths = find(svg)
    
    def parse(self):
        return [tuple(float(p) for p in match.group().split(','))
                for match in re.finditer('[-.\d,]+', self.paths[0].get('d'))]
