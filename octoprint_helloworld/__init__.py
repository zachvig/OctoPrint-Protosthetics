from __future__ import absolute_import, unicode_literals
from gpiozero import Button

import octoprint.plugin

class HelloWorldPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin):
					   
  def __init__(self):
    self.test = 42
    self.button = Button(5)
	
  def on_after_startup(self):
    self._logger.info("hello world!!!")

  def get_settings_defaults(self):
    return dict(words="Is it Christmas?")

  def get_template_vars(self):
    return dict(words=self._settings.get(["words"]),
	            test=self.button.is_pressed)

  def get_template_configs(self):
    return [
      dict(type="navbar", custom_bindings=False),
      dict(type="settings", custom_bindings=False)
    ]

__plugin_name__ = "Hey there"
__plugin_pythoncompat__ = ">=3,<4"
__plugin_implementation__ = HelloWorldPlugin()
