# -*- coding: utf-8 -*-

import traceback

try:
    sys = traceback.sys  # type: ignore
    if sys.getdefaultencoding() != "utf-8":
        sys = reload(sys)  # type: ignore
        sys.setdefaultencoding("utf-8")  # type: ignore
except Exception:
    pass
