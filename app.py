import streamlit as st
import csv, os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="My E-Commerce Store", page_icon="🛍️", layout="wide")

# =========================================================
# PROFESSIONAL WEBSITE STYLE
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #fafafa;
    }

    .stTitle {
        text-align: center;
    }

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #dddddd;
        font-weight: 600;
        padding: 0.55rem 0.8rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 12px;
        background: white;
    }

    div[data-testid="stImage"] {
        border-radius: 12px;
    }

    .store-banner {
        padding: 18px;
        border-radius: 15px;
        background: white;
        border: 1px solid #e5e5e5;
        margin-bottom: 20px;
        text-align: center;
    }

    .store-banner h1 {
        margin-bottom: 5px;
    }

    .store-banner p {
        margin-top: 0;
        color: #666666;
    }
</style>
""")


products = [
    {"id":1,"name":"Designer Saree","category":"Sarees","price":799,"image":"static/saree.jpg","description":"Beautiful designer saree for everyday and special occasions."},
    {"id":2,"name":"Ladies Handbag","category":"Bags","price":599,"image":"static/handbag.jpg","description":"Stylish and spacious handbag for daily use."},
    {"id":3,"name":"Cotton Kurti","category":"Kurtis","price":699,"image":"static/kurti.jpg","description":"Comfortable cotton kurti with a simple modern design."},
    {"id":4,"name":"Printed Saree","category":"Sarees","price":899,"image":"static/saree.jpg","description":"Trendy printed saree with an elegant design."},
    {"id":5,"name":"Fashion Handbag","category":"Bags","price":749,"image":"static/handbag.jpg","description":"Modern handbag suitable for casual and office use."},
    {"id":6,"name":"Casual Kurti","category":"Kurtis","price":549,"image":"static/kurti.jpg","description":"Soft and comfortable kurti for daily wear."},
]

def save_order(name, phone, address, cart):
    os.makedirs("data", exist_ok=True)
    path = "data/sales_data.csv"
    new_file = not os.path.exists(path)
    order_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["Order ID","Date","Customer Name","Phone","Address","Product","Category","Price","Quantity","Amount"])
        for item in cart:
            p = item["product"]
            q = item["quantity"]
            w.writerow([order_id,date,name,phone,address,p["name"],p["category"],p["price"],q,p["price"]*q])

for key, default in [("page","Home"),("cart",[]),("wishlist",[]),("selected_product",None),("orders",[])]:
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown("""<div class="store-banner"><h1>🛍️ ShopEase</h1><p>Smart E-Commerce Store with Python Sales Analytics</p></div>""", unsafe_allow_html=True)

search = st.text_input("🔍 Search Products", placeholder="Search for saree, bag, kurti...")

nav = st.columns(5)
for col, label, page in zip(
    nav,
    ["🏠 Home","🛒 Cart","❤️ Wishlist","📦 Orders","📊 Analytics"],
    ["Home","Cart","Wishlist","Orders","Analytics"]
):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.page = page
            st.rerun()

st.divider()

if st.session_state.page == "Home":
    st.subheader("Shop by Category")
    cols = st.columns(3)
    for col, label, page in zip(cols,["👗 Sarees","👜 Bags","👚 Kurtis"],["Sarees","Bags","Kurtis"]):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.page = page
                st.rerun()

    st.divider()
    shown = products
    if search:
        s = search.lower()
        shown = [p for p in products if s in p["name"].lower() or s in p["category"].lower()]
    st.subheader("⭐ Featured Products")
    if not shown:
        st.warning("No products found.")
    for i in range(0, len(shown), 3):
        for col, p in zip(st.columns(3), shown[i:i+3]):
            with col:
                st.image(p["image"], use_container_width=True)
                st.markdown(f"### {p['name']}")
                st.write(f"Category: {p['category']}")
                st.write(f"💰 ₹{p['price']}")
                if st.button("View Product", key=f"home_{p['id']}", use_container_width=True):
                    st.session_state.selected_product = p
                    st.session_state.page = "Product"
                    st.rerun()

elif st.session_state.page in ["Sarees","Bags","Kurtis"]:
    category = st.session_state.page
    st.subheader(f"{category} Collection")
    for p in [x for x in products if x["category"] == category]:
        c1,c2 = st.columns([1,2])
        with c1:
            st.image(p["image"], width=300)
        with c2:
            st.markdown(f"### {p['name']}")
            st.write(p["description"])
            st.write(f"💰 **₹{p['price']}**")
            if st.button("View Product", key=f"cat_{p['id']}"):
                st.session_state.selected_product = p
                st.session_state.page = "Product"
                st.rerun()
        st.divider()

elif st.session_state.page == "Product":
    p = st.session_state.selected_product
    if p:
        c1,c2 = st.columns(2)
        with c1:
            st.image(p["image"], width=400)
        with c2:
            st.subheader(p["name"])
            st.write(f"## 💰 ₹{p['price']}")
            st.write(f"**Category:** {p['category']}")
            st.write(p["description"])
            st.divider()
            if st.button("🛒 Add to Cart", use_container_width=True):
                found = next((x for x in st.session_state.cart if x["product"]["id"] == p["id"]), None)
                if found:
                    found["quantity"] += 1
                else:
                    st.session_state.cart.append({"product":p,"quantity":1})
                st.success("Product added to cart!")
            if st.button("❤️ Add to Wishlist", use_container_width=True):
                if not any(x["id"] == p["id"] for x in st.session_state.wishlist):
                    st.session_state.wishlist.append(p)
                    st.success("Added to wishlist!")
                else:
                    st.info("Product already in wishlist.")
            if st.button("⬅️ Back to Home", use_container_width=True):
                st.session_state.page = "Home"
                st.rerun()

elif st.session_state.page == "Cart":
    st.subheader("🛒 My Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0
        for i,item in enumerate(st.session_state.cart):
            p,q = item["product"],item["quantity"]
            c1,c2,c3 = st.columns([1,2,2])
            with c1: st.image(p["image"], width=130)
            with c2:
                st.write(f"### {p['name']}")
                st.write(f"₹{p['price']}")
                st.write(f"Quantity: **{q}**")
            with c3:
                a,b,c = st.columns(3)
                with a:
                    if st.button("➕",key=f"plus_{i}"):
                        item["quantity"] += 1
                        st.rerun()
                with b:
                    if st.button("➖",key=f"minus_{i}"):
                        if item["quantity"] > 1: item["quantity"] -= 1
                        st.rerun()
                with c:
                    if st.button("❌",key=f"remove_{i}"):
                        st.session_state.cart.pop(i)
                        st.rerun()
            total += p["price"]*q
            st.divider()
        st.subheader(f"Total Amount: ₹{total}")
        if st.button("✅ Proceed to Checkout", use_container_width=True):
            st.session_state.page = "Checkout"
            st.rerun()

elif st.session_state.page == "Checkout":
    st.subheader("🧾 Checkout")
    if not st.session_state.cart:
        st.warning("Your cart is empty.")
    else:
        total = sum(x["product"]["price"]*x["quantity"] for x in st.session_state.cart)
        for item in st.session_state.cart:
            p,q = item["product"],item["quantity"]
            st.write(f"**{p['name']}** × {q} = ₹{p['price']*q}")
        st.divider()
        st.subheader(f"Total: ₹{total}")
        st.write("### Delivery Details")
        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        address = st.text_area("Delivery Address")
        if st.button("🛍️ Place Order", use_container_width=True):
            if name and phone and address:
                save_order(name,phone,address,st.session_state.cart)
                st.session_state.orders.append({"name":name,"total":total,"items":len(st.session_state.cart)})
                st.session_state.cart = []
                st.session_state.page = "Orders"
                st.rerun()
            else:
                st.warning("Please fill all delivery details.")

elif st.session_state.page == "Wishlist":
    st.subheader("❤️ My Wishlist")
    if not st.session_state.wishlist:
        st.info("Your wishlist is empty.")
    else:
        for p in st.session_state.wishlist:
            c1,c2 = st.columns([1,3])
            with c1: st.image(p["image"], width=150)
            with c2:
                st.write(f"### {p['name']}")
                st.write(f"₹{p['price']}")
                st.write(p["description"])
            st.divider()

elif st.session_state.page == "Orders":
    st.subheader("📦 My Orders")

    sales_path = "data/sales_data.csv"

    # Read saved orders from CSV so order history remains after refresh/restart.
    if os.path.exists(sales_path):
        orders_df = pd.read_csv(sales_path, dtype={"Order ID": str})

        if not orders_df.empty:
            orders_df["Amount"] = pd.to_numeric(orders_df["Amount"], errors="coerce").fillna(0)
            orders_df["Quantity"] = pd.to_numeric(orders_df["Quantity"], errors="coerce").fillna(0)

            grouped_orders = orders_df.groupby(
                "Order ID", sort=False
            )

            for i, (order_id, group) in enumerate(grouped_orders, 1):
                customer_name = str(group["Customer Name"].iloc[0])
                order_date = str(group["Date"].iloc[0])
                item_count = int(group["Quantity"].sum())
                order_total = group["Amount"].sum()

                st.write(f"### 📦 Order #{i}")
                st.write(f"**Customer:** {customer_name}")
                st.write(f"**Order Date:** {order_date}")
                st.write(f"**Items:** {item_count}")
                st.write(f"**Total:** ₹{order_total:,.0f}")
                st.write("**Status:** ✅ Order Placed")

                with st.expander("View Order Details"):
                    for _, row in group.iterrows():
                        st.write(
                            f"• {row['Product']} × {int(row['Quantity'])} "
                            f"= ₹{float(row['Amount']):,.0f}"
                        )

                st.divider()
        else:
            st.info("No orders placed yet.")
    elif st.session_state.orders:
        # Fallback for any order created before CSV saving was added.
        for i, o in enumerate(st.session_state.orders, 1):
            st.write(f"### 📦 Order #{i}")
            st.write(f"**Customer:** {o['name']}")
            st.write(f"**Items:** {o['items']}")
            st.write(f"**Total:** ₹{o['total']}")
            st.write("**Status:** ✅ Order Placed")
            st.divider()
    else:
        st.info("No orders placed yet.")

elif st.session_state.page == "Analytics":
    st.subheader("📊 Sales Data Analytics")
    st.write("Python and Pandas are used to analyse sales data collected from customer orders.")
    path = "data/sales_data.csv"
    if not os.path.exists(path):
        st.info("No sales data available yet. Place an order first.")
    else:
        df = pd.read_csv(path, dtype={"Order ID": str, "Phone": str})
        if df.empty:
            st.info("No sales records available.")
        else:
            for col in ["Price","Quantity","Amount"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            total_sales = df["Amount"].sum()
            total_products = df["Quantity"].sum()
            total_orders = df["Order ID"].nunique()
            avg_order = total_sales / total_orders if total_orders else 0
            product_qty = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
            product_sales = df.groupby("Product")["Amount"].sum().sort_values(ascending=False)
            category_sales = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

            st.subheader("📌 Key Sales Metrics")
            a,b,c,d = st.columns(4)
            a.metric("💰 Total Sales",f"₹{total_sales:,.0f}")
            b.metric("📦 Total Orders",total_orders)
            c.metric("🛍️ Products Sold",int(total_products))
            d.metric("⭐ Best-Selling Product",product_qty.index[0])

            st.divider()
            st.subheader("💵 Average Order Value")
            st.write(f"₹{avg_order:,.2f}")

            st.divider()
            st.subheader("🏆 Product-wise Sales")
            st.bar_chart(product_sales)

            st.divider()
            st.subheader("📂 Category-wise Sales")
            st.bar_chart(category_sales)

            st.divider()
            st.subheader("📦 Quantity Sold by Product")
            st.bar_chart(product_qty)

            st.divider()
            st.subheader("📅 Sales Trend")
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            daily = df.groupby(df["Date"].dt.date)["Amount"].sum()
            st.line_chart(daily)

            st.divider()
            st.subheader("📋 Sales Data")
            st.dataframe(df.astype({"Order ID": str, "Phone": str}), use_container_width=True)
            st.download_button("⬇️ Download Sales Data", df.to_csv(index=False), "sales_data.csv", "text/csv")
