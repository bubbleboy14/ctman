man.browsers.Section = CT.Class({
	CLASSNAME: "man.browsers.Section",
	asec: function(d, n) {
		var sbro = this.opts.sections || this,
			nonoz = [d.key].concat(d.sections);
		return function() {
			items = sbro._.items.filter(i => !nonoz.includes(i.key));
			items.length ? CT.modal.choice({
				prompt: "please select a section",
				data: items,
				style: "multiple-choice",
				cb: function(sz) {
					d.sections = d.sections.concat(sz.map(s => s.key));
					CT.db.put({
						key: d.key,
						sections: d.sections
					}, n.refresh);
				}
			}) : alert('click "new section" to create a new section');
		};
	},
	move: function(key, d, shnode) {
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
	},
	section: function(key, d) {
		var s = CT.data.get(key), n = CT.dom.div([
			CT.dom.button("move", _ => this.move(key, d, n), "right"),
			s.name
		], "choice_cell", null, {
			onclick: function() {
				CT.dom.id("tl" + key).trigger();
			}
		})
		return n;
	},
	sections: function(d) {
		var sec = this.section;
		return man.util.refresher("sections", "add section",
			n => this.asec(d, n), function() {
				return d.sections.map(s => sec(s, d));
			});
	},
	unheader: function(d) {
		var _ = this._;
		if (!d.key || !this.opts.headerlessness) return;
		return CT.dom.checkboxAndLabel("headerless", d.headerless,
			null, null, "abs ctr bordered round shiftup", function(cb) {
				_.edit({
					key: d.key,
					headerless: cb.checked
				});
			});
	},
	inject: function(ta) {
		return CT.dom.button("inject variable", function() {
			CT.modal.choice({
				prompt: "choose an injection variable",
				data: core.config.ctman.injections.map(i => i.name),
				cb: function(ivar) {
					tinyMCE.activeEditor.selection.setContent("{{" + ivar + "}}");
				}
			});
		}, "right");
	},
	view: function(d) {
		var _ = this._, mcfg = core.config.ctman, val;
		CT.dom.setContent(_.nodes.content, [
			this.unheader(d),
			CT.dom.div(d.name, "bigger centered"),
			man.util.form(d, "template", function(vals) {
				for (val in vals)
					d[val] = vals[val];
				_.edit(d.key ? CT.merge({
					key: d.key
				}, vals) : d);
			}, {
				description: this.inject
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
	init: function(opts) {
		this.opts = CT.merge(opts, {
			owner: false,
			headerlessness: true,
			modelName: "section",
			blurs: ["section name", "section title", "name that section"]
		}, this.opts);
	}
}, CT.Browser);