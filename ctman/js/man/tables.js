man.tables = {
	_: {
		chemicals: {}
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
			d = rows.map(r => r.split(", ").join("</td><td>")).join("</td></tr><tr><td>");
		return "<table><tbody><tr><td>" + d + "</td></tr></tbody></table>";
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
	button: function() {
		return CT.dom.button("inject table",
			man.tables.selector);
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