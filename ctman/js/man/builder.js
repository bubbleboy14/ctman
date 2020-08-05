man.builder = {
	_: {
		list: CT.dom.div(null, "ctlist"),
		content: CT.dom.div(null, "ctcontent"),
		edit: function(data, cb, action, pname) {
			var params = {
				action: action || "edit",
				pw: core.config.keys.storage
			};
			params[pname || "data"] = data;
			CT.net.post({
				path: "/_db",
				params: params,
				cb: cb
			});
		},
		build: function(d) {
			var n = CT.dom.div(null, "margined padded bordered round");
			n.refresh = function() {
				CT.dom.setContent(n, [
					"pdf build",
					d.pdf && CT.dom.link("click here to download", null, d.pdf, "block"),
					CT.dom.button("click here to build/rebuild", function() {
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
					})
				]);
			};
			n.refresh();
			return n;
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
		view: function(d) {
			var _ = man.builder._, haz = _.hazards(d),
				mcfg = core.config.ctman;
			CT.dom.setContent(_.content, [
				CT.dom.div(d.name, "bigger centered"),
				CT.dom.div([
					"hazards",
					haz
				], "margined padded bordered round"),
				CT.dom.div([
					"injections",
					CT.layout.form({
						button: true,
						labels: true,
						bname: "save",
						values: d.injections,
						items: mcfg.injections,
						cb: function(vals) {
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
							} : d, function(dfull) {
								if (d.key)
									return _.view(dfull);
								_.tlist.postAdd(dfull, true);
							});
						}
					}),
				], "margined padded bordered round"),
				d.key && _.build(d)
			]);
		}
	},
	view: function(d) {
		var _ = man.builder._;
		if (d.name)
			return _.view(d);
		CT.dom.setContent(_.content, CT.dom.div([
			CT.dom.div("what's this document/project called?", "bigger centered"),
			CT.dom.smartField({
				classname: "w1",
				blurs: ["project name", "document title", "project/document name"],
				cb: function(name) {
					d.name = name;
					_.view(d);
				}
			})
		], "margined padded bordered round"));
	},
	build: function(docs) {
		var _ = man.builder._;
		_.tlist = CT.panel.triggerList(["new document"].concat(docs), function(d) {
			man.builder.view((d == "new document") ? {
				modelName: "document",
				owner: user.core.get("key"),
				assembly: {
					hazards: {
						chemical: []
					}
				}
			} : d);
		});
		CT.dom.setContent(_.list, _.tlist);
		CT.dom.id("tlnewdocument").trigger();
	},
	form: function() {
		var _ = man.builder._;
		CT.dom.setContent("ctmain", [
			_.list,
			_.content
		]);
		CT.db.get("document", man.builder.build, null, null, null, {
			owner: user.core.get("key")
		});
	}
};