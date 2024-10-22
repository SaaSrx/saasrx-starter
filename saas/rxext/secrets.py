import os
from dataclasses import dataclass, field, fields, make_dataclass


@dataclass
class SecretConfig:
    @classmethod
    def from_env(cls, **kwargs):
        """
        Create an instance of the class using environment variables.

        This class method iterates over the fields of the class and checks if
        each field name exists in the environment variables. If a field name
        is found in the environment variables, its value is added to the
        keyword arguments. Finally, an instance of the class is created using
        the collected keyword arguments.

        Args:
            **kwargs: Additional keyword arguments to pass to the class
                    constructor.

        Returns:
            An instance of the class with values populated from environment
            variables and any additional keyword arguments.
        """
        for f in fields(cls):
            if f.name in os.environ:
                if f.name not in kwargs:
                    # only set if we dont pass in an override
                    kwargs[f.name] = os.environ[f.name]

        return cls(**kwargs)

    @classmethod
    def setup(cls, **kwargs):
        """
        Sets up the dataclass instance from environment variables.

        Use like:
        ```
        class Secrets(SecretConfig):
            key_name: str
            key_kwarg: str = "default"
        secrets = Secrets.setup(key_kwarg="override")
        ```

        Args:
            **kwargs: Arbitrary keyword arguments that can be passed to the dataclass.

        Returns:
            An instance of the dataclass populated with values from the environment variables.
        """

        # TODO: allow kwargs to get passed from elsewhere?
        return dataclass(cls).from_env(**kwargs)

    @classmethod
    def instance(cls, cls_base: type) -> type:
        """
        Sets up a new dataclass type based on the provided base class and returns an instance
        of that type populated with environment variables.

        Not sure I like this idea, but trying it out.  Can use like:
        ```
        @SecretConfig.instance
        class secrets:
            key_name: str

        assert (secrets.key_name == os.environ["key_name"]) && (secrets.__classs__.__name__ == "secrets")
        ```

        Args:
            cls_base (type): The base class to create the new dataclass type from.

        Returns:
            type: An instance of the newly created dataclass type populated with environment variables.

        The function performs the following steps:
        1. Defines an inner function `make` that creates a tuple containing the field name and type,
           and if the field name exists in the base class dictionary, it adds a default value.
        2. Uses `make_dataclass` to create a new dataclass type with the same name as the base class,
           including fields processed by the `make` function and inheriting from `SecretConfig`.
        3. Returns an instance of the newly created dataclass type populated with environment variables
           using the `from_env` method.
        """

        def make(f):
            out = (f.name, f.type)
            if f.name in cls_base.__dict__:
                out += (field(default=cls_base.__dict__[f.name]),)
            return out

        cls_type = make_dataclass(
            cls_base.__name__,
            [make(f) for f in fields(dataclass(cls_base))],
            bases=(SecretConfig, cls_base),
        )

        inst = cls_type.from_env()
        return inst

    def __getitem__(self, key: str):
        return getattr(self, key)
