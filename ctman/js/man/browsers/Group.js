man.browsers.Group = CT.Class({
	CLASSNAME: "man.browsers.Group",
	noders: {
		item: function(d) {
			return CT.dom.div(e.email ? [
				d.firstName + " " + d.lastName,
				d.email
			] : (d.name || d), "bordered margined padded round inline-block");
		},
		editor: function(variety, inode, adder) {
			var cb = adder;
			if (!cb) {
				if (variety == "permissions")
					cb = this.setPerms;
				else
					cb = () => this.selector(variety);
			}
			return [
				CT.dom.button(adder ? "add" : "edit", cb, "right"),
				CT.dom.div(variety, "big bold"),
				inode
			];
		},
		perm: function(p) {
			var node = this.noders.item("can " + p);
			node.classList.add(this._.group.permissions[p] ? "green" : "red");
			return node;
		}
	},
	setter: function(variety, items, noder) {
		CT.dom.setContent(this._.nodes[variety], items.map(this.noders[noder || "item"]));
	},
	selector: function(variety) {
		var _ = this._;
		CT.modal.choice({
			prompt: "please select the " + variety + " for this group",
			style: "multiple-choice",
			data: _[variety],
			selections: _.group[variety],
			cb: function(selections) {
				_.group[variety] = selections.map(s => s.key);
				_.edit(_.group);
			}
		});
	},
	editor: function(variety) {
		var enode = this._.nodes[variety] = CT.dom.div();
		CT.db.multi(d[variety], items => this.setter(variety, items));
		return this.noders.editor(variety, enode);
	},
	addMem: function() {
		// TODO...
	},
	members: function(d) {
		var memsnode = this._.nodes.members = CT.dom.div();
		CT.db.get("member", mems => this.setter(variety, mems), null, null, {
			group: d.key
		});
		return this.noders.editor("members", memsnode, this.addMem);
	},
	perms: ["access", "build",
		"edit section", "edit template", "edit document",
		"create section", "create template", "create document"],
	setPerms: function() {
		// TODO...
	},
	permissions: function(d) {
		var pnode = this._.nodes.permissions = CT.dom.div();
		this.setter("permissions", this.perms, "perm");
		return this.noders.editor("permissions", pnode);
	},
	view: function(d) {
		this._.group = d;
		CT.dom.setContent(this._.nodes.content, [
			this.namer(d),
			this.members(d),
			this.editor("sections"),
			this.editor("templates"),
			this.permissions(d)
		]);
	},
	defaults: function() {
		return {
			sections: [],
			templates: [],
			permissions: {}
		};
	},
	init: function(opts) {
		var _ = this._;
		this.opts = CT.merge(opts, {
			owner: false,
			modelName: "group",
			saveMessage: "group saved",
			prebuild: function(groups) {
				CT.db.get("section", function(sz) {
					_.sections = sz;
					CT.db.get("template", function(tz) {
						_.templates = tz;
						_.build(groups);
					});
				});
			}
		});
	}
}, CT.Browser);