# sec-helpers
Collection of dynamic security related helpers.

Sec-helpers is a bundle of useful tests and validators to ensure the security of a given domain.

## Usage
1. Select specifc sec-helper.
2. Run `main.py` with a domain as parameter (strip domain of extra information: example.com): `python verify{test}/main.py {domain}.{tld}`.

_Do you want all the sec-helpers ready in a container? Configure [cloudbuilders-dast](https://github.com/vwt-digital/cloudbuilder-dast)._

##### Exception
`verify-no-ssl` requires [openssl-1.0.2](https://www.openssl.org/source/old/1.0.2/openssl-1.0.2k.tar.gz) and can be run using the following command: <br>
`bash verify-no-ssl/ssl3.sh {domain}.{tld}`

### Helpers
**verify-no-http**
> Ensures domain redirects on http (and checks if https is active to not pass on incorrect domain)

**verify-hsts**
> Ensures that the Strict-Transport-Security header on the domain is higher than 10368000

**verify-high-tls**
> Ensures that TLS versions on domain are inline with [Mozilla's recommended configurations](https://wiki.mozilla.org/Security/Server_Side_TLS)

**verify-no-ssl**
> Ensures that no SSL version is used.

**verify-cors-policy**
> Ensures that Allowed Origins are specified.

**verify-encryption-in-transit** (Abandoned)
> Returns TLS rating grades from ssllabs.com API

### Examples
`python verify-high-tls/main.py {domain}.com`
```
-------
Protocol: TLSv1.3
Should be active: True
	Wrong configuration

-------
Protocol: TLSv1.2
Should be active: True
Connected with: TLSv1.2
Using cipher: ('ECDHE-RSA-AES128-GCM-SHA256', 'TLSv1.2', 128)

-------
Protocol: TLSv1
Should be active: False

-------
Protocol: TLSv1.1
Should be active: False
Connected with: TLSv1.1
Using cipher: ('ECDHE-RSA-AES128-SHA', 'TLSv1.0', 128)
	Wrong configuration

Test on {domain}.com failed
```
TLSv1.3 is not active on domain: verify-high-tls will fail.
TLSv1.1 is active on domain: verify-high-tls will fail.
__________

`python verify-no-http/main.py {domain}.com`
```
Starting GET request to http://{domain}.com
GET request to http://{domain}.com returned status 302
Starting GET request to https://{domain}.com
GET request to https://{domain}.com returned status 200
Successful http status check: http is disabled or redirects to https
```
Http request returned 302 Found redirect. Https returned 200. Verify-no-http passed.
__________

`python verify-hsts/main.py {domain}.com`
```
Starting GET request to http://{domain}.com
Strict-Transport-Security header on https://{domain}.com returned max-age=31536000
Successful HSTS status check
```
Strict Transport Security header found, with max age 31536000. Verify-hsts passed.
__________

`python verify-cors-policy/main.py {domain}.com`
```
Failing policy test: No Allowed Origins Specified
```
No allowed origins specified. Verify-cors-policy failed.

## Dependencies
* Python >= 3
* (specific for `verify-no-ssl`) = [openssl-1.0.2](https://www.openssl.org/source/old/1.0.2/openssl-1.0.2k.tar.gz)
