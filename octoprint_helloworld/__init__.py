from __future__ import absolute_import, unicode_literals
from gpiozero import Button, LED

import octoprint.plugin

class HelloWorldPlugin(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.AssetPlugin,
                       #octoprint.plugin.StartupPlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.SimpleApiPlugin):
					   
  def __init__(self):
    self.button = Button(5, hold_time=3, pull_up=None, active_state=True)
    self.led = LED(22)
    self.button.when_pressed = self.buttonPress
    self.button.when_released = self.buttonRelease
    self.button.when_held = self.longPress
    self.mode = 0
	
  #def on_after_startup(self):
  #  self._logger.info("hello world!!!")

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
      "js": ["js/helloworld.js"]
    }

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
    
    # if printing, do something different here
    if self.mode == 'OPERATIONAL':
      self._printer.set_temperature('tool0',100)
      # when warm, retract filament
      # advance to next mode
    if self.mode == 'PRINTING':
      self._printer.script('M600')
    if self.mode == 'PAUSED':
      self._printer.script('M108')
    
  def on_api_get(self, request):
    if True:
        self.led.toggle()
        self._logger.info('GUI button pressed')
        self._logger.info(request)
	

__plugin_name__ = "Hey there"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = HelloWorldPlugin()
