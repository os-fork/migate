from rich.console import Console

ORANGE = "bold color(208)"
WHITE = "bold white"
DIM = "dim"
RED = "bold red"
GREEN = "bold green"

console = Console()
loader = console.status("", spinner="dots")

BASE_URL = "https://account.xiaomi.com"
SERVICELOGIN_URL = "https://account.xiaomi.com/pass/serviceLogin"
SERVICELOGINAUTH2_URL = "https://account.xiaomi.com/pass/serviceLoginAuth2"
LIST_URL = "https://account.xiaomi.com/identity/list"
SEND_EM_TICKET = "https://account.xiaomi.com/identity/auth/sendEmailTicket"
SEND_PH_TICKET = "https://account.xiaomi.com/identity/auth/sendPhoneTicket"
VERIFY_EM = "https://account.xiaomi.com/identity/auth/verifyEmail"
VERIFY_PH = "https://account.xiaomi.com/identity/auth/verifyPhone"
USERQUOTA_URL = "https://account.xiaomi.com/identity/pass/sms/userQuota"
REGION_URL = "https://account.xiaomi.com/pass/user/login/region"
CONFIG_URL = "https://account.xiaomi.com/pass2/config"
LONGPOLLING_URL = "https://account.xiaomi.com/longPolling/loginUrl"
CONFIGURATION_URL = "https://api.account.xiaomi.com/pass/configuration"
PROFILE_HOME_URL = "https://account.xiaomi.com/pass2/profile/home"
SECURITY_HOME_URL = "https://account.xiaomi.com/pass2/security/home"
