# PySpective
## About
You totallly wondering: "Who is this guy?" or "What is this?"

Welp, 1st question: "I'm a student who use free time for coding."

2nd question: "This is a simplified version of Google's Perspective API which is kinda easy to use."
## Installation
To install, use
```pip install PySpective```
## Example
```
from pyspective import pyspective

perspective = pyspective.PyspectiveAPI('Your-API-key')
print(perspective.score('hi'))
```