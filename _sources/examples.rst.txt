
Examples
========

This chapter showcases a selection of examples, each accompanied by the specific command line arguments used to generate the depicted maze. These examples are intended to inspire and guide you through creating various maze designs and configurations.

.. code-block:: console

    generate_maze.py -x 300 -y 300 -t 0.5 -e nw -e se -m w/3/1 -m nw/5 -m n/3/1 -m ne/5 -m e/3/1 -m se/5 -m s/3/1 -m sw/5 -b c/5 -b c/3/-6,0 -b c/3/6,0 -b c/3/0,-6 -b c/3/0,6 -f 2 -c ^m/w/3/1 -c ^m/nw/5 -c ^m/n/3/1 -c ^m/ne/5 -c ^m/e/3/1 -c ^m/se/5 -c ^m/s/3/1 -c ^m/sw/5

.. figure:: /images/example_1.svg
    :width: 100%

.. code-block:: console

    generate_maze.py -x 300 -y 100 -l 4 -t 2.5 -e w/10 -e e/10 -m w/3/10 -m e/3/10 -b nw/5 -b ne/5 -b se/5 -b sw/5

.. figure:: /images/example_2.svg
    :width: 100%

.. code-block:: console

    generate_maze.py -x 200 -y 300 --height-parity=none --width-parity=none -l 4 -t 0.5 -e nw -e n/0/x -e ne/0/x -e e/20/x -e se -e s/0/x -e sw/1/x -m sw/2/1 -b w/2x67 -b ne/30x20/-4,12 -b se/30x20/-4,-12 -b e/20x43

.. figure:: /images/example_3.svg
    :width: 400px

.. code-block:: console

    generate_maze.py -x 125 -y 255 -l 5.0 -t 2.5 -f 0,0,2,0 -c ^mn/s/3/3 -c ^ms/n/5/3 -e n/8 -m n/5/8 -c ^m/n/5/8 -e s/0/x -m s/3 -e s/-5,0/x -m s/3/-5,0 -e s/-10,0/x -m s/3/-10,0 -e s/5,0 -m s/3/5,0 -e s/10,0/x -m s/3/10,0 -c c/s/3/-10,0 -c c/s/3/-5,0 -c c/s/3 -c c/s/3/5,0 -c c/s/3/10,0

.. figure:: /images/example_4.svg
    :width: 300px

From the Documentation
----------------------

.. code-block:: console

    generate_maze.py -x 55 -y 55 -l 5 -t 0.4 -f 1

.. figure:: /images/example_cmd_thickness_2.svg
    :width: 275px

.. code-block:: console

    generate_maze.py -x 50 -y 50 -f 1 -e w -e c -e n/0/x -e e/0/x -e s/0/x -m c/3

.. figure:: /images/example_dead_end.svg
    :width: 250px

.. code-block:: console

    generate_maze.py -x 80 -y 80 --width-parity=even --height-parity=even -f 2 -m nw/3 -m ne/3 -m se/3 -m sw/3 -m w/2/1 -m n/2/1 -m e/2/1 -m s/2/1 -m c/4 -e nw/0/x -e ne/0 -e sw/0/x -e se/0/x -e c

.. figure:: /images/example_cmd_frame_2.svg
    :width: 400px

.. code-block:: console

   generate_maze.py -x 60 -y 60 -b c/7

.. figure:: /images/example_cmd_blank_1.svg
   :width: 300px

.. code-block:: console

   generate_maze.py -x 60 -y 60 -b nw/5 -b ne/5 -b se/5 -b sw/5

.. figure:: /images/example_cmd_blank_2.svg
   :width: 300px

.. code-block:: console

   generate_maze.py -x 80 -y 80 -c dh/w/4x17 -c dv/n/17x4 -c dh/e/4x17 -c dv/s/17x4 -b c/17 -e c/-8,0 -e c/8,0 -t 0.3 -l 3

.. figure:: /images/example_cmd_close_3.svg
    :width: 400px

.. code-block:: console

   generate_maze.py -x 60 -y 100 -f 0,0,2,0 -m s/3 -c ^mn/s/3/3 -m n/5/3 -c ^ms/n/5/3 -e n/3 -e s

.. figure:: /images/example_cmd_close_4.svg
    :width: 300px

.. code-block:: console

    generate_maze.py -x 84 -y 60 -e nw -e se -m w/3/1 -m nw/3 -m n/3/1 -m ne/3 -m e/3/1 -m se/3 -m s/3/1 -m sw/3 -b c/5 -f 1 -c ^m/w/3/1 -c ^m/nw/3 -c ^m/n/3/1 -c ^m/ne/3 -c ^m/e/3/1 -c ^m/se/3 -c ^m/s/3/1 -c ^m/sw/3

.. figure:: /images/example_cmd_merge_2.svg
    :width: 420px