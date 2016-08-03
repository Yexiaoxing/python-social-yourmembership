# python-social-yourmembership

This is a plugin for YourMembership SSO based on [python-social-auth](https://github.com/omab/python-social-auth/).

## Reference

- [YourMembership.com API](https://api.yourmembership.com/reference/2_03/Methods.htm)
- [Adding a new backend for python-social-auth](http://psa.matiasaguirre.net/docs/backends/implementation.html)

## Install

**Note: You need to have a working project using python-social-auth. This plugin is only adding a new backend for it.**

Run the following codes in your virtualenv of python (2 and 3 both aupported).

    git clone https://github.com/Yexiaoxing/python-social-yourmembership/
    python setup.py install

Add a new social backend and related settings to the setting (use flask as example):

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = ('backends.yourmembership.YourMembershipAuth')
    SOCIAL_AUTH_YOURMEMBERSHIP_KEY = 'Your API Key Here'
    SOCIAL_AUTH_YOURMEMBERSHIP_SECRET = 'Your Private Key. You may leave it empty if you are not using sa. functions.'
    
Add a link to the login page in your template, for example:

    <a href="{{ url_for("social.auth", backend="yourmembership") }}">YourMembership Auth</a> <br />

You are all done!

## Integrating with Mailman 3

Run the following codes in your virtualenv of python 2 (the running venv of the web interface).

    git clone https://github.com/Yexiaoxing/python-social-yourmembership/
    python setup.py install

In settings_local.py, add the following lines

    AUTHENTICATION_BACKENDS = (
        'backends.yourmembership.YourMembershipAuth',
        #'social.backends.open_id.OpenIdAuth',
        # http://python-social-auth.readthedocs.org/en/latest/backends/google.html
        'social.backends.google.GoogleOpenId',
        #'social.backends.google.GoogleOAuth2',
        #'social.backends.twitter.TwitterOAuth',
        'social.backends.yahoo.YahooOpenId',
        # BrowserID is off.
        #'django_browserid.auth.BrowserIDBackend',
        'django.contrib.auth.backends.ModelBackend',
    )
    
    SOCIAL_AUTH_YOURMEMBERSHIP_KEY = 'Your API Key Here'
    SOCIAL_AUTH_YOURMEMBERSHIP_SECRET = 'Your Private Key. You may leave it empty if you are not using sa. functions.'
    
    # Disable authentication with the internal user database, optional
    USE_INTERNAL_AUTH = False

Add one logo of the ym backend in static_path/hyperkitty/img/login/ called yourmembership.png

Note: If you are using mailman-bundler, it is time to update HyperKitty to 1.0.4. 

All done. Have a test now.
