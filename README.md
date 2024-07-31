# Weishaupt_modbus

This integration lets you monitor and controll your weishaupt heatpump through modbus
This is how it might look:
![Bildschirmfoto vom 2024-07-31 21-41-56](https://github.com/user-attachments/assets/3fde9b18-f9ea-4e75-94ee-25ef6f799dcf)

## Installation

### Install through HACS 

- Not working yet

### HACS (manually add Repository)

Add this repository to HACS.
* In the HACS GUI, select "Custom repositories"
* Enter the following repository URL: https://github.com/MadOne/weishaupt_modbus/releases
* Category: Integration
* After adding the integration, restart Home Assistant.
* Now under Configuration -> Integrations, "Weishaupt Modbus Integration" should be available.

### Manual install

Create a directory called `weishaupt_modbus` in the `<config directory>/custom_components/` directory on your Home Assistant
instance. Install this component by copying all files in `/custom_components/weishaupt_modbus/` folder from this repo into the
new `<config directory>/custom_components/weishaupt-modbus/` directory you just created.

This is how your custom_components directory should look like:

```bash
custom_components
├── weishaupt_modbus
│   ├── __init__.py
│   ├── ...
│   ├── ...
│   ├── ...
│   └── wp.py  
```


