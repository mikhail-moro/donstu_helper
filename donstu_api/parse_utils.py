import datetime
import types


def _api_parse(parser: types.FunctionType):
    def parser_wrapper(*args, **kwargs):
        response_type = parser.__name__[6:]
        try:
            return {
                "type": response_type,
                "data": parser(*args, **kwargs)
            }
        except:
            return {
                "type": response_type,
                "data": None
            }

    return parser_wrapper


@_api_parse
def parse_rasp_today(data):
    date_str = datetime.date.today().strftime('%Y-%m-%d')
    base = data["data"]["raspList"]
    data = []

    for item in base:
        if item["start"][:10] == date_str:
            data.append(
                {
                    "name": item["name"],
                    "module": item["info"]["moduleName"],
                    "start": item["start"],
                    "end": item["end"]
                }
            )

    return data


@_api_parse
def parse_rasp_tomorrow(data):
    date_str = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    base = data["data"]["raspList"]
    data = []

    for item in base:
        if item["start"][:10] == date_str:
            data.append(
                {
                    "name": item["name"],
                    "module": item["info"]["moduleName"],
                    "start": item["start"],
                    "end": item["end"]
                }
            )

    return data


@_api_parse
def parse_marks(data):
    base = data["data"]["marks"]
    return [{"name": i["moduleName"], "percent": i["percent"]} for i in base]


parsers = {
    "get_rasp_today": parse_rasp_today,
    "get_rasp_tomorrow": parse_rasp_tomorrow,
    "get_marks": parse_marks
}
