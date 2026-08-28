What Brazil's Delivery Data Taught Me About Where E-commerce Breaks Down

I recently analyzed data from Brazil's largest e-commerce marketplace to answer a question that keeps coming up in any delivery-driven business: when something goes wrong with shipping, does it happen everywhere at once, or does it cluster somewhere specific?

Using the Olist Brazilian E-commerce dataset (96,478 delivered orders and 112,650 order items across the country), I checked two things: how often deliveries run late, and how much freight costs eat into the price of each item. Both broken down by state.

The delay numbers surprised me a little. Nationally, only 6.8% of orders arrive later than the estimated date, a figure that on its own doesn't look alarming. But five states, Alagoas, Maranhao, Sergipe, Piaui, and Ceara, run two to three times above that average. Alagoas alone hits 21.4%. And when an order there is late, it's not by a day or two: the average delay across all late orders is 10.6 days.

The freight numbers told a related but separate story. Nationally, shipping costs run about 16.6% of what a customer pays for the item itself. In Maranhao, Rondonia, and Piaui, that ratio climbs past 24%, nearly double what customers in Sao Paulo pay in relative freight, even though Sao Paulo is by far the largest market at 47,449 items sold.

Put together, these two findings point at the same handful of states. That's the part worth acting on: a business dealing with delivery complaints or margin pressure from freight doesn't need a nationwide fix. It needs to start with a short list of states where both problems overlap, review the logistics partners serving them, and weigh whether a regional distribution hub would pay for itself faster there than anywhere else.

I built this as a self-contained project: the full analysis in Python (pandas), a dashboard in Power BI to make the pattern visible at a glance, and an Excel report with the underlying calculations left as live formulas rather than static numbers, so anyone reviewing it can check the math rather than take my word for it.

Full code and the dashboard are on GitHub: [add your repo link here]
