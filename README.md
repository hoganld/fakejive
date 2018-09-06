# Fake Jive SAML test app

This app is intended to as a second SAML Service Provider for a SimpleSAMLPHP IDP, useful to make sure your SSO & SLO is functioning correctly.

I wrote this to stand in place of a Jive SP which I cannot test locally, for the new Python-based BecomeAnEX project for the Truth Initiative. The only reason you would be interested in this is repository is if you are on the TI dev team and you want to test the SAML SSO/SLO for Snakex. So that's who I'm assuming you are throughout the rest of this document.

## Installation & Setup

There are a few steps, but getting this running should be pretty straightforward:

1. Clone this repo locally

2. Generate your SAML private key & X509 certificate. From the `saml` directory of this repo:
```
$ openssl genrsa -out fakejive.key 2048
$ openssl req -new -x509 -key fakejive.key -out fakejive.crt
```

3. Copy the XML metadata file from your SAML IDP into the `saml` directory as "idp_metadata.xml". If you're testing Snakex locally, and thus running EX/Simplesamlphp in a vagrant VM, you can get the metadata file by pointing your browser at https://www.exdev.test/saml/saml2/idp/metadata.php

4. Install the requirements into virtualenv:
```
(venv)$ pip install -r requirements.txt
```

5. Install the xmlsec1 library. This will depend on your platform. On Linux, you should be able to install the package with `apt` or `yum`. On a Mac, you can install it with Homebrew:
```
$ brew install libxmlsec1
```
You'll also need to make sure you have the correct absolute path to the `xmlsec1` binary in `settings.py`. The default is `/usr/local/bin/xmlsec1`, which should be correct if you installed it on Mac using Homebrew. On Linux, I've always seen it under `/usr/bin/xmlsec1`. If in doubt, you can check the path like so:
```
$ which xmlsec1
```

6. Run the migrations to generate your database.
```
$ ./manage.py migrate
```

7. Create a superuser
```
$ ./manage.py createsuperuser
```

8. Start the app in HTTPS mode, with django-sslserver: 
```
$ ./manage.py runsslserver
```
Note that by default this will use a self-signed certificate, and your browser will yell and scream about this. Either just click through the warnings, or generate a real cert using Let's Encrypt and use that:
```
$ ./manage.py runsslserver --certificate /path/to/certificate.crt --key /path/to/private.key
```

9. Log in to the Django Admin and create a user in the local app that corresponds to the Snakex/Plan *user* you are going to test with. Note the difference between a Snakex `User` and `Person` is relevant here. For your new user here, you'll want to use the username of the Snakex user, not the person. If PHPPlan created this user automatically via the Snakex API, this might be an integer rather than a username-looking string. You'll need to confer with your Snakex DB for the right value here.

10. Log out of the Django Admin, so that you are unauthenticated.

## Running it

At this point, the app should be up and running, unless I forgot a step in these instructions. If you visit the home page of this app you should see it greet you with "Welcome to Fake Jive, Guest."

In order to get the login and logout buttons actually working with the IDP, you'll need to add SP metadata for this app to your IDP. In the case of EX's Simplesamlphp IDP, you just need to checkout the `SNAKEX-70` branch of ex-infra-config and deploy ex-plan/simplesamlphp to your web-static VM. From your ex-infra-config directory:

```
$ git checkout SNAKEX-70
$ ./deploy.sh phpplan dev --phpplan-version dev --simplesamlphp-version dev
```

Using the `SNAKEX-70` branch of ex-infra-config will copy the correct SP metadata for this app into Simplesamlphp's config, assuming that you are running this app on localhost port 8000.

At this point, all of the hyperlinks on the index page of this app should be working:

- Login should redirect you to the IDP to authenticate, and then you should be redirected back and see "Guest" replaced with your username in the welcome message.

- Logout should redirect you back to the IDP and then immediately back to this app, at which point you should be addressed as "Guest" again.

- Metadata should show you your local SP metadata.xml file, which is useful if you need to debug a config issue with talking to the IDP.

- SAML Test Page should show you a couple of diagnostics about your current SAML session -- user ID and display name.

You should also be able to see debug logs for each SAML request, including the incoming SLO requests from the IDP when you logout of SAML from a different SP, like Snakex.

Happy Testing!
