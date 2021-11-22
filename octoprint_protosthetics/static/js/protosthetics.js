/*
 * View model for OctoPrint-Protosthetics
 *
 * Author: Aaron Burton
 * License: AGPLv3
 */
$(function() {
    function ProtostheticsViewModel(parameters) {
        var self = this;
		console.log("this much is working");
		
		self.moreWords = ko.observable("Ready");
		//self.words = ko.observable("Is it Christmas?");

		self.onDataUpdaterPluginMessage = function(plugin, data) {
			if (plugin != "protosthetics") {
				return;
			}
			console.log("a message from protosthetics");
			if (data == "PRESS!!") {
				self.moreWords("press");
				console.log("button pressed");
			}
			else if (data == "RELEASE") {
				self.moreWords("release");
				console.log("button released");
			}
			else if (data == "HELD") {
				self.moreWords("held");
				console.log("holding");
			}
			else {
				console.log(data);
			}
		}
		self.coolJSfunction = function() {
		  console.log("Cool button was clicked");
		  OctoPrint.simpleApiGet("protosthetics");
		}
    }
	
	

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: ProtostheticsViewModel,
        dependencies: [ ], // "settingsViewModel"  ],
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        // Elements to bind to, e.g. #settings_plugin_helloworld, #tab_plugin_helloworld, ...
        elements: [ "#navbar_plugin_protosthetics" , "#settings_plugin_protosthetics" ]
    });
});
