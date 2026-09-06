What Brazil's Delivery Data Taught Me About Where E-commerce Breaks Down

I recently analyzed data from Brazil's largest e-commerce marketplace to answer a question that keeps coming up in any delivery-driven business: when something goes wrong with shipping, does it happen everywhere at once, or does it cluster somewhere specific?

Using the Olist Brazilian E-commerce dataset (96,478 delivered orders and 112,650 order items across the country), I checked how often deliveries run late, how much freight costs eat into the price of each item, and — the question that turned out to matter most — what that delay actually costs a business in customer trust.

The delay numbers surprised me a little. Nationally, only 6.8% of orders arrive later than the estimated date, a figure that on its own doesn't look alarming. But five states, Alagoas, Maranhao, Sergipe, Piaui, and Ceara, run two to three times above that average. Alagoas alone hits 21.4%. And when an order there is late, it's not by a day or two: the average delay across all late orders is 10.6 days.

The freight numbers told a related but separate story. Nationally, shipping costs run about 16.6% of what a customer pays for the item itself. In Maranhao, Rondonia, and Piaui, that ratio climbs past 24%, nearly double what customers in Sao Paulo pay in relative freight, even though Sao Paulo is by far the largest market at 47,449 items sold.

Rate isn't the same as reach, though. When I queried the data by absolute volume instead of percentage, Rio de Janeiro stood out for a different reason: 1,495 of its 12,353 orders arrived late. Its delay rate (12.1%) is lower than Alagoas's, but it affects more real customers than any other state in the country — the kind of number that matters more to a support team than a percentage does.

The most important finding, though, wasn't about geography at all. I used SQL to join delivery outcomes against review scores directly, and the result was stark: orders that arrived late averaged a review score of 2.27, against 4.29 for orders that arrived on time. The share of 1-2 star reviews jumped from 9.3% to 62.4% the moment a delivery was late. Delay isn't just a logistics metric sitting off to the side — it's the single strongest predictor of a bad review in this entire dataset.

Freight had its own hidden pattern too, once I looked at it by product category instead of by state: electronics carried a freight cost averaging 29.1% of the product's price, well above other high-volume categories. Combined with the state-level freight gap, it points to two separate levers worth pulling, not one.

Put together, these findings point at a short, specific list of actions rather than a nationwide fix. A business dealing with delivery complaints or margin pressure from freight doesn't need to fix everything at once. It needs to treat on-time delivery as a retention lever first (the review-score data makes that case on its own), prioritize carrier reviews in Rio de Janeiro given its outsized real-customer impact, keep the five highest-delay states on a separate watch list, and look specifically at packaging and freight partnerships for electronics.

I built this as a self-contained project: the full analysis in Python (pandas) and SQL (DuckDB), a dashboard in Power BI to make the pattern visible at a glance, and an Excel report with the underlying calculations left as live formulas rather than static numbers, so anyone reviewing it can check the math rather than take my word for it.

Full code, SQL queries, and the dashboard are on GitHub: github.com/sri-setiowati/olist-ecommerce-analysis
