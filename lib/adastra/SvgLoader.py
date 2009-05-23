from adastra.Path import *
from lxml import etree
import re

class SvgLoader(object):
    def __init__(self, path):
        svg = etree.parse(path)
        find = etree.ETXPath('//path')
        self.path = find(svg)[0]

    def parse(self):
        path = Path()
        path.points = [tuple(float(p) for p in match.group().split(','))
                       for match in re.finditer('[-.\d,]+', self.path.get('d'))]
        if self.path.attrib.has_key('style'):
            style = dict(kv.split(':') for kv in self.path.get('style').split(';'))
            if style.has_key('fill'):
                path.fill = style['fill']
            if style.has_key('stroke'):
                path.stroke = style['stroke']
        return path
