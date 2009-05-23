from __future__ import division

from adastra import config
from lxml import etree
import os

SVG_NS = 'http://www.w3.org/2000/svg'
INKSCAPE_NS = 'http://www.inkscape.org/namespaces/inkscape'

def get_ref_point(svg):
    find = etree.ETXPath('//{%s}path[@id="ref_point"]' % SVG_NS)
    element = find(svg)[0]
    d = element.get('d').split(' ')[1].split(',')
    return float(d[0]) - 5, float(d[1])

def get_shape_elements(svg, scale):
    ref_point = get_ref_point(svg)

    find = etree.ETXPath('//{%s}path[@id!="ref_point"]' % SVG_NS)
    elements = find(svg)

    def parse_path(points, scale):
        points = points.strip('Mz ')
        points = points.replace(',', ' ')
        points = points.split('L')
        points = [p.split()[-2:] for p in points]
        points = [((float(x) - ref_point[0]) * scale, (float(y) - ref_point[1]) * -scale) for x, y in points]
        if points[0] == points[-1]:
            points.pop()
        return points
    
    def get_color(style):
        def parse_kv(kv):
            k, v = kv.split(':')
            return k.strip(), v.strip()

        def parse_color(rgb):
            return int(rgb[1:3], 16) / 255, int(rgb[3:5], 16) / 255, int(rgb[5:7], 16) / 255
        
        data = dict(parse_kv(kv) for kv in style.split(';'))
        return parse_color(data['fill'])

    def parse(e):
        return {'id': e.get('id'), 'material': e.get('{%s}label' % INKSCAPE_NS),
                'path': parse_path(e.get('d'), scale), 'color': get_color(e.get('style'))}

    return map(parse, elements)

def load_svg(path, scale=0.1):
    svg = etree.parse(os.path.join(config.root, path))

    return get_shape_elements(svg, scale)