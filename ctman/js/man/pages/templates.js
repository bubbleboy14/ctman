CT.require("CT.all");
CT.require("CT.rte");
CT.require("core");
CT.require("user.core");
CT.require("man.util");
CT.require("man.injections");
CT.require("man.browsers.Section");
CT.require("man.browsers.Template");

CT.onload(function() {
	CT.initCore();
	var tophalf = CT.dom.div(null, "abs tophalf"),
		bottomhalf = CT.dom.div(null, "abs bottomhalf");
	CT.dom.setContent("ctmain", [
		tophalf,
		bottomhalf,
		man.util.sideslide()
	]);
	var secs = new man.browsers.Section({
		parent: bottomhalf
	});
	new man.browsers.Template({
		parent: tophalf,
		sections: secs
	});
});