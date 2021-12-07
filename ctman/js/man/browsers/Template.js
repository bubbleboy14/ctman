man.browsers.Template = CT.Class({
	CLASSNAME: "man.browsers.Template",
	goodsecs: function(d, secs) {
		var newsecs = secs.filter(s => !d.sections.includes(s.key)),
			sinjs = man.injections.extract(newsecs),
			tinjs = CT.data.getSet(d.injections).map(i => i.name),
			bads = sinjs.filter(i => !tinjs.includes(i));
		return bads.length ? alert("For these Sections to render properly you will need to define insertion variables for the following: " + bads.join(", ")) : true;
	},
	choosevar: function(d, cb) {
		d.injections.length ? CT.modal.choice({
			prompt: "choose an insertion variable",
			data: d.injections.map(i => CT.data.get(i).name),
			cb: cb
		}) : alert("no insertion variables defined! please define some :)");
	},
	extra: function(d) {
		if (!d.key) return;
		var injed = man.injections.editor(d);
		CT.dom.setContent(this.opts.injections, injed);
		this.opts.injections.scroller = injed.getElementsByClassName("template_injections")[0];
		return this.sections(d);
	},
	items: function(items) {
		man.relations.geneologize(items);
	},
	init: function(opts) { // requires opts.sections
		this.opts = CT.merge(opts, {
			owner: true,
			secbutts: false,
			modelName: "template",
			blurs: ["template name", "template title", "name that template"]
		}, this.opts);
		man.injections.init();
	}
}, man.browsers.Section);