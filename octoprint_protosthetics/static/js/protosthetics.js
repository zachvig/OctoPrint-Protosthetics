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
		self.printerStatus = ko.observable("Printer ON?");
		self.dryerStatus = ko.observable("Dryer ON?");
		self.buttonStatus = ko.observable("Ready");
		self.lightStatus = ko.observable("Lights ON?");

		self.moreWords.subscribe(function(newValue) {
			console.log(newValue);
			OctoPrint.simpleApiCommand("protosthetics","passSerial",{"payload": newValue});
		});
		
		self.onDataUpdaterPluginMessage = function(plugin, data) {
			if (plugin != "protosthetics") {
				return;
			}
			//console.log("a message from protosthetics≈ " + data);
			if (data.startsWith("ERROR≈")){
				alert(data.substring(6));
			} else if (data.startsWith("L")){
				if (data[1]=="1") {
					self.lightStatus("Lights ON");
				} else if (data[1]=="0") {
					self.lightStatus("Lights OFF");
				}
			} else if (data.startsWith("D")){
				if (data[1]=="1") {
					self.dryerStatus("Dryer ON");
				} else if (data[1]=="0") {
					self.dryerStatus("Dryer OFF");
				}
			} else if (data.startsWith("P")){
				if (data[1]=="1") {
					self.printerStatus("Printer ON");
				} else if (data[1]=="0") {
					self.printerStatus("Printer OFF");
				}
			} else if (data.startsWith("B")) {
				if (data[1]=="0") {
				  self.buttonStatus("press");
				} else if (data[1] == "1") {
				  self.buttonStatus("release");
				} else if (data[1] == "2") {
			      self.buttonStatus("held");
				}
			} else {
				console.log(data);
			}
		}
		self.lightButtonFunction = function() {
		  //console.log("Light button was clicked");
		  OctoPrint.simpleApiCommand("protosthetics","lightToggle");
		}
		
		self.dryerButtonFunction = function() {
			//console.log("Dryer button was clicked");
			OctoPrint.simpleApiCommand("protosthetics","dryerToggle");
		}
		
		self.printerPowerFunction = function() {
			//console.log("Other Button was pressed");
			OctoPrint.simpleApiCommand("protosthetics","printerToggle");
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
