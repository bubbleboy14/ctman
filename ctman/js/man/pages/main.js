CT.require("CT.all");
CT.require("core");
CT.require("user.core");
CT.require("man.builder");

CT.onload(function() {
	CT.initCore();
	new man.builder.Browser();
});