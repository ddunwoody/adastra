from adastra.svg.Path import *
from adastra.svg.Svg import *
from lxml import etree
import re

def load_svg(path):
    tree = etree.parse(path)
    xpath = etree.XPathEvaluator(tree)

    svg = Svg()
    svg.size = float(tree.getroot().attrib['width']), float(tree.getroot().attrib['height'])

    for element in xpath('//circle'):
        svg.reference_point = float(element.get('cx')), float(element.get('cy'))

    for element in xpath('//path'):
        path = Path()
        path.points = [tuple(float(p) for p in match.group().split(','))
                       for match in re.finditer('[-.\d,]+', element.get('d'))]

        if element.attrib.has_key('style'):
            style = dict(kv.split(':') for kv in element.get('style').split(';'))
            if style.has_key('fill'):
                path.fill = style['fill']
            if style.has_key('stroke'):
                path.stroke = style['stroke']

        svg.paths.append(path)
    return svg
