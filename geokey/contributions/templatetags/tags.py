from django import template

from osgeo import ogr

register = template.Library()

@register.filter(name='kml_geom')
def kml_geom(place):
    geojson_geom = place.get('location').get('geometry')
    json_geom = ogr.CreateGeometryFromJson(str(geojson_geom))
    kml_geom = json_geom.ExportToKML()
    return kml_geom

@register.filter(name='kml_name')
def kml_name(place):
    geojson_name = place.get('display_field').get('value')
    return geojson_name

@register.filter(name='kml_desc')
def kml_desc(place):
    geojson_properties = place.get('properties')
    geojson_desc = '<![CDATA[<table>'

    for key in geojson_properties:
        if geojson_properties[key] is not None:
            geojson_desc = geojson_desc + '<tr><td>{key}</td><td>{value}</td></tr>'.format(
                key=key,
                value=geojson_properties[key]
            )

    geojson_desc = geojson_desc + '</table>]]>'

    return geojson_desc

@register.filter(name='kml_style')
def kml_style(place):
    geojson_colour = place.get('meta').get('category').get('colour')
    geojson_colour = geojson_colour.replace('#','')
    return geojson_colour
