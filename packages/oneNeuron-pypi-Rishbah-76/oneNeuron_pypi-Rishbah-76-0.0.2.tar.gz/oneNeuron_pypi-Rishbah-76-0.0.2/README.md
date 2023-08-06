# oneNeuron_pypi
oneNeuron_pypi | Perceptron Pypi Package

# How to Use this
```python
pip install oneNeuron-pypi-Rishbah-76
from oneNeuronPerceptron.Perceptron import Perceptron,all_utils

## get X and y and then use below commands
model = Perceptron(eta=eta, epochs=epochs)
model.fit(X, y)

#THis is from utils package
save_model(model,filename="and.model")
save_plot(df,"and.png",model)
```
# Referecnce -
[Official Python Package](https://packaging.python.org/tutorials/packaging-projects/)
[Github official Doc for Github actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)