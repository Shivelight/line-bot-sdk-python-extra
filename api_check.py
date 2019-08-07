from linebot.api import LineBotApi
from linebotx.api import LineBotApiAsync

linebot_funcs = [
    x
    for x in dir(LineBotApi)
    if callable(getattr(LineBotApi, x)) and not x.startswith("_")
]
linebotx_funcs = [
    x
    for x in dir(LineBotApiAsync)
    if callable(getattr(LineBotApiAsync, x)) and not x.startswith("_")
]
missing_func = [x for x in linebot_funcs if x not in linebotx_funcs]

print("Missing methods (linebotx):\n * {}".format("\n * ".join(missing_func)))
