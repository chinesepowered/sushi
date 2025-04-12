from nearai.agents.environment import Environment
import re


def run(env: Environment):
    messages = env.list_messages()
    
    if not messages:
        # Initial message
        system_prompt = {
            "role": "system", 
            "content": "I'm an AI Code Auditor that evaluates AI agent code for risks and quality. When a user pastes code, analyze it for:\n"
                      "1. Code complexity (length, nesting)\n"
                      "2. Security risks (eval, exec, insecure patterns)\n" 
                      "3. AI-specific bad patterns (high temperature, token limits, prompt injection risks)\n"
                      "4. TODO comments and incomplete functions\n\n"
                      "Return:\n"
                      "- Overall risk score out of 10\n"
                      "- List of key findings\n"
                      "- Specific recommendations for improvement\n"
                      "- For any TODO comments or incomplete functions, suggest proper implementations"
        }
        env.add_reply("Welcome to the AI Code Auditor! Paste your AI agent code, and I'll analyze it for risks, complexity, and provide recommendations for improvement.")
        env.completion([system_prompt])
        env.request_user_input()
        return
    
    # Extract code from the latest message and pass it to LLM for analysis
    latest_message = messages[-1]['content']
    
    # Check if the message contains code
    if "```" in latest_message:
        # Extract code between backticks
        code_blocks = re.findall(r"```(?:python)?(.*?)```", latest_message, re.DOTALL)
        if code_blocks:
            code = "\n".join(code_blocks)
        else:
            code = latest_message
    else:
        code = latest_message
    
    # Create a prompt for code analysis
    analysis_prompt = [
        {"role": "system", "content": "You are an AI code auditor that evaluates code for risks and quality issues. Analyze the provided code and return a risk assessment with recommendations."},
        {"role": "user", "content": f"Analyze this AI agent code and provide:\n\n"
                                   f"1. An overall risk score out of 10 (where 10 is best)\n"
                                   f"2. Key findings about code complexity, security issues, and AI patterns\n"
                                   f"3. Recommendations for improvement\n"
                                   f"4. For any TODO comments or incomplete/empty functions, suggest proper implementations\n\n"
                                   f"CODE:\n```\n{code}\n```"}
    ]
    
    # Get analysis from the LLM
    result = env.completion(analysis_prompt)
    
    # Send response
    env.add_reply(result)
    env.request_user_input()


run(env)

