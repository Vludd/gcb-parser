last_event_with_buttons = None

def show_event(event, label="💬"):
    global last_event_with_buttons
    print(f'\n{label}: {event.raw_text}')

    if event.buttons:
        print("┌─[Buttons]:")
        flat_buttons = []
        for row in event.buttons:
            for button in row:
                flat_buttons.append(button)
                print(f"[{len(flat_buttons)-1}] {button.text}")
        last_event_with_buttons = event
    else:
        last_event_with_buttons = None

    print("> ", end='', flush=True)