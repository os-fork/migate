<div align="center">

<a href="https://github.com/offici5l/migate/releases/latest">
  <img src="https://img.shields.io/badge/migate-%23FF6900?style=flat&logo=xiaomi&logoColor=white" alt="migate" width="200"/>
</a>

**Xiaomi authentication gateway for Python..**

---

[![Version](https://img.shields.io/pypi/v/migate?label=Version&labelColor=black&color=brightgreen)](https://pypi.org/project/migate/)
[![Changelog](https://img.shields.io/badge/Changelog-blue?style=flat&logoColor=white)](CHANGELOG.md)

---

</div>


## Install

```
pip install migate
```

## Usage

```python
import migate
# default param = { 'sid': 'passport'}
pass_token = migate.get_passtoken()
service    = migate.get_service(pass_token)
```

To use a custom param ex:

```python
param      = {"sid": "unlockApi", "checkSafeAddress": True}
pass_token = migate.get_passtoken(param)
service    = migate.get_service(pass_token, param)
```

To get the account region:

```python
account_region = migate.get_region(pass_token)
region_cfg     = migate.get_regionConfig(account_region)
```
---

<div align="center">

🤝 [Contributing](CONTRIBUTING.md)

<a href="https://github.com/offici5l/migate/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=offici5l/migate" />
</a>

---

[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)


