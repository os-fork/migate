# migate 

**migate** is a simplified Xiaomi authentication gateway for Python projects

```

## Usage

```python
import migate

service_id = ''

param = {"sid": service_id}

# Required for some service IDs like "unlockApi" :
# param["checkSafeAddress"] = True

passToken = migate.get_passtoken(param)
service = migate.get_service(passToken, param)

```


___

<div align="center">

![MIT License](https://img.shields.io/badge/License-MIT-green.svg)

</div>