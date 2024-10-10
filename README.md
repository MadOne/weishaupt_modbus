This is a fork from MadOne: https://github.com/MadOne/weishaupt_modbus/

I started to build a structure that finally will allow loading of the modbus structure from a file. 
As a first step, all modbus parameters will be concentrated in the file hpconst.py as a set of object lists.
This allows generic setup of all entities and a more easy completion of messages and entity behavior

# Weishaupt_modbus

This integration lets you monitor and controll your weishaupt heatpump through modbus.
This is how it might look:
![image](https://github.com/user-attachments/assets/00e7b8fa-1779-428d-9361-7c66e228c2c6)

## Installation

### HACS (manually add Repository)

Add this repository to HACS.
* In the HACS GUI, select "Custom repositories"
* Enter the following repository URL: https://github.com/OStrama/weishaupt_modbus/releases
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
## Configuration

![Bildschirmfoto vom 2024-07-31 21-46-18](https://github.com/user-attachments/assets/45ad403e-c721-40bd-b723-95fe05fca5c5)

Just enter the IP of your Weishaupt heatpump. Port should be ok at default unless you changed it in the Heatpump configuration.

You have to enable modbus in your heatpump settings. 


ToDo: Pictures and explanation of how to enable modbus
