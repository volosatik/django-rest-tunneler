from sshtunnel import SSHTunnelForwarder
from time import ctime, sleep
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


class TunnelDmz(metaclass=IterRegistry):
    _registry = []

    def __init__(self, scheduler, username, password, local_host, remote_host, private_host, port_list, remote_port=22, private_port=80, name=None):
        self._registry.append(self)
        self.name = name
        self.username = username
        self.password = password
        self.local_host = local_host

        self.remote_host = remote_host
        self.remote_port = remote_port
        self.private_host = private_host
        self.private_port = private_port
        self.tunnel = None
        self.started = datetime.now()
        self.ended = None

        self.scheduler = scheduler
        self.port_list = port_list
        if len(self.port_list) != 0:
            self.local_port = self.port_list.pop(0)

        else:
            pass
            #here should be exception
        self.desc = str(str(self.name)+ ' ' + str(self.local_port) + ' ' + str(self.private_host) + ' ' + str(self.private_port))

    def create(self):
        self.tunnel = SSHTunnelForwarder(
            (self.remote_host, self.remote_port),
            ssh_username=self.username,
            ssh_password=self.password,
    #            ssh_pkey ="MY_PKEY",
    #            ssh_private_key_password="secret",
            remote_bind_address=(self.private_host, self.private_port),
            local_bind_address=(self.local_host, self.local_port)
        )
        self.tunnel.start()
        print(ctime(), 'start!')
        print('should end on :', self.started + timedelta(minutes=5))
        print('started ', self.desc)
        self.scheduler.add_job(self.destruct, 'date', run_date=self.started + timedelta(minutes=5), id=self.desc)

    def return_uri(self):
        return 'http://'+str(self.local_host)+':'+str(self.local_port)

    def destruct(self):
        print(ctime(), 'finish!')
        # proveriat est' li job
        if self.scheduler.get_job(self.desc):
            self.scheduler.remove_job(self.desc)
        print('ended ', self.desc)
        self.tunnel.stop()
        self.port_list.append(self.local_port)
        self._registry.pop(self._registry.index(self))
        print("udalenie iz iteratora vizivaet destruktor? ya ebal")

    def __del__(self):
        print('closing: ', self.desc)




