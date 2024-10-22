from saas.rxext.patched import patch_reflex


def main():
    patch_reflex()
    from reflex.reflex import cli

    cli()
