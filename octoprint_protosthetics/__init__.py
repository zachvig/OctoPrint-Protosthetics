from __future__ import absolute_import, unicode_literals
from gpiozero import Button, LED, DigitalOutputDevice
import time, os, serial

import octoprint.plugin

class ProtostheticsPlugin(octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.ProgressPlugin,
                       octoprint.plugin.EventHandlerPlugin,
                       #octoprint.plugin.StartupPlugin,
                       octoprint.plugin.ShutdownPlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.SimpleApiPlugin):
					   
  def __init__(self):
    self.button1 = Button(4, hold_time=3, pull_up=None, active_state=True)
    self.button2 = Button(5, hold_time=3, pull_up=None, active_state=True)
    self.button3 = Button(6, hold_time=3, pull_up=None, active_state=True)
    self.printer = DigitalOutputDevice(22, active_high=False, initial_value=True)
    self.dryer   = DigitalOutputDevice(23, active_high=True, initial_value=False)
    self.led = LED(12, initial_value=True)
    self.flash = DigitalOutputDevice(17, active_high=False, initial_value=False)
    self.ESPreset = DigitalOutputDevice(16, active_high=False, initial_value=False)
    
    self.button1.when_pressed = self.buttonPress
    self.button1.when_released = self.buttonRelease
    self.button1.when_held = self.longPress
    self.custom_mode = 0
    try:
      self.com = serial.Serial('/dev/ttyS0', 9600)
      self.hasSerial = True
    except: #what exception goes here?
      self._logger.warning("No connection to LED controller.  Check raspi-config settings.")
      self.hasSerial = False
    self.send('P3') #plasma
    self.send('C0') #Ocean colors
  '''	
  def on_after_startup(self):
    self._logger.info("hello world!!!")
    #self.printer.off()
    #time.sleep(3)
    #self.printer.on()
  '''    
  
  def on_shutdown():
    self.button.close()
    self.led.close()
    self.printer.close()
    self.dryer.close()
  
  def get_settings_defaults(self):
    return dict(words="Is it ☺")
  
  
  def get_template_vars(self):
    return dict(words=self._settings.get(["words"]),
	            test=self.button1.is_pressed)
  

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
    if progress == 100:
      # don't send (use print_done event instead)
      return
    self.send('P8') #progress bar with plasma
    self.send('D%i' %progress)

  # Button status: B?
  # where ? is 0 for press, 1 for release, 2 for held
  def buttonRelease(self):
    self.led.off()
    self._plugin_manager.send_plugin_message(self._identifier, 'B1')
    self._plugin_manager.send_plugin_message(self._identifier, 'L%i' %self.led.value)
	
  def buttonPress(self):
    self.led.on()
    
    self._plugin_manager.send_plugin_message(self._identifier, 'L%i' %self.led.value)
    
  def longPress(self):
    self._plugin_manager.send_plugin_message(self._identifier, 'B2')
    self.led.blink(0.05,0.05,5)  #change this to be LED indicator
    self._plugin_manager.send_plugin_message(self._identifier, 'L%i' %self.led.value)
    self._logger.info('~~~~~~~~~~~~~~~~~~~~~~')
    self.mode = self._printer.get_state_id()
    self._logger.info(self.mode)
    
    
    if self.mode == "PAUSED" or self.mode == "PAUSING" or self.custom_mode == "PAUSED":
      # break and continue (after filament change)
      self._printer.commands("M108")
      #self._printer.resume_print()
      self._logger.info('Theoretically resuming')
      self._logger.info(self.custom_mode)
      if self.custom_mode:
        self.custom_mode = 0
        self._printer.set_temperature('tool0',self.whatItWas)
        self.led.on()
    # if printing, do something different here
    elif self._printer.is_printing():
      # change filament command
      self._printer.commands("M600")
      self._logger.info('Theoretically pausing')
    elif self._printer.is_ready():
      temps = self._printer.get_current_temperatures()
      self.whatItWas = temps.get('tool0').get('target')
      self._logger.info(temps)
      self._logger.info(self.whatItWas)
      if temps.get('tool0').get('actual') < 200:
        if self.whatItWas < 200:
          #self._printer.set_temperature('tool0',220)
          self._printer.commands("M109 S220")
        else:
          self._printer.commands("M109 S%i" %self._printer.get_current_temperatures().get('tool0').get('target'))
      self._printer.commands("M600")
      self.led.on()
      self.custom_mode = "PAUSED"
        
        
   
        
  def send(self, data):
    if self.hasSerial:
      self.com.write((data + '\n').encode())
        
  def get_api_commands(self):
    return dict(
                  lightToggle=[],
                  dryerToggle=[],
                  printerToggle=[],
                  passSerial=['payload']
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
    elif command == 'printerToggle':
      self.printer.toggle()
      self._logger.info('Printer power button pressed')
      self._plugin_manager.send_plugin_message(self._identifier, 'P%i' %self.printer.value)
    elif command == 'passSerial':
      self.send(data.get('payload'))
      self._logger.info('Serial command sent')
               
  def on_event(self,event,payload):
    if event == octoprint.events.Events.PRINT_STARTED:
      self.send('C1')  #party colors
    if event == octoprint.events.Events.PRINT_DONE:
      self.send('P1')  #theater chase
    if event == octoprint.events.Events.PRINT_CANCELLED:
      self.send('P7')  #Fire
      self.send('C2')  #Lava colors
    if event == octoprint.events.Events.PRINT_FAILED:
      self._plugin_manager.send_plugin_message(self._identifier, 'ERROR≈Print Failed')
    if event == octoprint.events.Events.FILE_ADDED:
      self._logger.warning('FILE ADDED!!!' + payload.get('name'))
      if payload.get('name').endswith('.bin.gcode'):
        self._logger.info('Might be firmware')
        if not self._printer.is_ready():
          self._logger.warning("Do not try to upload new firmware while printing‼")
          return
        self._plugin_manager.send_plugin_message(self._identifier, 'new firmware found')
        uploads = '/home/pi/.octoprint/uploads'
        files = os.listdir(uploads)
        for file in files:
          if file.endswith('.bin.gcode'):
            os.system('mv '+uploads+'/'+file+' '+uploads+'/LEDfirmware.bin')
            
            self._plugin_manager.send_plugin_message(self._identifier, 'uploading new firmware!')
            # add the reset pin sequence here when the new hat
            self.flash.on()
            self.ESPreset.on()
            time.sleep(0.1)
            self.ESPreset.off()
            time.sleep(0.2)
            self._plugin_manager.send_plugin_message(self._identifier, 'Firmware started')
            os.system('esptool.py -p /dev/ttyS0 write_flash 0x00 '+uploads+'/LEDfirmware.bin')
            self._plugin_manager.send_plugin_message(self._identifier, 'Firmware uploaded')
            self.flash.off()
            self.ESPreset.on()
            time.sleep(0.1)
            self.ESPreset.off()
            break
	
  def get_update_information(self):
    return {
        "protosthetics": {
          'displayName': "Protosthetics Plugin",
          'displayVersion': self._plugin_version,
          'type': "github_release",
          'user': "aburtonProto",
          'repo': "OctoPrint-Protosthetics",
          'current': self._plugin_version,
          "stable_branch": {
                    "name": "Stable",
                    "branch": "master",
                    "comittish": ["master"],
                },
          'pip': "https://github.com/aburtonProto/OctoPrint-Protosthetics/archive/{target_version}.zip"
        }
    }
    
    
__plugin_name__ = "Protosthetics Plugin"
__plugin_pythoncompat__ = ">=3,<4"

__plugin_implementation__ = ProtostheticsPlugin()
__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}