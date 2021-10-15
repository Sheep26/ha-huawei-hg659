# 📶  huawei-hg659
Home Assistant presence detection for the Huawei HG659 router

**Maintenance Note:** I no longer have my trusty HG659, so I don't have any way of testing changes. Use at your own risk!

## Installation
To enable presence detection in Home Assistant, clone this repo in your installation's `custom_components` directory as `hg659`:

```console
$ git clone git@github.com:johnpaton/huawei-hg659.git custom_components/hg659
Cloning into 'custom_components/hg659'...
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 12 (delta 1), reused 7 (delta 0), pack-reused 0
Receiving objects: 100% (12/12), 5.36 KiB | 5.36 MiB/s, done.
Resolving deltas: 100% (1/1), done.
```

## Home Assistant configuration

Once you've installed the code, you need to configure 

```yaml
# configuration.yaml
device_tracker:
  - platform: hg659
    host: YOUR_GATEWAY_IP  # this is the IP of your touter
    username: !secret hg659_username
    password: !secret hg659_password
```
You can also set normal `device_tracker` settings like `interval_seconds` or `consider_home`. The login credentials should be stored in `secrets.yaml` and are just the credentials you use to log in to the router's interface:

```
# secrets.yaml
hg659_username: YOUR_USERNAME
hg659_password: YOUR_PASSWORD
```

Restart Home Assistant and you should be good to go! You will see `known_devices.yaml` start to get populated with devices matching those you see as connected to the network in the router's UI.

### Logging
If you want to keep an eye on the presence detection you can enable logging in your configuration file as well:
```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    custom_components.hg659: info
```

## Inspiration

The device tracker code is heavily inspired by the official [Huawei Router](https://github.com/home-assistant/core/tree/dev/homeassistant/components/huawei_router) device tracker, which you have undoubtedly encountered before finding this project.

The client for the HG659's API (especially the encoding & decoding of data) was inspired and informed by [ericyan/hg659](https://github.com/ericyan/hg659).
