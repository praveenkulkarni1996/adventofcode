load("@rules_python//python:defs.bzl", "py_binary")
load("@pypi//:requirements.bzl", "requirement")

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

py_binary(
  name = "solve03",
  srcs = ["solve03.py"],
  args = ["$(location :data/03.txt)"],
  data = ['data/03.txt'],
)

py_binary(
  name = "solve04",
  srcs = ["solve04.py"],
  args = ["$(location :data/04.txt)"],
  data = ['data/04.txt'],
  deps = [
    requirement("more-itertools"),
  ]
)
py_binary(
  name = "solve05",
  srcs = ["solve05.py"],
  args = ["$(location :data/05.txt)"],
  data = ['data/05.txt'],
)