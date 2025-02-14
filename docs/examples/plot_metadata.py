# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
Metadata
========

.. index:: metadata

ONNX format contains metadata related to how the
model was produced. It is useful when the model
is deployed to production to keep track of which
instance was used at a specific time.
Let's see how to do that with a simple
logistic regression model trained with
*scikit-learn* and converted with *onnxmltools*.
"""

import skl2onnx
import onnxruntime
import sklearn
import numpy
from onnxruntime import InferenceSession
import onnx
from onnxruntime.datasets import get_example

example = get_example("logreg_iris.onnx")

model = onnx.load(example)

print("doc_string={}".format(model.doc_string))
print("domain={}".format(model.domain))
print("ir_version={}".format(model.ir_version))
print("metadata_props={}".format(model.metadata_props))
print("model_version={}".format(model.model_version))
print("producer_name={}".format(model.producer_name))
print("producer_version={}".format(model.producer_version))

#############################
# With *ONNX Runtime*:

sess = InferenceSession(example)
meta = sess.get_modelmeta()

print("custom_metadata_map={}".format(meta.custom_metadata_map))
print("description={}".format(meta.description))
print("domain={}".format(meta.domain, meta.domain))
print("graph_name={}".format(meta.graph_name))
print("producer_name={}".format(meta.producer_name))
print("version={}".format(meta.version))

#################################
# **Versions used for this example**

print("numpy:", numpy.__version__)
print("scikit-learn:", sklearn.__version__)
print("onnx: ", onnx.__version__)
print("onnxruntime: ", onnxruntime.__version__)
print("skl2onnx: ", skl2onnx.__version__)
