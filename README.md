

# setup the keys

there are two approaches to setup the keys:

- use mise to setup the keys
    - this is ideal, as allows you to have .mise.test.toml, .mise.prod.toml, etc where each keys are stored
- edit the rxconfig.toml to pass in the keys
    - this is not ideal, as you have to remember to not commit the keys


# docs

docs are currently in the `docs` folder above the root of this project. as this project is currently private, to allow for github pages to serve they will need to be a public project.

for what i want, i would like to have the docs basically be a part of the actual code base (similar to the huggingface transformer docs)

can probably just use something like a submodule or subtree to keep the docs in this repo but moving out for now is fine.

