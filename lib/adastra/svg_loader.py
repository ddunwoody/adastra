from adastra.svg.Path import *
from lxml import etree
import re

def load_svg(path):
    svg = etree.parse(path)
    find = etree.ETXPath('//path')
    elements = find(svg)

    paths = []
    for element in elements:
        path = Path()
        path.points = [tuple(float(p) for p in match.group().split(','))
                       for match in re.finditer('[-.\d,]+', element.get('d'))]
        if element.attrib.has_key('style'):
            style = dict(kv.split(':') for kv in element.get('style').split(';'))
            if style.has_key('fill'):
                path.fill = style['fill']
            if style.has_key('stroke'):
                path.stroke = style['stroke']
        paths.append(path)
    return paths
