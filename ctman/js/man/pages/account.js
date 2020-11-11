CT.require("CT.all");
CT.require("CT.pay");
CT.require("core");
CT.require("user.core");
CT.require("man.util");
CT.require("man.account");

CT.onload(function() {
	CT.initCore();
	man.account.init();
});