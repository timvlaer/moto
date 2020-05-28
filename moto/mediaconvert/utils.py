from __future__ import unicode_literals


def make_arn_for_job(account_id, job_id, region_name):
    return "arn:aws:mediaconvert:{0}:{1}:jobs/{2}".format(region_name, account_id, job_id)
