import pandas as pd

def apply_rule_engine(current, predicted):
    if current == 'Red' and predicted == 'Red':
        return 'URGENT REDIRECT', 'Trigger concierge alerts — surface nearest MIU and GP'
    if current == 'Amber' and predicted == 'Red':
        return 'EARLY WARNING', 'Notify concierge users now before status worsens'
    if current == 'Red' and predicted in ['Amber', 'Green']:
        return 'IMPROVING', 'Send concierge notifications that wait is dropping'
    if current == 'Amber' and predicted == 'Amber':
        return 'MONITOR', 'Flag for next 30-minute refresh cycle'
    if current == 'Green':
        return 'NO ACTION', 'Operating within normal capacity'
    return 'MONITOR', 'Insufficient data for full prediction'

def run_prescriptive(df):
    df = df.copy()
    if 'predicted_traffic_light' not in df.columns:
        df['predicted_traffic_light'] = df['traffic_light_status']
    results = []
    hosp_col = 'Hospital' if 'Hospital' in df.columns else 'hospital'
    for _, row in df.iterrows():
        action, detail = apply_rule_engine(
            row.get('traffic_light_status', 'Unknown'),
            row.get('predicted_traffic_light', 'Unknown')
        )
        results.append({
            'Hospital':        row.get(hosp_col, ''),
            'Current Status':  row.get('traffic_light_status', 'Unknown'),
            'Predicted':       row.get('predicted_traffic_light', 'Unknown'),
            'System Action':   action,
            'Action Detail':   detail,
        })
    return pd.DataFrame(results)
