# NSO Service with device groups and external integration

This example shows how an external HTTP call can be done in a NSO service, and to apply a configuration to a group of devices.

**For training purposes only, do not use this code as it is in production**

## Installation

In your NSO packages running directory clone the repo and run make

```bash
git clone https://github.com/CiscoSE/nso_svc_external_query.git
mv nso_svc_external_query api_group_example
cd src
make
```

After that is done, reload the packages in the NSO command line:

```bash
packages reload
```

Once the package is installed, you can get a web server running using the following command. Note that docker needs to be
running in advance

```bash
docker run -p 12345:80 -d sfloresk/api_description_server
```

## Contacts

* Santiago Flores Kanter - sfloresk@cisco.com