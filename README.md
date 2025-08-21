# bullish-percent-index-tracker

I have a very conservative investing strategy that (besides monthly IRA contributions) consists of investing in the market when the Bullish Percent Index (BPI) drops into a specific range. The BPI is a technical indicator that measures the percentage of stocks within a specific index sector that are on a "buy" signal according to point-and-figure (P&F) charts. It helps traders guage market sentiment and identify potential overbought or oversold conditions. A high BPI (above 70%) generally indicates overbought conditions, while a low BPI (in the 30% - 14% range) suggests oversold conditions. BPI is calculated by dividing the number of stocks with buy signals by the total number of stocks in the index or sector. A common stock strategy is buying "low" (when the BPI drops below a certain percent).

This program scrapes StockCharts.com for the daily $BPNDX, and sends me an email if it drops into my buy signal range.
