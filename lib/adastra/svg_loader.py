from __future__ import division

from adastra.svg.Path import *
from adastra.svg.Svg import *
from lxml import etree
import re

def load_svg(path):
    INKSCAPE_NS = 'http://www.inkscape.org/namespaces/inkscape'

    tree = etree.parse(path)
    xpath = etree.XPathEvaluator(tree)

    svg = Svg()
    svg.size = float(tree.getroot().attrib['width']), float(tree.getroot().attrib['height'])

    for element in xpath('/svg/g'):
        if 'transform' in element.keys():
            match = re.search('scale\(([-\d.]+)\)', element.get('transform'))
            if match is not None:
                svg.scale = float(match.group(1))
            match = re.search('translate\(([-\d., ]+)\)', element.get('transform'))
            if match is not None:
                svg.translate = tuple(float(x) for x in match.group(1).split(','))

    for element in xpath('//circle'):
        svg.reference_point = float(element.get('cx')), float(element.get('cy'))

    for element in xpath('//path'):
        path = Path(points=[tuple(float(p) for p in match.group().split(','))
                            for match in re.finditer('[-.\d,]+', element.get('d'))])

        if 'style' in element.keys():
            style = dict(kv.split(':') for kv in element.get('style').split(';'))
            path.fill = parse_color(style.get('fill'))
            path.stroke = parse_color(style.get('stroke'))

        path.label = element.get('{%s}label' % INKSCAPE_NS)
        path.id = element.get('id')

        svg.paths.append(path)
    return svg

def parse_color(color):
    if color is None:
        return None
    return int(color[1:3], 16) / 255, int(color[3:5], 16) / 255, int(color[5:7], 16) / 255
