import enum
import inspect
import datetime
from typing import Type, TypeVar, Union, Optional, get_origin, get_args

from fastapi import Form, Query
from pydantic import BaseModel
from pydantic.fields import FieldInfo

BaseModelVar = TypeVar('BaseModelVar', bound=BaseModel)


def is_scalar_type(annotation) -> bool:
    """
    判断是否为标量类型（FastAPI查询参数支持的类型）
    只允许基本标量类型通过，排除集合类型和复杂对象类型
    """
    # FastAPI 支持的标量类型
    scalar_types = (
        int, float, str, bool, bytes,
        datetime.datetime, datetime.date, datetime.time,
    )

    # 要忽略的集合/复杂类型
    ignore_types = (dict, list, tuple, set)

    # 1. 直接是标量类型
    if annotation in scalar_types:
        return True

    # 2. 直接是要忽略的集合类型
    if annotation in ignore_types:
        return False

    # 3. 检查是否是 BaseModel 的子类（包括 BaseModel 本身）
    #    必须用 inspect.isclass 守门，避免对泛型别名调用 issubclass 抛 TypeError
    if inspect.isclass(annotation) and issubclass(annotation, BaseModel):
        return False

    # 4. 枚举类型视为标量
    if inspect.isclass(annotation) and issubclass(annotation, enum.Enum):
        return True

    # 5. 处理 Optional[X] / Union[X, None] / Union[X, Y, ...]
    origin = get_origin(annotation)
    if origin is Union:
        args = get_args(annotation)
        # 去掉 NoneType，只检查实际类型
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            return is_scalar_type(non_none_args[0])   # 递归：Optional[X] → 检查 X
        # 多个非 None 类型时，全部都是标量才算标量
        return all(is_scalar_type(arg) for arg in non_none_args)

    # 6. 其他泛型类型（List[str]、Dict[str,int] 等）
    if origin is not None:
        if origin in ignore_types:
            return False
        # origin 本身是 BaseModel 子类的泛型（理论上不常见，但保险起见）
        if inspect.isclass(origin) and issubclass(origin, BaseModel):
            return False

    # 7. 未知类型一律保守拒绝
    return False


def as_query(cls: Type[BaseModelVar]) -> Type[BaseModelVar]:
    """
    Pydantic 模型查询参数装饰器，将 Pydantic 模型用于接收 Query 参数。
    自动跳过非标量类型字段（dict、list、嵌套 BaseModel 等）。

    用法：
        @as_query
        class MyQuery(BaseModel):
            page: int = 1
            keyword: Optional[str] = None
            config: Optional[SomeModel] = None   # ← 自动忽略

        @router.get("/list")
        async def list_items(q: MyQuery = Depends(MyQuery.as_query)):
            ...
    """
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():
        model_field: FieldInfo  # type: ignore

        # 跳过非标量类型的字段（含 Optional[BaseModel] 等复杂嵌套类型）
        if not is_scalar_type(model_field.annotation):
            continue

        # 优先使用别名作为参数名
        param_name = model_field.alias if model_field.alias else field_name

        if not model_field.is_required():
            new_parameters.append(
                inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Query(
                        default=model_field.default,
                        description=model_field.description,
                    ),
                    annotation=model_field.annotation,
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Query(..., description=model_field.description),
                    annotation=model_field.annotation,
                )
            )

    async def as_query_func(**data):
        """
        只用标量字段数据实例化模型；
        被忽略的复杂字段将使用模型自身定义的默认值（通常为 None）。
        """
        return cls(**data)

    sig = inspect.signature(as_query_func)
    sig = sig.replace(parameters=new_parameters)
    as_query_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_query', as_query_func)
    return cls


def as_form(cls: Type[BaseModelVar]) -> Type[BaseModelVar]:
    """
    Pydantic 模型表单参数装饰器，将 Pydantic 模型用于接收 Form 参数。

    用法：
        @as_form
        class LoginForm(BaseModel):
            username: str
            password: str

        @router.post("/login")
        async def login(form: LoginForm = Depends(LoginForm.as_form)):
            ...
    """
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():
        model_field: FieldInfo  # type: ignore

        param_name = model_field.alias if model_field.alias else field_name

        if not model_field.is_required():
            new_parameters.append(
                inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(
                        default=model_field.default,
                        description=model_field.description,
                    ),
                    annotation=model_field.annotation,
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    param_name,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(..., description=model_field.description),
                    annotation=model_field.annotation,
                )
            )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls