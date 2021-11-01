from __future__ import absolute_import, unicode_literals
from gpiozero import Button, LED

import octoprint.plugin

class HelloWorldPlugin(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.StartupPlugin,
                       octoprint.plugin.SettingsPlugin):
					   
  def __init__(self):
    self.test = 42
    self.button = Button(5)
    self.led = LED(22)
    self.button.when_pressed = self.buttonPress
    self.button.when_released = self.led.on
	
  def on_after_startup(self):
    self._logger.info("hello world!!!")

  def get_settings_defaults(self):
    return dict(words="Is it Christmas?")

  def get_template_vars(self):
    return dict(words=self._settings.get(["words"]),
	            test=self.button.is_pressed)

  def get_template_configs(self):
    return [
      dict(type="navbar", custom_bindings=False, data_bind=self.test),
      dict(type="settings", custom_bindings=False)
    ]
  
  def get_assets(self):
    return {
      "js": ["js/helloworld.js"]
    }

  def buttonPress(self):
    self.led.off()
    self._plugin_manager.send_plugin_message(self._identifier, 'PRESS!!')
    self.on_settings_save(dict(test="wow!"))
    self._logger.info("pressed")
    self.test += 1
	
  def buttonRelease(self):
    self.led.on()
    self._plugin_manager.send_plugin_message(self._identifier, 'RELEASE')
	

__plugin_name__ = "Hey there"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = HelloWorldPlugin()
