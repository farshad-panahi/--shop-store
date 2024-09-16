source = "https://github.com/farshad-panahi/--shop-store"
source_code = f'<a href="{source}">Click to see source code on github</a>'

description = """
    Store like simple[nothing special] api.
        features:
            1- Anon users can add items to their carts created by uuid. Before checkout, they login and we change cart to real order.


      Many Thanks
"""

SPECTACULAR_SETTINGS = {
    "TITLE": "ONLINE STORE API",
    "DESCRIPTION": description + source_code,
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
