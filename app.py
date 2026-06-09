import random
from dataclasses import dataclass
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


OPTION_NAMES = {
    "long_call": "Long call – vételi opció vétele",
    "short_call": "Short call – vételi opció kiírása",
    "long_put": "Long put – eladási opció vétele",
    "short_put": "Short put – eladási opció kiírása",
}

EXPLANATIONS = {
    "long_call": "A vevő jogosult az alapterméket K kötési áron megvenni. Árfolyam-emelkedésre számít. Maximális vesztesége a prémium.",
    "short_call": "A kiíró kötelezettséget vállal az alaptermék K kötési áron történő eladására. Mérsékelt vagy csökkenő árfolyamra számít. Maximális nyeresége a prémium.",
    "long_put": "A vevő jogosult az alapterméket K kötési áron eladni. Árfolyamcsökkenésre számít. Maximális vesztesége a prémium.",
    "short_put": "A kiíró kötelezettséget vállal az alaptermék K kötési áron történő megvételére. Mérsékelt emelkedésre vagy oldalazásra számít. Maximális nyeresége a prémium.",
}


@dataclass
class OptionTask:
    option_type: str
    stock_price: float
    strike: float
    premium: float


def option_profit(option_type: str, s: np.ndarray | float, k: float, premium: float):
    """Lejáratkori profit/prémium utáni eredmény."""
    if option_type == "long_call":
        return np.maximum(np.asarray(s) - k, 0) - premium
    if option_type == "short_call":
        return premium - np.maximum(np.asarray(s) - k, 0)
    if option_type == "long_put":
        return np.maximum(k - np.asarray(s), 0) - premium
    if option_type == "short_put":
        return premium - np.maximum(k - np.asarray(s), 0)
    raise ValueError("Ismeretlen opciótípus")


def breakeven(option_type: str, k: float, premium: float) -> float:
    if option_type in ["long_call", "short_call"]:
        return k + premium
    return k - premium


def max_profit_loss(option_type: str, k: float, premium: float) -> Tuple[str, str]:
    if option_type == "long_call":
        return "korlátlan", f"{premium:.2f}"
    if option_type == "short_call":
        return f"{premium:.2f}", "korlátlan"
    if option_type == "long_put":
        return f"{max(k - premium, 0):.2f}", f"{premium:.2f}"
    if option_type == "short_put":
        return f"{premium:.2f}", f"{max(k - premium, 0):.2f}"
    raise ValueError("Ismeretlen opciótípus")


def generate_task() -> OptionTask:
    option_type = random.choice(list(OPTION_NAMES.keys()))
    strike = random.choice([80, 90, 100, 110, 120])
    premium = random.choice([3, 5, 8, 10, 12])
    stock_price = random.choice([60, 70, 80, 90, 100, 110, 120, 130, 140])
    return OptionTask(option_type, float(stock_price), float(strike), float(premium))


def plot_payoff(option_type: str, k: float, premium: float, current_s: float | None = None):
    max_s = max(2 * k, k + 4 * premium, 150)
    s_values = np.linspace(0, max_s, 400)
    profits = option_profit(option_type, s_values, k, premium)

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(s_values, profits, linewidth=2, label="Lejáratkori eredmény")
    ax.axhline(0, linewidth=1)
    ax.axvline(k, linestyle="--", linewidth=1, label="Kötési ár")
    ax.axvline(breakeven(option_type, k, premium), linestyle=":", linewidth=1.5, label="Nyereségküszöb")

    if current_s is not None:
        current_profit = float(option_profit(option_type, current_s, k, premium))
        ax.scatter([current_s], [current_profit], s=60, label="Aktuális példa")
        ax.annotate(
            f"S={current_s:.0f}\nEredmény={current_profit:.2f}",
            xy=(current_s, current_profit),
            xytext=(10, 10),
            textcoords="offset points",
        )

    ax.set_title(OPTION_NAMES[option_type])
    ax.set_xlabel("Alaptermék árfolyama lejáratkor (S)")
    ax.set_ylabel("Opciós pozíció eredménye lejáratkor")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig


def initialize_state():
    if "task" not in st.session_state:
        st.session_state.task = generate_task()
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempts" not in st.session_state:
        st.session_state.attempts = 0


def main():
    st.set_page_config(page_title="Opciós alapstratégiák gyakorlása", page_icon="📈", layout="wide")
    initialize_state()

    st.title("Opciós alapstratégiák gyakorlása")
    st.caption("Long call, short call, long put és short put gyakorlása lejáratkori eredménnyel. A feladatok során a pénz időértékével nem számolunk.")
    st.caption("© Csongrádi")
    
    tab1, tab2, tab3 = st.tabs(["Interaktív grafikon", "Gyakorló feladat", "Összefoglaló"])

    with tab1:
        st.subheader("Állítsd be a paramétereket, és figyeld a nyereségfüggvényt!")
        st.info("A számítások lejáratkori eredményre vonatkoznak; a pénz időértékével a feladatok során nem számolunk.")
        left, right = st.columns([1, 2])

        with left:
            option_type = st.selectbox(
                "Opciós pozíció",
                options=list(OPTION_NAMES.keys()),
                format_func=lambda x: OPTION_NAMES[x],
            )
            strike = st.slider("Kötési ár (K)", min_value=20, max_value=200, value=100, step=5)
            premium = st.slider("Opciós díj / prémium", min_value=1, max_value=50, value=10, step=1)
            current_s = st.slider("Lejáratkori alaptermékár (S)", min_value=0, max_value=250, value=120, step=5)

            profit = float(option_profit(option_type, current_s, strike, premium))
            be = breakeven(option_type, strike, premium)
            max_profit, max_loss = max_profit_loss(option_type, strike, premium)

            st.metric("Lejáratkori eredmény", f"{profit:.2f}")
            st.write(f"**Nyereségküszöb:** {be:.2f}")
            st.write(f"**Maximális nyereség:** {max_profit}")
            st.write(f"**Maximális veszteség:** {max_loss}")
            st.info(EXPLANATIONS[option_type])

        with right:
            st.pyplot(plot_payoff(option_type, strike, premium, current_s))

    with tab2:
        st.subheader("Számítási feladat")
        task: OptionTask = st.session_state.task

        st.write(
            f"Egy befektető **{OPTION_NAMES[task.option_type]}** pozíciót nyit. "
            f"A kötési ár **K = {task.strike:.0f}**, az opciós díj **{task.premium:.0f}**, "
            f"az alaptermék lejáratkori árfolyama **S = {task.stock_price:.0f}**. "
            f"A feladat során a pénz időértékével nem számolunk."
        )

        correct_profit = float(option_profit(task.option_type, task.stock_price, task.strike, task.premium))
        correct_be = breakeven(task.option_type, task.strike, task.premium)
        correct_max_profit, correct_max_loss = max_profit_loss(task.option_type, task.strike, task.premium)

        col1, col2 = st.columns(2)
        with col1:
            user_profit = st.number_input("Mennyi a lejáratkori eredmény?", value=0.0, step=1.0)
            user_be = st.number_input("Mennyi a nyereségküszöb?", value=0.0, step=1.0)
        with col2:
            user_direction = st.radio(
                "Milyen árfolyammozgás kedvez ennek a pozíciónak?",
                ["Árfolyam-emelkedés", "Árfolyamcsökkenés", "Oldalazás / mérsékelt mozgás"],
            )

        expected_direction: Dict[str, str] = {
            "long_call": "Árfolyam-emelkedés",
            "short_call": "Oldalazás / mérsékelt mozgás",
            "long_put": "Árfolyamcsökkenés",
            "short_put": "Oldalazás / mérsékelt mozgás",
        }

        if st.button("Ellenőrzés"):
            st.session_state.attempts += 1
            ok_profit = abs(user_profit - correct_profit) < 0.01
            ok_be = abs(user_be - correct_be) < 0.01
            ok_direction = user_direction == expected_direction[task.option_type]

            points = int(ok_profit) + int(ok_be) + int(ok_direction)
            st.session_state.score += points

            if points == 3:
                st.success("Helyes megoldás! Mindhárom válasz jó.")
            else:
                st.warning(f"Részben jó megoldás: {points}/3 pont.")

            st.write(f"**Helyes eredmény:** {correct_profit:.2f}")
            st.write(f"**Helyes nyereségküszöb:** {correct_be:.2f}")
            st.write(f"**Kedvező árfolyammozgás:** {expected_direction[task.option_type]}")
            st.write(f"**Maximális nyereség:** {correct_max_profit}")
            st.write(f"**Maximális veszteség:** {correct_max_loss}")
            st.pyplot(plot_payoff(task.option_type, task.strike, task.premium, task.stock_price))

        if st.button("Új feladat"):
            st.session_state.task = generate_task()
            st.rerun()

        st.divider()
        st.write(f"Eddigi pontszám: **{st.session_state.score}** / **{st.session_state.attempts * 3}**")

    with tab3:
        st.subheader("Négy alap opciós pozíció")
        st.markdown(
            """
| Pozíció | Mire számít? | Nyereségküszöb | Maximális nyereség | Maximális veszteség |
|---|---:|---:|---:|---:|
| Long call | Árfolyam-emelkedés | K + prémium | korlátlan | prémium |
| Short call | Nem emelkedik jelentősen | K + prémium | prémium | korlátlan |
| Long put | Árfolyamcsökkenés | K - prémium | K - prémium | prémium |
| Short put | Nem csökken jelentősen | K - prémium | prémium | K - prémium |
"""
        )
        st.info(
            "A táblázat lejáratkori eredményre vonatkozik, a prémium figyelembevételével. "
            "A pénz időértékével a feladatok során nem számolunk. "
            "A short pozícióknál a prémium bevételként jelenik meg, de kötelezettségvállalással jár."
        )


if __name__ == "__main__":
    main()
