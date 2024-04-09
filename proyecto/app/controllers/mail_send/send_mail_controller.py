from flask import Blueprint, jsonify, Response
import subprocess

mail_bp = Blueprint('mail', __name__)

@mail_bp.route('/send-email')
def send_email():
    try:
        subprocess.run([
            './swaks', '--auth',
            '--server', 'smtp.mailgun.org',
            '--au', 'username_mailgun',
            '--ap', 'default_password',
            '--to', 'authorized_email',
            '--h-Subject', 'Hello',
            '--body', 'buenas tardes desde mi querida y odiada'
        ], check=True)
        return jsonify({'message': 'Email sent successfully'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'message': f'Failed to send email: {e}'}, 500)