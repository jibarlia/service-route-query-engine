"""Import every filter submodule so ``@register_filter`` runs on package import.

Dropping a new ``*_filter.py`` file in this package is enough to register it;
no central list to maintain.
"""

import pkgutil
from importlib import import_module

for _module in pkgutil.iter_modules(__path__):
    import_module(f"{__name__}.{_module.name}")
