python=$(pyenv which python)
pip=$(pyenv which pip)
export PATH="/home/ivan/Documentos/nanotts/:$PATH"

$python -m pytest tests_unitary/tests_pyaudio.py -s
$python -m pytest tests_unitary/tests_ffmpeg.py -s
$python -m pytest tests_unitary/tests_tts.py -s
$python -m pytest tests_unitary/tests_sr.py -s
$python -m pytest tests_unitary/tests_chatbot.py -s
$python -m pytest tests_environment -s