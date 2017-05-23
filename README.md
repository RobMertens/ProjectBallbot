# ProjectBallbot
This project contains code for the course integrated project (KULeuven).

The _authors_ of this project are:

* Rob Mertens <rob.mertens@student.kuleuven.be>

* Ibe Denaux <ibe.denaux@student.kuleuven.be>

We would like to say thank you to the project supervisor Maarten Verbandt and omg-tools expert Ruben Van Parys.

## Short description
_Given_: A ball-balancing robot <Ballbot> w/ attitude/velocity control already implemented.

_Task_: Implement a position controller based on a 2D-camera mounted on the roof. Coding in python.

_Modules_: The modules/packages available for this project are:

1. OMG-Tools: Spline based optimization for path planning.

2. Zyre/Pyre: An open-source framework for proximity-based peer-to-peer applications.

3. ProjectEagle: Image capturing and processing.

## Project status
Finished.

## Short description
A short discription for all files.

1. <main.py>

The main controller file. Must be runned on the Raspberry Pi 1B.

2. <external_pc.py>

The script for the external pc. It receives information about the process for logging and/or plotting.

3. <ballbot.py>

A general script for testing the ballbot. Given at start of the assignment.

4. <simulator.py> 

A script containing a simulation for the position control loop.

5. <eagle_receiver_test.py>

A test script for receiving information from the eagle-camera over the Zyre/Pyre API.

6. <omg_test.py>

A test script for omg-tools.

7. <pid_test.py>

A ballbot test script. Position control for a step error.

8. <whisper_transmitter.py> _and_ <whisper_receiver.py>

Two test scripts for sending and receiving whispers w/ the Pyre API.


