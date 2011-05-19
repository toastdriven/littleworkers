import logging
import os
import subprocess
import time


__author__ = 'Daniel Lindsley'
__version__ = (0, 1, 0)
__license__ = 'BSD'


class LittleWorkersException(Exception):
    pass


class NotEnoughWorkers(LittleWorkersException):
    pass


class Pool(object):
    def __init__(self, workers=1, debug=False):
        if workers < 1:
            raise NotEnoughWorkers("You need to use at least one worker.")
        
        self.workers = workers
        self.pool = {}
        self.commands = []
        self.debug = debug
    
    def prepare_commands(self, commands):
        self.commands = commands
    
    def next_command(self):
        try:
            return self.commands.pop(0)
        except IndexError:
            if self.debug:
                raise
        
        return None
    
    def create_process(self, command):
        logging.debug("Starting process to handle command '%s'." % command)
        return subprocess.Popen(command, shell=True)
    
    def add_to_pool(self, proc):
        logging.debug("Adding %s to the pool." % proc.pid)
        self.pool[proc.pid] = proc
    
    def remove_from_pool(self, pid):
        try:
            logging.debug("Removing %s from the pool" % pid)
            del(self.pool[pid])
        except KeyError:
            if self.debug:
                raise
    
    def inspect_pool(self):
        logging.debug("Current pool size: %s" % len(self.pool))
    
    def busy_wait(self):
        time.sleep(0.1)
    
    def run(self, commands=None):
        if commands is not None:
            self.prepare_commands(commands)
        
        while len(self.commands):
            self.inspect_pool()
            
            if len(self.pool) <= min(self.commands, self.workers):
                command = self.next_command()
                proc = self.create_process(command)
                self.add_to_pool(proc)
            
            # Go in reverse order so offsets never get screwed up.
            for pid in self.pool.keys():
                logging.debug("Checking status on %s" % self.pool[pid].pid)
                
                if self.pool[pid].poll() >= 0:
                    self.remove_from_pool(pid)
            
            self.busy_wait()


if __name__ == "__main__":
    commands = [
        'ls -al',
        'cd /tmp && mkdir foo',
        'date',
        'echo "Hello There."',
        'sleep 2 && echo "Done."'
    ]
    lil = Pool(workers=2)
    lil.run(commands)
