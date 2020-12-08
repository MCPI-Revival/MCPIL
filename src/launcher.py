import subprocess
import os

# Feature Parse Failure
def _parse_fail():
    raise Exception('Unable To Parse Features')

# Get All Available MCPI-Docker Features
def _get_features() -> dict:
    out: dict = {}

    # Block X11 If Using Older MCPi-Docker
    env = os.environ.copy()
    del env['DISPLAY']

    result: subprocess.CompletedProcess = subprocess.run(['/usr/bin/minecraft-pi', '--print-features'], capture_output=True, text=True, env=env)
    result.check_returncode()

    stage = 0
    skip = 0
    escaped = False
    current_default = False
    current_name = ''
    for part in str(result.stdout):
        if skip > 0:
            skip -= 1
            continue
        if stage == 0:
            if part == 'T':
                current_default = True
                skip = 3
                stage += 1
            elif part == 'F':
                current_default = False
                skip = 4
                stage += 1
            elif part != ' ' and part != '\n':
                _parse_fail()
        elif stage == 1:
            if part == '\'':
                stage += 1
        elif stage == 2:
            is_escaped = False
            if part == '\\':
                escaped = True
            elif escaped:
                is_escaped = True
                escaped = False
                if part == 'n':
                    # Hide Newline
                    part = ''
                elif part == 't':
                    # Add Tab
                    part = '\t'
            if part == '\'' and not is_escaped:
                out[current_name] = current_default
                current_name = ''
                current_default = False
                stage = 0
            else:
                current_name += part
        else:
            _parse_fail()

    return out

# All Available MCPI-Docker Features
AVAILABLE_FEATURES = _get_features()
print('Loaded Available Features: ' + str(AVAILABLE_FEATURES))

# Run MCPI-Docker
def run(features: list, username: str):
    env = os.environ.copy()
    env['MCPI_FEATURES'] = '|'.join(features)
    env['MCPI_USERNAME'] = username
    process = subprocess.run(['/usr/lib/minecraft-pi/run.sh'], env=env)
    process.check_returncode()