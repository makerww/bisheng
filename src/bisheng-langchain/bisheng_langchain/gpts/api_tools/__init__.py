import inspect
from typing import Any, Callable, Dict, List, Tuple

from bisheng_langchain.gpts.api_tools.tianyancha import CompanyInfo
from langchain_core.tools import BaseTool, Tool
from mypy_extensions import KwArg


def _get_tianyancha_api(name, **kwargs: Any) -> BaseTool:

    class_method = getattr(CompanyInfo, name)

    return Tool(name=name,
                description=class_method.__doc__,
                func=class_method(**kwargs).run,
                coroutine=class_method(**kwargs).arun)


# 筛选出类方法
tianyancha_class_methods = [
    attr for attr in dir(CompanyInfo) if inspect.ismethod(getattr(CompanyInfo, attr))
]

API_TOOLS: Dict[str, Tuple[Callable[[KwArg(Any)], BaseTool], List[str]]] = {
    f'tianyancha.{name}': (_get_tianyancha_api, ['api_key'])
    for name in tianyancha_class_methods
}
