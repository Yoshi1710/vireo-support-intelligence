import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Vireo Support Intelligence", layout="centered")

st.title("🎧 Vireo Audio - Support Intelligence Desk")
st.markdown("AI-assisted ticket categorisation, smart routing, and headcount impact engine.")

@st.cache_resource
def load_classifier():
    return joblib.load('src/ticket_classifier.pkl')

try:
    model = load_classifier()
except Exception as e:
    st.error("Model file not found! Please run `python src/classifier.py` first.")
    st.stop()

ROUTING_MAP = {
    'Delivery & Shipping': {'team': 'Logistics', 'auto_resolvable': True, 'action': 'Send real-time courier tracking link via WhatsApp/SMS'},
    'Returns & Refunds': {'team': 'Returns Desk', 'auto_resolvable': False, 'action': 'Verify serial & initiate pickup via reverse-logistics portal'},
    'Billing & Payments': {'team': 'Billing', 'auto_resolvable': False, 'action': 'Check payment gateway txn logs (Razorpay/PG)'},
    'Charging & Battery': {'team': 'Bengaluru Technical / Escalations', 'auto_resolvable': False, 'action': 'Run battery diagnostics & warranty entitlement check'},
    'Audio Quality': {'team': 'Bengaluru Technical / Escalations', 'auto_resolvable': False, 'action': 'Troubleshoot codec/ANC firmware; evaluate hardware swap'},
    'Connectivity': {'team': 'Chat Frontline', 'auto_resolvable': True, 'action': 'Send Bluetooth reset & multi-point pairing guide'},
    'App & Firmware': {'team': 'Chat Frontline', 'auto_resolvable': True, 'action': 'Push OTA update instructions and cache clearing steps'},
    'Account & Login': {'team': 'Chat Frontline', 'auto_resolvable': True, 'action': 'Trigger self-service OTP reset link'},
    'Product Enquiry': {'team': 'Chat Frontline', 'auto_resolvable': True, 'action': 'Share product spec sheet and compatibility matrix'},
    'Warranty & Repair': {'team': 'Escalations & Warranty', 'auto_resolvable': False, 'action': 'Verify invoice lot code and generate RMA pickup'},
    'Other': {'team': 'Chat Frontline', 'auto_resolvable': False, 'action': 'Route to human agent for manual triage'}
}

with st.form("ticket_form"):
    st.subheader("Simulate New Customer Ticket")
    customer_msg = st.text_area(
        "Customer Opening Message",
        value="paid, confirmed, then nothing. 5 days and counting. Where is my package?",
        help="Paste raw message from WhatsApp, email, or chat bot"
    )
    agent_note = st.text_input(
        "Agent Notes / Metadata (Optional)",
        value="Customer demanding update on shipment delay"
    )
    submitted = st.form_submit_button("Analyze & Route Ticket")

if submitted:
    full_text = f"{customer_msg} {agent_note}".strip()
    if not full_text:
        st.warning("Please provide customer message text.")
    else:
        pred_category = model.predict([full_text])[0]
        probs = model.predict_proba([full_text])[0]
        confidence = max(probs) * 100
        
        routing_info = ROUTING_MAP.get(pred_category, {'team': 'Chat Frontline', 'auto_resolvable': False, 'action': 'Manual Review'})
        
        st.success("Triage Analysis Complete")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Category", pred_category)
        col2.metric("Routed Team", routing_info['team'])
        col3.metric("Confidence", f"{confidence:.1f}%")
        
        st.markdown("---")
        st.subheader("Operational Recommendation")
        if routing_info['auto_resolvable']:
            st.info(f"⚡ **Can be auto-resolved without agent intervention.**\n\n**Action:** {routing_info['action']}")
        else:
            st.warning(f"🧑‍💻 **Requires human agent handling.**\n\n**Recommended Next Action:** {routing_info['action']}")