

# setup the keys

there are two approaches to setup the keys:

- use mise to setup the keys
    - this is ideal, as allows you to have .mise.test.toml, .mise.prod.toml, etc where each keys are stored
- edit the rxconfig.toml to pass in the keys
    - this is not ideal, as you have to remember to not commit the keys
