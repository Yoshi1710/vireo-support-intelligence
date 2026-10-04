import pandas as pd
import numpy as np

print("--- 1. Loading Data ---")
tickets = pd.read_csv('data/tickets.csv')
print(f"Total tickets: {len(tickets)}")

print("\n--- 2. Bot Category Distribution (Priya's View) ---")
category_counts = tickets['category'].value_counts(normalize=True) * 100
team_counts = tickets['assigned_team'].value_counts(normalize=True) * 100
print("Top Categories (%):")
print(category_counts.head(6))
print("\nTop Assigned Teams (%):")
print(team_counts.head(6))

print("\n--- 3. Misrouting Clues: Transfers and Notes in Billing ---")
billing_tickets = tickets[tickets['assigned_team'] == 'Billing']
print(f"Total tickets routed to Billing: {len(billing_tickets)}")

logistics_keywords = ['dlvry', 'delivery', 'courier', 'dispatch', 'crr partner', 'shipped', 'tracking', 'order status', 'shipment']
mask_logistics_in_billing = billing_tickets['agent_notes'].str.lower().str.contains('|'.join(logistics_keywords), na=False) | \
                            billing_tickets['customer_message'].str.lower().str.contains('|'.join(logistics_keywords), na=False)

print(f"Billing tickets that are actually Logistics/Delivery: {mask_logistics_in_billing.sum()} ({mask_logistics_in_billing.mean()*100:.1f}%)")

print("\n--- 4. Resolution Time & Escalation Analysis ---")
tickets['created_at'] = pd.to_datetime(tickets['created_at'])
tickets['resolved_at'] = pd.to_datetime(tickets['resolved_at'])
tickets['resolution_hours'] = (tickets['resolved_at'] - tickets['created_at']).dt.total_seconds() / 3600.0

team_perf = tickets.groupby('assigned_team').agg(
    ticket_count=('ticket_id', 'count'),
    avg_resolution_hours=('resolution_hours', 'mean'),
    avg_transfers=('transfers', 'mean'),
    avg_csat=('csat_score', 'mean')
).reset_index()

print(team_perf.to_string(index=False))