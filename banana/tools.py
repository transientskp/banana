def recur_getattr(obj, attr):
    """Use this on a model object and string representing a django model
    reference.

    example::

    >>> recur_getattr(transient, "runcat__wm_ra")

    would translate to::

    >>> transient.runcat.wm_ra
    """
    attrs = attr.split('__')
    if len(attrs) == 1:
        return getattr(obj, attr)
    else:
        return recur_getattr(getattr(obj, attrs[0]), '__'.join(attrs[1:]))