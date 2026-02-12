import os
import re

def remove_contact_info(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'index.html' and root != directory:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # More robust pattern to match the contact-info-box div
                pattern = r'\s*<div class="contact-info-box".*?</div>\s*</div>\s*(?=<!-- Registration Closed -->)'
                
                # Let's try to match from <div class="contact-info-box" until the closing </div> of that specific box.
                # Since it has nested divs, we need to be careful.
                # However, in this specific case, it seems the contact-info-box has one inner div that wraps the contact-groups.
                
                # Let's use a simpler approach: match from <div class="contact-info-box" up to the comment "Registration Closed"
                new_content = re.sub(r'\s*<div class="contact-info-box".*?\s*(?=<!-- Registration Closed -->)', '\n\n    ', content, flags=re.DOTALL)
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {file_path}")
                else:
                    print(f"No match in {file_path}")

if __name__ == "__main__":
    remove_contact_info('Registration')
