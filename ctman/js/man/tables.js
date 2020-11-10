man.tables = {
	_: {
		chemicals: {},
		entable: function(contents) {
			return "<table><tbody><tr><td>" + contents + "</td></tr></tbody></table>";
		},
		jrows: function(rows) {
			return rows.join("</td></tr><tr><td>");
		},
		r2t: function(rows) {
			var _ = man.tables._;
			return _.entable(_.jrows(rows));
		}
	},
	upload: function(name) {
		CT.modal.modal(CT.file.dragdrop(function(ctfile) {
			CT.db.put({
				modelName: "table",
				name: "name"
			}, function(tdata) {
				ctfile.upload("/_db", function(csvurl) {
					tdata.csv = csvurl;
					man.tables._.tables.push(tdata);
					man.tables.inject(tdata);
				}, {
					action: "blob",
					key: tdata.key,
					property: "csv"
				});
			});
		}));
	},
	create: function() {
		CT.modal.prompt({
			prompt: "what's the table's name?",
			cb: man.tables.upload
		});
	},
	transform: function(t) {
		var csv = CT.net.get(t.csv), rows = csv.split("\n"),
			d = rows.map(r => r.split(", ").join("</td><td>"));
		return man.tables._.r2t(d);
	},
	inject: function(t) {
		man.util.inject(man.tables.transform(t));
	},
	selector: function() {
		var _ = man.tables._;
		CT.modal.choice({
			prompt: "select or upload a csv table",
			data: ["upload"].concat(_.tables),
			cb: function(sel) {
				if (sel == "upload")
					man.tables.create();
				else
					man.tables.inject(sel);
			}
		});
	},
	chemproc: function(chems, cols) {

	},
	chemsel: function(cols) {
		var _ = man.tables._, proc = this.chemproc;
		CT.modal.choice({
			prompt: "please select chems",
			style: "multiple-choice",
			data: man.tables._.chemicals.names,
			cb: function(chems) {
				CT.db.multi(chems.map(c => c.key),
					cz => proc(cz, cols), null, "code");
			}
		});
	},
	chemcols: function() {
		CT.modal.choice({
			prompt: "please select columns",
			style: "multiple-choice",
			data: man.tables._.chemicals.schema,
			cb: this.chemsel
		});
	},
	button: function() {
		return CT.dom.button("inject table",
			man.tables.selector);
	},
	chembutt: function() {
		return CT.dom.button("inject chem table",
			man.tables.chemcols);
	},
	init: function() {
		var _ = man.tables._;
		CT.db.get("table", function(tz) {
			_.tables = tz;
		});
		CT.db.withSchema(function(schema) {
			_.chemicals.schema = Object.keys(schema.chemical).filter(function(k) {
				return ["string", "text"].includes(schema.chemical[k]);
			});
		});
		CT.db.get("chemical", function(cz) {
			_.chemicals.names = cz;
		}, null, null, null, null, null, null, "basic");
	}
};