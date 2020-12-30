# iKamand


**This component will set up the following platforms.**

| Platform        | Description                                                               |
| --------------- | ------------------------------------------------------------------------- |
| `sensor`        | Show info from iKamand. |
| `climate`       | Control the iKamand. |


## Installation

### HACS
1. Add this repository as a cutom repository in HACS
2. Install iKamand
3. Add config into configuration.yaml as per below config section.
4. Restart HA

### Custom

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `ikamand`.
4. Download _all_ the files from the `custom_components/ikamand/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add the config into configuration.yaml
7. Restart Home Assistant


## Configuration

```
ikamand:
  ip_address: <iKamand IP Address>
```

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template


