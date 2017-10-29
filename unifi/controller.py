# -*- coding: utf-8 -*-


import sys


import json
import logging
from time import time
from requests import Session

log = logging.getLogger(__name__)


class APIError(Exception):
    pass


class Controller:
    """Interact with a UniFi controller.

    Uses the JSON interface on port 8443 (HTTPS) to communicate with a UniFi
    controller. Operations will raise unifi.controller.APIError on obvious
    problems (such as login failure), but many errors (such as disconnecting a
    nonexistant client) will go unreported.

    >>> from unifi.controller import Controller
    >>> c = Controller('192.168.1.99', 'admin', 'p4ssw0rd')
    >>> for ap in c.get_aps():
    ...     print 'AP named %s with MAC %s' % (ap.get('name'), ap['mac'])
    ...
    AP named Study with MAC dc:9f:db:1a:59:07
    AP named Living Room with MAC dc:9f:db:1a:59:08
    AP named Garage with MAC dc:9f:db:1a:59:0b

    """

    def __init__(self, host, username, password, port=8443, site_id='default', verify=True):
        """Create a Controller object.

        Arguments:
            host     -- the address of the controller host; IP or name
            username -- the username to log in with
            password -- the password to log in with
            port     -- the port of the controller host
            site_id  -- the site ID to connect to (UniFi >= 3.x)
            verify   -- check SSL certificate; True or False

        """

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.site_id = site_id
        self.url = 'https://' + host + ':' + str(port) + '/'
        self.api_url = self.url + 'api/s/{site_id}/'.format(site_id=site_id)

        log.debug('Controller for %s', self.url)

        self.opener = Session()
        self.opener.verify = verify

        self._login()

    def __del__(self):
        if self.opener != None:
            self._logout()

    def _responsecheck(self, response):
        if 'meta' in response:
            if response['meta']['rc'] != 'ok':
                raise APIError(response['meta']['msg'])
        if 'data' in response:
            return response['data']
        else:
            return None

    def _login(self):
        log.debug('login() as %s', self.username)
        params = {'username': self.username, 'password': self.password}
        login_url = self.url
        login_url += 'api/login'
        res = self.opener.post(login_url, json=params)
        pass

    def _logout(self):
        log.debug('logout()')
        self.opener.get(self.url + 'logout')

    def _get(self, url, params=None):
        res = self.opener.get(url, params=params)
        return self._responsecheck(res.json())

    def _post(self, url, params=None):
        res = self.opener.post(url, json=params)
        return self._responsecheck(res.json())

    def get_clients(self):
        """Return a list of all active clients, with significant information about each."""

        return self._get(self.api_url + 'stat/sta')

    def authorize_guest(self, mac, minutes, up_bandwidth=None, down_bandwidth=None, byte_quota=None, ap_mac=None):
        """
        Authorize a client device
        required parameter <mac>     = client MAC address
        required parameter <minutes> = minutes (from now) until authorization expires
        optional parameter <up>      = upload speed limit in kbps
        optional parameter <down>    = download speed limit in kbps
        optional parameter <MBytes>  = data transfer limit in MB
        optional parameter <ap_mac>  = AP MAC address to which client is connected, should result in faster authorization
        """

        log.debug('authorize_guest() {mac} for {minutes} minutes'.format(mac=mac, minutes=minutes))
        json = {'cmd': 'authorize-guest', 'mac': mac, 'minutes': minutes}
        if up_bandwidth:
            json['up'] = up_bandwidth
        if down_bandwidth:
            json['down'] = down_bandwidth
        if byte_quota:
            json['bytes'] = byte_quota
        if ap_mac and self.version != 'v2':
            json['ap_mac'] = ap_mac

        return self._post(self.api_url + 'cmd/stamgr', json)

    def unauthorize_guest(self, mac):
        """"
        Unauthorize a client device
        required parameter <mac>     = client MAC address

        """

        log.debug('unauthorize_guest() {mac}'.format(mac=mac))
        json = {'cmd': 'unauthorize-guest', 'mac': mac}

        return self._post(self.api_url + 'cmd/stamgr', json)

    def kick_sta(self, mac):
        """"
        Kick a client device
        required parameter <mac>     = client MAC address

        """

        log.debug('kick_sta() {mac}'.format(mac=mac))
        json = {'cmd': 'kick-sta', 'mac': mac}

        return self._post(self.api_url + 'cmd/stamgr', json)

    def block_sta(self, mac):
        """"
        Block a client device
        required parameter <mac>     = client MAC address
        """

        log.debug('block_sta() {mac}'.format(mac=mac))
        json = {'cmd': 'block-sta', 'mac': mac}

        return self._post(self.api_url + 'cmd/stamgr', json)

    def unblock_sta(self, mac):
        """"
        Unblock a client device
        required parameter <mac>     = client MAC address
        """

        log.debug('unblock_sta() {mac}'.format(mac=mac))
        json = {'cmd': 'unblock-sta', 'mac': mac}

        return self._post(self.api_url + 'cmd/stamgr', json)

