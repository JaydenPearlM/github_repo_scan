def build_analysis_prompt(repo_name, files):
    file_sections = []

    for file in files:
        file_sections.append(
            f"""
FILE: {file['path']}

{file['content']}
"""
        )

    return f"""
You are a senior software engineer and code reviewer.

Analyze this repository:

{repo_name}

Code:
{"".join(file_sections)}

Output must be clean markdown with these sections:

# Strong Code
Identify the best code and explain why it is strong.

# Weak Code
Identify weak or questionable code and explain why.

# Engineering Breakdown
Explain architecture, structure, and decisions.

# Improvements
Give direct improvements.

# LinkedIn Post
Write a clean professional LinkedIn post.
No emojis.
No em dashes.
Make it sound human and confident.

# Hashtags
Provide 5-8 relevant hashtags.
"""