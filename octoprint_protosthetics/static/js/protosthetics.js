/*
 * View model for OctoPrint-Helloworld
 *
 * Author: Aaron Burton
 * License: AGPLv3
 */
$(function() {
    function HelloworldViewModel(parameters) {
        var self = this;
		console.log("this much is working");
		
		self.moreWords = ko.observable("Ready");
		//self.words = ko.observable("Is it Christmas?");

		self.onDataUpdaterPluginMessage = function(plugin, data) {
			if (plugin != "helloworld") {
				return;
			}
			console.log("a message from helloworld");
			if (data == "PRESS!!") {
				self.moreWords("press");
				console.log("button pressed");
			}
			if (data == "RELEASE") {
				self.moreWords("release");
				console.log("button released");
			}
			if (data == "HELD") {
				self.moreWords("held");
				console.log("holding");
				
			}
		}
		self.coolJSfunction = function() {
		  console.log("Cool button was clicked");
		  OctoPrint.simpleApiGet("helloworld");
		}
    }
	
	

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: HelloworldViewModel,
        dependencies: [ ], // "settingsViewModel"  ],
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        // Elements to bind to, e.g. #settings_plugin_helloworld, #tab_plugin_helloworld, ...
        elements: [ "#navbar_plugin_helloworld" , "#settings_plugin_helloworld" ]
    });
});
