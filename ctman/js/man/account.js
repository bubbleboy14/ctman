man.account = {
	_: {
		nodes: {
			payform: CT.dom.div(),
			options: CT.dom.div(),
			info: CT.dom.div()
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
		info: function() { // TODO: payment history etc
			var u = user.core.get();
			if (u.admin) return "you're an admin";
			if (!u.expiration) return "you haven't finished your registration";
			var n = new Date(), e = new Date(u.expiration),
				ex = u.expiration.split(" ").shift();
			return "your account " + ((n > e) ?
				"expires" : "expired") + " on " + ex;
		},
		form: function(item, amount) {
			var _ = man.account._, pf = _.nodes.payform;
			CT.dom.clear(pf);
			new CT.pay.Form({
				parent: pf,
				item: "one month",
				amount: "$10.00",
				onpaid: _.refresh
			});
		},
		plan: function(item, amount) {
			var _ = man.account._, butt = CT.dom.button(item + " for " + amount,
				e => _.form(item, amount));
			_.nodes.options.appendChild(butt);
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