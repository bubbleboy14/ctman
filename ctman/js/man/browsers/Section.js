man.browsers.Section = CT.Class({
	CLASSNAME: "man.browsers.Section",
	goodsecs: function(d, secs) {
		return true;
	},
	asec: function(d, n) {
		var sbro = this.opts.sections || this,
			nonoz = [d.key].concat(d.sections),
			goodsecs = this.goodsecs;
		nonoz = nonoz.concat(man.relations.ancestors(d.key));
		return function() {
			items = sbro._.items.filter(i => !nonoz.includes(i.key));
			items.length ? CT.modal.choice({
				prompt: "please select a section",
				data: items,
				style: "multiple-choice",
				cb: function(sz) {
					if (!goodsecs(d, sz)) return;
					d.sections = d.sections.concat(sz.map(s => s.key));
					CT.db.put({
						key: d.key,
						sections: d.sections
					}, n.refresh);
				}
			}) : alert('click "new section" to create a new section');
		};
	},
	move: function(key, d, shnode, e) {
		var options = [], freshies = this.refreshers;
		if (key != d.sections[0])
			options.push("up");
		options.push("remove");
		if (key != d.sections[d.sections.length - 1])
			options.push("down");
		CT.modal.choice({
			prompt: "shift or remove?",
			data: options,
			cb: function(move) {
				var i = CT.dom.childNum(shnode),
					el = d.sections.splice(i, 1)[0];
				if (move == "remove")
					shnode.remove();
				else if (move == "up") {
					d.sections.splice(i - 1, 0, el);
					shnode.parentNode.insertBefore(shnode, shnode.previousSibling);
				} else {
					d.sections.splice(i + 1, 0, el);
					if (shnode.nextSibling.nextSibling)
						shnode.parentNode.insertBefore(shnode, shnode.nextSibling.nextSibling);
					else
						shnode.parentNode.appendChild(shnode);
				}
				CT.db.put({
					key: d.key,
					sections: d.sections
				});
			}
		});
		e && e.stopPropagation();
	},
	section: function(key, d) {
		var oz = this.opts, n = CT.dom.div(null, "choice_cell", null, {
			onclick: function() {
				CT.dom.id("tl" + key).trigger();
				oz.onsection && oz.onsection();
			}
		}), mover = this.move;
		CT.db.one(key, function(s) { // meh shouldn't be necessary...
			CT.dom.setContent(n, [
//				CT.dom.button("move", e => mover(key, d, n, e), "right"),
				CT.dom.button("remove", function() {
					d.sections.splice(CT.dom.childNum(n), 1);
					n.remove();
					CT.db.put({
						key: d.key,
						sections: d.sections
					});
				}, "right"),
				s.name
			]);
		});
		return n;
	},
	sections: function(d) {
		var sec = this.section;
		return man.util.refresher("sections", "add section",
			n => this.asec(d, n), function() {
//				return d.sections.map(s => sec(s, d));
				return CT.dom.dragList(d.sections, k => sec(k, d), function(secs) {
					d.sections = secs;
					CT.db.put({
						key: d.key,
						sections: d.sections
					});
				});
			}, core.config.ctman.classes[d.modelName].sections);
	},
	secbutts: function(d) {
		var _ = this._;
		if (!d.key || !this.opts.secbutts) return;
		return CT.dom.div([
			CT.dom.checkboxAndLabel("headerless", d.headerless,
				null, null, "inline rmargined", function(cb) {
					_.edit({
						key: d.key,
						headerless: cb.checked
					});
				}
			),
			CT.dom.button("preview", function() {
				CT.net.post({
					spinner: true,
					path: "/_man",
					params: {
						key: d.key
					},
					cb: function(pdfurl) {
						CT.modal.modal([
							"your preview is ready!",
							CT.dom.link("click here to view", null,
								"/" + pdfurl, "centered block", null, null, true)
						]);
					}
				});
			})
		], "abs ctr bordered round shiftup");
	},
	choosevar: function(d, cb) {
		CT.modal.prompt({
			prompt: "what's the injection variable?",
			cb: cb
		})
	},
	injectors: function(d) {
		var cvar = this.choosevar;
		return CT.dom.div([
			CT.dom.button("inject variable", function() {
				cvar(d, function(ivar) {
					man.util.inject("{{" + ivar + "}}");
				});
			}),
			CT.dom.button("inject image", function() {
				man.relations.images(function(img) {
					man.util.inject("<img style='display: block; max-width: 100%' src='" + img + "'>");
				});
			}),
			man.tables.button()
		], "right");
	},
	view: function(d) {
		var _ = this._, mcfg = core.config.ctman, val;
		CT.dom.setContent(_.nodes.content, [
			this.secbutts(d),
			this.namer(d),
			man.util.form(d, "template", function(vals) {
				for (val in vals)
					d[val] = vals[val];
				_.edit(d.key ? CT.merge({
					key: d.key
				}, vals) : d);
			}, {
				description: ta => this.injectors(d)
			}),
			this.extra(d)
		]);
	},
	extra: function(d) {
		return d.key && [
			man.util.image(d),
			this.sections(d)
		];
	},
	defaults: function() {
		return {
			sections: []
		};
	},
	items: function(items) {
		man.relations.geneologize(items);
		man.relations.imaginate(items);
	},
	init: function(opts) {
		this.opts = CT.merge(opts, {
			owner: false,
			secbutts: true,
			modelName: "section",
			blurs: ["section name", "section title", "name that section"]
		}, this.opts);
		man.tables.init();
	}
}, CT.Browser);