man.dash = {
	build: function(dox) {
		CT.dom.setContent("ctmain", CT.dom.flex([
			CT.dom.flex(["name", "template", "revision", "created",
				"modified", "delete"], "row jccenter big bold")
		].concat(dox.map(d => CT.dom.flex([
			CT.dom.link(d.name, null, "/man#" + d.key),
			d.template ? CT.dom.link(d.template.name, null,
				"/man/templates.html#" + d.template.key) : "(none)",
			CT.dom.link(d.revision, null, "/" + d.pdf, null, null, null, true),
			d.created, d.modified, CT.dom.link("delete", function() {
				if (!(confirm("are you sure you want to delete this section?")
					&& confirm("really? no takebacks!")))
					return;
				CT.db.put(d.key, function() {
					CT.dom.id(d.key).remove();
				}, "delete", "key");
			}, null, "red")
		], "row jccenter", d.key))), "col margined"));
	},
	init: function() {
		CT.db.get("document", man.dash.build, null, null, null, {
			owner: user.core.get("key")
		}, null, null, "summary");
	}
}