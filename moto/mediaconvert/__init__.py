from __future__ import unicode_literals
from .models import mediaconvert_backends
from ..core.models import base_decorator

mediaconvert_backend = mediaconvert_backends["us-east-1"]
mock_mediaconvert = base_decorator(mediaconvert_backends)
