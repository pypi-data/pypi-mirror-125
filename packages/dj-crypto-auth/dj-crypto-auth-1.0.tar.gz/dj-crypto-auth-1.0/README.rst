=============================================
OAuth based Login System for Crypto Exchanges
=============================================

Django Crypto Auth allows you generate user's crypto exchage data without compromising security.

Quick Start
===========

1. Add "cryptoAuth" to INSTALLED_APPS setting like this:

	INSTALLED_APPS = [
		...
	    'cryptoAuth',
	]

2. Include other settings like:

	CRYPTO_AUTH_COINBASE_KEY = "..."
	CRYPTO_AUTH_COINBASE_SECRET = "..."

	CRYPTO_AUTH_REDIRECT = 'portofolio:port_home'

	CRYPTO_AUTH_BACKLOGS = True

3. Add To urls.py like this:

	urlpatterns = [
		...
	    path('auth/', include('cryptoAuth.urls')),
	]

3. Run `python manage.py migrate` to create the BACKLOGS model.

4. Link to the exchange for example, https://www.coinbase.com/oauth/authorize?response_type=code&client_id=416753f30c4369d96bbb485280034311f9609434e9900c8bebc1ec079de81135&redirect_uri=http://{{ request.META.HTTP_HOST }}/auth/coinbase/confirm_auth&state=SECURE_RANDOM&scope=wallet:accounts:read,wallet:buys:read