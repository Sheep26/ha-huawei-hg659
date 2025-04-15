import re
import json

import requests
from bs4 import BeautifulSoup

import hashlib
import base64 as b64

_WHITESPACE_RX = re.compile(r"\s")

def base64(s):
    #Base64 encode a string, removing all whitespace from the output.
    encoded = b64.encodebytes(s.encode()).decode()
    return _WHITESPACE_RX.sub("", encoded)  # remove all whitespace

def sha256(s):
    #Encode a string into its SHA256 hex digest
    return hashlib.sha256(s.encode()).hexdigest()

class HG659Client:
    _response_data_rx = re.compile(r"/\*(.*)\*/$")

    def __init__(self, host, username, password):
        """
        A client for the Huawei HG659 router.

        :param host: The IP of the router, e.g. "192.168.1.1"
        :param username: The login username
        :param password: The login password
        """
        self.host = host
        self.username = username
        self.password = password

        self._csrf_param = None
        self._csrf_token = None

        # Always use session to maintain cookies
        self._session = requests.Session()

        # init csrf state
        self._refresh_csrf()

    def login(self):
        """
        Log the client in to the router.

        While logged in, the same user cannot log in to the web
        interface. Call .logout() to log back out and unblock the web
        interface again

        :return: The response data from the login attempt
        """
        self._refresh_csrf()
        data = self._auth_data()
        response = self._post("/api/system/user_login", json=data)
        output = self._extract_json(response.text)

        return output

    def logout(self):
        """
        Log the client out of the router

        :return: The response status of the logout request
        """
        data = self._csrf_data()
        response = self._post("/api/system/user_logout", json=data)
        return response.status_code

    def get_device_count(self) -> int:
        response = self._get("/api/system/device_count")
        output = self._extract_json(response.text)
        
        return int(output["ActiveDeviceNumbers"])
        #return sum(1 for d in self.get_devices() if d["Active"])
    
    def get_device_info(self):
        response = self._get("/api/system/deviceinfo")
        output = self._extract_json(response.text)
        
        return output
    
    def get_wifi_info(self):
        response = self._get("/api/system/wizard_wifi")
        output = self._extract_json(response.text)
        
        return output
    
    def get_network_info(self):
        response = self._get("/api/system/diagnose_internet")
        output = self._extract_json(response.text)
        
        return output
    
    def get_wan_st(self):
        response = self._get("/api/ntwk/wan_st", json=self._auth_data())
        output = self._extract_json(response.text)
        
        return output
    
    def get_connected(self):
        return self.get_network_info()["ConnectionStatus"]
    
    def get_external_ip_addr(self):
        return self.get_network_info()["ExternalIPAddress"]
    
    def get_active_devices(self):
        return [
            d
            for d in self.get_devices()
            if d["Active"]
        ]
    
    def get_devices(self):
        """
        List all devices known to the router

        :return: A list of dicts containing device info
        """
        response = self._get("/api/system/HostInfo")
        output = self._extract_json(response.text)
        return output
    
    def get_uptime(self):
        # Get uptime.
        return int(self.get_device_info()["UpTime"])

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = base64(sha256(value))

    def _request(self, method, path, **kwargs):
        url = f"http://{self.host}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", 2)

        response = self._session.request(method, url, **kwargs,)

        param, token = self._extract_csrf(response.text)
        if param and token:
            self._csrf_param = param
            self._csrf_token = token

        return response

    def _get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)

    def _post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)

    def _refresh_csrf(self):
        self._get("/", timeout=1)

    @staticmethod
    def _extract_csrf(response_text):
        """Extract the csrf tokens from an HTML response"""
        param, token = None, None
        soup = BeautifulSoup(response_text, features="html.parser")

        param_elem = soup.find("meta", attrs={"name": "csrf_param"})
        if param_elem:
            param = param_elem.attrs.get("content")

        token_elem = soup.find("meta", attrs={"name": "csrf_token"})
        if token_elem:
            token = token_elem.attrs.get("content")

        return param, token

    @classmethod
    def _extract_json(cls, response_text):
        """Extract the json data from an api response"""
        match = cls._response_data_rx.search(response_text)
        if not match:
            return None
        return json.loads(match.group(1))

    def _encode_password(self):
        return sha256(
            self.username + self.password + self._csrf_param + self._csrf_token
        )

    def _csrf_data(self):
        return dict(csrf=dict(csrf_param=self._csrf_param, csrf_token=self._csrf_token))

    def _auth_data(self):
        data = self._csrf_data()
        data.update(
            dict(data=dict(UserName=self.username, Password=self._encode_password()))
        )
        return data

    def __del__(self):
        try:
            self.logout()
            self._session.close()
        except Exception as e:
            pass
