from rest_framework.authentication import TokenAuthentication as BaseTokenAuth

# Recreate a new TokenAuthentication that inherits TokenAuthentication as BaseTokenAuth
# Purpose: To have a new keyword token (Bearer)
class TokenAuthentication(BaseTokenAuth):
	# Redefine the keyword for token
	keyword = 'Bearer'