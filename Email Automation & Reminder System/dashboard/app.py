import streamlit as st
import pandas as pd
from datetime import datetime
import sys, os, time, threading
from dateutil import parser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import init_db, get_connection
from src.mailer import send_email
from src.logger import log

# =========================
# INIT
# =========================
init_db()
st.set_page_config(page_title="Email Automation System", layout="wide")

st.title("📧 Email Automation & Reminder System")

# =========================
# DB SAFE CONNECTOR
# =========================
def get_cursor():
    conn = get_connection()
    return conn, conn.cursor()

# =========================
# ENGINE STATE
# =========================
if "engine_running" not in st.session_state:
    st.session_state.engine_running = False

# =========================
# REMINDER ENGINE
# =========================
def process_due_reminders():

    conn, cur = get_cursor()

    now = datetime.now().replace(second=0, microsecond=0)

    cur.execute("""
        SELECT id, email, subject, time, status 
        FROM reminders 
        WHERE status='pending'
    """)

    rows = cur.fetchall()
    sent_count = 0

    for rid, email, subject, time_str, status in rows:

        try:
            if not email:
                continue

            reminder_time = parser.parse(str(time_str)).replace(second=0, microsecond=0)

            if reminder_time <= now:

                success, error = send_email(
                    email,
                    subject,
                    f"⏰ Reminder: {subject}"
                )

                if success:
                    cur.execute(
                        "UPDATE reminders SET status='sent' WHERE id=?",
                        (rid,)
                    )
                    conn.commit()
                    log(f"SENT → {email}")
                    sent_count += 1

                else:
                    log(f"FAILED → {email} → {error}")

        except Exception as e:
            log(f"ENGINE ERROR → {str(e)}")

    conn.close()
    return sent_count


# =========================
# BACKGROUND ENGINE
# =========================
def background_engine():
    while True:
        try:
            sent = process_due_reminders()
            if sent > 0:
                log(f"AUTO SENT → {sent}")
        except Exception as e:
            log(f"ENGINE ERROR → {e}")

        time.sleep(60)


if not st.session_state.engine_running:
    threading.Thread(target=background_engine, daemon=True).start()
    st.session_state.engine_running = True
    st.toast("🚀 Reminder Engine Started")


# =========================
# LOADERS
# =========================
def load_contacts():
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    conn.close()
    return rows


def load_reminders():
    conn, cur = get_cursor()
    cur.execute("SELECT id, email, subject, time, status FROM reminders")
    rows = cur.fetchall()
    conn.close()
    return rows


# =========================
# MENU
# =========================
menu = st.sidebar.radio(
    "📌 Menu",
    ["Dashboard", "Contacts", "Bulk Email", "Reminders", "Logs"]
)

# =====================================================
# DASHBOARD
# =====================================================
if menu == "Dashboard":

    contacts = load_contacts()
    reminders = load_reminders()

    df = pd.DataFrame(reminders, columns=["ID", "Email", "Subject", "Time", "Status"])

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Contacts", len(contacts))
    col2.metric("Pending", len(df[df["Status"] == "pending"]))
    col3.metric("Sent", len(df[df["Status"] == "sent"]))

    st.dataframe(df, use_container_width=True)


# =====================================================
# CONTACTS (ADD / UPDATE / DELETE)
# =====================================================
elif menu == "Contacts":

    st.subheader("👥 Contacts Management")

    input_text = st.text_area("Add Contacts (name,email per line)")

    if st.button("Add Contacts"):
        conn, cur = get_cursor()

        for line in input_text.split("\n"):
            try:
                name, email = line.split(",")
                cur.execute(
                    "INSERT INTO contacts(name,email) VALUES (?,?)",
                    (name.strip(), email.strip())
                )
            except:
                st.error(f"Invalid: {line}")

        conn.commit()
        conn.close()
        st.success("Contacts added")
        st.rerun()

    df = pd.DataFrame(load_contacts(), columns=["ID", "Name", "Email"])
    st.dataframe(df, use_container_width=True)

    st.markdown("### ✏️ Update Contact")

    if not df.empty:
        cid = st.selectbox("Select Contact", df["ID"].tolist(), key="contact_edit")

        row = df[df["ID"] == cid].iloc[0]

        name = st.text_input("Name", value=row["Name"], key=f"c_name_{cid}")
        email = st.text_input("Email", value=row["Email"], key=f"c_email_{cid}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Update Contact", key=f"upd_c_{cid}"):
                conn, cur = get_cursor()
                cur.execute(
                    "UPDATE contacts SET name=?, email=? WHERE id=?",
                    (name, email, cid)
                )
                conn.commit()
                conn.close()
                st.success("Updated")
                st.rerun()

        with col2:
            if st.button("Delete Contact", key=f"del_c_{cid}"):
                conn, cur = get_cursor()
                cur.execute("DELETE FROM contacts WHERE id=?", (cid,))
                conn.commit()
                conn.close()
                st.warning("Deleted")
                st.rerun()


# =====================================================
# BULK EMAIL
# =====================================================
elif menu == "Bulk Email":

    contacts = pd.DataFrame(load_contacts(), columns=["ID", "Name", "Email"])

    emails = st.multiselect("Select Emails", contacts["Email"].tolist())

    subject = st.text_input("Subject") 
    message = st.text_area("Message", "Hello {name}")

    if st.button("Send Emails"):

        sent, failed = 0, 0

        for _, row in contacts[contacts["Email"].isin(emails)].iterrows():

            success, error = send_email(row["Email"], subject, message.format(name=row["Name"]))

            if success:
                sent += 1
            else:
                failed += 1

        st.success(f"Sent: {sent}, Failed: {failed}")


# =====================================================
# REMINDERS (ADD / UPDATE / DELETE)
# =====================================================
# =====================================================
# REMINDERS (FULL CRUD FIXED)
# =====================================================
elif menu == "Reminders":

    st.subheader("⏰ Reminder System")

    # =========================
    # CREATE REMINDER
    # =========================
    email = st.text_input("Email")
    subject = st.text_input("Subject")

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date")

    with col2:
        time_input = st.time_input("Time", step=60)

    dt_value = datetime.combine(date, time_input)

    if st.button("Create Reminder"):
        conn, cur = get_cursor()
        cur.execute(
            "INSERT INTO reminders(email,subject,time,status) VALUES (?,?,?,?)",
            (email, subject, dt_value.isoformat(), "pending")
        )
        conn.commit()
        conn.close()

        st.success("Reminder created")
        st.rerun()

    # =========================
    # LOAD DATA
    # =========================
    df = pd.DataFrame(load_reminders(), columns=["ID", "Email", "Subject", "Time", "Status"])

    st.markdown("### 🟡 Pending Reminders")
    st.dataframe(df[df["Status"] == "pending"], use_container_width=True)

    st.markdown("### 🟢 Sent Reminders")
    st.dataframe(df[df["Status"] == "sent"], use_container_width=True)

    # =========================
    # EDIT ONLY PENDING
    # =========================
    st.markdown("### ✏️ Edit Pending Reminder")

    pending = df[df["Status"] == "pending"]

    if not pending.empty:

        rid = st.selectbox("Select Reminder to Edit", pending["ID"].tolist(), key="edit_rem")

        row = pending[pending["ID"] == rid].iloc[0]

        e_email = st.text_input("Email", value=row["Email"], key=f"edit_email_{rid}")
        e_subject = st.text_input("Subject", value=row["Subject"], key=f"edit_sub_{rid}")

        existing_dt = parser.parse(str(row["Time"]))

        e_date = st.date_input("Date", value=existing_dt.date(), key=f"edit_date_{rid}")
        e_time = st.time_input("Time", value=existing_dt.time(), key=f"edit_time_{rid}")

        new_dt = datetime.combine(e_date, e_time)

        if st.button("Update Reminder", key=f"update_{rid}"):

            conn, cur = get_cursor()
            cur.execute("""
                UPDATE reminders
                SET email=?, subject=?, time=?
                WHERE id=?
            """, (e_email, e_subject, new_dt.isoformat(), rid))

            conn.commit()
            conn.close()

            st.success("Reminder updated")
            st.rerun()

    else:
        st.info("No pending reminders")

    # =========================
    # 🚨 GLOBAL DELETE SECTION (NEW FIX)
    # =========================
    st.markdown("### 🗑️ Delete Any Reminder (Pending or Sent)")

    if not df.empty:

        del_id = st.selectbox(
            "Select Reminder to Delete",
            df["ID"].tolist(),
            key="delete_any_rem"
        )

        del_row = df[df["ID"] == del_id].iloc[0]

        st.write(f"📧 **{del_row['Email']}** | {del_row['Subject']} | {del_row['Status']}")

        if st.button("Delete Reminder", key="final_delete_rem"):

            conn, cur = get_cursor()
            cur.execute("DELETE FROM reminders WHERE id=?", (del_id,))
            conn.commit()
            conn.close()

            st.warning("Reminder deleted successfully")
            st.rerun()

# =====================================================
# LOGS
# =====================================================
elif menu == "Logs":

    st.subheader("📜 Logs")

    log_file = "logs/app.log"

    if os.path.exists(log_file):
        st.text(open(log_file).read())
    else:
        st.warning("No logs found")