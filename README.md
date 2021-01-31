# Mesa-visualization-SFL
This is a visualization tool for social computing researchers




## Summary

This model is meant to modeling the complex contagion spreading of information based on the virus on a Netwotk example provided by Mesa. It is intended to provide a framework for understanding misinformation flow on a network, based very strongly on the models of complex contagion designed by Centola and Macy (2007).

JavaScript library used in this example to render the network: [d3.js].

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

~~ ```
~~     $ pip install -r requirements.txt
~~ ```

## How to Run

To run the model interactively, run `mesa runserver` in this directory. e.g.

~~ ```
~~     $ mesa runserver
~~ ```

Then open your browser to [http://127.0.0.1:8521/] and press Reset, then Run.

## Files

* `run.py`: Launches a model visualization server.
* `model.py`: Contains the agent class, and the overall model class.
* `server.py`: Defines classes for visualizing the model (network layout) in the browser via Mesa's modular server, and instantiates a visualization server.
* `batchrun.py`: batch run all the modeling with range of input and 
