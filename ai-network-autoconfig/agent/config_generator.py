import openai
import json
from template_renderer import render_template
 
def generate_and_save_config(device_name, vendor, intent):
    # 1. Instruct the LLM to output a JSON object containing the data needed for the template
    prompt = f"""
    You are a network engineer. Based on the following intent, generate a JSON object 
    containing the variables needed to fill the {vendor} template. 
    
    Intent: {intent}
    
    Available variables in the template are: hostname, ip, mask, network.
    
    Output ONLY the JSON object. Do not include any explanation or markdown.
    """
 
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", # Use a reliable model for JSON output
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        json_data = json.loads(response["choices"][0]["message"]["content"])
        
        # 2. Use the generated JSON data to fill the safe Jinja2 template
        final_config = render_template(vendor, json_data)
        
        # 3. Save the final configuration to the desired-configs folder
        desired_file = f"desired-configs/{device_name}.cfg"
        with open(desired_file, 'w') as f:
            f.write(final_config)
            
        print(f"[✓] New config generated for {device_name} and saved to {desired_file}")
        
    except (json.JSONDecodeError, Exception) as e:
        print(f"[!] Error processing AI response: {e}")
        return None

# Example usage to test the LLM agent:
# generate_and_save_config(
#     device_name="r1", 
#     vendor="cisco", 
#     intent="Set the hostname to R1-CORE and configure interface G0/0 with 10.0.0.1/24. OSPF network 10.0.0.0 area 0."
# )