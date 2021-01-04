LOCAL_MEDIA_ROOT = 'media/'
LOCAL_STATIC_ROOT = 'webs/static/'

LOCAL_DEBUG = True

LOGGER_PRINT = False

LOCAL_ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

import os

if os.name == 'nt':
    import platform

    OSGEO4W = r"C:\OSGeo4W"
    if '64' in platform.architecture()[0]:
        OSGEO4W += "64"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']
