import os

def notify(title, subtitle, message, url):
    os.system(f"""terminal-notifier -title '{title}' -subtitle '{subtitle}' -message '{message}' -open '{url}'""")

