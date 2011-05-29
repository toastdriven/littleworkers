import logging
import time
from Queue import Queue, Empty
import subprocess
import unittest
from littleworkers import Pool, NotEnoughWorkers


class FakeProcess(object):
    def __init__(self, *args, **kwargs):
        pass


class StdOutPool(Pool):
    def __init__(self, *args, **kwargs):
        super(StdOutPool, self).__init__(*args, **kwargs)
        self.collected_output = []
    
    def create_process(self, command):
        logging.debug("Starting process to handle command '%s'." % command)
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    
    def remove_from_pool(self, pid):
        self.collected_output.append(self.pool[pid].stdout.read())
        return super(StdOutPool, self).remove_from_pool(pid)


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


class BasicUsage(unittest.TestCase):
    def test_simple_usage(self):
        commands = [
            'ls',
        ]
        
        lil = Pool(workers=1)
        lil.run(commands)
        
        lil = Pool(workers=2)
        lil.run(commands)
        
        # Should raise an exception.
        self.assertRaises(NotEnoughWorkers, Pool, workers=0)
    
    def test_prepare_commands(self):
        lil = Pool(workers=2)
        
        commands = []
        lil.prepare_commands(commands)
        self.assertEqual(len(lil.commands), 0)
        
        commands = [
            'ls',
            'cd /tmp',
        ]
        lil.prepare_commands(commands)
        self.assertEqual(len(lil.commands), 2)
    
    def test_next_command(self):
        lil = Pool(workers=2)
        
        commands = [
            'ls',
            'cd /tmp',
        ]
        lil.prepare_commands(commands)
        
        cmd1 = lil.next_command()
        self.assertEqual(cmd1, 'ls')
        
        cmd2 = lil.next_command()
        self.assertEqual(cmd2, 'cd /tmp')
        
        cmd3 = lil.next_command()
        self.assertEqual(cmd3, None)

    def test_inspect_pool(self):
        lil = Pool(workers=1)
        self.assertEqual(lil.inspect_pool(), 0)
        
        ls_command = lil.create_process('sleep 1')
        lil.add_to_pool(ls_command)
        self.assertEqual(lil.inspect_pool(), 1)
        
        tmp_command = lil.create_process('sleep 1')
        lil.add_to_pool(tmp_command)
        self.assertEqual(lil.inspect_pool(), 2)
    
    def test_add_to_pool(self):
        lil = Pool(workers=2)
        
        ls_command = lil.create_process('ls')
        tmp_command = lil.create_process('cd /tmp')
        
        self.assertEqual(len(lil.pool), 0)
        
        lil.add_to_pool(ls_command)
        self.assertEqual(len(lil.pool), 1)
        
        lil.add_to_pool(tmp_command)
        self.assertEqual(len(lil.pool), 2)
    
    def test_remove_from_pool(self):
        lil = Pool(workers=2)
        lil.pool = {
            1: FakeProcess('fake'),
            2: FakeProcess('fake'),
        }
        # Fake more data.
        lil.pool[1].pid = 1
        lil.pool[2].pid = 2
        
        self.assertEqual(len(lil.pool), 2)
        
        lil.remove_from_pool(2)
        self.assertEqual(len(lil.pool), 1)
        
        lil.remove_from_pool(1)
        self.assertEqual(len(lil.pool), 0)
        
        lil.remove_from_pool(1)
        self.assertEqual(len(lil.pool), 0)

    def test_long_wait_time(self):
        lil = Pool(workers=1)
        start = time.time()
        lil.run(['ls'])
        end = time.time()
        self.assertTrue(end - start < 1.0)
        
        # Now with a longer wait.
        lil = Pool(workers=1, wait_time=1.25)
        start = time.time()
        lil.run(['ls'])
        end = time.time()
        self.assertTrue(end - start > 1.0)

    def test_process_kwargs(self):
        lil = Pool(workers=1)
        self.assertEqual(lil.process_kwargs(None), {'shell': True})
        self.assertEqual(lil.process_kwargs('ls -al'), {'shell': True})


class StdOutUsage(unittest.TestCase):
    def test_usage(self):
        commands = [
            'ulimit -n',
            'uname -a',
        ]
        
        lil = StdOutPool(workers=2)
        lil.run(commands)
        
        self.assertEqual(set(lil.collected_output), set(['256\n', 'Darwin Europa.local 10.7.0 Darwin Kernel Version 10.7.0: Sat Jan 29 15:17:16 PST 2011; root:xnu-1504.9.37~1/RELEASE_I386 i386\n']))


class QueueUsage(unittest.TestCase):
    def test_usage(self):
        commands = [
            'ls',
            'cd /tmp',
        ]
        
        lil = QueuePool(workers=2)
        lil.prepare_commands(commands)
        self.assertTrue(isinstance(lil.commands, Queue))
        self.assertEqual(lil.commands.qsize(), 2)
        
        lil.run()
        self.assertEqual(lil.commands.qsize(), 0)
    
