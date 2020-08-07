man.browsers.Template = CT.Class({
	CLASSNAME: "man.browsers.Template",
	init: function(opts) { // requires opts.sections
		this.opts = CT.merge(opts, {
			owner: true,
			modelName: "template",
			blurs: ["template name", "template title", "name that template"]
		}, this.opts);
	}
}, man.browsers.Section);