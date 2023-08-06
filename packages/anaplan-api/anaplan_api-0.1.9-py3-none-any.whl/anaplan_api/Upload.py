#===============================================================================
# Created:			1 Nov 2021
# @author:			Jesse Wilson (Anaplan Asia Pte Ltd)
# Description:		Abstract Anaplan Authentication Class
# Input:			Username & Password, or SHA keypair
# Output:			Anaplan JWT and token expiry time
#===============================================================================
import json, logging, requests, re
from typing import List
from requests.exceptions import HTTPError, ConnectionError, SSLError, Timeout, ConnectTimeout, ReadTimeout
from anaplan_api.AnaplanConnection import AnaplanConnection

logger = logging.getLogger(__name__)


class Upload(object):

	authorization: str
	workspace: str
	model: str
	file_id: str

	base_url = "https://api.anaplan.com/2/0/workspaces"

	def __init__(self, conn: AnaplanConnection, file_id: str):
		self.authorization = conn.get_auth()
		self.workspace = conn.get_workspace()
		self.model = conn.get_model()
		self.file_id = file_id

	def get_base_url(self) -> str:
		return self.base_url

	def get_workspace(self) -> str:
		return self.workspace

	def get_model(self) -> str:
		return self.model

	def get_file_id(self) -> str:
		return self.file_id

	def upload():
		pass

	def file_metadata(self, url: str) -> bool:

		authorization = self.authorization
		file_id = self.file_id

		post_header = {
						"Authorization": authorization,
						"Content-Type":"application/json"
			}

		stream_metadata = {
							"id": file_id,
							"chunkCount":-1
			}

		meta_post = None
		try:
			logger.debug("Updating file metadata.")
			meta_post = requests.post(url, headers=post_header, json=stream_metadata, timeout=(5,30))
			logger.debug("Complete!")
		except (HTTPError, ConnectionError, SSLError, Timeout, ConnectTimeout, ReadTimeout) as e:
			logger.error(f"Error setting metadata {e}")

		if meta_post.ok:
			return True
		else:
			return False

	def file_data(self, url: str, chunk_num: int, data) -> bool:

		authorization = self.authorization

		put_header = {
						"Authorization": authorization,
						"Content-Type":"application/octet-stream"
			}

		stream_upload = None
		try:
			logger.debug(f"Attempting to upload chunk {chunk_num + 1}")
			stream_upload = requests.put(url, headers=put_header, data=data, timeout=(5,30))
			logger.debug(f"Chunk {chunk_num + 1} uploaded successfully.")
		except (HTTPError, ConnectionError, SSLError, Timeout, ConnectTimeout, ReadTimeout) as e:
			logger.error(f"Error uploading chunk {chunk_num + 1}, {e}")

		if stream_upload.ok:
			return True
		else:
			return False
