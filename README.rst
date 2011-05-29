=============
littleworkers
=============

Little process-based workers to do your bidding.

Deliberately minimalist, you provide the number of ``workers`` to use &
a list of commands (to be executed at the shell) & ``littleworkers`` will eat
through the list as fast as it can.


Why littleworkers?
==================

``littleworkers`` shines when you just want to parallelize something without a
lot of fuss & when you care more about the data/commands to be run.

* Tiny source
* Easy to queue a set of actions
* Works with any runnable commands
* Uses processes
* Non-blocking

Seriously, it's not a replacement for threading or multiprocessing if your
application needs to share a ton of data with the children.


Usage
=====

Usage is trivial::

    from littleworkers import Pool
    
    # Define your commands.
    commands = [
        'ls -al',
        'cd /tmp && mkdir foo',
        'date',
        'echo "Hello There."',
        'sleep 2 && echo "Done."'
    ]
    
    # Setup a pool. Since I have two cores, I'll use two workers.
    lil = Pool(workers=2)
    
    # Run!
    lil.run(commands)

You want the stdout back::

    import subprocess
    from littleworkers import Pool
    
    
    class MyPool(Pool):
        def __init__(self, *args, **kwargs):
            super(MyPool, self).__init__(*args, **kwargs)
            self.collected_output = []
        
        def create_process(self, command):
            logging.debug("Starting process to handle command '%s'." % command)
            return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        
        def remove_from_pool(self, pid):
            self.collected_output.append(self.pool[pid].stdout.read())
            return super(MyPool, self).remove_from_pool(pid)

You want to use a ``Queue`` instead of the default ``list``::

    from Queue import Queue, Empty
    from littleworkers import Pool
    
    
    class QueuePool(Pool):
        def __init__(self, *args, **kwargs):
            super(QueuePool, self).__init__(*args, **kwargs)
            self.commands = Queue()
        
        def prepare_commands(self, commands):
            for command in commands:
                self.commands.put(command)
        
        def command_count(self):
            return self.commands.qsize()
        
        def next_command(self):
            try:
                return self.commands.get()
            except Empty:
                return None

You want to setup a callback::

    from littleworkers import Pool
    
    codes = []
    
    def track(proc):
        codes.append("%s returned status %s" % (proc.pid, proc.returncode))
    
    commands = [
        'sleep 1',
        'busted_command --here',
        'sleep 1',
    ]
    lil.run(commands, callback=track)


Requirements
============

* Python 2.6+


:author: Daniel Lindsley
:updated: 2011/05/19
:version: 0.2.0
:license: BSD