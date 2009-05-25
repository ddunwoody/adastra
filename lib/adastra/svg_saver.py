from lxml import etree
from lxml.etree import ElementTree 

def save_svg(svg, file):
    root = etree.Element('svg', nsmap={'inkscape': 'http://www.inkscape.org/namespaces/inkscape'})
    parent = root
    root.set('width', str(int(svg.size[0])))
    root.set('height', str(int(svg.size[1])))

    transform = ''
    if svg.scale != 1:
        transform = 'scale(%.1f)' % svg.scale
    if svg.translate != (0, 0):
        transform += ' translate(%s)' % tuple_to_str(svg.translate)
    if len(transform) > 0:
        element = etree.Element('g')
        root.append(element)
        element.set('transform', transform.strip())
        parent = element
    
    for path in svg.paths:
        element = etree.Element('path')
        parent.append(element)

        element.set('d', 'M ' + ' L '.join(map(tuple_to_str, path.points)) + ' z')

        style = {}
        if path.fill:
            style['fill'] = parse_color(path.fill)
        if path.stroke:
            style['stroke'] = parse_color(path.stroke)
        if len(style) > 0:
            element.set('style', ';'.join([':'.join(kv) for kv in style.items()]))

        if path.label:
            element.set('{http://www.inkscape.org/namespaces/inkscape}label', path.label)
        if path.id:
            element.set('id', path.id)
            
        
    ElementTree(root).write(file)
    
def tuple_to_str(t):
    return "%.f,%.f" % (t[0], t[1])

def parse_color(color):
    def mul(x): return x * 255
    return "#%02X%02X%02X" % tuple(map(mul, color))
