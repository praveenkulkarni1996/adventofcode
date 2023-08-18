load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
  name = "solve01",
  srcs = ["solve01.py"],
  args = ["$(location :data/01.txt)"],
  data = ['data/01.txt'],
)

py_binary(
  name = "solve02",
  srcs = ["solve02.py"],
  args = ["$(location :data/02.txt)"],
  data = ['data/02.txt'],
)
