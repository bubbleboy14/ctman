man.browsers.Section = CT.Class({
	CLASSNAME: "man.browsers.Section",
	init: function(opts) {
		this.opts = CT.merge(opts, {
			owner: false,
			modelName: "section",
			blurs: ["section name", "section title", "name that section"]
		}, this.opts);
	}
}, man.browsers.Template);