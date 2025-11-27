{
    'name': 'Portal Login Redirect',
    'version': '1.0',
    'summary': 'Redirect portal user to /my after login',
    'description': """
Automatically redirect portal users to /my after successful login.
""",
    'author': 'Madhusudan Ray',
    'category': 'Website',
    'depends': ['web', 'portal', 'website'],
    'data': [
        # we don't need XML for redirect, but keeping folder for future
    ],
    'installable': True,
    'application': False,
}
