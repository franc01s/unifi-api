unifi-api
=========

---

A rewrite of https://github.com/calmh/unifi-api, support for 4+ unifi versions.  
Usage of requests to simplify api calls 

Install
-------

    sudo pip install -U unifiapi

API Example
-----------

```python
from unifi.controller import Controller
c = Controller('192.168.1.99', 'admin', 'p4ssw0rd')
for ap in c.get_aps():
	print 'AP named %s with MAC %s' % (ap.get('name'), ap['mac'])
```

API
---

### `class Controller`

Interact with a UniFi controller.

Uses the JSON interface on port 8443 (HTTPS) to communicate with a UniFi
controller. Operations will raise unifi.controller.APIError on obvious
problems (such as login failure), but many errors (such as disconnecting a
nonexistant client) will go unreported.

### `__init__(self, host, username, password, site_id, verify)`

Create a Controller object.

 - `host`		-- the address of the controller host; IP or name
 - `username`	-- the username to log in with
 - `password`	-- the password to log in with
 -  `port`		-- the port of the controller host
 -  `site_id`	-- the site ID to connect to
 -  `verify`	-- check SSL certificate

### `block_client(self, mac)`

Add a client to the block list.

 - `mac` -- the MAC address of the client to block.

### `kick_client(self, mac)`

Disconnects a client, forcing them to reassociate. Useful when the
connection is of bad quality to force a rescan.

 - `mac` -- the MAC address of the client to disconnect.

### `authorize_guest(self, guest_mac, minutes, up_bandwidth=None, down_bandwidth=None, byte_quota=None, ap_mac=None)`

Authorize a guest based on his MAC address.

   - `guest_mac`     -- the guest MAC address : aa:bb:cc:dd:ee:ff
   - `minutes`      -- duration of the authorization in minutes
   - `up_bandwith`  -- up speed allowed in kbps (optional)
   - `down_bandwith` -- down speed allowed in kbps (optional)
   - `byte_quota`    -- quantity of bytes allowed in MB (optional)
   - `ap_mac`        -- access point MAC address (UniFi >= 3.x) (optional)

### `unauthorize_guest(self, guest_mac)`
Unauthorize a guest based on his MAC address.

  - `guest_mac` -- the guest MAC address : aa:bb:cc:dd:ee:ff


# TO DO


### `get_alerts(self)`

Return a list of Alerts.

### `get_alerts_unarchived(self)`

Return a list of unarchived Alerts.

### `get_events(self)`

Return a list of Events.

### `get_aps(self)`

Return a list of all AP:s, with significant information about each.

### `get_clients(self)`

Return a list of all active clients, with significant information about each.

### `get_statistics_last_24h(self)`

Return statistical data of the last 24h

### `get_statistics_24h(self, endtime)`

Return statistical data last 24h from endtime

 - `endtime` -- the last time of statistics.

### `get_users(self)`

Return a list of all known clients, with significant information about each.

### `get_user_groups(self)`

Return a list of user groups with its rate limiting settings.

### `get_wlan_conf(self)`

Return a list of configured WLANs with their configuration parameters.

### `restart_ap(self, mac)`

Restart an access point (by MAC).

 - `mac` -- the MAC address of the AP to restart.

### `restart_ap_name(self, name)`

Restart an access point (by name).

 - `name` -- the name address of the AP to restart.

### `unblock_client(self, mac)`

Remove a client from the block list.

 - `mac` -- the MAC address of the client to unblock.

### `archive_all_alerts(self)`

Archive all alerts of site.

### `create_backup(self)`

Tells the controller to create a backup archive that can be downloaded with download_backup() and
then  be used to restore a controller on another machine.

Remember that this puts significant load on a controller for some time (depending on the amount of users and managed APs).

### `get_backup(self, targetfile)`

Tells the controller to create a backup archive and downloads it to a file. It should have a .unf extension for later restore.

 - `targetfile` -- the target file name, you can also use a full path. Default creates unifi-backup.unf in the current directoy.


License
-------

MIT

