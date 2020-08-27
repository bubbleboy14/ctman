man.browsers.Template = CT.Class({
	CLASSNAME: "man.browsers.Template",
	extra: function(d) {
		return d.key && [
			this.sections(d),
			man.injections.editor(d)
		];
	},
	init: function(opts) { // requires opts.sections
		this.opts = CT.merge(opts, {
			owner: true,
			headerlessness: false,
			modelName: "template",
			blurs: ["template name", "template title", "name that template"]
		}, this.opts);
		man.injections.init();
	}
}, man.browsers.Section);