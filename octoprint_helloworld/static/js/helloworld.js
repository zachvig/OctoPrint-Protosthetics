/*
 * View model for OctoPrint-Helloworld
 *
 * Author: Aaron Burton
 * License: AGPLv3
 */
 console.log('the file loaded at least');
$(function() {
    function HelloworldViewModel(parameters) {
        var self = this;
		console.log("this much is working");
        self.settingsViewModel = parameters[0];
		console.log(self.settingsViewModel.settings);
		
		self.moreWords = ko.observable("something");
		self.words = ko.observable("nothing");


        // TODO: Implement your plugin's view model here.
		self.onDataUpdaterPluginMessage = function(plugin, data) {
			if (plugin != "helloworld") {
				return;
			}
			console.log("a message from helloworld");
			if (data == "PRESS!!") {
				self.moreWords("press");
				console.log("thing happened");
			}
			if (data == "RELEASE") {
				self.moreWords("release");
			}
		}
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: HelloworldViewModel,
        dependencies: [ "settingsViewModel"  ],
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        // Elements to bind to, e.g. #settings_plugin_helloworld, #tab_plugin_helloworld, ...
        elements: [ "#navbar_plugin_helloworld" ]//, "#settings_plugin_helloworld" ]
    });
});
