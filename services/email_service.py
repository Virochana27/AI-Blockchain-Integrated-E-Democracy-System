# services/email_service.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def send_otp_email(to_email, otp):
    print(f"[OTP SENT] {to_email} -> {otp}")
    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    smtp_host = os.getenv("MAIL_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("MAIL_PORT", 587))

    if not sender_email or not sender_password:
        raise Exception("Email service not configured")

    subject = "Your OTP — E-Democracy System"

    html_body = f"""
    <html>
    <body style="margin:0; padding:0; background-color:#f5f5f7; font-family: 'DM Sans', Arial, sans-serif;">

      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f7; padding: 40px 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:4px; overflow:hidden; box-shadow: 0 2px 16px rgba(79,70,229,0.08); border: 1px solid rgba(79,70,229,0.12);">

              <!-- HEADER / LOGO -->
              <tr>
                <td style="background-color:#ffffff; padding: 28px 40px 20px 40px; border-bottom: 1px solid rgba(79,70,229,0.1);">
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="vertical-align: middle; padding-right: 12px;">
                        <div style="width:40px; height:40px; background: rgba(79,70,229,0.08); border: 1.5px solid rgba(79,70,229,0.2); border-radius:4px; display:inline-block; text-align:center; line-height:40px; font-size:18px;">🗳️</div>
                      </td>
                      <td style="vertical-align: middle;">
                        <div style="font-family: Arial Black, sans-serif; font-size: 1.3rem; letter-spacing: 0.06em; color: #4f46e5; line-height:1;">E-DEMOCRACY</div>
                        <div style="font-family: 'Courier New', monospace; font-size: 0.5rem; letter-spacing: 0.3em; text-transform: uppercase; color: #888; line-height:1; margin-top:2px;">AI · BLOCKCHAIN · GOVERNANCE</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- HERO BAND -->
              <tr>
                <td style="background: linear-gradient(135deg, #4f46e5 0%, #0d9488 100%); padding: 36px 40px;">
                  <p style="margin:0 0 6px 0; font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.2em; text-transform:uppercase; color:rgba(255,255,255,0.7);">Identity Verification</p>
                  <h1 style="margin:0; font-size:1.9rem; font-weight:700; color:#ffffff; line-height:1.2;">Your One-Time<br>Password (OTP) 🔐</h1>
                  <p style="margin:12px 0 0 0; font-size:0.92rem; color:rgba(255,255,255,0.8); line-height:1.6;">Use the code below to verify your identity. Do not share this code with anyone.</p>
                </td>
              </tr>

              <!-- OTP BOX -->
              <tr>
                <td style="padding: 40px 40px 24px 40px; text-align:center;">
                  <p style="margin:0 0 16px 0; font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; color:#4f46e5; font-weight:700;">Your OTP Code</p>
                  <div style="display:inline-block; background: rgba(79,70,229,0.06); border: 1.5px solid rgba(79,70,229,0.2); border-radius:4px; padding: 20px 48px;">
                    <span style="font-family:'Courier New',monospace; font-size:2.6rem; font-weight:700; color:#4f46e5; letter-spacing:0.35em;">{otp}</span>
                  </div>
                </td>
              </tr>

              <!-- WARNING BOX -->
              <tr>
                <td style="padding: 8px 40px 36px 40px;">
                  <table width="100%" cellpadding="0" cellspacing="0" style="background:rgba(13,148,136,0.07); border-left:3px solid #0d9488; border-radius:0 4px 4px 0;">
                    <tr>
                      <td style="padding:14px 18px;">
                        <p style="margin:0; font-size:0.88rem; color:#0f0f14; line-height:1.6;">⏱️ <strong>This OTP is valid for 5 minutes only.</strong></p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- FOOTER -->
              <tr>
                <td style="background-color:#fafafa; padding: 20px 40px; border-top: 1px solid rgba(79,70,229,0.1); text-align:center;">
                  <p style="color:#aaa; font-size:0.75rem; margin:0; font-family:'Courier New',monospace; letter-spacing:0.05em;">This is an automated message — please do not reply · AI-Blockchain Integrated E-Democracy System</p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        raise Exception("Failed to send OTP email")

def send_vote_receipt_email(to_email, election_name, constituency_name, receipt_hash):
    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    smtp_host = os.getenv("MAIL_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("MAIL_PORT", 587))

    if not sender_email or not sender_password:
        raise Exception("Email service not configured")

    subject = "Your Vote Receipt — E-Democracy System"

    html_body = f"""
    <html>
    <body style="margin:0; padding:0; background-color:#f5f5f7; font-family: 'DM Sans', Arial, sans-serif;">

      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f7; padding: 40px 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:4px; overflow:hidden; box-shadow: 0 2px 16px rgba(79,70,229,0.08); border: 1px solid rgba(79,70,229,0.12);">

              <!-- HEADER / LOGO -->
              <tr>
                <td style="background-color:#ffffff; padding: 28px 40px 20px 40px; border-bottom: 1px solid rgba(79,70,229,0.1);">
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="vertical-align: middle; padding-right: 12px;">
                        <div style="width:40px; height:40px; background: rgba(79,70,229,0.08); border: 1.5px solid rgba(79,70,229,0.2); border-radius:4px; display:inline-block; text-align:center; line-height:40px; font-size:18px;">🗳️</div>
                      </td>
                      <td style="vertical-align: middle;">
                        <div style="font-family: Arial Black, sans-serif; font-size: 1.3rem; letter-spacing: 0.06em; color: #4f46e5; line-height:1;">E-DEMOCRACY</div>
                        <div style="font-family: 'Courier New', monospace; font-size: 0.5rem; letter-spacing: 0.3em; text-transform: uppercase; color: #888; line-height:1; margin-top:2px;">AI · BLOCKCHAIN · GOVERNANCE</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- HERO BAND -->
              <tr>
                <td style="background: linear-gradient(135deg, #4f46e5 0%, #0d9488 100%); padding: 36px 40px;">
                  <p style="margin:0 0 6px 0; font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.2em; text-transform:uppercase; color:rgba(255,255,255,0.7);">Vote Confirmed</p>
                  <h1 style="margin:0; font-size:1.9rem; font-weight:700; color:#ffffff; line-height:1.2;">Your Vote Has Been<br>Successfully Recorded ✅</h1>
                  <p style="margin:12px 0 0 0; font-size:0.92rem; color:rgba(255,255,255,0.8); line-height:1.6;">Thank you for participating in the democratic process. Your ballot has been securely recorded on the blockchain and remains completely anonymous.</p>
                </td>
              </tr>

              <!-- RECEIPT DETAILS BOX -->
              <tr>
                <td style="padding: 36px 40px 24px 40px;">
                  <p style="margin:0 0 16px 0; font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; color:#4f46e5; font-weight:700;">Vote Details</p>

                  <table width="100%" cellpadding="0" cellspacing="0" style="border:1.5px solid rgba(79,70,229,0.18); border-radius:4px; overflow:hidden;">
                    <tr style="border-bottom:1px solid rgba(79,70,229,0.1);">
                      <td style="padding:14px 20px; background:#fafafa; width:160px;">
                        <span style="font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase; color:#888;">Election</span>
                      </td>
                      <td style="padding:14px 20px; background:#ffffff;">
                        <span style="font-size:0.95rem; color:#0f0f14; font-weight:500;">{election_name}</span>
                      </td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,70,229,0.1);">
                      <td style="padding:14px 20px; background:#fafafa;">
                        <span style="font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase; color:#888;">Constituency</span>
                      </td>
                      <td style="padding:14px 20px; background:#ffffff;">
                        <span style="font-size:0.95rem; color:#0f0f14; font-weight:500;">{constituency_name}</span>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:14px 20px; background:#fafafa;">
                        <span style="font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase; color:#888;">Receipt Hash</span>
                      </td>
                      <td style="padding:14px 20px; background:#ffffff;">
                        <span style="font-family:'Courier New',monospace; font-size:0.78rem; color:#4f46e5; font-weight:700; letter-spacing:0.03em; word-break:break-all;">{receipt_hash}</span>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- INFO BOX -->
              <tr>
                <td style="padding: 0 40px 36px 40px;">
                  <table width="100%" cellpadding="0" cellspacing="0" style="background:rgba(13,148,136,0.07); border-left:3px solid #0d9488; border-radius:0 4px 4px 0;">
                    <tr>
                      <td style="padding:14px 18px;">
                        <p style="margin:0; font-size:0.88rem; color:#0f0f14; line-height:1.6;">🔒 <strong>Your vote is anonymous.</strong> The receipt hash above is your proof that your vote was recorded. You can verify it anytime on the platform using the <strong>Verify Vote</strong> option.</p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- FOOTER -->
              <tr>
                <td style="background-color:#fafafa; padding: 20px 40px; border-top: 1px solid rgba(79,70,229,0.1); text-align:center;">
                  <p style="color:#aaa; font-size:0.75rem; margin:0; font-family:'Courier New',monospace; letter-spacing:0.05em;">This is an automated message — please do not reply · AI-Blockchain Integrated E-Democracy System</p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception:
        raise Exception("Failed to send receipt email")

def send_voter_welcome_email(to_email, full_name, voter_id_number, temp_password):
    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    smtp_host = os.getenv("MAIL_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("MAIL_PORT", 587))

    if not sender_email or not sender_password:
        raise Exception("Email service not configured")

    subject = "Registration Successful — E-Democracy System"

    # ── Build steps HTML BEFORE the f-string (no backslashes in {} allowed in Python < 3.12) ──
    steps_data = [
        ("01", 'Go to the login page and click on <strong>"Forgot Password"</strong>'),
        ("02", "Enter your registered email address"),
        ("03", "Enter the OTP sent to this email"),
        ("04", "Set your new secure password"),
    ]

    steps_html = "".join([f"""
    <tr>
      <td style="vertical-align:top; padding-bottom:12px;">
        <table cellpadding="0" cellspacing="0">
          <tr>
            <td style="vertical-align:top; padding-right:14px;">
              <div style="width:26px; height:26px; background: rgba(79,70,229,0.08); border:1.5px solid rgba(79,70,229,0.2); border-radius:2px; text-align:center; line-height:24px; font-family:'Courier New',monospace; font-size:0.75rem; font-weight:700; color:#4f46e5; flex-shrink:0;">{num}</div>
            </td>
            <td style="vertical-align:middle;">
              <span style="font-size:0.9rem; color:#2d2d3a; line-height:1.5;">{step}</span>
            </td>
          </tr>
        </table>
      </td>
    </tr>""" for num, step in steps_data])

    html_body = f"""
    <html>
    <body style="margin:0; padding:0; background-color:#f5f5f7; font-family: 'DM Sans', Arial, sans-serif;">

      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f5f5f7; padding: 40px 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius:4px; overflow:hidden; box-shadow: 0 2px 16px rgba(79,70,229,0.08); border: 1px solid rgba(79,70,229,0.12);">

              <!-- HEADER / LOGO -->
              <tr>
                <td style="background-color:#ffffff; padding: 28px 40px 20px 40px; border-bottom: 1px solid rgba(79,70,229,0.1);">
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="vertical-align: middle; padding-right: 12px;">
                        <div style="width:40px; height:40px; background: rgba(79,70,229,0.08); border: 1.5px solid rgba(79,70,229,0.2); border-radius:4px; display:inline-block; text-align:center; line-height:40px; font-size:18px;">🗳️</div>
                      </td>
                      <td style="vertical-align: middle;">
                        <div style="font-family: Arial Black, sans-serif; font-size: 1.3rem; letter-spacing: 0.06em; color: #4f46e5; line-height:1;">E-DEMOCRACY</div>
                        <div style="font-family: 'Courier New', monospace; font-size: 0.5rem; letter-spacing: 0.3em; text-transform: uppercase; color: #888; line-height:1; margin-top:2px;">AI · BLOCKCHAIN · GOVERNANCE</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- HERO BAND -->
              <tr>
                <td style="background: linear-gradient(135deg, #4f46e5 0%, #0d9488 100%); padding: 36px 40px;">
                  <p style="margin:0 0 6px 0; font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.2em; text-transform:uppercase; color:rgba(255,255,255,0.7);">Registration Confirmed</p>
                  <h1 style="margin:0; font-size:1.9rem; font-weight:700; color:#ffffff; line-height:1.2;">Welcome to the Platform,<br>{full_name}! 🎉</h1>
                  <p style="margin:12px 0 0 0; font-size:0.92rem; color:rgba(255,255,255,0.8); line-height:1.6;">Your voter account has been successfully created on the AI-Blockchain Integrated E-Democracy System. You are now registered to participate in elections in your constituency.</p>
                </td>
              </tr>

              <!-- CREDENTIALS BOX -->
              <tr>
                <td style="padding: 36px 40px 24px 40px;">
                  <p style="margin:0 0 16px 0; font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; color:#4f46e5; font-weight:700;">Your Login Credentials</p>

                  <table width="100%" cellpadding="0" cellspacing="0" style="border:1.5px solid rgba(79,70,229,0.18); border-radius:4px; overflow:hidden;">
                    <tr style="border-bottom:1px solid rgba(79,70,229,0.1);">
                      <td style="padding:14px 20px; background:#fafafa; width:140px;">
                        <span style="font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase; color:#888;">Email</span>
                      </td>
                      <td style="padding:14px 20px; background:#ffffff;">
                        <span style="font-size:0.95rem; color:#0f0f14; font-weight:500;">{to_email}</span>
                      </td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(79,70,229,0.1);">
                      <td style="padding:14px 20px; background:#fafafa;">
                        <span style="font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase; color:#888;">Voter ID</span>
                      </td>
                      <td style="padding:14px 20px; background:#ffffff;">
                        <span style="font-family:'Courier New',monospace; font-size:0.95rem; color:#4f46e5; font-weight:700; letter-spacing:0.05em;">{voter_id_number}</span>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:14px 20px; background:#fafafa;">
                        <span style="font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase; color:#888;">Password</span>
                      </td>
                      <td style="padding:14px 20px; background:#ffffff;">
                        <span style="font-family:'Courier New',monospace; font-size:0.95rem; color:#0f0f14; font-weight:600; background: rgba(79,70,229,0.06); padding: 3px 10px; border-radius:2px;">{temp_password}</span>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- WARNING -->
              <tr>
                <td style="padding: 0 40px 28px 40px;">
                  <table width="100%" cellpadding="0" cellspacing="0" style="background:rgba(13,148,136,0.07); border-left:3px solid #0d9488; border-radius:0 4px 4px 0; padding:0;">
                    <tr>
                      <td style="padding:14px 18px;">
                        <p style="margin:0; font-size:0.88rem; color:#0f0f14; line-height:1.5;">⚠️ <strong>This is a temporary password.</strong> Please change it immediately after your first login to keep your account secure.</p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>

              <!-- STEPS -->
              <tr>
                <td style="padding: 0 40px 36px 40px;">
                  <p style="margin:0 0 16px 0; font-family:'Courier New',monospace; font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; color:#4f46e5; font-weight:700;">How to Change Your Password</p>
                  <table width="100%" cellpadding="0" cellspacing="0">
                    {steps_html}
                  </table>
                </td>
              </tr>

              <!-- FOOTER -->
              <tr>
                <td style="background-color:#fafafa; padding: 20px 40px; border-top: 1px solid rgba(79,70,229,0.1); text-align:center;">
                  <p style="color:#aaa; font-size:0.75rem; margin:0; font-family:'Courier New',monospace; letter-spacing:0.05em;">This is an automated message — please do not reply · AI-Blockchain Integrated E-Democracy System</p>
                </td>
              </tr>

            </table>
          </td>
        </tr>
      </table>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception:
        raise Exception("Failed to send welcome email")