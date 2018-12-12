# 6.869-project
Course project for 6.869: automatic summarization for neural net interpretability

The goal here was to experiment with the idea of aggressively summarizing activations for each layer, and see what sort of information you may still recover from what was learned by the neural network.  E.g., if you cluster images by layer activations, where each dimension is represented by an agressively summarized activation unit (=avg/max/min of all activations in the unit), are final clusters still cohesive? And can this help you identify reasons why examples might've been incorrectly misclassified?

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
