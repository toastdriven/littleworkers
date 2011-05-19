import subprocess
import unittest
from littleworkers import Pool, NotEnoughWorkers


class FakeProcess(object):
    def __init__(self, *args, **kwargs):
        pass


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
    