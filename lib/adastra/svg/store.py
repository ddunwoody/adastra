from __future__ import division

from adastra.svg.Path import *
from adastra.svg.Svg import *
from lxml import etree
from lxml.etree import ElementTree 
import re

def load(path):
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
            path.fill = _hex_to_color(style.get('fill'))
            path.stroke = _hex_to_color(style.get('stroke'))

        path.label = element.get('{%s}label' % INKSCAPE_NS)
        path.id = element.get('id')

        svg.paths.append(path)
    return svg

def save(svg, file):
    root = etree.Element('svg', nsmap={'inkscape': 'http://www.inkscape.org/namespaces/inkscape'})
    parent = root
    root.set('width', str(int(svg.size[0])))
    root.set('height', str(int(svg.size[1])))

    transform = ''
    if svg.scale != 1:
        transform = 'scale(%.1f)' % svg.scale
    if svg.translate != (0, 0):
        transform += ' translate(%s)' % _tuple_to_str(svg.translate)
    if len(transform) > 0:
        element = etree.Element('g')
        root.append(element)
        element.set('transform', transform.strip())
        parent = element
    
    for path in svg.paths:
        element = etree.Element('path')
        parent.append(element)

        element.set('d', 'M ' + ' L '.join(map(_tuple_to_str, path.points)) + ' z')

        style = {}
        if path.fill:
            style['fill'] = _color_to_hex(path.fill)
        if path.stroke:
            style['stroke'] = _color_to_hex(path.stroke)
        if len(style) > 0:
            element.set('style', ';'.join([':'.join(kv) for kv in style.items()]))

        if path.label:
            element.set('{http://www.inkscape.org/namespaces/inkscape}label', path.label)
        if path.id:
            element.set('id', path.id)
            
        
    ElementTree(root).write(file, pretty_print=True)
    
def _tuple_to_str(t):
    return "%.f,%.f" % (t[0], t[1])

def _hex_to_color(hex):
    if hex is None:
        return None
    return int(hex[1:3], 16) / 255, int(hex[3:5], 16) / 255, int(hex[5:7], 16) / 255

def _color_to_hex(color):
    def mul(x): return x * 255
    return "#%02X%02X%02X" % tuple(map(mul, color))


