from __future__ import division

from adastra.svg.Group import *
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

    # Parse top-level transform
    for element in xpath('/svg/g'):
        if 'transform' in element.keys():
            match = re.search('scale\(([-\d.]+)\)', element.get('transform'))
            if match is not None:
                svg.scale = float(match.group(1))
            match = re.search('translate\(([-\d., ]+)\)', element.get('transform'))
            if match is not None:
                svg.translate = tuple(float(x) for x in match.group(1).split(','))

    # Parse each group
    for g in xpath('/svg/g/g'):
        group = Group()
        svg.groups[g.get('id')] = group

        # Parse each path in group
        for path_elem in g.getiterator('path'):
            path = Path(points=[tuple(float(p) for p in match.group().split(','))
                                for match in re.finditer('[-.\d,]+', path_elem.get('d'))])
            if path.points[-1] == path.points[0]:
                path.points.pop()
    
            if 'style' in path_elem.keys():
                style = _unpack(path_elem.get('style'))
                path.fill = _hex_to_color(style.get('fill'))
                path.stroke = _hex_to_color(style.get('stroke'))
    
            label = path_elem.get('{%s}label' % INKSCAPE_NS)
            if label is not None:
                path.data = _unpack(label)

            path.id = path_elem.get('id')
    
            group.paths.append(path)

    return svg

def save(svg, file):
    root = etree.Element('svg', nsmap={'inkscape': 'http://www.inkscape.org/namespaces/inkscape'})
    root.set('width', str(int(svg.size[0])))
    root.set('height', str(int(svg.size[1])))

    transform = ''
    if svg.scale != 1:
        transform = 'scale(%.1f)' % svg.scale
    if svg.translate != (0, 0):
        transform += ' translate(%s)' % _tuple_to_str(svg.translate)
    if len(transform) > 0:
        transform_group = etree.Element('g')
        root.append(transform_group)
        transform_group.set('transform', transform.strip())
    
    for group_id, group in svg.groups.items():
        group_elem = etree.Element('g')
        transform_group.append(group_elem)
        group_elem.set('id', group_id)
        for path in group.paths:
            path_elem = etree.Element('path')
            group_elem.append(path_elem)
    
            path_elem.set('d', 'M ' + ' L '.join(map(_tuple_to_str, path.points)) + ' z')
    
            style = {}
            if path.fill:
                style['fill'] = _color_to_hex(path.fill)
            if path.stroke:
                style['stroke'] = _color_to_hex(path.stroke)
            if len(style) > 0:
                path_elem.set('style', _pack(style))
    
            if path.data:
                path_elem.set('{http://www.inkscape.org/namespaces/inkscape}label', _pack(path.data))
            if path.id:
                path_elem.set('id', path.id)
            
        
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

def _unpack(data):
    return dict(kv.split(':') for kv in data.split(';'))

def _pack(data):
    return ';'.join([':'.join(kv) for kv in data.items()])
