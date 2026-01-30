import streamlit as st

st.set_page_config(page_title="Korea Trip Budget (7 Nights)", page_icon="💸", layout="wide")

# -----------------------------
# LOCKED ASSUMPTIONS (fixed)
# -----------------------------
FX_KRW_PER_USD = 1447                 # fixed
NIGHTS = 7                            # fixed, not editable
FLIGHT_USD = 1500                     # fixed
ACCOM_WEEK_USD_PER_PERSON = 100       # fixed, per person (whole trip)

# Savings model:
# Solo tourist "foreigner pricing" on-ground costs are ~2.7x higher than traveling with Robin.
FOREIGNER_MULTIPLIER_ON_GROUND = 2.7

# -----------------------------
# HELPERS
# -----------------------------
def usd_to_krw(usd: float) -> float:
    return usd * FX_KRW_PER_USD

def krw_to_usd(krw: float) -> float:
    return krw / FX_KRW_PER_USD

def fmt_krw(x: float) -> str:
    return f"₩{x:,.0f}"

def fmt_usd(x: float) -> str:
    return f"${x:,.2f}"

# -----------------------------
# FIXED DAILY BASELINES (KRW/day)
# Everything shown in KRW first.
# -----------------------------
DAILY_FIXED = {
    "Food (regular restaurants)": 35_000,  # fixed
    "Transit": 10_000,                      # fixed
    "Activities": 40_000,                   # fixed
}

# Optional daily categories (editable)
DAILY_EDITABLE_DEFAULTS = {
    "Cafes/snacks": 8_000,
    "Shopping": 15_000,
}

# One-time costs (KRW) - editable
ONE_TIME_DEFAULTS = {
    "SIM/eSIM": 30_000,
    "Airport train (AREX)": 12_000,
    "Buffer": 40_000,
}

# -----------------------------
# UI
# -----------------------------
st.title("💸 Korea Trip Budget (7 Nights)")
st.caption("Everything is calculated and shown in **KRW first**. USD conversion is shown at the end.")

with st.sidebar:
    st.header("Locked settings")
    st.write(f"🗓️ Trip: **{NIGHTS} nights** (locked)")
    st.write(f"💱 FX: **{FX_KRW_PER_USD} KRW = 1 USD** (locked)")
    st.write(f"✈️ Flight: **{fmt_usd(FLIGHT_USD)}** (locked)")
    st.write(f"🏨 Accommodation: **{fmt_usd(ACCOM_WEEK_USD_PER_PERSON)} per person** (locked)")

    st.divider()
    st.header("Savings (foreigner pricing)")
    st.write(f"Solo tourist **on-ground** costs: **{FOREIGNER_MULTIPLIER_ON_GROUND}×**")
    show_savings_panel = st.toggle("Show savings panel", value=True)

# Convert locked big items to KRW (we do everything in KRW)
flight_krw = usd_to_krw(FLIGHT_USD)
accom_krw = usd_to_krw(ACCOM_WEEK_USD_PER_PERSON)

# -----------------------------
# MAIN LAYOUT
# -----------------------------
colA, colB = st.columns([1.25, 0.75])

with colA:
    st.subheader("🧾 Daily budget (KRW/day)")
    st.caption("Food, Transit, and Activities are fixed to your exact numbers. Optional categories can be edited.")

    # Show fixed daily items as metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Food (fixed)", f"{fmt_krw(DAILY_FIXED['Food (regular restaurants)'])} / day")
    m2.metric("Transit (fixed)", f"{fmt_krw(DAILY_FIXED['Transit'])} / day")
    m3.metric("Activities (fixed)", f"{fmt_krw(DAILY_FIXED['Activities'])} / day")

    st.write("")
    st.markdown("**Optional daily categories (edit if you want)**")

    edited_daily = dict(DAILY_FIXED)
    d1, d2 = st.columns(2)
    for i, (k, v) in enumerate(DAILY_EDITABLE_DEFAULTS.items()):
        with [d1, d2][i % 2]:
            edited_daily[k] = st.number_input(
                f"{k} (KRW/day)",
                min_value=0,
                max_value=500_000,
                value=int(v),
                step=1_000,
            )

    daily_total_krw = sum(edited_daily.values())
    daily_trip_total_krw = daily_total_krw * NIGHTS

    st.info(
        f"Daily total: **{fmt_krw(daily_total_krw)}**  \n"
        f"Daily total for **{NIGHTS} nights**: **{fmt_krw(daily_trip_total_krw)}**"
    )

    st.subheader("🎫 One-time costs (KRW)")
    o1, o2, o3 = st.columns(3)
    edited_one_time = {}
    for i, (k, v) in enumerate(ONE_TIME_DEFAULTS.items()):
        with [o1, o2, o3][i % 3]:
            edited_one_time[k] = st.number_input(
                f"{k} (KRW)",
                min_value=0,
                max_value=500_000,
                value=int(v),
                step=1_000,
            )
    one_time_total_krw = sum(edited_one_time.values())

    st.subheader("✈️ + 🏨 Big items (KRW, locked)")
    b1, b2 = st.columns(2)
    b1.metric("Flight (KRW)", fmt_krw(flight_krw))
    b2.metric("Accommodation (KRW, per person)", fmt_krw(accom_krw))

    # Total with Robin (KRW)
    with_robin_on_ground_krw = daily_trip_total_krw + one_time_total_krw + accom_krw
    with_robin_total_krw = with_robin_on_ground_krw + flight_krw

    st.success(f"✅ Total (traveling with Robin): **{fmt_krw(with_robin_total_krw)}**")

    st.divider()
    st.subheader("💵 USD conversion (shown only at the end)")
    st.write(f"Total in USD (traveling with Robin): **{fmt_usd(krw_to_usd(with_robin_total_krw))}**")

with colB:
    st.subheader("📊 KRW breakdown")
    st.write("**Daily categories**")
    for k, v in edited_daily.items():
        st.write(f"- {k}: {fmt_krw(v)} / day")

    st.write("")
    st.write("**One-time**")
    for k, v in edited_one_time.items():
        st.write(f"- {k}: {fmt_krw(v)}")

    st.write("")
    st.write("**Locked big items**")
    st.write(f"- Flight: {fmt_krw(flight_krw)}")
    st.write(f"- Accommodation (per person): {fmt_krw(accom_krw)}")

    st.divider()

    if show_savings_panel:
        st.subheader("✨ She saves money by traveling with Robin")
        st.caption("This model assumes solo tourist on-ground costs are much higher due to tourist pricing + inefficiency.")

        # Solo tourist estimate (KRW):
        # On-ground is multiplied; flight stays same.
        solo_on_ground_krw = with_robin_on_ground_krw * FOREIGNER_MULTIPLIER_ON_GROUND
        solo_total_krw = solo_on_ground_krw + flight_krw

        savings_krw = max(solo_total_krw - with_robin_total_krw, 0)

        s1, s2 = st.columns(2)
        s1.metric("Solo tourist estimate (KRW)", fmt_krw(solo_total_krw))
        s2.metric("With Robin estimate (KRW)", fmt_krw(with_robin_total_krw))

        st.metric("Estimated savings (KRW)", fmt_krw(savings_krw))

        # Extra clarity: show the multiplier and % cheaper on-ground
        # With Robin is 1 / multiplier of solo, so % cheaper = 1 - 1/multiplier
        pct_cheaper = 1 - (1 / FOREIGNER_MULTIPLIER_ON_GROUND)

        st.write(
            f"**Why she saves with Robin:** Solo tourist **on-ground** costs are modeled as "
            f"**{FOREIGNER_MULTIPLIER_ON_GROUND}×** higher. That means going with Robin makes the on-ground portion "
            f"about **{pct_cheaper * 100:.0f}% cheaper** (flight is the same either way)."
        )

        st.write("")
        st.write("**Examples of where the savings comes from (rename these to your real plans):**")
        st.write("- Avoiding tourist-trap pricing and overpriced neighborhoods")
        st.write("- Better routing and fewer costly mistakes (taxis, ticketing, timing)")
        st.write("- Knowing which activities are worth it vs overpriced packages")
        st.write("- Ordering, reservations, and local recommendations that keep costs normal")

        st.divider()
        st.subheader("💵 USD conversion (solo vs with Robin)")
        st.write(f"Solo tourist estimate (USD): **{fmt_usd(krw_to_usd(solo_total_krw))}**")
        st.write(f"With Robin estimate (USD): **{fmt_usd(krw_to_usd(with_robin_total_krw))}**")
        st.write(f"Estimated savings (USD): **{fmt_usd(krw_to_usd(savings_krw))}**")

st.divider()
st.caption("Nothing is stored. This is just a calculator.")
