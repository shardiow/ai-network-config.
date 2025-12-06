from jinja2 import Environment, FileSystemLoader

def render_template(vendor, data):
    # Set up Jinja2 to look in the 'templates/' folder
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
    
    template_name = f"{vendor}.j2"
    template = env.get_template(template_name)
    
    return template.render(data)