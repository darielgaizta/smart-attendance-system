from dataclasses import dataclass
from getpass import getpass

import requests
import pathlib
import json

@dataclass
class JwtClient:
	access: str = None
	refresh: str = None

	# Make sure this matches the simplejwt config
	header_type: str = 'Bearer'

	# Make sure to have Django running on 8000
	base_endpoint = 'http://localhost:8000/api'

	# Fullpath for storing the credentials token (insecure)
	cred_path: pathlib.Path = pathlib.Path('creds.json')

	def __post_init__(self):
		if self.cred_path.exists():
			# Verifiy or refresh token in existing creds.json
			# If that fails, restart log in process
			try:
				data = json.loads(self.cred_path.read_text())
			except Exception as e:
				print('Cred has been tampered')
				data = None

			if data:
				self.access, self.refresh = data.get('access'), data.get('refresh')

				# Verify access token --> Boolean
				token_verified = self.verify_token()

				if not token_verified:
					# If token is invalid or has expired, refresh token
					refreshed = self.perform_refresh()

					if not refreshed:
						# If token refresh failed, perform login
						print('Invalid data, log in again.')
						self.clear_tokens()
						self.perform_auth()
			else:
				# Clear creds.json and log in again
				self.clear_tokens()
				self.perform_auth()
		else:
			# Log in process
			self.perform_auth()

	# Get default headers for HTTP requests including the JWT token
	def get_headers(self, header_type=None):
		_type = header_type or self.header_type
		token = self.access

		if token:
			return { 'Authorization': f'{_type} {token}' }
		return { }

	# Perform authentication without exposing password
	def perform_auth(self):
		# Define the endpoint to log in
		endpoint = f'{self.base_endpoint}/token/'

		username = input('What is your username?\n')
		password = getpass('What is your password?\n')

		data = {
			'username': username,
			'password': password
		}

		# When logged in, server will send response of access and refresh token
		# Access token for accessing content, meanwhile refresh token for refreshing access token
		response = requests.post(endpoint, json=data)

		# If failed to POST to endpoint
		if response.status_code != 200:
			raise Exception(f'Access not granted: {response.text}')

		print('Access granted.')
		self.write_creds(response.json())

	# Store access and refresh token to creds.json locally
	def write_creds(self, data: dict):
		if self.cred_path:
			self.access, self.refresh = data.get('access'), data.get('refresh')
			if self.access and self.refresh:
				self.cred_path.write_text(json.dumps(data))

	# Verify access token, see if it works and sent status code 200
	def verify_token(self):
		data = {
			'token': f'{self.access}'
		}

		endpoint = f'{self.base_endpoint}/token/verify/'
		response = requests.post(endpoint, json=data)

		return response.status_code == 200

	# Remove any/all JWT token data from instance as well as store creds file
	def clear_tokens(self):
		self.access, self.refresh = None, None
		if self.cred_path.exists():
			self.cred_path.unlink()

	# Refresh access token using refresh token and authentication headers
	def perform_refresh(self):
		data = {
			'refresh': f'{self.refresh}'
		}

		endpoint = f'{self.base_endpoint}/token/refresh/'
		response = requests.post(endpoint, json=data, headers=self.get_headers())

		if response.status_code != 200:
			self.clear_tokens()
			return False

		refresh_data = response.json()

		# If the response does not contain access token
		if 'access' not in refresh_data:
			self.clear_tokens()
			return False

		new_data_token = {
			'access': refresh_data.get('access'),
			'refresh': self.refresh
		}

		self.write_creds(new_data_token)
		return True

if __name__ == '__main__':
	# Perform authentication immediately while instancing
	try:
		client = JwtClient()
		print(client.access)
		print('Authentication done.')
	except Exception as e:
		print(e)