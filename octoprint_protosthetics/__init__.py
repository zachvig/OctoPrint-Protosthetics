from __future__ import absolute_import, unicode_literals
from gpiozero import Button, LED, DigitalOutputDevice
import time

import octoprint.plugin

class ProtostheticsPlugin(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.ProgressPlugin,
                       octoprint.plugin.StartupPlugin,
                       octoprint.plugin.ShutdownPlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.SimpleApiPlugin):
					   
  def __init__(self):
    self.button = Button(5, hold_time=3, pull_up=None, active_state=True)
    self.printer = DigitalOutputDevice(22, active_high=False, initial_value=True)
    self.led = LED(24, initial_value=True)
    self.button.when_pressed = self.buttonPress
    self.button.when_released = self.buttonRelease
    self.button.when_held = self.longPress
    self.mode = 0
	
  def on_after_startup(self):
    self._logger.info("hello world!!!")
    self.printer.off()
    time.sleep(1)
    self.printer.on()
    
  
  def on_shutdown():
    self.button.close()
    self.led.close()

  def get_settings_defaults(self):
    return dict(words="Is it Christmas?")

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
    
    
    if self.mode == "PAUSED":
      # break and continue (after filament change)
      self._printer.commands("M108")
      self._logger.info('Theoretically resuming')
    # if printing, do something different here
    elif self._printer.is_printing():
      # change filament command
      self._printer.commands("M600 B{}".format(3,))
      self._logger.info('Theoretically pausing')
    elif self._printer.is_ready():
      self._printer.set_temperature('tool0',100)
      # testing this out to see if it does things
    
  def on_api_get(self, request):
    if True:
        self.led.toggle()
        self._logger.info('GUI button pressed')
        self._logger.info(request)
	

__plugin_name__ = "☺ Protosthetics Plugin :-)"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = ProtostheticsPlugin()
