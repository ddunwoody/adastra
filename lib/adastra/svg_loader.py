from adastra.svg.Path import *
from adastra.svg.Svg import *
from lxml import etree
import re

def load_svg(path):
    tree = etree.parse(path)
    xpath = etree.XPathEvaluator(tree, namespaces={'svg': 'http://www.w3.org/2000/svg'})

    svg = Svg()

    root_attribs = tree.getroot().attrib
    if root_attribs.has_key('width') and root_attribs.has_key('height'):
        svg.size = float(root_attribs['width']), float(root_attribs['height'])

    for element in xpath('//svg:path'):
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
