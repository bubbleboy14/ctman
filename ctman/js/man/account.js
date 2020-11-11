man.account = {
	info: function() { // TODO: payment history etc
		var u = user.core.get();
		if (u.admin) return "you're an admin";
		var n = new Date(), e = new Date(u.expiration),
			ex = u.expiration.split(" ").shift();
		return "your account " + ((n > e) ?
			"expires" : "expired") + " on " + ex;
	},
	init: function() {
		var payform = CT.dom.div();
		CT.pay.init({
			mode: "braintree",
			cb: function() {
				new CT.pay.Form({ parent: payform });
			}
		});
		CT.dom.setMain([
			"Hello " + user.core.get("firstName"),
			man.account.info(), payform
		]);
	}
};