from __future__ import absolute_import, unicode_literals
from gpiozero import Button, LED, DigitalOutputDevice
import time, os

import octoprint.plugin

class ProtostheticsPlugin(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.ProgressPlugin,
                       octoprint.plugin.EventHandlerPlugin,
                       octoprint.plugin.StartupPlugin,
                       octoprint.plugin.ShutdownPlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.SimpleApiPlugin):
					   
  def __init__(self):
    self.button = Button(4, hold_time=3, pull_up=None, active_state=True)
    self.printer = DigitalOutputDevice(22, active_high=False, initial_value=True)
    self.dryer   = DigitalOutputDevice(23, active_high=False, initial_value=True)
    self.led = LED(24, initial_value=True)  #will be 12 on new board
    self.button.when_pressed = self.buttonPress
    self.button.when_released = self.buttonRelease
    self.button.when_held = self.longPress
    self.mode = 0
	
  def on_after_startup(self):
    self._logger.info("hello world!!!")
    #self.printer.off()
    #time.sleep(3)
    #self.printer.on()
    
  
  def on_shutdown():
    self.button.close()
    self.led.close()
    self.printer.close()
    self.dryer.close()

  def get_settings_defaults(self):
    return dict(words="Is it ☺")

  def get_template_vars(self):
    return dict(words=self._settings.get(["words"]),
	            test=self.button.is_pressed)

  def get_template_configs(self):
    return [
      dict(type="navbar"),
      dict(type="settings", custom_bindings=True)
    ]
  
  def get_assets(self):
    return {
      "js": ["js/protosthetics.js"]
    }
    
  def on_print_progress(self,storage,path,progress):
    self._plugin_manager.send_plugin_message(self._identifier, str(progress))
    self._logger.warning(path)

  def buttonRelease(self):
    self.led.off()
    self._plugin_manager.send_plugin_message(self._identifier, 'RELEASE')
	
  def buttonPress(self):
    self.led.on()
    self._plugin_manager.send_plugin_message(self._identifier, 'PRESS!!')
    
  def longPress(self):
    self._plugin_manager.send_plugin_message(self._identifier, 'HELD')
    self.led.blink(0.05,0.05,5)
    self._logger.info('~~~~~~~~~~~~~~~~~~~~~~')
    self.mode = self._printer.get_state_id()
    self._logger.info(self.mode)
    
    
    if self.mode == "PAUSED" or self.mode == "PAUSING":
      # break and continue (after filament change)
      self._printer.commands("M108")
      #self._printer.resume_print()
      self._logger.info('Theoretically resuming')
    # if printing, do something different here
    elif self._printer.is_printing():
      # change filament command
      self._printer.commands("M600")
      self._logger.info('Theoretically pausing')
    elif self._printer.is_ready():
      self._printer.set_temperature('tool0',100)
      # testing this out to see if it does things
   
        
  def get_api_commands(self):
    return dict(
                  lightToggle=[],
                  dryerToggle=[],
                  powerToggle=[],
               )

  def on_api_command(self,command,data):
    self._logger.info(command+str(data))
    if command == 'lightToggle':
      self.led.toggle()
      self._logger.info('Light button pressed')
      self._plugin_manager.send_plugin_message(self._identifier, 'L%i' %self.led.value)
    elif command == 'dryerToggle':
      self.dryer.toggle()
      self._logger.info('Dryer button pressed')
      self._plugin_manager.send_plugin_message(self._identifier, 'D%i' %self.dryer.value)
    elif command == 'powerToggle':
      self.printer.toggle()
      self._logger.info('Printer power button pressed')
      self._plugin_manager.send_plugin_message(self._identifier, 'P%i' %self.printer.value)
               
  def on_event(self,event,payload):
    if event == octoprint.events.Events.FILE_ADDED:
      self._logger.warning('FILE ADDED!!!' + payload.get('name'))
      if payload.get('name').endswith('.bin.gcode'):
        self._logger.info('Might be firmware')
        if not self._printer.is_ready():
          self._logger.warning("Do not try to upload new firmware while printing‼")
          return
        self._plugin_manager.send_plugin_message(self._identifier, 'new firmware found?')
        uploads = '/home/pi/.octoprint/uploads'
        files = os.listdir(uploads)
        for file in files:
          if file.endswith('.bin.gcode'):
            os.system('mv '+uploads+'/'+file+' '+uploads+'/LEDfirmware.bin')
            self._plugin_manager.send_plugin_message(self._identifier, 'uploading new firmware!')
            # add the reset pin sequence here when the new hat
            os.system('esptool.py -p /dev/ttyS0 write_flash 0x00 '+uploads+'/LEDfirmware.bin')
	

__plugin_name__ = "☺ Protosthetics Plugin :-)"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = ProtostheticsPlugin()
