# Sec-helpers
Collection of dynamic security related helpers (DAST).

Sec-helpers is a bundle of useful tests and validators to ensure the security of a given domain.

## Usage
1. Install package `pip install sec-helpers`: https://pypi.org/project/sec-helpers
2. Copy and change the following to run all the tests:
```python
import sec_helpers

domain: str = 'vwt-digital.github.io' # {domain}.{tld}

sec_helpers.CorsPolicy(domain=domain)
sec_helpers.HighTls(domain=domain, slide=False) # Slide is False by default
sec_helpers.Hsts(domain=domain, age=10368000) # Age is 10368000 by default
sec_helpers.NoHttp(domain=domain)
sec_helpers.NoSsl(domain=domain)
```

_Do you want all the sec-helpers ready in a container? Configure [cloudbuilders-dast](https://github.com/vwt-digital/cloudbuilder-dast)._

##### Exception
`NoSsl` requires [openssl-1.0.2](https://www.openssl.org/source/old/1.0.2/openssl-1.0.2k.tar.gz) and can be run using the following: <br>
`sec_helpers.NoSsl(domain={domain}.{tld})`,
but will result in exit code 0 when the wrong openssl version is present.

### Helpers
**NoHttp**
> Ensures domain redirects on http (and checks if https is active to not pass on incorrect domain)

**Hsts**
> Ensures that the Strict-Transport-Security header on the domain is higher than 10368000

**HighTls**
> Ensures that TLS versions on domain are inline with [Mozilla's recommended configurations](https://wiki.mozilla.org/Security/Server_Side_TLS)

**NoSsl**
> Ensures that no SSL version is used.

**CorsPolicy**
> Ensures that Allowed Origins are specified.


### Examples
`sec_helpers.HighTls({domain}.com)`
```
-------
Protocol: TLSv1.3
Should be active: True
	Wrong configuration

-------
Protocol: TLSv1.2
Should be active: True
Connected with: TLSv1.2
Using cipher: ('{cipher_info}', 'TLSv1.2', 128)

-------
Protocol: TLSv1
Should be active: False

-------
Protocol: TLSv1.1
Should be active: False
Connected with: TLSv1.1
Using cipher: ('{cipher_info}', 'TLSv1.0', 128)
	Wrong configuration

Test on {domain}.com failed
```
TLSv1.3 is not active on domain: HighTls will fail.
TLSv1.1 is active on domain: HighTls will fail.
__________

`sec_helpers.NoHttp({domain}.com)`
```
Starting GET request to http://{domain}.com
GET request to http://{domain}.com returned status 302
Starting GET request to https://{domain}.com
GET request to https://{domain}.com returned status 200
Successful http status check: http is disabled or redirects to https
```
Http request returned 302 Found redirect. Https returned 200. NoHttp passed.
__________

`sec_helpers.Hsts({domain}.com)`
```
Starting GET request to http://{domain}.com
Strict-Transport-Security header on https://{domain}.com returned max-age=31536000
Successful HSTS status check
```
Strict Transport Security header found, with max age 31536000. Hsts passed.
__________

`sec_helpers.CorsPolicy({domain}.com)`
```
Failing policy test: No Allowed Origins Specified
```
No allowed origins specified. CorsPolicy failed.

## Dependencies
* Python >= 3.6
* (specific for `NoSsl`) = [openssl-1.0.2](https://www.openssl.org/source/old/1.0.2/openssl-1.0.2k.tar.gz)
