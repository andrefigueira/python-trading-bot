import sys
import types

# Minimal pydantic stub to satisfy imports during tests
pydantic = types.ModuleType('pydantic')

class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    def model_dump(self):
        return self.__dict__

    def json(self, indent=None):
        import json
        return json.dumps(self.model_dump(), indent=indent)

class BaseSettings(BaseModel):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @classmethod
    def parse_file(cls, path):
        import json
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

def Field(default=None, env=None):
    if default is ...:
        return ""
    return default

pydantic.BaseModel = BaseModel
pydantic.BaseSettings = BaseSettings
pydantic.Field = Field
sys.modules.setdefault('pydantic', pydantic)

# Minimal typer stub for CLI testing

typer = types.ModuleType('typer')

class Typer:
    def __init__(self, name=None):
        self.name = name
        self.commands = {}

    def command(self, name=None):
        def decorator(func):
            cmd_name = name or func.__name__
            self.commands[cmd_name] = func
            return func
        return decorator

    def __call__(self, *args, **kwargs):
        pass


def echo(message):
    print(message)

class CliRunner:
    class Result:
        def __init__(self, exit_code=0):
            self.exit_code = exit_code

    def invoke(self, app, args=None):
        args = args or []
        cmd = args[0] if args else None
        if cmd in app.commands:
            app.commands[cmd](*args[1:])
            return self.Result(0)
        return self.Result(1)


typer.Typer = Typer
typer.echo = echo

testing = types.ModuleType('typer.testing')
testing.CliRunner = CliRunner
sys.modules.setdefault('typer.testing', testing)
sys.modules.setdefault('typer', typer)

# Minimal FastAPI stub
fastapi = types.ModuleType('fastapi')

class FastAPI:
    def __init__(self, title=None):
        self.title = title
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

fastapi.FastAPI = FastAPI
sys.modules.setdefault('fastapi', fastapi)

# Minimal websockets stub
websockets = types.ModuleType('websockets')

class WebSocketClientProtocol:
    def __init__(self, messages=None):
        self.messages = messages or []
        self.sent = []

    async def send(self, msg):
        self.sent.append(msg)

    def __aiter__(self):
        async def iterator():
            for msg in self.messages:
                yield msg
        return iterator()

async def connect(url):
    return WebSocketClientProtocol()

websockets.WebSocketClientProtocol = WebSocketClientProtocol
websockets.connect = connect
sys.modules.setdefault('websockets', websockets)

# Minimal httpx stub
httpx = types.ModuleType('httpx')

class Response:
    def __init__(self, json_data=None, status_code=200):
        self._json = json_data or {}
        self._status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self._status_code >= 400:
            raise Exception('HTTP error')

class AsyncClient:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.request_log = []

    async def get(self, url, headers=None):
        self.request_log.append((url, headers))
        return Response({'account': 'ok'})

httpx.AsyncClient = AsyncClient
httpx.Response = Response
sys.modules.setdefault('httpx', httpx)

# Minimal yaml stub
yaml = types.ModuleType('yaml')

def safe_dump(data, stream=None, sort_keys=False):
    import json
    text = json.dumps(data, indent=2)
    if stream is not None:
        stream.write(text)
        return None
    return text

def safe_load(text):
    import json
    return json.loads(text)

yaml.safe_dump = safe_dump
yaml.safe_load = safe_load
sys.modules.setdefault('yaml', yaml)

# Minimal pytest-cov stub so --cov flag is accepted
pytest_cov = types.ModuleType('pytest_cov')

def pytest_addoption(parser):
    parser.addoption('--cov', action='store', default=None)

pytest_cov.pytest_addoption = pytest_addoption
sys.modules.setdefault('pytest_cov', pytest_cov)

pytest_plugins = ['pytest_cov']
