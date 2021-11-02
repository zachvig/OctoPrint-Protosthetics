from __future__ import absolute_import, unicode_literals
from gpiozero import Button, LED

import octoprint.plugin

class HelloWorldPlugin(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.StartupPlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.SimpleApiPlugin):
					   
  def __init__(self):
    self.test = 42
    self.button = Button(5, hold_time=3)
    self.led = LED(22)
    self.button.when_pressed = self.buttonPress
    self.button.when_released = self.buttonRelease
    self.button.when_held = self.longPress
	
  def on_after_startup(self):
    self._logger.info("hello world!!!")

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
    self._plugin_manager.send_plugin_message(self._identifier, 'PRESS!!')
    self.on_settings_save(dict(test="wow!"))
    self._logger.info("pressed")
    self.test += 1
	
  def buttonPress(self):
    self.led.on()
    self._plugin_manager.send_plugin_message(self._identifier, 'RELEASE')
    
  def longPress(self):
    self._plugin_manager.send_plugin_message(self._identifier, 'HELD')
    self.led.blink(0.1,0.1,5)
    self._printer.set_temperature('tool0',100)
    
  def on_api_get(self, request):
    if True:
        self.led.toggle()
        self._logger.info('GUI button pressed')
        self._logger.info(request)
	

__plugin_name__ = "Hey there"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = HelloWorldPlugin()
