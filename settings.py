PORT = 5000
DEBUG = True

#the codes below are about the login page
SECRET_KEY = 'secret'
WTF_CSRF_ENABLED = True

PASSWORDS = {
  'admin': '$6$rounds=702382$2wkwLY3/D2qLgX7K$tAQC6L3G8D/GWHzx5FQIP/4.LtSNT/q5KG0avCcf0MKsRucwUXCW.nhmjkpkVaSCbvb1QOQJz321fKZ0DxSJP/',
  'normaluser': '$6$rounds=627096$AscnqlDtN2bWotwE$2s38G2w3xupwFf7woYv8XTWvwYc9sBk7t0reSU0VLZhXQCd6FFjlkysWpy8eYL06SQGcMgFQfvuP2XRB/BeTb.'
}

ADMIN_USERS = ['admin']
