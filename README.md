# 16.412 Final Project
## by Enrique Fernandez and James Paterson ##

This repository contains our final project for the MIT Course 16.412 Cognitive Robotics: pyPlanGenius (Spring 2013)

pyPlanGenius is a python library capable of generating total order plans from user input and then extracting partial order plans and displaying them using graphs.

pyPlanGenius can parse PDDL domain and problem files located in the top pddl folder.

In order to run pyPlanGenius, please run:

```
pyplangenius.py [-h] [pddl_domain] [pddl_problem]
```

and follow instructions.

Note that you only need to specify the pddl file names and not the complete location as the script considers that all pddl files are located in the top pddl folder.

More instructions about the algorithms and the code can be found in the [project report](FinalProject_report_JamesPaterson_EnriqueFernandez.pdf).


Enrique Fernández
James Paterson

![example](example_partial_order.png?raw=true)


