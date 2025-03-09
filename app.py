import streamlit as st
import datetime
import json
import matplotlib.pyplot as plt
import requests
import time
import time
import openai
import streamlit as st

# Configure OpenAI API
openai.api_key = st.secrets["openai"]["api_key"]

# Page configuration
st.set_page_config(
    page_title="Personal Savings Assistant",
    page_icon=":money_with_wings:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Disable Streamlit's default behavior of looking for a secrets.toml file
st.config.set_option("server.enableCORS", False)
st.config.set_option("server.enableXsrfProtection", False)
st.config.set_option("server.cookieSecret", "some_random_string")

# Custom CSS (style.css)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Language selection
language = st.sidebar.radio("Select language", ("English", "Español"))

# Translation dictionary
translations = {
    "English": {
        "savings_goals": "Savings Goals",
        "enter_savings_goal": "Enter your savings goal:",
        "enter_timeframe": "Enter the timeframe in months:",
        "personal_savings_assistant": "Personal Savings Assistant :money_with_wings:",
        "enter_monthly_income": "Enter your monthly income:",
        "enter_monthly_expenses": "Enter your monthly expenses:",
        "your_savings_potential": "Your Savings Potential",
        "you_can_save": "You can save ${:.2f} per month.",
        "savings_recommendation": "Savings Recommendation",
        "to_reach_goal": "To reach your savings goal of ${:.2f} in {} months, you need to save ${:.2f} per month.",
        "reduce_expenses": "Recommendation: Reduce expenses or increase income to meet your savings goal.",
        "on_track": "Recommendation: You are on track to meet your savings goal. Keep saving consistently!",
        "additional_tips": "Additional Tips",
        "create_budget": "- Create a budget and track your spending.",
        "automate_savings": "- Automate your savings by setting up recurring transfers to a savings account.",
        "consider_investing": "- Consider investing your savings to earn a higher return.",
        "daily_expenses": "Daily Expenses",
        "select_date": "Select a date:",
        "expense_category": "Expense Category:",
        "expense_amount": "Expense Amount:",
        "add_expense": "Add Expense",
        "date": "Date",
        "category": "Category",
        "amount": "Amount",
        "no_expenses": "No expenses added for this day.",
        "promotions": "Promotions",
        "supermarket": "Supermercado",
        "promotion": "Promotion",
        "link": "Link",
        "expenses_by_category": "Expenses by Category",
        "savings_strategies": "Savings Strategies",
        "reduce_food_expenses": "- Reduce food expenses by eating out less and cooking at home more often.",
        "use_public_transportation": "- Consider using public transportation, biking, or walking instead of driving to save on gas and parking.",
        "find_free_entertainment": "- Find free or low-cost entertainment options, such as visiting parks, attending community events, or borrowing books from the library.",
        "avoid_impulse_purchases": "- Avoid impulse purchases and create a shopping list before going to the store.",
        "conserve_energy": "- Ahorre energía apagando las luces al salir de una habitación, utilizando electrodomésticos de bajo consumo y ajustando el termostato.",
        "no_specific_strategies": "No se pudieron determinar estrategias de ahorro específicas en función de sus gastos actuales. Considere realizar un seguimiento más de cerca de sus gastos para identificar posibles áreas de ahorro.",
        "savings_goal_tab": "Meta de Ahorro",
        "expenses_tab": "Gastos",
        "strategies_tab": "Estrategias",
        "pareto_chart_title": "Gráfico de Pareto de Gastos por Fecha",
        "pie_chart_title": "Gastos por Categoría",
    },
    "Español": {
        "savings_goals": "Metas de Ahorro",
        "enter_savings_goal": "Ingrese su meta de ahorro:",
        "enter_timeframe": "Ingrese el plazo en meses:",
        "personal_savings_assistant": "Asistente Personal de Ahorros :money_with_wings:",
        "enter_monthly_income": "Ingrese su ingreso mensual:",
        "enter_monthly_expenses": "Ingrese sus gastos mensuales:",
        "your_savings_potential": "Su Potencial de Ahorro",
        "you_can_save": "Puede ahorrar ${:.2f} por mes.",
        "savings_recommendation": "Recomendación de Ahorro",
        "to_reach_goal": "Para alcanzar su meta de ahorro de ${:.2f} en {} meses, necesita ahorrar ${:.2f} por mes.",
        "reduce_expenses": "Recomendación: Reduzca los gastos o aumente los ingresos para alcanzar su meta de ahorro.",
        "on_track": "Está en camino de alcanzar su meta de ahorro. ¡Siga ahorrando constantemente!",
        "additional_tips": "Consejos Adicionales",
        "create_budget": "- Cree un presupuesto y realice un seguimiento de sus gastos.",
        "automate_savings": "- Automatice sus ahorros configurando transferencias recurrentes a una cuenta de ahorros.",
        "consider_investing": "- Considere invertir sus ahorros para obtener un mayor rendimiento.",
        "daily_expenses": "Gastos Diarios",
        "select_date": "Seleccione una fecha:",
        "expense_category": "Categoría de Gasto:",
        "expense_amount": "Monto del Gasto:",
        "add_expense": "Agregar Gasto",
        "date": "Fecha",
        "category": "Categoría",
        "amount": "Monto",
        "no_expenses": "No se han agregado gastos para este día.",
        "promotions": "Promociones",
        "supermercado": "Supermercado",
        "promotion": "Promoción",
        "link": "Enlace",
        "expenses_by_category": "Gastos por Categoría",
        "savings_strategies": "Estrategias de Ahorro",
        "reduce_food_expenses": "- Reduzca los gastos de comida comiendo menos fuera y cocinando en casa más a menudo.",
        "use_public_transportation": "- Considere usar el transporte público, andar en bicicleta o caminar en lugar de conducir para ahorrar en gasolina y estacionamiento.",
        "find_free_entertainment": "- Encuentre opciones de entretenimiento gratuitas o de bajo costo, como visitar parques, asistir a eventos comunitarios o tomar prestados libros de la biblioteca.",
        "avoid_impulse_purchases": "- Evite las compras impulsivas y cree una lista de compras antes de ir a la tienda.",
        "conserve_energy": "- Ahorre energía apagando las luces al salir de una habitación, utilizando electrodomésticos de bajo consumo y ajustando el termostato.",
        "no_specific_strategies": "No se pudieron determinar estrategias de ahorro específicas en función de sus gastos actuales. Considere realizar un seguimiento más de cerca de sus gastos para identificar posibles áreas de ahorro.",
        "savings_goal_tab": "Meta de Ahorro",
        "expenses_tab": "Gastos",
        "strategies_tab": "Estrategias",
        "pareto_chart_title": "Gráfico de Pareto de Gastos por Fecha",
        "pie_chart_title": "Gastos por Categoría",
    },
}

# Set session state
if "language" not in st.session_state:
    st.session_state.language = "English"

# Update session state if language != st.session_state.language:
st.session_state.language = language

# Get translations for the selected language
t = translations[st.session_state.language]

# Main application content
st.markdown(f"<h1 style='text-align: center;'>{t['personal_savings_assistant']}</h1>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs([t["savings_goal_tab"], t["expenses_tab"], t["strategies_tab"]])

with tab1:
    # Savings Goal form
    st.header(t["savings_goal_tab"])
    savings_goal = st.number_input(t["enter_savings_goal"], min_value=0.0)
    timeframe = st.number_input(t["enter_timeframe"], min_value=1)
    income = st.number_input(t["enter_monthly_income"], min_value=0.0)

with tab2:
    # Expenses section
    st.header(t["expenses_tab"])
    selected_date = st.date_input(
        t["select_date"],
        min_value=datetime.date(2020, 1, 1),
        max_value=datetime.date(2030, 12, 31),
    )

    # Initialize session state for expenses
    if "expenses" not in st.session_state:
        st.session_state.expenses = {}

    # Expense categories
    expense_categories = [
        "Food",
        "Transportation",
        "Housing",
        "Entertainment",
        "Utilities",
        "Shopping",
        "Other",
    ]

    expense_categories_translation = {
        "English": {
            "Food": "Food",
            "Transportation": "Transportation",
            "Housing": "Housing",
            "Entertainment": "Entertainment",
            "Utilities": "Utilities",
            "Shopping": "Shopping",
            "Other": "Other",
        },
        "Español": {
            "Food": "Comida",
            "Transportation": "Transporte",
            "Housing": "Vivienda",
            "Entertainment": "Entretenimiento",
            "Utilities": "Servicios Públicos",
            "Shopping": "Compras",
            "Other": "Otro",
        },
    }

    # Get translations for expense categories
    et = expense_categories_translation[st.session_state.language]

    # Expense input form
    with st.form("expense_form"):
        st.subheader(t["select_date"])
        category = st.selectbox(t["expense_category"], [et[cat] for cat in expense_categories])
        amount = st.number_input(t["expense_amount"], min_value=0.0)
        submitted = st.form_submit_button(t["add_expense"])

        if submitted:
            if selected_date:
                date_str = selected_date.strftime("%Y-%m-%d")
                if date_str not in st.session_state.expenses:
                    st.session_state.expenses[date_str] = []
                st.session_state.expenses[date_str].append({"category": category, "amount": amount})
                st.success("Expense added!")
            else:
                st.error("Please select a date.")

    # Display expenses for the selected date
    if selected_date:
        date_str = selected_date.strftime("%Y-%m-%d")
        if date_str in st.session_state.expenses:
            st.subheader(f"Expenses for {selected_date.strftime('%Y-%m-%d')}")
            expenses = st.session_state.expenses[date_str]
            st.write(f"{t['date']}: {date_str}")
            for expense in expenses:
                st.write(f"- {t['category']}: {expense['category']}, {t['amount']}: ${expense['amount']:.2f}")
        else:
            st.write(t["no_expenses"])

    # Pareto Chart by Date
    st.header(t["pareto_chart_title"])

    # Calculate expenses by date
    expenses_by_date = {}
    for date_str, expenses in st.session_state.expenses.items():
        total_expenses = sum(expense["amount"] for expense in expenses)
        expenses_by_date[date_str] = total_expenses

    # Sort expenses by date in descending order
    sorted_expenses_by_date = sorted(expenses_by_date.items(), key=lambda x: x[1], reverse=True)

    # Calculate cumulative percentage
    cumulative_percentage = []
    total_expenses = sum(expenses_by_date.values())
    cumulative_sum = 0
    for date_str, expenses in sorted_expenses_by_date:
        cumulative_sum += expenses
        cumulative_percentage.append(cumulative_sum / total_expenses * 100)

    # Create Pareto chart
    dates = [date_str for date_str, expenses in sorted_expenses_by_date]
    expenses = [expenses for date_str, expenses in sorted_expenses_by_date]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Bar chart for expenses
    ax1.bar(dates, expenses, color="steelblue", label="Expenses")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Expenses", color="steelblue")
    ax1.tick_params(axis="y", labelcolor="steelblue")

    # Create a second y-axis for cumulative percentage
    ax2 = ax1.twinx()
    ax2.plot(dates, cumulative_percentage, color="red", marker="o", label="Cumulative Percentage")
    ax2.set_ylabel("Cumulative Percentage", color="red")
    ax2.tick_params(axis="y", labelcolor="red")
    ax2.set_ylim(0, 100)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha="right")

    # Add title and legend
    plt.title("Pareto Chart of Expenses by Date")
    plt.legend(loc="upper left")

    # Show grid
    plt.grid(True)

    # Display the chart in Streamlit
    st.pyplot(fig)

    # Calculate expenses by category
    expenses_by_category = {}
    for date_str, expenses in st.session_state.expenses.items():
        for expense in expenses:
            category = expense["category"]
            amount = expense["amount"]
            if category not in expenses_by_category:
                expenses_by_category[category] = 0
            expenses_by_category[category] += amount

    st.header(t["expenses_by_category"])
    # Create pie chart
    if expenses_by_category:
        fig, ax = plt.subplots()
        ax.pie(expenses_by_category.values(), labels=expenses_by_category.keys(), autopct="%1.1f%%")
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
        st.caption(t["pie_chart_title"])
    else:
        st.write("No expenses added yet.")

with tab3:

    # Function to generate savings strategies using OpenAI
    def generate_savings_strategies_gemini(income, expenses, savings_goal, language):
        prompt = f"""
        Financial situation:
            - Monthly Income: ${income}
            - Monthly Expenses: ${expenses}
            - Savings Goal: ${savings_goal}

        Provide 3 personalized savings strategies in {language} language.
        Each strategy should be concise and actionable.
        """
        try:
            client = openai.OpenAI()
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            print(f"OpenAI API Key: {openai.api_key}")
            print(f"OpenAI API Response: {completion}")
            time.sleep(5)  # Add a 5-second delay to avoid exceeding the quota
            return completion.choices[0].message.content
        except openai.AuthenticationError as e:
            print(f"OpenAI AuthenticationError: {e}")
            return "Error: OpenAI Authentication failed. Please check your API key."
        except openai.APIConnectionError as e:
            print(f"OpenAI APIConnectionError: {e}")
            return "Error: Could not connect to OpenAI API. Please check your internet connection."
        except openai.RateLimitError as e:
            print(f"OpenAI RateLimitError: {e}")
            return "Error: OpenAI Rate Limit exceeded. Please try again later."
        except Exception as e:
            print(f"Error generating content: {e}")
            return f"Error generating content: {e}. Please check the logs for more details and try again later."

    # Modify get_savings_strategies function to use Gemini
    def get_savings_strategies(income, expenses_by_category, savings_goal, language):
        strategies = []
        # Call Gemini to generate savings strategies
        print("Expenses by category:", expenses_by_category)
        gemini_strategies = generate_savings_strategies_gemini(income, sum(expenses_by_category.values()), savings_goal, language)
        strategies.append(gemini_strategies)
        return strategies

    # Generate savings strategies
    st.write("Expenses by category:", expenses_by_category)
    savings_strategies = get_savings_strategies(income, expenses_by_category, savings_goal, st.session_state.language)

    # Display savings strategies
    st.write("The following savings strategies are based on the expenses you have entered:")
    st.write(savings_strategies)