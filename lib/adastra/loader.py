from lxml import etree

SVG_NS = 'http://www.w3.org/2000/svg'
SODIPODI_NS = 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'

def load_svg(path, scale=0.1):
    svg = etree.parse(path)
    find = etree.ETXPath('//{%s}path[@id="ref_point"]' % SVG_NS)
    element = find(svg)[0]
    ref_point = float(element.get('{%s}cx' % SODIPODI_NS)), float(element.get('{%s}cy' % SODIPODI_NS))
    print ref_point
