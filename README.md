# setup the keys

there are two approaches to setup the keys:

- use mise to setup the keys
  - this is ideal, as allows you to have .mise.test.toml, .mise.prod.toml, etc where each keys are stored
- edit the rxconfig.toml to pass in the keys
  - this is not ideal, as you have to remember to not commit the keys

# admin dashboard

the admin dashboard requires installing starlette-admin. this is not included in the reflex package, so you need to install it manually.

```
pip install starlette-admin
```

# docs

docs are currently in the `docs` folder above the root of this project. as this project is currently private, to allow for github pages to serve they will need to be a public project.

for what i want, i would like to have the docs basically be a part of the actual code base (similar to the huggingface transformer docs)

can probably just use something like a submodule or subtree to keep the docs in this repo but moving out for now is fine.

# Routes

## Admin

The admin dashboard that is built into reflex is available on the backend at '/admin'. On the dev deployment this can be accessed at 'http://localhost:8000/admin'

# Development

## Debugging

previously you could use the breakpoint() function to debug the code. now, this requires using `REFLEX_USE_GRANIAN=0`

# deployment

`pip install -e ./packages/rxext` fails by referring to the git url, better just to stick with uv for everything as seems to work with reflex at this point
