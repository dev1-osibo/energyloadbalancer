# optena_marketing.py

import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="Optena - Real-Time Energy Optimization",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define a reusable function to add space between sections
def add_vertical_space(lines=1):
    for _ in range(lines):
        st.write("")

# Load and display logo or hero image
st.image("path_to_optena_logo.png", use_column_width=True)

# Hero Section
st.title("Optena - Real-Time Data Center Energy Optimization")
st.subheader("Empowering data centers with real-time insights for sustainable energy management")
st.write(
    "**Optena** leverages predictive analytics and live data integration to help data centers optimize energy use, reduce costs, and minimize environmental impact in real-time."
)
st.button("Request a Demo")

add_vertical_space(2)

# Key Features Section
st.header("Key Features")
features = [
    {
        "title": "Real-Time Energy Optimization",
        "description": "Automatically adjust workloads and prioritize renewable energy sources in real-time using API-driven live data.",
    },
    {
        "title": "Predictive Analytics",
        "description": "Forecast future energy demands and costs with advanced machine learning, enabling proactive energy management.",
    },
    {
        "title": "Dynamic Cost and Emissions Management",
        "description": "Continuously track energy costs and carbon emissions, with instant insights on savings opportunities.",
    },
    {
        "title": "Interactive Dashboard",
        "description": "Easily monitor energy data, optimize performance, and generate actionable insights through an intuitive, customizable interface.",
    },
]

cols = st.columns(len(features))
for col, feature in zip(cols, features):
    col.subheader(feature["title"])
    col.write(feature["description"])
    col.image("path_to_feature_image.png", use_column_width=True)  # Optional

add_vertical_space(2)

# Benefits Section
st.header("Why Optena?")
st.write(
    "Optena goes beyond traditional energy management tools by providing real-time insights and adaptive optimization. Here's how it benefits your data center operations:"
)

# Example stats or benefits
st.metric(label="Average Cost Savings", value="15% Reduction")
st.metric(label="CO? Emissions Reduction", value="Up to 25% Reduction")
st.metric(label="Operational Efficiency", value="30% Improvement")
add_vertical_space(2)

# Interactive Demo Section
st.header("Experience Optena in Action")

renewable_threshold = st.slider("Set Renewable Energy Availability Threshold (%)", min_value=0, max_value=100, value=70)
energy_price_per_kwh = st.slider("Set Energy Price per kWh ($)", min_value=0.05, max_value=1.00, value=0.1, step=0.01)

if st.button("Run Optimization"):
    # Run a simple simulation with example data
    st.write("Displaying estimated energy savings and emissions reduction based on your inputs...")
    # Example metrics to display - replace with real results from your app if possible
    st.metric("Estimated Savings", value="20%")
    st.metric("Estimated Emissions Reduction", value="10%")

add_vertical_space(2)

# Testimonials Section (Optional)
st.header("What Our Clients Say")
st.write(
    "“Optena has revolutionized our approach to energy management. We've seen significant savings and a substantial reduction in emissions.” – Data Center Manager, TechCorp"
)
add_vertical_space(2)

# Contact Form
st.header("Get in Touch")
st.write("Interested in learning more? Contact us to schedule a demo or discuss how Optena can benefit your operations.")

contact_form_placeholder = st.empty()
with contact_form_placeholder.form("contact_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message", "I'm interested in learning more about Optena's capabilities...")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Thank you for reaching out! We will contact you soon.")

---

### 4. **Adjustments for Live Data, Predictions, and Positioning**

In the **Feature Overview** section, we emphasized Optena’s **real-time** and **predictive** capabilities. For the **Interactive Demo**, you can link a simplified version of your optimization function if you'd like to give users a taste of Optena’s predictive power. 

To truly demonstrate the app’s predictive abilities in real-time, you might eventually consider adding a **live data feed** if this is accessible from an API. You could show real-time energy availability and costs on the page as part of the demo experience.

### 5. **Refinement Ideas for a Professional Look**

- **Custom Domain Integration**: After building the page, deploy it on Streamlit Cloud and connect it to your domain `optena.app`.
- **Visuals**: Use high-quality icons and a color scheme that aligns with Optena’s branding for consistency.
- **Analytics Integration**: To track engagement on the page, integrate a simple analytics tool like Google Analytics.

---

### 6. **Deployment**

1. **Test the Page Locally**:
   ```bash
   streamlit run optena_marketing.py