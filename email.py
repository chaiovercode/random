from email import policy
from email.parser import BytesParser
from email.generator import BytesGenerator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timezone, timedelta
import email.utils
import os

# === CONFIGURATION ===
# Paths relative to your Obsidian vault, or absolute paths
input_path = "attachments/original.eml"     # EML to load
output_path = "attachments/cleaned.eml"     # Final output EML
pdf_path = "attachments/extra-doc.pdf"      # PDF to attach

# === LOAD ORIGINAL EMAIL ===
with open(input_path, 'rb') as f:
    msg = BytesParser(policy=policy.default).parse(f)

# === SET CUSTOM DATE ===
ist = timezone(timedelta(hours=5, minutes=30))
custom_date = datetime(2025, 7, 11, 13, 35, 0, tzinfo=ist)
formatted = email.utils.format_datetime(custom_date)
if 'Date' in msg:
    msg.replace_header('Date', formatted)
else:
    msg['Date'] = formatted
print(f"✓ Date set to: {formatted}")

# === STRIP INTERNAL HEADERS ===
internal_headers = [
    k for k in msg.keys()
    if k.lower().startswith('received')
    or k.lower().startswith('arc')
    or (k.lower().startswith('x-') and not k.startswith("X-Gm"))
]
for k in internal_headers:
    del msg[k]
print(f"✓ Removed {len(internal_headers)} internal headers")

# === EXTRACT BODY + INLINE IMAGES ===
plain_body = None
html_body = None
inline_images = []

for part in msg.walk():
    content_type = part.get_content_type()
    disposition = part.get_content_disposition()
    content_id = part.get('Content-ID')
    charset = part.get_content_charset() or 'utf-8'

    if disposition == 'attachment':
        continue  # remove all true attachments
    elif content_type == 'text/plain':
        plain_body = part.get_payload(decode=True).decode(charset, errors='replace')
    elif content_type == 'text/html':
        html_body = part.get_payload(decode=True).decode(charset, errors='replace')
    elif disposition == 'inline' and content_id:
        inline_images.append(part)

# === BUILD CLEAN EMAIL STRUCTURE ===
clean_msg = MIMEMultipart()
for k, v in msg.items():
    clean_msg[k] = v

# Build nested MIME: alternative inside related
related = MIMEMultipart("related")
alt = MIMEMultipart("alternative")

if plain_body:
    alt.attach(MIMEText(plain_body, "plain", _charset="utf-8"))
if html_body:
    alt.attach(MIMEText(html_body, "html", _charset="utf-8"))
related.attach(alt)

# Attach inline images
for img in inline_images:
    related.attach(img)
    print(f"✓ Preserved inline image: {img.get_filename()}")

clean_msg.attach(related)
print("✓ Attached body and inline images")

# === ADD NEW PDF ATTACHMENT ===
if os.path.exists(pdf_path):
    with open(pdf_path, 'rb') as f:
        part = MIMEBase('application', 'pdf')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{os.path.basename(pdf_path)}"'
        )
        clean_msg.attach(part)
    print(f"✓ Attached new PDF: {os.path.basename(pdf_path)}")
else:
    print("✗ PDF not found, skipping attachment")

# === SAVE FINAL EMAIL ===
with open(output_path, 'wb') as f:
    BytesGenerator(f, policy=policy.default).flatten(clean_msg)

print(f"✓ Final email saved to: {output_path}")