# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
.. _l-errors-onnxruntime:

Errors with onnxruntime
=======================

Many mistakes might happen with *onnxruntime*.
This example looks into several common situations
in which *onnxruntime* does not return the model
prediction but raises an exception instead.
It starts by loading a model
(see :ref:`l-rf-iris-example`).
which produces a logistic regression
trained on *Iris* datasets. The model takes
a vector of dimension 2 and returns a class among three.
"""
import skl2onnx
import onnxruntime
import onnx
import sklearn
import onnxruntime as rt
import numpy
from onnxruntime.datasets import get_example

example2 = get_example("logreg_iris.onnx")
sess = rt.InferenceSession(example2)

input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name

#############################
# The first example fails due to *bad types*.
# *onnxruntime* only expects single floats (4 bytes)
# and cannot handle any other kind of floats.

try:
    x = numpy.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=numpy.float64)
    sess.run([output_name], {input_name: x})
except Exception as e:
    print("Unexpected type")
    print("{0}: {1}".format(type(e), e))

#########################
# The model fails to return an output if the name
# is misspelled.

try:
    x = numpy.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=numpy.float32)
    sess.run(["misspelled"], {input_name: x})
except Exception as e:
    print("Misspelled output name")
    print("{0}: {1}".format(type(e), e))

###########################
# The output name is optional, it can be replaced by *None*
# and *onnxruntime* will then return all the outputs.

x = numpy.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=numpy.float32)
res = sess.run(None, {input_name: x})
print("All outputs")
print(res)

#########################
# The same goes if the input name is misspelled.

try:
    x = numpy.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=numpy.float32)
    sess.run([output_name], {"misspelled": x})
except Exception as e:
    print("Misspelled input name")
    print("{0}: {1}".format(type(e), e))

#########################
# *onnxruntime* does not necessarily fail if the input
# dimension is a multiple of the expected input dimension.

for x in [
        numpy.array([1.0, 2.0, 3.0, 4.0], dtype=numpy.float32),
        numpy.array([[1.0, 2.0, 3.0, 4.0]], dtype=numpy.float32),
        numpy.array([[1.0, 2.0], [3.0, 4.0]], dtype=numpy.float32),
        numpy.array([1.0, 2.0, 3.0], dtype=numpy.float32),
        numpy.array([[1.0, 2.0, 3.0]], dtype=numpy.float32)]:
    try:
        r = sess.run([output_name], {input_name: x})
        print("Shape={0} and predicted labels={1}".format(x.shape, r))
    except RuntimeError as e:
        print("Shape={0} and error={1}".format(x.shape, e))

for x in [
        numpy.array([1.0, 2.0, 3.0, 4.0], dtype=numpy.float32),
        numpy.array([[1.0, 2.0, 3.0, 4.0]], dtype=numpy.float32),
        numpy.array([[1.0, 2.0], [3.0, 4.0]], dtype=numpy.float32),
        numpy.array([1.0, 2.0, 3.0], dtype=numpy.float32),
        numpy.array([[1.0, 2.0, 3.0]], dtype=numpy.float32)]:
    try:
        r = sess.run(None, {input_name: x})
        print("Shape={0} and predicted probabilities={1}".format(
            x.shape, r[1]))
    except RuntimeError as e:
        print("Shape={0} and error={1}".format(x.shape, e))

#########################
# It does not fail either if the number of dimension
# is higher than expects but produces a warning.

for x in [
        numpy.array([[[1.0, 2.0], [3.0, 4.0]]], dtype=numpy.float32),
        numpy.array([[[1.0, 2.0, 3.0]]], dtype=numpy.float32),
        numpy.array([[[1.0, 2.0]], [[3.0, 4.0]]], dtype=numpy.float32)]:
    try:
        r = sess.run([output_name], {input_name: x})
        print("Shape={0} and predicted labels={1}".format(x.shape, r))
    except RuntimeError as e:
        print("Shape={0} and error={1}".format(x.shape, e))

#################################
# **Versions used for this example**

print("numpy:", numpy.__version__)
print("scikit-learn:", sklearn.__version__)
print("onnx: ", onnx.__version__)
print("onnxruntime: ", onnxruntime.__version__)
print("skl2onnx: ", skl2onnx.__version__)
