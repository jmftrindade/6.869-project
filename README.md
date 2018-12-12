## Automatic Summarization for Neural Net Interpretability
Class project for Fall 2017's edition of [MIT's 6.869: Advances in Computer Vision](http://6.869.csail.mit.edu/fa17/).

The goal here was to experiment with the idea of aggressively summarizing activations for each layer, and see what sort of information you can still recover from what the neural network has learned.  E.g., if you cluster images by layer activations, where each dimension is represented by an agressively summarized activation unit (=avg/max/min of all activations in the unit), are final clusters still cohesive? And can this help you identify reasons why examples might've been incorrectly misclassified?

## TODO
- [ ] Add some documentation on project structure, e.g., how to run the scripts.
- [ ] Add link to rendered PDF of the report.

# Requirements

Python packages:
```
$ pip install -r requirements.txt
```

# External modules

To update to latest version of dependencies, run:
```
$ git submodule update --init --recursive
```
