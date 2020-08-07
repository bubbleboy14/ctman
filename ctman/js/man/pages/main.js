CT.require("CT.all");
CT.require("core");
CT.require("user.core");
CT.require("man.util");
CT.require("man.browsers.Document");

CT.onload(function() {
	CT.initCore();
	new man.browsers.Document();
});