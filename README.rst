=============
littleworkers
=============

Little process-based workers to do your bidding.

Deliberately minimalist, you provide the number of ``workers`` to use &
a list of commands (to be executed at the shell) & ``littleworkers`` will eat
through the list as fast as it can.


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


Requirements
============

Python 2.6+


:author: Daniel Lindsley
:updated: 2011/05/19
:version: 0.1
:license: BSD