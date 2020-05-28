from __future__ import unicode_literals
from .responses import MediaConvertResponse

url_bases = ["https?://mediaconvert.(.+).amazonaws.com"]

url_paths = {
    "{0}/2017-08-29/endpoints": MediaConvertResponse.dispatch,
    "{0}/2017-08-29/jobs": MediaConvertResponse.dispatch,
}
