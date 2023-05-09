if (-not (Test-Path -Path "$env:USERPROFILE\env")) {
  # Create Python virtual environment if it does not exist 
  python -m venv $env:USERPROFILE\env

  # Activate the Python virtual environment 
  & $env:USERPROFILE\env\Scripts\Activate.ps1

  # Install the requirements of the project if not installed
  python -m pip install -r "..\requirements.txt"
}

Exit 0
