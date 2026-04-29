import smtplib
import configparser
from email.message import EmailMessage
from pathlib import Path

def generate_html_report(metrics_dict):
    """Generates an HTML report from the metrics dictionary with a styled table."""
    html = """
    <html>
    <head>
        <style>
            table { border-collapse: collapse; width: 60%; font-family: Arial, sans-serif; }
            th, td { border: 1px solid #dddddd; padding: 10px; text-align: left; }
            th { background-color: #f2f2f2; color: #333333; }
            body { font-family: Arial, sans-serif; color: #333333; }
        </style>
    </head>
    <body>
        <h2>Daily Auto-Adjudication Report</h2>
        <p>Please find the daily summary of healthcare claims below:</p>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
    """
    
    for key, value in metrics_dict.items():
        html += f"            <tr><td>{key}</td><td>{value}</td></tr>\n"
        
    html += """
        </table>
        <p>The detailed Excel report is attached to this email.</p>
    </body>
    </html>
    """
    return html

def generate_and_send_email(metrics, email_config, attachment_path=None):
    """Sends an email with the HTML report and an optional attachment using SMTP_SSL."""
    html_content = generate_html_report(metrics)
    
    # Load credentials from config.ini
    config = configparser.ConfigParser()
    config_path = Path(__file__).parent.parent / 'config.ini'
    config.read(config_path)
    
    smtp_server = config.get('SMTP', 'server', fallback='smtp.gmail.com')
    smtp_port = config.getint('SMTP', 'port', fallback=465)
    smtp_user = config.get('SMTP', 'username', fallback=email_config.get('sender'))
    smtp_password = config.get('SMTP', 'password', fallback='')
    
    msg = EmailMessage()
    msg['Subject'] = email_config.get('subject', 'Daily Healthcare Claims Report')
    msg['From'] = smtp_user
    msg['To'] = ", ".join(email_config.get('recipients', []))
    
    msg.set_content("Please enable HTML to view this report.")
    msg.add_alternative(html_content, subtype='html')
    
    if attachment_path and Path(attachment_path).exists():
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = Path(attachment_path).name
        msg.add_attachment(file_data, maintype='application', 
                           subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                           filename=file_name)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            if smtp_password:
                server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"  Email sent successfully to: {msg['To']}")
    except Exception as e:
        print(f"  Failed to send email: {e}")

    # ==============================================================================
    # Original win32com (Outlook) corp context implementation (Windows-only)
    # ==============================================================================
    # import win32com.client as win32
    # try:
    #     outlook = win32.Dispatch('outlook.application')
    #     mail = outlook.CreateItem(0)
    #     mail.To = ";".join(email_config.get('recipients', []))
    #     mail.Subject = email_config.get('subject', '')
    #     mail.HTMLBody = html_content
    #     if attachment_path:
    #         mail.Attachments.Add(str(Path(attachment_path).absolute()))
    #     mail.Send()
    #     print("  Email sent via Outlook.")
    # except Exception as e:
    #     print(f"  Failed to send email via Outlook: {e}")