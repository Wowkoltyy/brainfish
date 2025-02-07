from g4f.client import Client

model="gpt-4o-mini"
client = Client()

def answer_from_ai(data) : 
    response = client.chat.completions.create(
        model = model,
        messages =[{role: '''You are an expert in identifying and analyzing phishing, scam, and malicious websites. Your task is to evaluate the provided website and return a single malicious score from 0 to 100, where 0 indicates a safe site and 100 indicates a highly malicious site.
Consider the following variables:
 • Current URL: {URL}
 • User History: {HISTORY}
 • Visible Text on Page: {VISIBLE_TEXT}
 • Page HTML: {PAGE_HTML}
 • Page Assets: {PAGE_ASSETS}
 • User Report Score: {REPORT_SCORE}
 • DNS Information: {DNS_INFO}
Internal Guidelines for Analysis:
 1 Domain Name Similarity: Phishing and scam websites often use domain names that closely resemble legitimate sites by altering characters (e.g., "discord" to "disc0rd"). Check if the current URL follows this pattern.
 2 JavaScript and HTML Construction: Malicious sites frequently obfuscate their JavaScript code and create HTML structures that mimic legitimate websites. Analyze the provided HTML and assets for signs of obfuscation or unusual scripts that may indicate malicious intent.
 3 User Manipulation Techniques: Drainers and stealers employ various tactics to trick users into approving transactions, such as misleading text, images, or videos. Review the visible text and media on the page for any manipulative content designed to deceive users.
 4 DNS and Security Measures: Scammers often use services like Cloudflare to mask their real IP addresses and may create subdomains to mislead users (e.g., "captcha.bot" vs. "captcha.bot-verification.com"). Examine the DNS information for any indicators of such practices.
 5 Overall Malicious Score: Based on the analysis of the above factors, assign a malicious score from 0 to 100 to the current URL, taking into account the user report score and all other materials provided.
Return only the malicious score as your output.'''.format(URL=data['url'], HISTORY=data['history'], VISIBLE_TEXT=data['visible_text'], PAGE_HTML=data['page_html'], PAGE_ASSETS = data['page_assets']), 'history': data["urls"]}],
        web_search=False
    )
    return response.choices[0].message.content