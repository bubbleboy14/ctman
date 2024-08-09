man.browsers.Group = CT.Class({
	CLASSNAME: "man.browsers.Group",
	noders: {
		item: function(d) {
			return CT.dom.div(d.email ? [
				d.firstName + " " + d.lastName,
				d.email
			] : (d.name || d), "bordered margined padded round inline-block");
		},
		editor: function(variety, inode, adder) {
			return [
				CT.dom.button(adder ? "add" : "edit",
					adder || (() => this.selector(variety)), "right"),
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
		var _ = this._, options = _[variety], sels = _.group[variety],
			isperm = variety == "permissions", getPerms = this.getPerms;
		if (isperm) {
			options = this.perms.map(p => "can " + p);
			sels = this.perms.filter(p => _.group.permissions[p]);
		}
		CT.modal.choice({
			prompt: "please select the " + variety + " for this group",
			style: "multiple-choice",
			data: options,
			selections: sels,
			cb: function(selections) {
				_.group[variety] = isperm ? getPerms(selections) : selections.map(s => s.key);
				_.edit(_.group);
			}
		});
	},
	editor: function(variety) {
		var _ = this._, enode = _.nodes[variety] = CT.dom.div();
		CT.db.multi(_.group[variety], items => this.setter(variety, items));
		return this.noders.editor(variety, enode);
	},
	addMem: function() {
		var memnode = this._.nodes.members;
		user.core.join({
			group: this._.group.key
		}, function(u) {
			CT.dom.addContent(memnode, this.noders.item(u));
		}, true);
	},
	members: function(d) {
		var memsnode = this._.nodes.members = CT.dom.div();
		CT.db.get("member", mems => this.setter("members", mems), null, null, null, {
			group: d.key
		});
		return this.noders.editor("members", memsnode, this.addMem);
	},
	perms: ["access", "build",
		"edit section", "edit template", "edit document",
		"create section", "create template", "create document"],
	getPerms: function(selections) {
		var p, perms = {};
		for (p of this.perms)
			perms[p] = selections && selections.includes("can " + p);
		return perms;
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
	firstview: function(d) {
		this._.group = d;
		CT.dom.setContent(this._.nodes.content, [
			this.namer(d),
			this.editor("sections"),
			this.editor("templates")
		]);
	},
	defaults: function() {
		return {
			sections: [],
			templates: [],
			permissions: this.getPerms()
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
		}, this.opts);
	}
}, CT.Browser);