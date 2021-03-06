from lucy.models import LucyObject
from lucy.models.user import User
import datetime as dt


class Machine(LucyObject):
    _type = 'machines'

    def __init__(self, _id, owner, auth, last_ping=None, **kwargs):
        owner = User.load(owner)['_id']

        super(Machine, self).__init__(_id=_id,
                                      owner=owner,
                                      auth=auth,
                                      last_ping=last_ping,
                                      **kwargs)

    def auth(self, auth):
        return self['auth'] == auth

    @classmethod
    def get_by_key(cls, key):
        return cls.single({"gpg": key})

    def get_owner(self):
        return User.load(self['owner'])

    def ping(self):
        self['last_ping'] = dt.datetime.utcnow()
        self.save()

    def get_jobs(self):
        from lucy.models.job import Job
        return Job.assigned_jobs(self['_id'])

    @classmethod
    def get_builders(cls):
        return cls.query({})
