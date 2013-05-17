from distutils.core import setup

setup(name='mailgunapi-client',
      version='1.2',
      description='Python Wrapper around MailGun HTTP API',
      author='Zach Goldberg',
      author_email='zach@zachgoldberg.com',
      url='https://github.com/ZachGoldberg/mailgun-python-api',
      packages=[
          'mailgun',
          ],
      package_dir={
        'mailgun': 'mailgun/',
        },
      install_requires=[
        'requests',
          ],
      )
