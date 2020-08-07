CT.require("CT.all");
CT.require("core");
CT.require("user.core");
CT.require("man.templates");

CT.onload(function() {
	CT.initCore();
	new man.templates.Browser();
});