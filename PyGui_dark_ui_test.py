import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Main Window', width=400, height=200)
dpg.setup_dearpygui()

# Create a theme for the button
with dpg.theme() as button_theme:
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [76, 175, 80, 255])        # #4CAF50
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [69, 160, 73, 255]) # #45a049
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [69, 160, 73, 255])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])

with dpg.window(label="Main Window"):
    dpg.add_spacing(count=10)
    dpg.add_text("Lighter Box with White Text", color=[255,255,255])
    dpg.add_separator()
    btn = dpg.add_button(label="Styled Button")
    dpg.bind_item_theme(btn, button_theme)

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()