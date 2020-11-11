man.account = {
	_: {
		renew: function(expiration, info) {
			user.core.update({
				expiration: expiration
			});
			CT.dom.setContent(info,
				man.account.info());
			alert("success!");
		}
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
	init: function() {
		var payform = CT.dom.div(), renew = this._.renew,
			info = CT.dom.div(man.account.info());
		CT.pay.init({
			mode: "braintree",
			cb: function() {
				new CT.pay.Form({
					parent: payform,
					item: "one month",
					amount: "$10.00",
					onpaid: ex => renew(ex, info)
				});
			}
		});
		CT.dom.setMain([
			"Hello " + user.core.get("firstName"),
			info, payform
		]);
	}
};