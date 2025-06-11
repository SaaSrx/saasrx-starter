from rxext.dto import MenuItem, MenuLink, MenuButton

MenuItems = [
    # use any of these types: MenuItem or MenuLink or MenuButton
    MenuItem(text="Features", link="#features", typeof="link"),
    MenuLink("Pricing", "#pricing"),
    MenuLink("Testimonials", "#testimonials"),
    MenuLink("Guide", "/guide"),
    MenuButton("Get Started", "/signin"),
]
