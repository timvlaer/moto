from __future__ import unicode_literals

import json
import uuid

from six.moves.urllib.parse import urlsplit

from moto.core.responses import BaseResponse
from .models import mediaconvert_backends
from moto.sqs import sqs_backends

from moto.core import ACCOUNT_ID as DEFAULT_ACCOUNT_ID

MEDIACONVERT_UPDATES_QUEUE_NAME = "mediaconvert_updates"


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

        sqs_backend = sqs_backends[self.region]
        sqs_backend.create_queue(MEDIACONVERT_UPDATES_QUEUE_NAME)
        sqs_backend.send_message(MEDIACONVERT_UPDATES_QUEUE_NAME, json.dumps(self.create_state_change_msg(job)))

        return json.dumps({"job": job.to_dict()})

    def create_state_change_msg(self, job):
        return {
            "version": "0",
            "id": str(uuid.uuid4()),
            "detail-type": "MediaConvert Job State Change",
            "source": "aws.mediaconvert",
            "account": DEFAULT_ACCOUNT_ID,
            "time": "2020-05-12T18:21:14Z",
            "region": self.region,
            "resources": [job.arn],
            "detail": {
                "timestamp": 1589307674522,
                "accountId": "145599358451",
                "queue": job.queue,
                "jobId": job.job_id,
                "status": "COMPLETE",
                "userMetadata": {},
                "outputGroupDetails": [
                    {
                        "outputDetails": [
                            {
                                "outputFilePaths": [
                                    "s3://mediaconvert-processed-content/sample-hi-res.m3u8"
                                ],
                                "durationInMs": 18084,
                                "videoDetails": {
                                    "widthInPx": 1280,
                                    "heightInPx": 720
                                }
                            }
                        ],
                        "playlistFilePaths": [
                            "s3://mediaconvert-processed-content/sample.m3u8"
                        ],
                        "type": "HLS_GROUP"
                    }
                ]
            }
        }
