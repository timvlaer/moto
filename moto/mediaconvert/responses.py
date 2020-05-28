from __future__ import unicode_literals

import json

from six.moves.urllib.parse import urlsplit

from moto.core.responses import BaseResponse
from .models import mediaconvert_backends


class MediaConvertResponse(BaseResponse):
    @property
    def mediaconvert_backend(self):
        return mediaconvert_backends[self.region]

    @property
    def json(self):
        if not hasattr(self, "_json"):
            self._json = json.loads(self.body)
        return self._json

    def _error(self, code, message):
        return json.dumps({"__type": code, "message": message}), dict(status=400)

    def _get_action(self):
        # AWS MediaConvert api calls start with /2017-08-29
        url_parts = urlsplit(self.uri).path.lstrip("/").split("/")
        # [0] = '2017-08-29'

        return url_parts[1]

    # DescribeEndpoints
    def endpoints(self):
        next_token = self._get_param("NextToken")

        split_url = urlsplit(self.uri)
        return json.dumps({
            "endpoints": [
                {
                    "url": split_url.scheme + "://" + split_url.netloc
                }
            ]
        })

    def jobs(self):
        if self.method == "GET":
            # return job list
            pass
        elif self.method == "POST":
            # create job
            return self._create_job()

    def _create_job(self):
        job = self.mediaconvert_backend.put_job(self.json)
        return json.dumps(job)
