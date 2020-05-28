from __future__ import unicode_literals
import time
import uuid

from .utils import make_arn_for_job

from boto3 import Session

from moto.core import BaseBackend

from moto.core import ACCOUNT_ID as DEFAULT_ACCOUNT_ID


class MediaConvertBackend(BaseBackend):
    def __init__(self, region_name=None):
        super(MediaConvertBackend, self).__init__()
        self.region_name = region_name

        self._jobs = {}

    def reset(self):
        region_name = self.region_name
        self.__dict__ = {}
        self.__init__(region_name)

    def put_job(self, body):
        job_id = str(uuid.uuid4())
        job = {
            "job": {
                "arn": make_arn_for_job(DEFAULT_ACCOUNT_ID, job_id, self.region_name),
                "id": job_id,
                "createdAt": str(int(round(time.time() * 1000)))
            }
        }
        self._jobs.update(jobId=job)
        return job


mediaconvert_backends = {}
for region in Session().get_available_regions("mediaconvert"):
    mediaconvert_backends[region] = MediaConvertBackend(region)
for region in Session().get_available_regions("mediaconvert", partition_name="aws-us-gov"):
    mediaconvert_backends[region] = MediaConvertBackend(region)
for region in Session().get_available_regions("mediaconvert", partition_name="aws-cn"):
    mediaconvert_backends[region] = MediaConvertBackend(region)
