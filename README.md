<div align="center">

<a href="https://github.com/offici5l/migate/releases/latest">
  <img src="https://img.shields.io/badge/migate-%23FF6900?style=flat&logo=xiaomi&logoColor=white" alt="migate" width="100"/>
</a>

**Xiaomi authentication gateway for Python**

---

[![Version](https://img.shields.io/pypi/v/migate?label=Version&labelColor=black&color=brightgreen)](https://pypi.org/project/migate/)
[![Changelog](https://img.shields.io/badge/Changelog-blue?style=flat&logoColor=white)](CHANGELOG.md)

---

</div>

## Install

```sh
pip install migate
```

Or add it as a dependency in your project:

```toml
# pyproject.toml
dependencies = ["migate"]
```

```txt
# requirements.txt
migate
```

---

## Usage

```python
import migate

# --- passport (default) ---
# If no params are passed, sid defaults to passport.
# pass_token = migate.get_passtoken()
# service = migate.get_service(pass_token)

# --- unlockApi: bootloader unlock ---
# params = {"sid": "unlockApi", "checkSafeAddress": True}

# --- xiaomiio: Mi Home / smart home devices ---
# params = {"sid": "xiaomiio"}

# --- micoapi: Mi AI speaker ---
# params = {"sid": "micoapi"}

# --- i.mi.com: Mi Cloud / Find Device ---
# params = {"sid": "i.mi.com"}

# --- 18n_bbs_global: Mi Community ---
# params = {"sid": "18n_bbs_global"}

params = {"sid": "unlockApi", "checkSafeAddress": True}

pass_token = migate.get_passtoken(params)
# skip the interactive prompt if already logged in
# pass_token = migate.get_passtoken(params, silent=True)

service = migate.get_service(pass_token, params)

print(pass_token)
# {
#   "deviceId":  "wb_...",
#   "passToken": "...",
#   "userId":    "..."
# }

print(service)
# {
#   "servicedata": {
#     "nonce":     ...,
#     "ssecurity": "...",
#     "cUserId":   "...",
#     "psecurity": "...",
#     "deviceId":  "wb_..."
#   },
#   "cookies": {
#     # passport       -> {}
#     # unlockApi      -> serviceToken, unlockApi_slh, unlockApi_ph, userId
#     # xiaomiio       -> serviceToken, cUserId, userId
#     # micoapi        -> serviceToken, micoapi_slh, micoapi_ph, userId
#     # i.mi.com       -> serviceToken, i.mi.com_slh, i.mi.com_ph, userId
#     # 18n_bbs_global -> serviceToken, popRunToken, new_bbs_serviceToken, new_login, userId
#   }
# }
```

> All functions return `None` on failure. Always check the return value before passing it to the next call.

---

## Utilities

```python
# get account region 
region = migate.get_region(pass_token)

# get dataCenterZone
## get with account region
zone = migate.get_dataCenterZone(region)                 ## get with account ID 
zone = migate.get_dataCenterZone(userId)                 ## manual selection
zone = migate.get_dataCenterZone()                              

# get uRegion
uRegion = migate.get_uRegion()

# get uLocale
uLocale = migate.get_uLocale() 

# areaConfig, ex: with SG
area = migate.get_areaConfig("SG")
# {"code": "SG", "name": "Singapore", "dial": "+65"}
```


---

<div align="center">

🤝 [Contributing](CONTRIBUTING.md)

<a href="https://github.com/offici5l/migate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=offici5l/migate" />
</a>

---

[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

</div>
