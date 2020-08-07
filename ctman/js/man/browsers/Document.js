man.browsers.Document = CT.Class({
	CLASSNAME: "man.browsers.Document",
	builder: function(d, n) {
		return function() {
			CT.net.post({
				path: "/_man",
				params: {
					key: d.key
				},
				cb: function(newd) {
					d.pdf = newd.pdf;
					n.refresh();
				}
			});
		};
	},
	build: function(d) {
		return man.util.refresher("pdf build",
			"click here to build/rebuild", n => this.builder(d, n),
			_ => d.pdf && CT.dom.link("click here to download",
				null, d.pdf, "block"));
	},
	hazards: function(d) {
		var hcfg = core.config.ctman.hazards.chemical,
			cz = CT.dom.choices(hcfg.map(h => CT.dom.div(h)), true),
			selz = d.assembly.hazards.chemical;
		selz && CT.dom.each(cz, function(sel) {
			if (selz.includes(sel.innerHTML))
				sel.onclick();
		});
		return cz;
	},
	swaptemp: function(d, n) {
		var _ = this._;
		return function() {
			_.templates.length ? CT.modal.choice({
				prompt: "please select a template",
				data: ["default (static)"].concat(_.templates),
				cb: function(tmp) {
					d.template = (tmp == "default (static)")
						? null : tmp.key;
					CT.db.put({
						key: d.key,
						template: d.template
					}, n.refresh);
				}
			}) : alert("create a template on the templates page");
		};
	},
	section: function(d) {
		return CT.dom.div([
			d.name,
			CT.dom.choices(d.sections.map(this.section), true)
		]);
	},
	sections: function(d) {
		if (!d.template) return CT.dom.div("default (static)", "centered");
		return this.section(CT.data.get(d.template));
	},
	template: function(d) {
		return man.util.refresher("template", "swap",
			n => this.swaptemp(d, n), _ => this.sections(d));
	},
	view: function(d) {
		var _ = this._, haz = this.hazards(d),
			mcfg = core.config.ctman, view = this.view;
		CT.dom.setContent(_.nodes.content, [
			CT.dom.div(d.name, "bigger centered"),
			this.template(d),
			CT.dom.div([
				"hazards",
				haz
			], "margined padded bordered round"),
			man.util.form(d, "injections", function(vals) {
				d.injections = vals;
				d.assembly = {
					hazards: {
						chemical: haz.value.map(v => mcfg.hazards.chemical[v])
					}
				};
				_.edit(d.key ? {
					key: d.key,
					assembly: d.assembly,
					injections: d.injections
				} : d);
			}),
			d.key && this.build(d)
		]);
	},
	defaults: function() {
		return {
			assembly: {
				hazards: {
					chemical: []
				}
			}
		};
	},
	init: function(opts) {
		var _ = this._;
		this.opts = CT.merge(opts, {
			modelName: "document",
			blurs: ["project name", "document title", "project/document name"]
		}, this.opts);
		CT.db.get("template", function(tz) {
			_.templates = tz;
		}, 1000, 0, null, null, null, null, "unrolled");
	}
}, CT.Browser);