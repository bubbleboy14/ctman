CT.require("CT.all");
CT.require("CT.rte");
CT.require("core");
CT.require("user.core");
CT.require("man.util");
CT.require("man.tables");
CT.require("man.relations");
CT.require("man.injections");
CT.require("man.browsers.Section");
CT.require("man.browsers.Template");

CT.onload(function() {
	CT.initCore();
	CT.db.setLimit(1000);
	var tophalf = CT.dom.div(null, "abs tophalf"),
		bottomhalf = CT.dom.div(null, "abs bottomhalf"),
		minmax = man.util.minmax(tophalf, bottomhalf);
	CT.dom.setContent("ctmain", [
		tophalf,
		bottomhalf,
		man.util.sideslide(),
		minmax
	]);
	var secs = new man.browsers.Section({
		parent: bottomhalf
	});
	new man.browsers.Template({
		parent: tophalf,
		sections: secs,
		onsection: minmax.bottom
	});
});