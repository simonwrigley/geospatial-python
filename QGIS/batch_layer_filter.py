# Useful script will 'batch' filter all layer in QGIS that are left visible, to a common attribute stating in layer.setSubsetString()

layers = iface.mapCanvas().layers()
for layer in layers:
    layer.setSubsetString('"floor_name" = \'2\'')
