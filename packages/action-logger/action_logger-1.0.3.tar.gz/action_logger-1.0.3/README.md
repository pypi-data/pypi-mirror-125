### Project description

## Action logger

Action-logger is a simple, yet elegant, behavior tracking library.


#### Install

```python
pip install action_logger==1.0.2
```

Usage
```python
from action_logger.client import action_post


@action_post
def func(*args, **kwargs):
    """
    Need to record behavior func
    """
    pass
```

**Action logger records details about the client**
- IP address
- Hostname
- Action timestamp
- Function name
- Function parameters
- Function document
- Function model
- Function source code
- Etc.

