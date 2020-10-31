CT.require("CT.all");
CT.require("core");
CT.require("user.core");
CT.require("man.util");
CT.require("man.dash");

CT.onload(function() {
	CT.initCore();
	CT.db.setLimit(1000);
	man.dash.init();
});