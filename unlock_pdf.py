import subprocess

def unlock_pdf(password, input_file, output_file):
    try:
        subprocess.run(['qpdf', '--password=' + password, '--decrypt', input_file, output_file], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
