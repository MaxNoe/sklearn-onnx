"""
Tests examples from the documentation.
"""
import unittest
import os
import sys
import importlib
import subprocess


def import_source(module_file_path, module_name):
    if not os.path.exists(module_file_path):
        raise FileNotFoundError(module_file_path)
    module_spec = importlib.util.spec_from_file_location(
        module_name, module_file_path)
    if module_spec is None:
        raise FileNotFoundError(
            "Unable to find '{}' in '{}'.".format(
                module_name, module_file_path))
    module = importlib.util.module_from_spec(module_spec)
    return module_spec.loader.exec_module(module)


class TestDocumentationExample(unittest.TestCase):

    def test_documentation_examples(self):

        this = os.path.abspath(os.path.dirname(__file__))
        fold = os.path.normpath(os.path.join(this, '..', 'examples'))
        found = os.listdir(fold)
        tested = 0
        for name in found:
            if name.startswith("plot_") and name.endswith(".py"):
                print("run %r" % name)
                try:
                    mod = import_source(fold, os.path.splitext(name)[0])
                    assert mod is not None
                except FileNotFoundError:
                    # try another way
                    p = subprocess.Popen(
                        [sys.executable, "-u",
                            os.path.join(fold, name)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
                    res = p.communicate()
                    out, err = res
                    st = err.decode('ascii', errors='ignore')
                    if len(st) > 0 and 'Traceback' in st:
                        if "No such file or directory: 'dot': 'dot'" in st:
                            # dot not installed, this part
                            # is tested in onnx framework
                            pass
                        elif '"dot" not found in path.' in st:
                            # dot not installed, this part
                            # is tested in onnx framework
                            pass
                        else:
                            raise RuntimeError(
                                "Example '{}' failed due to\n{}"
                                "".format(name, st))
                tested += 1
        if tested == 0:
            raise RuntimeError("No example was tested.")


if __name__ == "__main__":
    unittest.main()
