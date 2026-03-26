# -*- coding: utf-8 -*-
# @author: xiaobai
import typing

from pydantic import BaseModel, Field, root_validator

from zerorunner.models.base import MethodEnum, Url, Headers, Cookies, Verify, VariablesMapping, ParametersMapping, \
    Export, BaseUrl, FunctionsMapping
from zerorunner.models.base import Name


class TStepBase(BaseModel):
    """步骤基类"""
    index: int = Field(0, description="排序")
    enable: bool = Field(True, description="是否有效")  # 是否有效
    version: int = Field(0, description="版本")
    is_quotation: int = Field(1, description="是否引用 0 否 1 是")
    source_id: typing.Union[str, int] = Field(None, description="源id")
    case_id: typing.Union[str, int] = Field(None, description="用例id")
    step_type: str = Field("", description="步骤类型 api if loop sql wait ui 等")
    name: Name = Field("", description="步骤名称")
    retry_times: int = Field(0, description="重试次数")
    retry_interval: int = Field(0, description="重试间隔")
    step_id: int = Field(None, description="步骤id")
    parent_step_id: int = Field(None, description="父级步骤id")


class ExtractData(BaseModel):
    """提取模型"""
    name: str = Field("", description="提取变量名称")
    path: str = Field("", description="提取路径")
    continue_extract = Field(False, description="是否继续提取")
    continue_index: int = Field(0, description="继续提取下标")
    extract_type: str = Field("", description="提取类型 jmespath jsonpath")


class ValidatorData(BaseModel):
    """验证模式"""
    mode: str = Field(None, description="校验方法")
    check: typing.Any = Field(None, description="校验值")
    comparator: str = Field(None, description="比较器")
    expect: typing.Any = Field(None, description="预期值")
    continue_extract: bool = Field(False, description="继续提取 针对 mode = JsonPath 才有效")
    continue_index: int = Field(0, description="提取index")


class TRequest(BaseModel):
    """api 请求模型"""
    request_type_: typing.Literal["api"] = Field('api', description="api", exclude=True)

    method: typing.Union[str, MethodEnum] = Field(..., description="请求方法")
    url: Url = Field(..., description="请求url")
    params: typing.Dict[str, str] = Field({}, description="参数")
    headers: Headers = Field({}, description="请求头")
    req_json: typing.Union[typing.Dict, typing.List, str] = Field(None, alias="json", description="json数据")
    data: typing.Union[str, typing.Dict[str, typing.Any]] = Field(None, description="data数据")
    cookies: Cookies = Field({}, description="cookies")
    timeout: float = Field(120, description="超时时间")
    allow_redirects: bool = Field(True, description="允许重定向")
    verify: Verify = Field(False, description="开启验证")
    upload: typing.Dict = Field({}, description="上传文件")  # used for upload files

    def dict(self, *args, **kwargs):
        if "by_alias" not in kwargs:
            kwargs["by_alias"] = True
        return super().dict(*args, **kwargs)


class TSqlRequest(BaseModel):
    """sql请求模型"""
    request_type_: typing.Literal["sql"] = Field('sql', description="sql", exclude=True)

    sql: str = Field("", description="sql")
    host: str = Field(None, description="host")
    port: typing.Optional[int] = Field(None, description="端口")
    user: typing.Optional[str] = Field(None, description="用户名")
    password: typing.Optional[str] = Field(None, description="密码")
    database: typing.Optional[str] = Field("", description="数据库")
    timeout: typing.Optional[int] = Field(None, description="超时时间")  # 超时时间
    variable_name: typing.Optional[str] = Field(None, description="变量赋值名称")  # 变量赋值名称


class TUiRequest(BaseModel):
    """ui请求模型"""
    request_type_: typing.Literal["ui"] = Field('ui', description="ui", exclude=True)

    action: str = Field(None, description="动作")
    data: str = Field(None, description="输入数据")
    location_method: str = Field(None, description="定位方法")
    location_value: str = Field(None, description="定位值")
    cookie: typing.Dict = Field(None, description="cookie")
    output: str = Field(None, description="输出")


class TIFRequest(BaseModel):
    """if请求模型"""
    request_type_: typing.Literal["if"] = Field('if', description="if", exclude=True)

    check: str = Field("", description="校验变量")
    comparator: str = Field("", description="对比规则")
    expect: str = Field("", description="对比值")
    remarks: str = Field("", description="备注")

    class Config:
        extra = "forbid"


class TWaitRequest(BaseModel):
    """等待请求"""
    request_type_: typing.Literal["wait"] = Field('wait', description="wait", exclude=True)

    wait_time: int = Field(0, description="等待时间秒(s)")


class TLoopRequest(BaseModel):
    """循环请求"""
    request_type_: typing.Literal["loop"] = Field('loop', description="loop", exclude=True)

    loop_type: str = Field("", description="count 次数循环  for 循环  while 循环")
    # loop_type == "count"
    count_number: int = Field(0, description="循环次数")
    count_sleep_time: int = Field(0, description="休眠时间")  # 休眠时间

    # loop_type == "for"
    for_variable_name: str = Field(None, description="循环变量名")  # 循环变量名
    for_variable: typing.Any = Field(None, description="循环变量")  # 循环变量
    for_sleep_time: int = Field(0, description="休眠时间")  # 休眠时间

    # loop_type == "while"
    while_comparator: str = Field(None, description="比对条件")  # 比对条件
    while_variable: typing.Any = Field(None, description="循环变量")  # 循环变量
    while_value: str = Field(None, description="循环值")  # 循环值
    while_sleep_time: int = Field(1, description="")
    while_timeout: int = Field(0, description="超时时间")  # 超时时间


class TScriptRequest(BaseModel):
    """脚本请求"""
    request_type_: typing.Literal["script"] = Field('script', description="script", exclude=True)

    script_content: str = Field(None, description="脚本类容")


class TPcBaseRequest(BaseModel):
    """PC自动化请求基类 —— 包含所有 PC 步骤公共字段"""
    # 图片字段
    image: typing.Optional[str] = Field(None, description="主图片URL")
    dragImage: typing.Optional[str] = Field(None, description="拖拽目标图片URL")
    referenceImage: typing.Optional[str] = Field(None, description="参考图片URL")
    targetImage: typing.Optional[str] = Field(None, description="目标图片URL")
    trackImage: typing.Optional[str] = Field(None, description="轨迹图片URL")
    parentImage: typing.Optional[str] = Field(None, description="父级区域图片URL")
    # 定位 & 比对
    comparator: typing.Optional[str] = Field(None, description="比对方式")
    location_strategy: typing.Optional[str] = Field(None, description="定位策略")
    picture_is_search: typing.Optional[bool] = Field(None, description="是否以图搜图")
    # 文字输入
    text: typing.Optional[str] = Field(None, description="键盘输入文本")
    remarks: typing.Optional[str] = Field(None, description="备注")
    # 区域偏移（父级区域）
    regionOffsetX: typing.Optional[float] = Field(None, description="父级区域X偏移")
    regionOffsetY: typing.Optional[float] = Field(None, description="父级区域Y偏移")
    regionWidth: typing.Optional[float] = Field(None, description="父级区域宽度")
    regionHeight: typing.Optional[float] = Field(None, description="父级区域高度")
    # 轨迹区域偏移
    trackRegionOffsetX: typing.Optional[float] = Field(None, description="轨迹区域X偏移")
    trackRegionOffsetY: typing.Optional[float] = Field(None, description="轨迹区域Y偏移")
    trackRegionWidth: typing.Optional[float] = Field(None, description="轨迹区域宽度")
    trackRegionHeight: typing.Optional[float] = Field(None, description="轨迹区域高度")
    # pip 专用
    targetPercentage: typing.Optional[float] = Field(None, description="目标百分比（pip拖拽用）")
    isHorizontal: typing.Optional[bool] = Field(None, description="是否水平方向（pip滑块用）")


# ---------- PC 具体请求类型（每个只覆写 request_type_ 的 Literal）----------

class TPcMouseLeftClickRequest(TPcBaseRequest):
    request_type_: typing.Literal["mouse_left_click"] = Field("mouse_left_click", exclude=True)


class TPcMouseRightClickRequest(TPcBaseRequest):
    request_type_: typing.Literal["mouse_right_click"] = Field("mouse_right_click", exclude=True)


class TPcMouseDoubleClickRequest(TPcBaseRequest):
    request_type_: typing.Literal["mouse_double_click"] = Field("mouse_double_click", exclude=True)


class TPcMouseHoverRequest(TPcBaseRequest):
    request_type_: typing.Literal["mouse_hover"] = Field("mouse_hover", exclude=True)


class TPcMouseDragRequest(TPcBaseRequest):
    request_type_: typing.Literal["mouse_drag"] = Field("mouse_drag", exclude=True)


class TPcMouseScrollDownRequest(TPcBaseRequest):
    request_type_: typing.Literal["mouse_scroll_wheel_down"] = Field("mouse_scroll_wheel_down", exclude=True)


class TPcMouseScrollUpRequest(TPcBaseRequest):
    request_type_: typing.Literal["mouse_scroll_wheel_up"] = Field("mouse_scroll_wheel_up", exclude=True)


class TPcKeyboardInputRequest(TPcBaseRequest):
    request_type_: typing.Literal["keyboard_input"] = Field("keyboard_input", exclude=True)


class TPcKeyboardClearRequest(TPcBaseRequest):
    request_type_: typing.Literal["keyboard_clear"] = Field("keyboard_clear", exclude=True)


class TPcKeyboardSelectAllRequest(TPcBaseRequest):
    request_type_: typing.Literal["keyboard_select_all"] = Field("keyboard_select_all", exclude=True)


class TPcKeyboardEnterRequest(TPcBaseRequest):
    request_type_: typing.Literal["keyboard_enter"] = Field("keyboard_enter", exclude=True)


class TPcKeyboardCombinationKeyRequest(TPcBaseRequest):
    request_type_: typing.Literal["keyboard_combination_key"] = Field("keyboard_combination_key", exclude=True)


class TPcFlowWaitRequest(TPcBaseRequest):
    request_type_: typing.Literal["flow_wait"] = Field("flow_wait", exclude=True)
    wait_time: int = Field(0, description="等待时间(ms)")


class TPcFlowWaitElementRequest(TPcBaseRequest):
    request_type_: typing.Literal["flow_wait_element"] = Field("flow_wait_element", exclude=True)
    timeout: int = Field(10000, description="超时时间(ms)")


class TPcFlowCaseTemplateRequest(TPcBaseRequest):
    request_type_: typing.Literal["flow_case_template"] = Field("flow_case_template", exclude=True)
    template_case_id: typing.Optional[int] = Field(None, description="模板用例id")


class TPcPipSwitchClickRequest(TPcBaseRequest):
    request_type_: typing.Literal["pip_switch_click"] = Field("pip_switch_click", exclude=True)


class TPcPipTimelineDragRequest(TPcBaseRequest):
    request_type_: typing.Literal["pip_timeline_drag"] = Field("pip_timeline_drag", exclude=True)


class TPcPipSliderDragRequest(TPcBaseRequest):
    request_type_: typing.Literal["pip_slider_drag"] = Field("pip_slider_drag", exclude=True)


TStepRequest = typing.Union[
    TRequest, TSqlRequest, TIFRequest, TWaitRequest, TScriptRequest, TLoopRequest, TUiRequest,
    # PC 自动化类型
    TPcMouseLeftClickRequest,
    TPcMouseRightClickRequest,
    TPcMouseDoubleClickRequest,
    TPcMouseHoverRequest,
    TPcMouseDragRequest,
    TPcMouseScrollDownRequest,
    TPcMouseScrollUpRequest,
    TPcKeyboardInputRequest,
    TPcKeyboardClearRequest,
    TPcKeyboardSelectAllRequest,
    TPcKeyboardEnterRequest,
    TPcKeyboardCombinationKeyRequest,
    TPcFlowWaitRequest,
    TPcFlowWaitElementRequest,
    TPcFlowCaseTemplateRequest,
    TPcPipSwitchClickRequest,
    TPcPipTimelineDragRequest,
    TPcPipSliderDragRequest,
]


class TStep(TStepBase):
    """步骤模型"""
    testcase: typing.Union[str, typing.Callable, None] = Field(None, description="测试用例")
    node_id: typing.Optional[str] = Field(None, description="步骤节点id")
    variables: VariablesMapping = Field({}, description="步骤变量")
    # pre_steps: "TStep" = Field([], description="前置步骤")
    # post_steps: "TStep" = Field([], description="后置步骤")
    # parameters 加入步骤 参数
    parameters: ParametersMapping = Field({}, description="步骤参数")
    setup_hooks: typing.List[typing.Union[str, dict, object]] = Field([], description="前置钩子")
    teardown_hooks: typing.List[typing.Union[str, dict, object]] = Field([], description="后置钩子")
    setup_code: str = Field(None, description="前置code")
    teardown_code: str = Field(None, description="后置code")
    # used to extract request's response field
    extracts: typing.List[ExtractData] = Field([], description="提取")
    # used to export session variables from referenced testcase
    export: Export = Field([], description="导出")
    validators: typing.List[ValidatorData] = Field([], alias="validate")
    request: TStepRequest = Field(None, description="请求信息", discriminator="request_type_")
    children_steps: typing.List['TStep'] = Field([], description="子步骤")

    @root_validator(pre=True)
    def insert_request_type(cls, values):
        request = values.get('request', {})
        step_type = values.get('step_type', None)
        if request:
            if not step_type:
                raise ValueError("step_type is required")
            values['request'] = {'request_type_': step_type} | request
        return values


class TConfig(BaseModel):
    """配置模型"""
    name: Name = Field(..., description="名称")
    case_id: typing.Union[str, int, None] = Field(None, description="用例id")
    verify: Verify = Field(False, description="是否校验")
    base_url: BaseUrl = Field("", description="base_url")
    functions: FunctionsMapping = Field({}, description="函数mapping")
    step_rely: bool = Field(False, description="步骤依赖")
    # Text: prepare variables in debugtalk.py, ${gen_variables()}
    variables: typing.Union[VariablesMapping, str] = Field({}, description="变量")
    env_variables: typing.Union[VariablesMapping, str] = Field({}, description="环境变量")
    parameters: typing.Union[VariablesMapping, str] = Field({}, description="参数")
    # 请求头
    headers: VariablesMapping = {}
    # teardown_hooks: Hooks = []
    export: Export = Field([], description="导出数据")


class TestCase(BaseModel):
    """用例模型"""
    config: TConfig = Field(..., description="配置")
    teststeps: typing.List[typing.Union[TStep, object]] = Field(..., description="用例步骤")
