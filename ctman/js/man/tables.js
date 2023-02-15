man.tables = {
	_: {
		chemicals: {
			presels: ["name", "classification", "synonyms_and_trade_names", "idlh", "physical_description",
				"symptoms", "first_aid", "exposure_routes", "exposure_limits", "target_organs"]
		},
		entable: function(contents) {
			return "<table><tbody><tr><td>" + contents + "</td></tr></tbody></table>";
		},
		jrows: function(rows) {
			return rows.join("</td></tr><tr><td>");
		},
		jcells: function(row) {
			return row.join("</td><td>");
		},
		r2t: function(rows) {
			var _ = man.tables._;
			return _.entable(_.jrows(rows.map(_.jcells)));
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
			d = rows.map(r => r.split(", "));
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
		var rows = [cols].concat(chems.map(c => cols.map(col => c[col])));
		man.util.inject(man.tables._.r2t(rows));
	},
	chemsel: function(cols) {
		CT.modal.choice({
			prompt: "please select chems",
			style: "multiple-choice",
			className: "basicpopup mosthigh w400p",
			data: man.tables._.chemicals.names,
			filter: "right up30",
			cb: function(chems) {
				CT.db.multi(chems.map(c => c.key),
					cz => man.tables.chemproc(cz, cols), null, "code");
			}
		});
	},
	chemord: function(cols) {
		CT.modal.choice({
			prompt: "reorder columns as necessary",
			style: "reorder",
			data: cols,
			cb: man.tables.chemsel
		})
	},
	chemcols: function() {
		var _ = man.tables._;
		CT.modal.choice({
			prompt: "please select columns",
			style: "multiple-choice",
			data: _.chemicals.schema,
			selections: _.chemicals.presels,
			cb: man.tables.chemord
		});
	},
	button: function() {
		return CT.dom.button("insert table",
			man.tables.selector);
	},
	chembutt: function() {
		return CT.dom.button("insert chem table",
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