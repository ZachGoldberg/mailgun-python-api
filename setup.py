from distutils.core import setup

setup(name='mailgunapi-client',
      version='1.0',
      description='Python Wrapper around MailGun HTTP API',
      author='Zach Goldberg',
      author_email='zach@zachgoldberg.com',
      url='zachgoldberg.com',
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
