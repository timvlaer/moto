from __future__ import unicode_literals
import time
import uuid

from .utils import make_arn_for_job, make_arn_for_queue

from boto3 import Session

from moto.core import BaseBackend, BaseModel

from moto.core import ACCOUNT_ID as DEFAULT_ACCOUNT_ID


class Job(BaseModel):
    def __init__(self, job_id, region_name, queue=""):
        self.job_id = job_id
        self.arn = make_arn_for_job(DEFAULT_ACCOUNT_ID, job_id, region_name)
        self.created_at = str(int(round(time.time() * 1000)))
        self.queue = queue if queue != "" else make_arn_for_queue(DEFAULT_ACCOUNT_ID, "Default", region_name)

    def to_dict(self):
        return {
            "arn": self.arn,
            "id": self.job_id,
            "createdAt": self.created_at,
            "queue": self.queue,
        }

    def __repr__(self):
        return "<Job {0}>".format(self.job_id)


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
        job = Job(job_id, self.region_name)
        self._jobs[job_id] = job
        return job


mediaconvert_backends = {}
for region in Session().get_available_regions("mediaconvert"):
    mediaconvert_backends[region] = MediaConvertBackend(region)
for region in Session().get_available_regions("mediaconvert", partition_name="aws-us-gov"):
    mediaconvert_backends[region] = MediaConvertBackend(region)
for region in Session().get_available_regions("mediaconvert", partition_name="aws-cn"):
    mediaconvert_backends[region] = MediaConvertBackend(region)
