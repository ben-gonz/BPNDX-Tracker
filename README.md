# $BPNDX-Tracker

The Bullish Percent Index (BPI) is a technical indicator that measures the percentage of stocks within a specific index sector that are on a "buy" signal according to point-and-figure (P&F) charts. It helps traders guage market sentiment and identify potential overbought or oversold conditions. A high BPI (above 70%) generally indicates overbought conditions, while a low BPI (in the 30% - 14% range) suggests oversold conditions. BPI is calculated by dividing the number of stocks with buy signals by the total number of stocks in the index or sector. A common stock strategy is buying "low" (when the BPI drops below a certain percent).

This program scrapes **StockCharts.com** for the daily $BPNDX, and sends me an email if it drops into my buy signal range.

I chose to use **ZohoMail**, an open-source email option after some issues with Gmail and Yahoo.

### AWS Workflow

```text
EventBridge (schedule) ──> Lambda: StartInstances ──> EC2 instance
                                                   └─(cron)--> bpndx_scrape_and_email.py --> Zoho SMTP
EventBridge (schedule) ──> Lambda: StopInstances ──┘
```
- EventBridge (CloudWatch Scheduler): Triggers start/stop at specific time of day
- Lambda (StartInstances/StopInstances): Powers the EC2 instance on and off
- EC2 instance: Runs a cron job that executes bpndx_scrape_and_email.py
- Zoho SMTP: Handles outgoing email delivery

![Buy Signal](https://github.com/user-attachments/assets/21515c0a-bc69-4d98-b087-deda9c23ed43)
