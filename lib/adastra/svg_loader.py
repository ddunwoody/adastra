from adastra.Path import *
from lxml import etree
import re

def load_svg(path):
    svg = etree.parse(path)
    find = etree.ETXPath('//path')
    element = find(svg)[0]

    path = Path()
    path.points = [tuple(float(p) for p in match.group().split(','))
                   for match in re.finditer('[-.\d,]+', element.get('d'))]
    if element.attrib.has_key('style'):
        style = dict(kv.split(':') for kv in element.get('style').split(';'))
        if style.has_key('fill'):
            path.fill = style['fill']
        if style.has_key('stroke'):
            path.stroke = style['stroke']
    return path
