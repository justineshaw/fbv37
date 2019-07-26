
Use Python 3 shutil.which on Python 2::

    try:
        from shutil import which
    except ImportError:
        from backports.shutil_which import which


