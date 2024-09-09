man.util = {
	current: {},
	gated: ['templates', 'Create I-HASP', 'man'],
	loaders: {
		account: function() {
			var u = user.core.get(), apage = "/man/account.html";
			if (!u || u.admin || u.group || location.pathname == apage)
				return;
			if (!u.expiration || (new Date(u.expiration) < new Date()))
				location = apage;
		},
		access: function() {
			var mu = man.util, l, linx = CT.dom.tag("a", CT.dom.id("ctll")),
				pname = location.pathname.split("/").pop().split(".").shift();
			if (mu.can("access")) return;
			if (mu.gated.includes(pname))
				location = "/man/dash.html";
			for (l of linx)
				if (mu.gated.includes(l.innerHTML))
					CT.dom.hide(l);
		},
		group: function() {
			var cur = man.util.current;
			cur.group = cur.group || CT.db.one(user.core.get("group"),
				null, null, true, true);
			return cur.group;
		}
	},
	m: function(d, cb, action) {
		CT.net.post({
			spinner: true,
			path: "/_man",
			params: {
				key: d.key,
				action: action
			},
			cb: cb
		});
	},
	perms: ["access", "build",
		"edit section", "edit template", "edit document",
		"create section", "create template", "create document"],
	getPerms: function(selections) {
		var p, perms = {};
		for (p of man.util.perms)
			perms[p] = selections && selections.includes("can " + p);
		return perms;
	},
	perm: function(p, g) {
		var mu = man.util;
		g = g || mu.loaders.group();
		var pz = g.permissions = g.permissions || mu.getPerms();
		return p ? pz[p] : pz;
	},
	can: function(perm) {
		return user.core.get("admin") || man.util.perm(perm);
	},
	load: function() {
		var loaders = man.util.loaders;
		loaders.account();
		loaders.access();
	},
	collapser: function(title) {
		var n = CT.dom.div(title, "pointer");
		n.onclick = function() {
			n._collapsed = !n._collapsed;
			n.parentNode.classList[n._collapsed ? "add" : "remove"]("collapsed");
		};
		setTimeout(function() {
			n.parentNode.classList.add("collapsible");
		});
		return n;
	},
	form: function(d, fname, cb, extra, items, collapsible) {
		var title = d[fname] && fname, n = CT.dom.div(null,
			core.config.ctman.classes[d.modelName].form);
		n.form = CT.layout.form({
			cb: cb,
			extra: extra,
			button: true,
			labels: true,
			bname: "save",
			values: d[fname] || d,
			items: items || core.config.ctman[fname]
		});
		CT.dom.setContent(n, [
			collapsible ? man.util.collapser(title) : title,
			n.form
		]);
		return n;
	},
	refresher: function(title, buttname, buttcb, bodgen, classes, collapsible, buttclass, canedit) {
		var n = CT.dom.div(null, classes || "margined padded bordered round");
		n.refresh = function() {
			CT.dom.setContent(n, [
				canedit && CT.dom.button(buttname, buttcb(n), buttclass || "right"),
				collapsible ? man.util.collapser(title) : title,
				bodgen()
			]);
		};
		n.refresh();
		return n;
	},
	image: function(d, iprop, title, collapsible) {
		iprop = iprop || "image";
		var inode = CT.dom.img(d[iprop], "w1"), dd = CT.file.dragdrop(function(ctfile) {
			ctfile.upload("/_db", function(ilink) {
				inode.src = d[iprop] = ilink;
			}, {
				action: "blob",
				key: d.key,
				property: iprop
			});
		}), name = title || iprop, dbutt = CT.dom.button("remove",
			function() {
				var edata = { key: d.key };
				d[iprop] = edata[iprop] = null;
				CT.db.put(edata, function(newd) {
					inode.src = "";
				});
			}, "right");
		return CT.dom.div([
			dbutt,
			collapsible ? man.util.collapser(name) : name,
			inode,
			dd
		], core.config.ctman.classes[d.modelName].image);
	},
	sideslide: function() {
		var b = CT.dom.button("retract side bar", function() {
			b._re = !b._re;
			b.innerHTML = (b._re ? "expand" : "retract") + " side bar";
			CT.dom.className("ctcontent").forEach(function(n) {
				n.classList[b._re ? "add" : "remove"]("noside");
			});
		}, "abs cbl");
		return b;
	},
	minmax: function(top, mid, bottom) {
		var fullt = function() {
			mid.style.top = top.style.height = "calc(90% - 25px)";
			bottom.style.height = "calc(10% - 25px)";
		}, fullb = function() {
			mid.style.top = top.style.height = "calc(10% - 25px)";
			bottom.style.height = "calc(90% - 25px)";
		}, same = function() {
			mid.style.top = top.style.height = bottom.style.height = "calc(50% - 25px)";
		}, n = CT.dom.div([
			CT.dom.button("Template Screen", fullt),
			CT.dom.button("Section Screen", fullb),
			CT.dom.button("Split Screen", same)
		], "abs ctr");
		n.top = fullt;
		n.bottom = fullb;
		n.same = same;
		return n;
	},
	help: function() {
		var hcfg = core.config.ctman.help,
			pname = location.pathname.slice(5, -5) || "documents";
		CT.modal.modal([
			CT.dom.div(pname + " page", "biggest centered"),
			CT.dom.div(hcfg[pname], "kidvp")
		]);
	},
	inject: function(content) {
		tinyMCE.activeEditor.selection.setContent(content);
	}
};