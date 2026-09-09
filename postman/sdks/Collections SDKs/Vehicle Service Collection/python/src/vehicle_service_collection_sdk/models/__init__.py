"""Lazy model exports.

Names are resolved on first attribute access via PEP 562 ``__getattr__``,
then cached in module globals. Avoids the multi-second eager-import cost
on SDKs with thousands of generated models.
"""

import importlib

_MODEL_TO_MODULE = {
    "CreateAVehicleRequest": "create_a_vehicle_request",
}

_REBUILD_NAMES = frozenset(
    {
        "CreateAVehicleRequest",
    }
)

__all__ = list(_MODEL_TO_MODULE.keys())

_rebuilt = False


def _load(name):
    module = _MODEL_TO_MODULE.get(name)
    if module is None:
        return None
    obj = getattr(importlib.import_module("." + module, __name__), name)
    globals()[name] = obj
    return obj


def _ensure_rebuilt():
    """Resolve forward refs across every BaseModel in one batched pass.

    Individual model files import their cross-references inside a
    ``TYPE_CHECKING`` block, so at runtime each file's globals contain
    only itself. ``model_rebuild()`` walks the call stack to find
    forward-ref names — calling it from this module once every
    BaseModel has been loaded into our globals is what lets pydantic
    resolve circular refs (the same shape the prior eager-import form
    relied on). Enums, Union types, and error models stay lazy.
    """
    global _rebuilt
    if _rebuilt:
        return
    _rebuilt = True
    for name in _REBUILD_NAMES:
        if name not in globals():
            try:
                _load(name)
            except Exception:
                pass
    ns = globals()
    for name in _REBUILD_NAMES:
        cls = ns.get(name)
        if cls is None:
            continue
        try:
            # _types_namespace is mandatory: pydantic resolves forward refs
            # against caller-frame locals by default, but we're calling from
            # inside a helper — the names live in this module's globals.
            cls.model_rebuild(_types_namespace=ns)
        except Exception:
            pass


def __getattr__(name):
    if name not in _MODEL_TO_MODULE:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    obj = _load(name)
    if name in _REBUILD_NAMES:
        _ensure_rebuilt()
    return obj


def __dir__():
    return sorted(set(globals()).union(_MODEL_TO_MODULE))
