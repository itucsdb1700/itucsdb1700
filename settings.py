PORT = 5000
DEBUG = True

#the codes below are about the login page
SECRET_KEY = 'secret'
WTF_CSRF_ENABLED = True

PASSWORDS = {
  'admin': '$6$rounds=656000$NhjGHwap0iYnsrNW$Y0sK0vHaShrBy0Q62GN3TIMQFdcDV7u98tjntyJUfN4EzDGKCr28UaG838uHaRNVCATFomj.d6gc.a1107lZm1',
  'normaluser': '$6$rounds=627096$AscnqlDtN2bWotwE$2s38G2w3xupwFf7woYv8XTWvwYc9sBk7t0reSU0VLZhXQCd6FFjlkysWpy8eYL06SQGcMgFQfvuP2XRB/BeTb.'
}

ADMIN_USERS = ['admin']
