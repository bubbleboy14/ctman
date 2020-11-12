man.account = {
	_: {
		nodes: {
			payform: CT.dom.div(),
			options: CT.dom.div(),
			info: CT.dom.div(),
			phbutt: CT.dom.button("payment history",
				e => man.account._.history(), "right")
		},
		refresh: function(expiration) {
			user.core.update({
				expiration: expiration
			});
			man.account._.ifresh();
			alert("success!");
		},
		ifresh: function() {
			CT.dom.setContent(man.account._.nodes.info,
				man.account._.info());
		},
		info: function() {
			var u = user.core.get();
			if (u.admin) return "you're an admin";
			if (!u.expiration) return "you haven't finished your registration";
			var n = new Date(), e = new Date(u.expiration),
				ex = u.expiration.split(" ").shift();
			return "your account " + ((n > e) ?
				"expired" : "expires") + " on " + ex;
		},
		form: function(item, amount) {
			var _ = man.account._, pf = _.nodes.payform;
			CT.dom.clear(pf);
			new CT.pay.Form({
				parent: pf,
				item: item,
				amount: amount,
				onpaid: _.refresh
			});
		},
		plan: function(item, amount) {
			var _ = man.account._, butt = CT.dom.button(item + " for " + amount,
				e => _.form(item, amount));
			_.nodes.options.appendChild(butt);
		},
		payment: function(p) {
			return CT.dom.flex([p.created, "$" + p.amount,
				p.duration + " days",
				p.successful.toString(), p.message], "row")
		},
		history: function() {
			var _ = man.account._, butt = _.nodes.phbutt;
			butt.disabled = true;
			CT.db.get("payment", function(pz) {
				CT.modal.modal(CT.dom.div([
					"your payment history",
					pz.length ? CT.dom.flex([
						CT.dom.flex(["date", "amount", "duration",
							"successful", "message"], "row big bold")
					].concat(pz.map(_.payment)), "col margined") : "nothing yet!"
				], "phist"), function() {
					butt.disabled = false;
				});
			}, null, null, null, {
				member: user.core.get("key")
			});
		}
	},
	init: function() {
		var _ = man.account._, nz = _.nodes,
			cfg = core.config.ctman, i;
		CT.pay.init({
			mode: "braintree",
			cb: function() {
				for (i in cfg.subs)
					_.plan(i, cfg.subs[i]);
			}
		});
		_.ifresh();
		CT.dom.setMain([
			CT.dom.div([
				nz.phbutt,
				"Hello " + user.core.get("firstName"),
				nz.info
			], "subpadded"),
			CT.dom.div([
				CT.dom.div("extend your subscription", "biggest"),
				nz.options, nz.payform
			], "bordered padded margined round centered")
		]);
	}
};