import logging
import os
import subprocess
import time


__author__ = 'Daniel Lindsley'
__version__ = (0, 1, 1)
__license__ = 'BSD'


class LittleWorkersException(Exception):
    pass


class NotEnoughWorkers(LittleWorkersException):
    pass


class Pool(object):
    """
    The main pool object. Manages a set of specified workers.
    
    Usage::
    
        commands = [
            'ls -al',
            'cd /tmp && mkdir foo',
            'date',
            'echo "Hello There."',
            'sleep 2 && echo "Done."'
        ]
        lil = Pool(workers=2)
        lil.run(commands)
    
    Optionally accepts a ``workers`` kwarg. Default is 1.
    
    Optionally accepts a ``debug`` kwarg. Default is False.
    """
    def __init__(self, workers=1, debug=False):
        if workers < 1:
            raise NotEnoughWorkers("You need to use at least one worker.")
        
        self.workers = workers
        self.pool = {}
        self.commands = []
        self.debug = debug
    
    def prepare_commands(self, commands):
        """
        A hook to override how the commands are added.
        
        By default, simply copies the provided command ``list`` to the
        internal ``commands`` list.
        """
        # Make a copy of the commands to run.
        self.commands = commands[:]
    
    def command_count(self):
        """
        Returns the number of commands to be run.
        
        Useful as a hook if you use a different structure for the commands.
        """
        return len(self.commands)
    
    def next_command(self):
        """
        Fetches the next command for processing.
        
        Will return ``None`` if there are no commands remaining (unless
        ``Pool.debug = True``).
        """
        try:
            return self.commands.pop(0)
        except IndexError:
            if self.debug:
                raise
        
        return None
    
    def create_process(self, command):
        """
        Given a provided command (string or list), creates a new process
        to execute the command.
        """
        logging.debug("Starting process to handle command '%s'." % command)
        return subprocess.Popen(command, shell=True)
    
    def add_to_pool(self, proc):
        """
        Adds a process to the pool.
        """
        logging.debug("Adding %s to the pool." % proc.pid)
        self.pool[proc.pid] = proc
    
    def remove_from_pool(self, pid):
        """
        Removes a process to the pool.
        
        Fails silently if the process id is no longer present (unless
        ``Pool.debug = True``).
        """
        try:
            logging.debug("Removing %s from the pool" % pid)
            del(self.pool[pid])
        except KeyError:
            if self.debug:
                raise
    
    def inspect_pool(self):
        """
        A hook for inspecting the pool's current status.
        
        By default, simply makes a log message.
        """
        logging.debug("Current pool size: %s" % len(self.pool))
    
    def busy_wait(self):
        """
        A hook to control how often the busy-wait loop runs.
        
        By default, sleeps for 0.1 seconds.
        """
        time.sleep(0.1)
    
    def run(self, commands=None):
        """
        The method to actually execute all the commands with the pool.
        
        Optionally accepts a ``commands`` kwarg, as a shortcut not to have to
        call ``Pool.prepare_commands``.
        """
        if commands is not None:
            self.prepare_commands(commands)
        
        keep_running = True
        
        while keep_running:
            self.inspect_pool()
            
            if len(self.pool) <= min(self.command_count(), self.workers):
                command = self.next_command()
                
                if not command:
                    self.busy_wait()
                    continue
                
                proc = self.create_process(command)
                self.add_to_pool(proc)
            
            # Go in reverse order so offsets never get screwed up.
            for pid in self.pool.keys():
                logging.debug("Checking status on %s" % self.pool[pid].pid)
                
                if self.pool[pid].poll() >= 0:
                    self.remove_from_pool(pid)
            
            keep_running = self.command_count() or len(self.pool) > 0
            self.busy_wait()
