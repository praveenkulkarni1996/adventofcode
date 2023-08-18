load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
  name = "solve01",
  srcs = ["solve01.py"],
  args = ["$(location :data/01.txt)"],
  data = ['data/01.txt'],
)
