import pandas as pd
import gradio as gr

df = pd.read_csv('../data/recipes_df.csv').fillna("").applymap(lambda x: x.replace('\xa0', ' ') if isinstance(x, str) else x)

chat_state = {
    "step": "start",
    "category": None,
    "ingredients": None,
    "current_index": 0,
    "filtered_df": None,
    "recipes_to_show": None,
    "selected_recipe": None
}


def chatbot(message):
    global chat_state
    print(f"Message received: {message}")
    print(f"Current state: {chat_state}")

    # Reset czatu po wpisaniu "start"
    if message.lower() == "start":
        chat_state = {
            "step": "start",
            "category": None,
            "ingredients": None,
            "current_index": 0,
            "filtered_df": None,
            "recipes_to_show": None,
            "selected_recipe": None
        }
        return "💬 **Czat został zresetowany. Witaj ponownie!** 🥗 Jakich składników chciałbyś/chciałabyś użyć w swoim daniu? 🍲"

    if chat_state["step"] == "start":
        chat_state["step"] = "ingredients"
        return "👋 **Witaj!** Jakich składników chciałbyś/chciałabyś użyć w swoim daniu? 🥕🍅"

    elif chat_state["step"] == "ingredients":
        chat_state["ingredients"] = message.lower().split(', ')
        filtered_df = df[df['ingredients_lemmatized'].apply(
            lambda x: all(ing in x.lower() for ing in chat_state["ingredients"])
        )]

        if len(filtered_df) == 0:
            return "😔 **Niestety, nie znalazłem przepisów z tymi składnikami.** Może spróbujmy innych składników? 🧐"

        chat_state["filtered_df"] = filtered_df
        categories = filtered_df['category'].unique()
        chat_state["step"] = "category"
        return f"✅ **Znalazłem przepisy z tymi składnikami w następujących kategoriach:** {', '.join(categories)}. 📂 Którą kategorię wybierasz?"

    elif chat_state["step"] == "category":
        category = message.strip()
        chat_state["category"] = category

        filtered_df = chat_state["filtered_df"][
            chat_state["filtered_df"]['category'].str.lower().str.strip() == category.lower().strip()
        ]

        if len(filtered_df) == 0:
            return f"🚫 **Niestety, nie znalazłem przepisów w kategorii:** {category}. Może spróbujmy czegoś innego? 🧐"

        chat_state["filtered_df"] = filtered_df
        chat_state["step"] = "choose_partial"
        return "🔍 **Znalazłem przepisy.** Czy chcesz zobaczyć pierwsze 5 przepisów? (tak/nie) 📝"

    elif chat_state["step"] == "choose_partial":
        if message.lower() == "tak":
            partial_recipes = chat_state["filtered_df"]
            start = chat_state["current_index"]
            end = start + 5
            chat_state["current_index"] = end

            recipes_to_show = partial_recipes.iloc[start:end]
            chat_state["recipes_to_show"] = recipes_to_show
            if recipes_to_show.empty:
                return "😕 **Nie ma więcej przepisów do pokazania.** Czy chcesz wybrać coś z wcześniej pokazanych? (Podaj numer lub 'nie')"

            response = "🍽️ **Oto przepisy:**\n"
            for i, (_, row) in enumerate(recipes_to_show.iterrows(), start=1):
                response += f"{i}. **{row['title']}** (Brakuje: {', '.join(set(row['ingredients_lemmatized'].split(', ')) - set(chat_state['ingredients']))})\n"
            response += "\n📋 **Podaj numer przepisu, który chcesz wybrać, lub 'nie' jeśli nie chcesz.**"
            chat_state["step"] = "select_recipe"
            return response

        elif message.lower() == "nie":
            return "🙋‍♂️ **Dziękuję za skorzystanie z naszego chatbota.** Do zobaczenia następnym razem! 👋"

        else:
            return "⚠️ **Nie zrozumiałem odpowiedzi.** Proszę odpowiedzieć 'tak' lub 'nie'."

    elif chat_state["step"] == "select_recipe":
        try:
            recipe_number = int(message)
            recipes_to_show = chat_state["recipes_to_show"]

            if 1 <= recipe_number <= len(recipes_to_show):
                selected_recipe = recipes_to_show.iloc[recipe_number - 1]
                chat_state["selected_recipe"] = selected_recipe
                chat_state["step"] = "display_recipe"
                return f"🍴 **Wybrałeś przepis:** {selected_recipe['title']}. Co chcesz zobaczyć?\n1. 🥕 **Składniki**\n2. 🧾 **Instrukcje**\n3. 📸 **Zdjęcie (link)**\nWybierz opcję (1, 2 lub 3)."
            else:
                return "❌ **Niestety, nie ma przepisu o tym numerze.** Proszę wybrać numer z listy."
        except ValueError:
            return "⚠️ **Proszę podać numer przepisu, a nie tekst.**"

    elif chat_state["step"] == "display_recipe":
        option = message.strip()
        recipe = chat_state["selected_recipe"]

        if option == "1":
            ingredients = ', '.join(eval(recipe['ingredients'])) if isinstance(recipe['ingredients'], str) else recipe['ingredients']
            return f"🥕 **Składniki:** {ingredients}"
        elif option == "2":
            instructions = ' '.join(eval(recipe['instructions'])) if isinstance(recipe['instructions'], str) else recipe['instructions']
            return f"📝 **Instrukcje:** {instructions}"
        elif option == "3":
            return f"🖼️ **Zdjęcie (link):** {recipe['image_url']}"
        else:
            return "Nieprawidłowa opcja. Wybierz 1, 2 lub 3."
    return "🤔 **Przepraszam, nie zrozumiałem.** Czy możesz powtórzyć?"


iface = gr.Interface(fn=chatbot, inputs="text", outputs="text")
iface.launch()
