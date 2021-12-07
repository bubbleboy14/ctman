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
	CT.db.setLimit(5000);
	var tophalf = CT.dom.div(null, "abs tophalf"),
		midrow = CT.dom.div(CT.dom.node("select a template",
			"center", "padded"), "abs midrow"),
		bottomhalf = CT.dom.div(null, "abs bottomhalf"),
		minmax = man.util.minmax(tophalf, midrow, bottomhalf);
	CT.dom.setMain([
		tophalf,
		midrow,
		bottomhalf,
		man.util.sideslide(),
		minmax
	]);
	midrow.onwheel = function(wevent) {
		midrow.firstChild.scrollLeft += wevent.deltaY;
		wevent.preventDefault();
		wevent.stopPropagation();
	};
	var secs = new man.browsers.Section({
		parent: bottomhalf
	});
	new man.browsers.Template({
		parent: tophalf,
		sections: secs,
		injections: midrow,
		onsection: minmax.bottom
	});
});