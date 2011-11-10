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

For more advanced uses, please see the API documentation.


Requirements
============

* Python 2.6+


:author: Daniel Lindsley
:updated: 2011/11/10
:version: 0.3.1
:license: BSD
