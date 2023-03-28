CT.require("CT.all");
CT.require("core");
CT.require("user.core");
CT.require("man.util");
CT.ruquire("man.builder");
CT.require("man.injections");
CT.require("man.browsers.Document");

CT.onload(function() {
	CT.initCore();
	CT.db.setLimit(1000);
	man.util.current.browser = new man.browsers.Document();
});