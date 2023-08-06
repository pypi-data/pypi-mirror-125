# thinknet-observer-python
A small demo library for thinknet-observer libraries.

### Installation
```
pip install thinknet-observer
```

### Get started
How to multiply one number by another with this lib:

```Python
from thinknet_observer import PrometheusMiddleware

# Instantiate a app framework
app = Flask(__name__)

# use middleware
PrometheusMiddleware(app).register_metrics()
```

