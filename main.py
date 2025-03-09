from customtkinter import *
import json
from CTkMessagebox import CTkMessagebox
from datetime import datetime


def read_file(filepath):
    try:
        with open(filepath, 'r', encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        CTkMessagebox(root, message=str(e), icon="cancel", title="Error")


def clear_order():
    global order
    for x in range(len(order)):
        order[x][0].grid_forget()
        order[x][1].grid_forget()
        order[x][2].grid_forget()
        order[x][3].grid_forget()
    order.clear()


def clear_order():
    for x in range(len(order)):
        order[x][0].grid_forget()
        order[x][1].grid_forget()
        order[x][2].grid_forget()
        order[x][3].grid_forget()


def load_order():
    clear_order()
    for i in range(len(order)):
        order[i][0].grid(row=i, column=1, padx=10, sticky="w")
        order[i][1].grid(row=i, column=2, padx=70)
        order[i][2].grid(row=i, column=3, padx=10)
        order[i][3].grid(row=i, column=4, padx=10)


def find_item(current, item_name) -> bool:
    match current:
        case "Десерти":
            if item_name in list(data["desserts"].keys()):
                return True
        case "Гарячі напої":
            if item_name in list(data["hot_drinks"].keys()):
                return True
        case "Холодні напої":
            if item_name in list(data["cold_drinks"].keys()):
                return True
        case "Обіди":
            if item_name in data["dinners"]:
                return True
    return False


def add_order():
    global o_value
    if not find_item(menu_frames_toggle.get(), order_input.get()):
        CTkMessagebox(root, message="Такої їжі немає!", icon="cancel", title="Error")
        return
    current = ""
    tail = ""
    match menu_frames_toggle.get():
        case "Десерти":
            current = "desserts"
            tail = "г"
        case "Гарячі напої":
            current = "hot_drinks"
            tail = "мл"
        case "Холодні напої":
            current = "cold_drinks"
            tail = "мл"
        case "Обіди":
            current = "dinners"
    c_input = order_input.get()
    empty_str = CTkLabel(orders_list, text="")
    item_name = CTkLabel(orders_list, text=f"{c_input}", font=("sans-serif", 18), text_color="black", wraplength=200)
    item_price = CTkLabel(orders_list, text=f"{data[current][c_input]["price"] if current != "dinners" else 165} грн",
                          font=("sans-serif", 18), text_color="black", wraplength=200)
    item_w_v = CTkLabel(orders_list,
                        text=f"{data[current][c_input]['w_v'] if current != 'dinners' else ''} {tail}",
                        font=("sans-serif", 18), text_color="black", wraplength=200)
    order.append([item_name, empty_str, item_price, item_w_v])
    o_value = float(o_value) + data[current][c_input]["price"] if current != "dinners" else 165
    order_value.configure(text=f"{o_value:.2f} грн")
    load_order()


def del_order():
    global o_value
    list_of_names = [i[0].cget("text") for i in order]
    if order_input.get() not in list_of_names:
        CTkMessagebox(root, message="Такого не має!", icon="cancel", title="Error")
        return
    index = list_of_names.index(order_input.get())
    o_value = (float(o_value) - float(order[index][2].cget("text").replace(" грн", "")))
    order_value.configure(text=f"{o_value:.2f} грн")
    if len(order) == 1:
        order[index][0].grid_forget()
        order[index][1].grid_forget()
        order[index][2].grid_forget()
        order[index][3].grid_forget()
        order.pop(index)
        return
    else:
        order.pop(index)
    load_order()


def make_order():
    global o_value
    if not order:
        return
    try:
        with open("./DataBase/customer_order.json", "w", encoding="utf-8") as f:
            now = f"{datetime.now().strftime('%d.%m.%Y %H:%M')}"
            js_data = {now: {"total_price": o_value, "orders": []}}
            for i in range(len(order)):
                js_data[now]["orders"].append([order[i][0].cget("text"), order[i][2].cget("text"),
                                               order[i][3].cget("text")])

            json.dump(js_data, f, ensure_ascii=False, indent=4)
        clear_order()
        order.clear()
        o_value = 0
        order_value.configure(text=f"{o_value} грн")
        CTkMessagebox(root, message='Замовлення успішно відправлено!', icon="check", title="Success")
    except Exception as e:
        CTkMessagebox(root, message=str(e), icon="cancel", title="Error")


def change_menu_frames(current):
    match current:
        case "Десерти":
            cold_drinks_frame.place_forget()
            hot_drinks_frame.place_forget()
            dinners_frame.place_forget()
            desserts_frame.place(y=60, x=root_x - 500 - 10)
        case "Гарячі напої":
            cold_drinks_frame.place_forget()
            desserts_frame.place_forget()
            dinners_frame.place_forget()
            hot_drinks_frame.place(y=60, x=root_x - 500 - 10)
        case "Холодні напої":
            desserts_frame.place_forget()
            hot_drinks_frame.place_forget()
            dinners_frame.place_forget()
            cold_drinks_frame.place(y=60, x=root_x - 500 - 10)
        case "Обіди":
            desserts_frame.place_forget()
            hot_drinks_frame.place_forget()
            cold_drinks_frame.place_forget()
            dinners_frame.place(y=60, x=root_x - 500 - 10)


root_x = 1200
root_y = 800
data = read_file("./DataBase/dishes.json")
order = []
o_value = 0

root = CTk()
root.title('Cafe menu')
root.geometry(f'{root_x}x{root_y}+0+0')
set_appearance_mode("light")
root.resizable(False, False)

menu_frames_btns = ["Десерти", "Гарячі напої", "Холодні напої", "Обіди"]
menu_frames_toggle = CTkSegmentedButton(root, width=400, height=40, values=menu_frames_btns,
                                        selected_color="sienna1",
                                        fg_color="navajo white",
                                        unselected_color="navajo white", corner_radius=6, font=("sans-serif", 16),
                                        text_color="black",
                                        selected_hover_color="sienna1",
                                        unselected_hover_color="navajo white",
                                        command=change_menu_frames)
menu_frames_toggle.place(x=root_x - 40 - 400, y=10)
menu_frames_toggle.set("Десерти")

desserts_frame = CTkScrollableFrame(root, fg_color="antique white", corner_radius=8, width=460, height=root_y - 90,
                                    border_width=2, border_color="rosy brown", scrollbar_fg_color="transparent",
                                    scrollbar_button_color="rosy brown")
desserts_frame.place(y=60, x=root_x - 500 - 10)
desserts_frame_header = CTkLabel(desserts_frame, text="Десерти", font=("sans-serif", 20), text_color="black")
desserts_frame_header.grid(row=0, column=0, columnspan=4, pady=10)

row_counter = 1
for dessert in list(data["desserts"].keys()):
    r_p = data["desserts"]
    name = CTkLabel(desserts_frame, text=dessert, text_color="black", font=("sans-serif", 16), wraplength=200)
    price = CTkLabel(desserts_frame, text=f"{r_p[dessert]["price"]}грн", font=("sans-serif", 16), wraplength=60)
    w_v = CTkLabel(desserts_frame, text=f"{r_p[dessert]['w_v']}г", font=("sans-serif", 16), wraplength=60)
    name.grid(row=row_counter, column=0, padx=10, sticky="W")
    CTkLabel(desserts_frame, text="").grid(row=row_counter, column=1, padx=70)
    price.grid(row=row_counter, column=2, padx=10)
    w_v.grid(row=row_counter, column=3, padx=10)
    row_counter += 1

hot_drinks_frame = CTkScrollableFrame(root, fg_color="antique white", corner_radius=8, width=460, height=root_y - 90,
                                      border_width=2, border_color="rosy brown", scrollbar_fg_color="transparent",
                                      scrollbar_button_color="rosy brown")
hot_drinks_frame.place(y=60, x=root_x - 500 - 10)
hot_drinks_frame_header = CTkLabel(hot_drinks_frame, text="Гарячі напої", font=("sans-serif", 20), text_color="black")
hot_drinks_frame_header.grid(row=0, column=0, columnspan=4, pady=10)

row_counter = 1
for h_drink in list(data["hot_drinks"].keys()):
    r_p = data["hot_drinks"]
    name = CTkLabel(hot_drinks_frame, text=h_drink, text_color="black", font=("sans-serif", 16), wraplength=200)
    price = CTkLabel(hot_drinks_frame, text=f"{r_p[h_drink]["price"]}грн", font=("sans-serif", 16), wraplength=60)
    w_v = CTkLabel(hot_drinks_frame, text=f"{r_p[h_drink]['w_v']}{"мл" if r_p[h_drink]["w_v"] else ""}",
                   font=("sans-serif", 16), wraplength=60)
    name.grid(row=row_counter, column=0, padx=10, sticky="w")
    CTkLabel(hot_drinks_frame, text="").grid(row=row_counter, column=1, padx=70)
    price.grid(row=row_counter, column=2, padx=10)
    w_v.grid(row=row_counter, column=3, padx=10)
    row_counter += 1
hot_drinks_frame.place_forget()

cold_drinks_frame = CTkScrollableFrame(root, fg_color="antique white", corner_radius=8, width=460, height=root_y - 90,
                                       border_width=2, border_color="rosy brown", scrollbar_fg_color="transparent",
                                       scrollbar_button_color="rosy brown")
cold_drinks_frame.place(y=60, x=root_x - 500 - 10)
cold_drinks_frame_header = CTkLabel(cold_drinks_frame, text="Холодні напої", font=("sans-serif", 20),
                                    text_color="black")
cold_drinks_frame_header.grid(row=0, column=0, columnspan=4, pady=10)

row_counter = 1
for c_drink in list(data["cold_drinks"].keys()):
    r_p = data["cold_drinks"]
    name = CTkLabel(cold_drinks_frame, text=c_drink, text_color="black", font=("sans-serif", 16), wraplength=200)
    price = CTkLabel(cold_drinks_frame, text=f"{r_p[c_drink]["price"]}грн", font=("sans-serif", 16), wraplength=60)
    w_v = CTkLabel(cold_drinks_frame, text=f"{r_p[c_drink]['w_v']}{"мл" if r_p[c_drink]["w_v"] else ""}",
                   font=("sans-serif", 16), wraplength=60)
    name.grid(row=row_counter, column=0, padx=10, sticky="w")
    CTkLabel(cold_drinks_frame, text="").grid(row=row_counter, column=1, padx=70)
    price.grid(row=row_counter, column=2, padx=10)
    w_v.grid(row=row_counter, column=3, padx=10)
    row_counter += 1
cold_drinks_frame.place_forget()

dinners_frame = CTkScrollableFrame(root, fg_color="antique white", corner_radius=8, width=460, height=root_y - 90,
                                   border_width=2, border_color="rosy brown", scrollbar_fg_color="transparent",
                                   scrollbar_button_color="rosy brown")
dinners_frame.place(y=60, x=root_x - 500 - 10)
dinners_frame_header = CTkLabel(dinners_frame, text="Обіди", font=("sans-serif", 20), text_color="black")
dinners_frame_header.grid(row=0, column=0, columnspan=4, pady=10)

row_counter = 1
for dinner in data["dinners"]:
    name = CTkLabel(dinners_frame, text=dinner, text_color="black", font=("sans-serif", 16), wraplength=200)
    price = CTkLabel(dinners_frame, text=f"165 грн", font=("sans-serif", 16), wraplength=60)
    name.grid(row=row_counter, column=0, padx=10, sticky="w")
    CTkLabel(dinners_frame, text="").grid(row=row_counter, column=1, padx=70)
    price.grid(row=row_counter, column=2, padx=10)
    row_counter += 1
dinners_frame.place_forget()

page_header = CTkLabel(root, text="Меню", font=("sans-serif", 34), text_color="black")
page_header.place(y=100, x=300)

name_of_order = CTkLabel(root, text="Ведіть назву замовлення:", font=("sans-serif", 24), text_color="black")
name_of_order.place(y=180, x=30)

order_input = CTkEntry(root, width=550, height=50, font=("sans-serif", 18), border_color="rosy brown", border_width=2,
                       corner_radius=8)
order_input.place(y=220, x=30)

btn_plate = CTkFrame(root, fg_color="transparent")
btn_plate.place(y=300, x=30)
add_btn = CTkButton(btn_plate, width=150, height=40, text="Додати в список", fg_color="sienna1", corner_radius=8,
                    hover_color="rosy brown", font=("sans-serif", 18), text_color="black", command=add_order)
add_btn.grid(row=0, column=0, padx=10)

del_btn = CTkButton(btn_plate, width=150, height=40, text="Видалити зі списку", fg_color="sienna1", corner_radius=8,
                    hover_color="rosy brown", font=("sans-serif", 18), text_color="black", command=del_order)
del_btn.grid(row=0, column=1, padx=10)

make_order_btn = CTkButton(btn_plate, width=150, height=40, text="Замовити", fg_color="sienna1", corner_radius=8,
                           hover_color="rosy brown", font=("sans-serif", 18), text_color="black", command=make_order)
make_order_btn.grid(row=0, column=2, padx=10)

order_list_label = CTkLabel(root, text="Ваші завмовлення", font=("sans-serif", 16), text_color="black")
order_list_label.place(y=375, x=35)
order_value_label = CTkLabel(root, text="Загальна вартість: ", font=("sans-serif", 16), text_color="black")
order_value_label.place(y=375, x=335)
order_value = CTkLabel(root, text=f"{o_value} грн", font=("sans-serif", 16), wraplength=100)
order_value.place(y=375, x=480)

orders_list = CTkScrollableFrame(root, width=550, height=370, border_color="rosy brown",
                                 corner_radius=8, fg_color="antique white", border_width=2,
                                 scrollbar_button_color="rosy brown")
orders_list.place(y=400, x=30)
root.mainloop()
